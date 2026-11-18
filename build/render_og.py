"""Render 1200x630 social images (JPG) from the 1200x675 article SVGs.

Tries headless Chrome/Chromium through Playwright first (best text rendering), then cairosvg.
"""
import io, pathlib, shutil


def _chrome():
    for exe in ("google-chrome", "chromium", "chromium-browser"):
        p = shutil.which(exe)
        if p:
            return p
    return None


def render(svgs, outdir):
    outdir = pathlib.Path(outdir)
    todo = [s for s in svgs if not (outdir / f"{s.stem}-og.jpg").exists()
            or (outdir / f"{s.stem}-og.jpg").stat().st_mtime < s.stat().st_mtime]
    if not todo:
        return []
    from PIL import Image
    done = []
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            exe = _chrome()
            b = p.chromium.launch(executable_path=exe, args=["--no-sandbox"]) if exe else p.chromium.launch()
            pg = b.new_page(viewport={"width": 1200, "height": 675})
            for s in todo:
                pg.goto(s.resolve().as_uri()); pg.wait_for_timeout(300)
                tmp = outdir / f"{s.stem}-tmp.png"
                pg.screenshot(path=str(tmp))
                Image.open(tmp).convert("RGB").crop((0, 22, 1200, 652)).save(
                    outdir / f"{s.stem}-og.jpg", quality=86, optimize=True, progressive=True)
                tmp.unlink(); done.append(s.stem)
            b.close()
        return done
    except Exception as e:  # fall back to cairosvg
        print("playwright render failed, trying cairosvg:", e)
    import cairosvg
    for s in todo:
        png = cairosvg.svg2png(url=str(s), output_width=1200, output_height=675)
        Image.open(io.BytesIO(png)).convert("RGB").crop((0, 22, 1200, 652)).save(
            outdir / f"{s.stem}-og.jpg", quality=86, optimize=True, progressive=True)
        done.append(s.stem)
    return done
