"""Build the SustainArc articles section as static files in ../site."""
import html, json, pathlib, re, shutil
from datetime import datetime
from email.utils import format_datetime
import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, SITE, BUILD = ROOT / "content", ROOT / "site", ROOT / "build"
BASE = "https://sustainarc.jarlhalla.com"
LANDING_MAX = 3  # newest articles shown on the front page
NO_DEK = {}  # legacy; each article now carries "no_dek" in its front matter
EXTERNAL = [  # published on jarlhalla.com, checked 15 Nov 2026 (HTTP 200)
    ("Whole-Life Carbon in Buildings: From EPDs to Decisions", "https://jarlhalla.com/whole-life-carbon-buildings-epd-decision-register/", "2026-11-04"),
    ("Excavated Soil and Rock Reuse: A Practical Nordic Guide", "https://jarlhalla.com/excavated-soil-rock-reuse-norway-circular-construction/", "2026-11-02"),
    ("Reclaimed Structural Steel: Safe Reuse, Testing and Carbon", "https://jarlhalla.com/reclaimed-structural-steel-testing-traceability-carbon/", "2026-10-24"),
    ("Bio-Based Insulation in Nordic Buildings: Moisture Before Carbon", "https://jarlhalla.com/bio-based-insulation-nordic-moisture-performance/", "2026-10-24"),
]
MONTHS = "January February March April May June July August September October November December".split()
MONTHS_NO = "januar februar mars april mai juni juli august september oktober november desember".split()


def fdate(d, no=False):
    y, m, dd = d.split("-")
    return f"{int(dd)}. {MONTHS_NO[int(m)-1]} {y}" if no else f"{int(dd)} {MONTHS[int(m)-1]} {y}"


def load(slug):
    raw = (SRC / f"{slug}.md").read_text(encoding="utf-8")
    head, body = raw.split("\n---\n", 1)
    meta = json.loads(head)
    return meta, body


def render_body(body):
    md = markdown.Markdown(extensions=["tables", "toc", "sane_lists"], extension_configs={"toc": {"permalink": False}})
    out = md.convert(body)
    # citation markers -> superscript links (not inside the sources list)
    main, sep, sources = out.partition('<h2 id="sources">Sources</h2>')
    main = re.sub(r"\[(\d+)\](?!\()", r'<sup><a href="#src-\1" aria-label="Source \1">[\1]</a></sup>', main)
    if sep:
        n = iter(range(1, 100))
        sources = sources.replace("<ol>", '<ol class="sources">', 1)
        sources = re.sub(r"<li>", lambda m: f'<li id="src-{next(n)}">', sources)
        out = main + sep + sources
    else:
        out = main
    out = out.replace('<a href="http', '<a rel="noopener" href="http')
    toc = [(t["id"], t["name"]) for t in md.toc_tokens if t["level"] == 2 and t["id"] != "sources"]
    return out, toc


HEAD_FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
              '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600'
              '&family=IBM+Plex+Mono:wght@400;500&family=Newsreader:opsz,wght@6..72,500;6..72,600&display=swap">')

UI_NO = {"by": "et Jarlhalla-initiativ", "n1": "Fokus", "n2": "I praksis", "n4": "Artikler", "n3": "Kontakt",
         "home": "Forside", "arts": "Artikler", "toc": "I denne artikkelen", "src": "Kilder",
         "cta_h": "Vil du bruke dette i et prosjekt?", "cta_p": "Send en kort beskrivelse av prosjektet, så svarer vi på hvordan vi kan hjelpe.",
         "cta_b": "Send e-post", "lang_note": "Artikkelen er på engelsk. Norsk sammendrag står øverst.",
         "f_tag": "Bærekraftig arkitektur og sirkulært byggeri. En del av Jarlhalla-økosystemet.",
         "ai": "Utarbeidet med KI-støtte og kontrollert av byggingeniør før publisering. Illustrasjonene er laget for artikkelen og viser ikke reelle prosjekter.",
         "list_eb": "Artikler", "list_h": "Fagartikler fra SustainArc",
         "list_p": "Praktiske artikler om klimagassregnskap, ombruk og rehabilitering, med kilder. Artiklene er på engelsk med norsk sammendrag.",
         "also": "Mer om bærekraftig bygging på jarlhalla.com", "read": "Les artikkelen"}


