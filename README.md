# sustainarc-site

Source and published files for **https://sustainarc.jarlhalla.com** (SustainArc, part of the Jarlhalla ecosystem).

## How publishing works

```
content/<slug>.md  ─┐
images/<name>.svg  ─┼─> python3 build/build.py ─> site/  ─> main branch ─> VPS pulls every 10 min ─> live
src/index.html     ─┘
```

- **Merge to `main` = publish.** The VPS (45.132.114.61) runs `/usr/local/sbin/sustainarc-pull.sh` from cron every 10 minutes. It fetches `main`, checks that `site/index.html` looks sane, backs up the current web root, and copies `site/` into it. Nothing else on the server is touched.
- New articles are drafted on a branch `draft/<slug>` and listed in Notion (Jarlhalla Editorial Calendar) with the title prefix `DRAFT — SustainArc:`.
- **Approve** by changing that prefix to `APPROVED — SustainArc:` in Notion. The daily Claude job then merges the branch into `main`, waits for the site to update, and renames the page to `PUBLISHED — SustainArc:` with the live URL.
- **Reject or pause** by leaving the page as `DRAFT` or renaming it `REJECTED — SustainArc:`. Nothing is published without the APPROVED prefix.

## Layout

| Path | What |
|---|---|
| `content/*.md` | One article per file: a JSON front-matter block, a line `---`, then Markdown. Newest date first on the site. |
| `images/*.svg` | One 1200×675 illustration per article (`"image"` in front matter). Social JPGs are rendered at build time. |
| `src/index.html` | The landing page without the articles block. Edit landing text here, not in `site/`. |
| `build/build.py` | Builds `site/`: article pages, `/articles/`, landing block (between `SA:` markers), sitemap, RSS. |
| `build/site.css` | Shared article styles (same tokens as the landing page). |
| `build/render_og.py` | SVG → 1200×630 JPG for link previews. |
| `build/illustrations.py` | Generator used for the first three illustrations (reference for style). |
| `site/` | Built output. Committed, because the server copies it as is. |

## Build locally

```bash
pip install markdown pillow playwright   # plus a Chrome/Chromium, or cairosvg as fallback
python3 build/build.py
python3 -m http.server -d site 8765      # http://localhost:8765
```

## Roll back

- Revert the commit on `main`; the server picks up the revert within 10 minutes.
- Or on the VPS: the pull script keeps the previous web root in `/root/backups/sustainarc/` (last 10).
