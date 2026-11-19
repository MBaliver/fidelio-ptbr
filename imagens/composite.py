#!/usr/bin/env python3
import subprocess
import sys
import os

def composite_image(orig_png, gen_jpg, out_png):
    orig_raw = bytearray(subprocess.check_output([
        'ffmpeg', '-v', 'error', '-i', orig_png, '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'
    ]))
    ow, oh = 2048, 1024

    # Check if image has transparency (diary page) or is full-frame opaque (newspaper)
    has_transp = False
    o_xs, o_ys = [], []
    for y in range(0, oh, 2):
        row = orig_raw[y*ow*4:(y+1)*ow*4]
        for x in range(0, ow, 2):
            a = row[x*4+3]
            if a > 128:
                o_xs.append(x)
                o_ys.append(y)
            elif a < 10:
                has_transp = True

    gen_raw = subprocess.check_output([
        'ffmpeg', '-v', 'error', '-i', gen_jpg, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'
    ])
    # Get gen dimensions via ffprobe
    dims = subprocess.check_output([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height', '-of', 'csv=p=0', gen_jpg
    ]).decode().strip().split(',')
    gw, gh = int(dims[0]), int(dims[1])

    if not has_transp:
        # Newspaper with black side bars (or full frame)
        # Find non-black x range in orig
        o_nxs = []
        for y in range(100, 900, 8):
            row = orig_raw[y*ow*4:(y+1)*ow*4]
            for x in range(ow):
                if row[x*4] > 25 or row[x*4+1] > 25 or row[x*4+2] > 25:
                    o_nxs.append(x)
        ox0, ox1 = min(o_nxs), max(o_nxs)
        ow_box = ox1 - ox0 + 1

        # Find non-black/non-white x range in gen
        g_nxs = []
        for y in range(100, gh - 100, 8):
            row = gen_raw[y*gw*3:(y+1)*gw*3]
            for x in range(gw):
                r, g, b = row[x*3], row[x*3+1], row[x*3+2]
                if (r > 25 or g > 25 or b > 25) and (r < 245 or g < 245 or b < 245):
                    g_nxs.append(x)
        gx0, gx1 = min(g_nxs), max(g_nxs)
        gw_box = gx1 - gx0 + 1

        scaled = subprocess.check_output([
            'ffmpeg', '-v', 'error', '-i', gen_jpg,
            '-vf', f'crop={gw_box}:{gh}:{gx0}:0,scale={ow_box}:{oh}:flags=lanczos',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'
        ])
        out_raw = bytearray(orig_raw)
        for y in range(oh):
            for x in range(ox0, ox1 + 1):
                gx = x - ox0
                oi = (y*ow + x)*4
                gi = (y*ow_box + gx)*3
                out_raw[oi] = scaled[gi]
                out_raw[oi+1] = scaled[gi+1]
                out_raw[oi+2] = scaled[gi+2]
    else:
        ox0, ox1 = min(o_xs), max(o_xs)
        oy0, oy1 = min(o_ys), max(o_ys)
        ow_box = ox1 - ox0 + 1
        oh_box = oy1 - oy0 + 1

        # Find non-white (and non-black if black bg) bounding box in gen
        # Check corner color of gen
        c_r, c_g, c_b = gen_raw[0], gen_raw[1], gen_raw[2]
        is_white_bg = (c_r > 200 and c_g > 200 and c_b > 200)

        g_xs, g_ys = [], []
        for y in range(gh):
            row = gen_raw[y*gw*3:(y+1)*gw*3]
            for x in range(gw):
                r, g, b = row[x*3], row[x*3+1], row[x*3+2]
                if is_white_bg:
                    if r < 235 or g < 235 or b < 235:
                        g_xs.append(x)
                        g_ys.append(y)
                else:
                    if r > 20 or g > 20 or b > 20:
                        g_xs.append(x)
                        g_ys.append(y)
        gx0, gx1 = min(g_xs), max(g_xs)
        gy0, gy1 = min(g_ys), max(g_ys)
        gw_box = gx1 - gx0 + 1
        gh_box = gy1 - gy0 + 1

        # Fine search around (ow_box, oh_box) and (ox0, oy0)
        best_err = 1e18
        best_params = (ow_box, oh_box, ox0, oy0)
        for d_sw in [-2, 0, 2, 4]:
            for d_sh in [-2, 0, 2, 4]:
                sw = ow_box + d_sw
                sh = oh_box + d_sh
                scaled = subprocess.check_output([
                    'ffmpeg', '-v', 'error', '-i', gen_jpg,
                    '-vf', f'crop={gw_box}:{gh_box}:{gx0}:{gy0},scale={sw}:{sh}:flags=lanczos',
                    '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'
                ])
                for d_ox in range(-3, 4):
                    for d_oy in range(-3, 4):
                        cur_ox = ox0 + d_ox
                        cur_oy = oy0 + d_oy
                        err = 0
                        cnt = 0
                        for y in range(120, 900, 16):
                            gy = y - cur_oy
                            if gy < 0 or gy >= sh: continue
                            for x in list(range(ox0 + 15, ox0 + 55, 8)) + list(range(ox1 - 55, ox1 - 15, 8)):
                                gx = x - cur_ox
                                if gx < 0 or gx >= sw: continue
                                oi = (y*ow + x)*4
                                if orig_raw[oi+3] < 200: continue
                                gi = (gy*sw + gx)*3
                                dr = orig_raw[oi] - scaled[gi]
                                dg = orig_raw[oi+1] - scaled[gi+1]
                                db = orig_raw[oi+2] - scaled[gi+2]
                                err += dr*dr + dg*dg + db*db
                                cnt += 1
                        if cnt > 0:
                            ae = err / cnt
                            if ae < best_err:
                                best_err = ae
                                best_params = (sw, sh, cur_ox, cur_oy)

        sw, sh, cur_ox, cur_oy = best_params
        print(f"[{os.path.basename(out_png)}] Best alignment: sw={sw}, sh={sh}, ox={cur_ox}, oy={cur_oy}, RMSE={best_err**0.5:.2f}")
        scaled = subprocess.check_output([
            'ffmpeg', '-v', 'error', '-i', gen_jpg,
            '-vf', f'crop={gw_box}:{gh_box}:{gx0}:{gy0},scale={sw}:{sh}:flags=lanczos',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'
        ])

        out_raw = bytearray(orig_raw)
        for y in range(oh):
            gy = y - cur_oy
            if gy < 0 or gy >= sh: continue
            for x in range(ow):
                gx = x - cur_ox
                if gx < 0 or gx >= sw: continue
                oi = (y*ow + x)*4
                a = orig_raw[oi+3]
                if a == 0: continue
                gi = (gy*sw + gx)*3
                r, g, b = scaled[gi], scaled[gi+1], scaled[gi+2]
                if is_white_bg and (r > 235 and g > 235 and b > 235):
                    continue
                if not is_white_bg and (r < 15 and g < 15 and b < 15):
                    continue
                out_raw[oi] = r
                out_raw[oi+1] = g
                out_raw[oi+2] = b

    p = subprocess.Popen([
        'ffmpeg', '-y', '-v', 'error',
        '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{ow}x{oh}', '-i', '-',
        out_png
    ], stdin=subprocess.PIPE)
    p.communicate(input=out_raw)
    if p.returncode != 0:
        raise RuntimeError(f"ffmpeg failed saving {out_png}")

if __name__ == '__main__':
    composite_image(sys.argv[1], sys.argv[2], sys.argv[3])