def header(active):
    nav = [("/#focus", "n1", "Focus"), ("/#practice", "n2", "In practice"), ("/articles/", "n4", "Articles"), ("/#contact", "n3", "Contact")]
    links = "\n      ".join(
        f'<a href="{h}" data-i18n="{k}"{" aria-current=\"page\"" if k == active else ""}>{t}</a>' for h, k, t in nav)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="bar">
  <div class="wrap">
    <a class="brand" href="/">SUSTAINARC <small data-i18n="by">a Jarlhalla initiative</small></a>
    <nav class="nav" aria-label="Sections">
      {links}
    </nav>
    <div class="lang" role="group" aria-label="Language">
      <button type="button" id="lang-en" aria-pressed="true">EN</button><span>/</span><button type="button" id="lang-no" aria-pressed="false">NO</button>
    </div>
  </div>
</header>'''


FOOTER = '''<footer>
  <div class="wrap">
    <div><div class="fb">SUSTAINARC</div><span data-i18n="f_tag">Sustainable architecture and circular construction. Part of the Jarlhalla ecosystem.</span></div>
    <nav aria-label="Footer">
      <a href="/articles/" data-i18n="arts">Articles</a>
      <a href="https://jarlhalla.com">jarlhalla.com</a>
      <a href="https://mykoknoks.jarlhalla.com">MykoKnoks</a>
      <span>© 2026 Jarlhalla</span>
    </nav>
  </div>
</footer>'''


def script(extra_no=None):
    no = dict(UI_NO, **(extra_no or {}))
    return f'''<script>
(function(){{
  var NO = {json.dumps(no, ensure_ascii=False)};
  var EN = {{}};
  document.querySelectorAll("[data-i18n]").forEach(function(el){{ EN[el.getAttribute("data-i18n")] = el.textContent; }});
  function setLang(lang){{
    var d = lang === "no" ? NO : EN;
    document.querySelectorAll("[data-i18n]").forEach(function(el){{ var k = el.getAttribute("data-i18n"); if (d[k]) el.textContent = d[k]; }});
    document.querySelectorAll("[data-only]").forEach(function(el){{ el.hidden = el.getAttribute("data-only") !== lang; }});
    document.getElementById("lang-en").setAttribute("aria-pressed", lang !== "no");
    document.getElementById("lang-no").setAttribute("aria-pressed", lang === "no");
    try {{ localStorage.setItem("sa-lang", lang); }} catch(e){{}}
  }}
  document.getElementById("lang-en").addEventListener("click", function(){{ setLang("en"); }});
  document.getElementById("lang-no").addEventListener("click", function(){{ setLang("no"); }});
  var saved = null; try {{ saved = localStorage.getItem("sa-lang"); }} catch(e){{}}
  setLang(saved || "en");
}})();
</script>'''


def head(title, desc, url, image=None, kind="website", jsonld=None, extra=""):
    e = html.escape
    img = (f'<meta property="og:image" content="{BASE}/images/{image}-og.jpg">\n'
           f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
           f'<meta name="twitter:card" content="summary_large_image">\n') if image else ""
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n' if jsonld else ""
    return f'''<!doctype html>
<html lang="en">
<head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="SustainArc">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="{kind}">
<meta property="og:url" content="{url}">
{img}<meta name="theme-color" content="#14332E">
<link rel="alternate" type="application/rss+xml" title="SustainArc articles" href="{BASE}/articles/feed.xml">
{HEAD_FONTS}
<link rel="stylesheet" href="/assets/site.css">
{ld}{extra}</head>'''


def article_page(meta, body_html, toc):
    url = f"{BASE}/articles/{meta['slug']}/"
    e = html.escape
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": meta["title"], "description": meta["description"],
          "datePublished": meta["date"], "dateModified": meta["updated"], "inLanguage": "en",
          "image": f"{BASE}/images/{meta['image']}-og.jpg", "mainEntityOfPage": url, "keywords": ", ".join(meta["tags"]),
          "author": {"@type": "Organization", "name": "SustainArc", "url": BASE + "/"},
          "publisher": {"@type": "Organization", "name": "Jarlhalla", "url": "https://jarlhalla.com"}}
    toc_html = "".join(f'<li><a href="#{i}">{e(n)}</a></li>' for i, n in toc)
    tags = "".join(f"<li>{e(t)}</li>" for t in meta["tags"])
    return f'''{head(meta["seo_title"], meta["description"], url, meta["image"], "article", ld)}
