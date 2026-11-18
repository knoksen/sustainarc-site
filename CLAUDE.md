# Instructions for Claude in this repository

This repo publishes https://sustainarc.jarlhalla.com. Anything merged to `main` goes live within about 10 minutes. Treat `main` as production.

## Hard rules

1. **Never push to `main` without an approval recorded in Notion**: a page in the Jarlhalla Editorial Calendar whose title starts with `APPROVED — SustainArc:` and names the article. Drafts go to a branch `draft/<slug>`.
2. Never put secrets, tokens, personal data or private addresses in this repo. It is public.
3. Do not change `src/index.html` content, contact details or services unless Jarle asked for it in the conversation or in the Notion page.
4. Do not delete or rewrite published articles. Corrections are allowed when the Notion page or Jarle asks for them; add the date to `"updated"` in the front matter.
5. Run `python3 build/build.py` and commit `content/`, `images/` and `site/` together. A commit where `site/` does not match the sources is a bug.

## Editorial standard (same as the Jarlhalla Editorial Calendar)

- Audience: architects, engineers, contractors, owners and municipalities in Norway and the Nordics. English, with a Norwegian title (`no_title`), summary (`no_summary`, 60–110 words) and card text (`no_dek`, one sentence).
- Themes: climate accounts and LCA, reuse and circularity, renovation and existing buildings, building physics and moisture, bio-based and low-carbon materials, digital delivery (BIM/IFC/IDS) for sustainability. Wednesday is the sustainability slot.
- At least five verifiable sources, primary first (lovdata.no, dibk.no, regjeringen.no, eur-lex.europa.eu, standards bodies, peer-reviewed papers, SINTEF/NGU/Enova). Number them `[1]`… in the text; the `## Sources` section is a numbered list with title, link and date. Never invent a source, figure, clause number or quote.
- Say clearly what is adopted law, what is a proposal or hearing, and what is the article's own recommendation. Check the status of any proposal on the day of writing and write the date into the text ("at the time of writing, November 2026").
- No claims of Jarlhalla/SustainArc project results, clients or certifications. Services are delivered through Taksdal Bygg Teknisk; end with a short "How SustainArc can help" section and a one-line disclaimer in italics.
- Check for duplicates before writing: the other files in `content/`, the Notion editorial calendar, and published jarlhalla.com articles. Link to related jarlhalla.com articles only with URLs you have confirmed return HTTP 200.
- Plain, precise sentences. No hype, no "game-changer", no emojis in the text.

## Front matter (JSON, then a line `---`)

```json
{
 "slug": "kebab-case-slug",
 "title": "…",
 "seo_title": "… (≤ 60 characters)",
 "description": "… (≤ 160 characters)",
 "dek": "One or two sentences under the title.",
 "date": "YYYY-MM-DD",
 "updated": "YYYY-MM-DD",
 "minutes": 9,
 "tags": ["…", "…"],
 "image": "short-image-name",
 "image_alt": "What the illustration shows",
 "no_title": "…",
 "no_summary": "…",
 "no_dek": "…"
}
```

## Illustrations

- One SVG per article in `images/<image>.svg`, 1200×675, `viewBox="0 0 1200 675"`, with `<title>` and `aria-label`.
- Flat editorial style matching `build/illustrations.py`: paper `#FAF8F3`, band `#E8ECDF`, warm `#F2E3D8`, ink `#14332E`, leaf `#3F7A55`, soft leaf `#B5CBA0`, accent `#A6481F`, line `#D5DACC`. 1.5–2 px ink outlines, no gradients, no photos, no logos, no real people, at most a few short mono labels.
- The picture should explain the article's idea (a layer build-up, a sequence, a decision chain), not decorate it. Keep the important content inside y = 22…652 so the 1200×630 social crop keeps it.
- If a photorealistic AI image tool is available and Jarle has asked for photos, a JPG/PNG may be used instead, but the build currently expects an SVG; wrap the photo in an SVG `<image>` with an embedded data URI if needed.

## Publishing checklist after a merge

1. Wait up to 15 minutes, then check `https://sustainarc.jarlhalla.com/articles/<slug>/` returns 200 and shows the new title.
2. Check `/articles/`, the landing page block and `sitemap.xml` list it.
3. Update the Notion page: prefix `PUBLISHED — SustainArc:`, publication date, live URL.
4. If the page is not live after 30 minutes, do not retry blindly: report it in the Notion page and to Jarle (the VPS log is `/var/log/sustainarc-pull.log`).