<body>
{header("n4")}
<main id="main">
  <div class="wrap">
    <p class="crumbs"><a href="/" data-i18n="home">Home</a> / <a href="/articles/" data-i18n="arts">Articles</a></p>
    <div class="art-head">
      <ul class="tags">{tags}</ul>
      <h1>{e(meta["title"])}</h1>
      <p class="dek">{e(meta["dek"])}</p>
      <p class="meta"><span>SustainArc</span><span><time datetime="{meta["date"]}">{fdate(meta["date"])}</time></span><span>{meta["minutes"]} min read</span></p>
    </div>
    <figure class="hero-img">
      <img src="/images/{meta["image"]}.svg" width="1200" height="675" alt="{e(meta["image_alt"])}">
    </figure>
    <div class="layout">
      <article class="prose">
        <section class="no-box" lang="no" aria-labelledby="no-h">
          <h2 id="no-h">Norsk sammendrag</h2>
          <p class="no-t">{e(meta["no_title"])}</p>
          <p>{e(meta["no_summary"])}</p>
        </section>
        {body_html}
        <div class="cta">
          <div><h2 data-i18n="cta_h">Want to apply this to a project?</h2>
          <p data-i18n="cta_p">Send a short description of the project and we will reply with how we can help.</p></div>
          <a class="btn" href="mailto:taksdalbt@gmail.com?subject={e("SustainArc - " + meta["title"][:60])}"><span class="arrow" data-i18n="cta_b">Email us</span></a>
        </div>
        <p class="ai-note" data-i18n="ai">Prepared with AI assistance and reviewed by a building engineer before publication. The illustrations were made for this article and do not show real projects.</p>
      </article>
      <aside class="side" aria-label="Article navigation">
        <p class="note" data-only="no" hidden data-i18n="lang_note">Artikkelen er på engelsk. Norsk sammendrag står øverst.</p>
        <div class="box"><span class="eyebrow" data-i18n="toc">In this article</span><ol>{toc_html}</ol></div>
        <div class="box"><span class="eyebrow" data-i18n="src">Sources</span><a href="#sources" data-i18n="srcn">{body_html.count('id="src-')} sources</a></div>
      </aside>
    </div>
  </div>
</main>
{FOOTER}
{script({"srcn": f"{body_html.count('id="src-')} kilder"})}
</body>
</html>
'''


def card(meta, prefix="/", mode="i18n"):
    e = html.escape
    no_dek = meta.get("no_dek") or NO_DEK.get(meta["slug"], "")
    if mode == "no":
        ta, da = f' data-no="{e(meta["no_title"])}"', f' data-no="{e(no_dek)}"'
    else:
        ta, da = f' data-i18n="t_{meta["image"]}"', f' data-i18n="d_{meta["image"]}"' 
    href = f"{prefix}articles/{meta['slug']}/"
    return (f'<li><a class="cover" href="{href}" tabindex="-1" aria-hidden="true"><img src="{prefix}images/{meta["image"]}.svg" '
            f'width="1200" height="675" alt="" loading="lazy"></a>'
            f'<span class="meta"><time datetime="{meta["date"]}">{fdate(meta["date"])}</time> · {meta["minutes"]} min</span>'
            f'<h3><a href="{href}"{ta}>{e(meta["title"])}</a></h3>'
            f'<p{da}>{e(meta["dek"])}</p></li>')


def ext_list():
    e = html.escape
    return "".join(f'<li><a href="{u}" rel="noopener">{e(t)}</a><span>jarlhalla.com · {fdate(d)}</span></li>' for t, u, d in EXTERNAL)


def card_no(metas):
    d = {}
    for m in metas:
        d[f"t_{m['image']}"] = m["no_title"]
        d[f"d_{m['image']}"] = m.get("no_dek") or NO_DEK.get(m["slug"], "")
    return d


def list_page(metas):
    url = f"{BASE}/articles/"
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "SustainArc articles", "url": url,
          "hasPart": [{"@type": "Article", "headline": m["title"], "url": f"{url}{m['slug']}/"} for m in metas]}
    return f'''{head("Articles · SustainArc", "Practical articles on climate accounts, reuse and renovation from SustainArc, with sources. English with Norwegian summaries.", url, metas[0]["image"], "website", ld)}
<body>
{header("n4")}
<main id="main">
  <div class="wrap">
    <div class="page-head">
      <span class="eyebrow" data-i18n="list_eb">Articles</span>
      <h1 data-i18n="list_h">Articles from SustainArc</h1>
      <p class="dek" data-i18n="list_p">Practical articles on climate accounts, reuse and renovation, with sources. Written in English with a Norwegian summary.</p>
    </div>
    <ul class="cards">{"".join(card(m) for m in metas)}</ul>
  </div>
  <section class="band" style="margin-top:48px">
    <div class="wrap">
      <h2 style="font-size:1.5rem;margin-bottom:16px" data-i18n="also">More on sustainable building at jarlhalla.com</h2>
      <ul class="ext">{ext_list()}</ul>
    </div>
  </section>
</main>
{FOOTER}
{script(card_no(metas))}
</body>
</html>
'''


LANDING_CSS = '''
/* articles section (added 2026-11-15) */
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px clamp(20px,3vw,36px);list-style:none;margin:0;padding:0}
.cards li{display:flex;flex-direction:column;gap:10px;min-width:0}
.cards a.cover{display:block;border-radius:6px;overflow:hidden;border:1px solid var(--line);background:var(--band)}
.cards img{width:100%;height:auto;display:block;aspect-ratio:16/9;object-fit:cover}
.cards h3 a{text-decoration:none}.cards h3 a:hover{text-decoration:underline;text-underline-offset:4px}
.cards p{font-size:.94rem}
.cards .meta{font-size:.78rem;color:var(--muted);font-family:var(--mono)}
.ext{list-style:none;margin:28px 0 0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 clamp(20px,4vw,56px)}
.ext li{padding:12px 0;border-bottom:1px solid var(--line);display:flex;flex-direction:column;gap:2px;min-width:0}
.ext a{text-decoration:none;color:var(--ink);font-weight:500}.ext a:hover{text-decoration:underline;text-underline-offset:4px}
.ext span{font-size:.8rem;color:var(--muted);font-family:var(--mono)}
.ext-h{font-family:var(--sans);font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);font-weight:500;margin-top:36px}
@media (max-width:960px){ .cards{grid-template-columns:repeat(2,minmax(0,1fr))} }
@media (max-width:640px){ .cards,.ext{grid-template-columns:minmax(0,1fr)} }
'''


MARKS = ["SA:HEAD", "SA:NAV", "SA:ARTICLES", "SA:FOOT"]


def strip_marks(s):
    for m in MARKS:
        s = re.sub(rf"<!-- {m} -->.*?<!-- /{m} -->\n?[ \t]*", "", s, flags=re.S)
    return re.sub(r"/\* SA:CSS \*/.*?/\* /SA:CSS \*/\n?", "", s, flags=re.S)


LANDING_JS = """<script>
(function(){
  var els = document.querySelectorAll("[data-no]"), en = [];
  els.forEach(function(el, i){ en[i] = el.textContent; });
  function apply(lang){ els.forEach(function(el, i){ el.textContent = lang === "no" ? el.getAttribute("data-no") : en[i]; }); }
  document.getElementById("lang-en").addEventListener("click", function(){ apply("en"); });
  document.getElementById("lang-no").addEventListener("click", function(){ apply("no"); });
  var saved = null; try { saved = localStorage.getItem("sa-lang"); } catch(e){}
  if (saved === "no") apply("no");
})();
</script>"""


def landing(metas):
    """Insert/refresh the articles block in the live landing page. Idempotent via SA markers."""
    src = strip_marks((ROOT / "src" / "index.html").read_text(encoding="utf-8"))
    assert src.count('<section id="contact">') == 1 and 'id="articles"' not in src, "unexpected landing layout"
    e = html.escape
    s = src.replace("</style>", "/* SA:CSS */" + LANDING_CSS + "/* /SA:CSS */\n</style>", 1)
    s = s.replace("</head>", f'''<!-- SA:HEAD --><meta property="og:image" content="{BASE}/images/{metas[0]["image"]}-og.jpg">
<link rel="alternate" type="application/rss+xml" title="SustainArc articles" href="{BASE}/articles/feed.xml"><!-- /SA:HEAD -->
</head>''', 1)
    s = s.replace('<a href="#contact" data-i18n="n3">Contact</a>',
                  '<!-- SA:NAV --><a href="#articles" data-no="Artikler">Articles</a>\n      <!-- /SA:NAV --><a href="#contact" data-i18n="n3">Contact</a>', 1)
    section = f'''<!-- SA:ARTICLES --><section class="band" id="articles">
    <div class="wrap">
      <div class="head">
        <span class="eyebrow" data-no="Artikler">Articles</span>
        <h2 data-no="Nytt fra SustainArc">New from SustainArc</h2>
        <p data-no="Praktiske artikler om klimagassregnskap, ombruk og rehabilitering, med kilder. På engelsk med norsk sammendrag.">Practical articles on climate accounts, reuse and renovation, with sources. In English with a Norwegian summary.</p>
      </div>
      <ul class="cards">{"".join(card(m, mode="no") for m in metas[:LANDING_MAX])}</ul>
      <p class="ext-h" data-no="Mer å lese på jarlhalla.com">Related reading on jarlhalla.com</p>
      <ul class="ext">{ext_list()}</ul>
      <p class="note"><a class="link" href="/articles/"><span class="arrow" data-no="Alle artikler ({len(metas)})">All articles ({len(metas)})</span></a></p>
    </div>
  </section>
  {LANDING_JS}
  <!-- /SA:ARTICLES -->
  <section id="contact">'''
    s = s.replace('<section id="contact">', section, 1)
    s = s.replace('<a href="https://jarlhalla.com">jarlhalla.com</a>',
                  '<!-- SA:FOOT --><a href="/articles/" data-no="Artikler">Articles</a>\n      <!-- /SA:FOOT --><a href="https://jarlhalla.com">jarlhalla.com</a>', 1)
    for m in MARKS:
        assert s.count(f"<!-- {m} -->") == 1, m
    return s


def feed(metas):
    e = html.escape
    items = "".join(
        f"<item><title>{e(m['title'])}</title><link>{BASE}/articles/{m['slug']}/</link><guid>{BASE}/articles/{m['slug']}/</guid>"
        f"<pubDate>{format_datetime(datetime.fromisoformat(m['date']+'T09:00:00+01:00'))}</pubDate>"
        f"<description>{e(m['description'])}</description></item>" for m in metas)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>SustainArc articles</title>'
            f'<link>{BASE}/articles/</link><description>Sustainable architecture and circular construction</description>'
            f'<language>en</language>{items}</channel></rss>\n')


def main():
    for p in (SITE / "articles", SITE / "assets"):
        shutil.rmtree(p, ignore_errors=True)
    (SITE / "assets").mkdir(parents=True)
    shutil.copy(BUILD / "site.css", SITE / "assets" / "site.css")
    # images: copy source SVGs and (re)render social JPGs only when an SVG changed
    img_out = SITE / "images"; img_out.mkdir(parents=True, exist_ok=True)
    svgs = sorted((ROOT / "images").glob("*.svg"))
    for s in svgs:
        if not (img_out / s.name).exists() or (img_out / s.name).read_bytes() != s.read_bytes():
            shutil.copy(s, img_out / s.name)
    import sys; sys.path.insert(0, str(BUILD))
    from render_og import render
    rendered = render([img_out / s.name for s in svgs], img_out)
    if rendered: print("rendered og:", ", ".join(rendered))
    metas = []
    slugs = [p.stem for p in SRC.glob("*.md")]
    order = sorted(slugs, key=lambda sl: (load(sl)[0]["date"], sl), reverse=True)
    for slug in order:
        meta, body = load(slug)
        assert (ROOT / "images" / f"{meta['image']}.svg").exists(), f"missing images/{meta['image']}.svg for {slug}"
        body_html, toc = render_body(body)
        d = SITE / "articles" / slug
        d.mkdir(parents=True)
        (d / "index.html").write_text(article_page(meta, body_html, toc), encoding="utf-8")
        metas.append(meta)
    (SITE / "articles" / "index.html").write_text(list_page(metas), encoding="utf-8")
    (SITE / "articles" / "feed.xml").write_text(feed(metas), encoding="utf-8")
    (SITE / "index.html").write_text(landing(metas), encoding="utf-8")
    urls = [(f"{BASE}/", "2026-11-15"), (f"{BASE}/articles/", "2026-11-15")] + [(f"{BASE}/articles/{m['slug']}/", m["updated"]) for m in metas]
    (SITE / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + "".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    print("built", len(metas), "articles")


if __name__ == "__main__":
    main()
