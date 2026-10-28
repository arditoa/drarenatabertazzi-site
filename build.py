# -*- coding: utf-8 -*-
import json, re, html
from content import PAGES

SITE = "https://drarenatabertazzi.com.br"
IG = "https://www.instagram.com/dra.renatabertazzi/"
BYSLUG = {p["slug"]: p for p in PAGES}

CLINICS = [
    {"name": "ICOG · Instituto de Catarata e Oftalmologia",
     "street": "ACSU SO 50, Av. LO 13, Conj. 02, Lote 01 (antiga 501 Sul)", "city": "Palmas", "zip": "77016-010",
     "phone": "+55-63-3322-2061", "phone_txt": "(63) 3322-2061",
     "maps": "https://www.google.com/maps/search/?api=1&query=ICOG+Instituto+de+Catarata+e+Oftalmologia+Palmas+TO"},
    {"name": "Oftalmologia Avançada",
     "street": "Quadra 104 Norte, Rua NE 5, nº 11", "city": "Palmas", "zip": "77006-020",
     "phone": "+55-63-3215-3335", "phone_txt": "(63) 3215-3335",
     "maps": "https://www.google.com/maps/search/?api=1&query=Oftalmologia+Avan%C3%A7ada+104+Norte+Palmas+TO"},
    {"name": "OPUS",
     "street": "Quadra 702 Sul, Av. Joaquim Teotônio Segurado, 15, Conj. 01, Sala 02", "city": "Palmas", "zip": None,
     "phone": None, "phone_txt": None,
     "maps": "https://www.google.com/maps/search/?api=1&query=OPUS+702+Sul+Avenida+Joaquim+Teot%C3%B4nio+Segurado+Palmas+TO"},
]

def url(slug):
    return SITE + "/" if slug == "index" else f"{SITE}/{slug}.html"

def head(title, desc, slug, schema, og_img="img/dra-renata-bertazzi-oftalmologista-palmas.webp"):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url(slug)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Dra. Renata Bertazzi">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url(slug)}">
<meta property="og:image" content="{SITE}/{og_img}">
<meta name="theme-color" content="#1f5aa6">
<link rel="icon" type="image/png" href="img/simbolo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
"""

def header(current):
    links = [("index.html#sobre", "Sobre", "sobre"),
             ("cirurgia-de-catarata-palmas.html", "Catarata", "cirurgia-de-catarata-palmas"),
             ("cirurgia-de-retina-palmas.html", "Retina", "cirurgia-de-retina-palmas"),
             ("index.html#duvidas", "Dúvidas", "duvidas"),
             ("index.html#onde-atendo", "Onde atendo", "onde")]
    nav = "\n".join(f'      <a href="{h}"{" aria-current=\"page\"" if k == current else ""}>{t}</a>' for h, t, k in links)
    return f"""<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html">
      <img class="mark" src="img/simbolo.png" alt="" width="46" height="46"><span class="bt"><strong>Dra. Renata Bertazzi</strong>
      <span>Oftalmologia | Retina e Catarata</span></span>
    </a>
    <nav class="nav" aria-label="Principal">
{nav}
      <a class="btn" href="{IG}" target="_blank" rel="noopener">Agendar</a>
    </nav>
  </div>
</header>
"""

def footer():
    pages = "\n".join(f'        <li><a href="{p["slug"]}.html">{p["nav"] if p["nav"] not in ("Catarata","Retina") else ("Cirurgia de catarata" if p["nav"]=="Catarata" else "Cirurgia de retina")}</a></li>' for p in PAGES)
    cl = "\n".join(f'        <li><b>{c["name"]}</b><br>{c["street"]} · {c["city"]} (TO){" · " + c["phone_txt"] if c["phone_txt"] else ""}</li>' for c in CLINICS)
    return f"""<footer class="site-foot">
  <div class="wrap foot-grid">
    <div class="stack">
      <img src="img/logo-dra-renata-bertazzi.png" alt="Dra. Renata Bertazzi · Oftalmologia | Retina e Catarata" class="foot-logo" width="260" height="49" loading="lazy">
      <p><strong>Dra. Renata Cerneiro Bertazzi</strong><br>Médica Oftalmologista · CRM-TO 7132 · RQE 3562<br>Membro da Sociedade Brasileira de Retina e Vítreo (SBRV)</p>
      <p><a href="{IG}" target="_blank" rel="noopener">Instagram @dra.renatabertazzi</a></p>
    </div>
    <div class="stack">
      <b>Tratamentos e doenças</b>
      <ul class="foot-list">
{pages}
      </ul>
    </div>
    <div class="stack">
      <b>Onde atendo em Palmas</b>
      <ul class="foot-list">
{cl}
      </ul>
    </div>
  </div>
  <div class="wrap"><p class="foot-note">As informações deste site são educativas e não substituem a consulta médica. Diagnóstico e tratamento dependem de avaliação individual.</p></div>
</footer>
</body>
</html>
"""

def physician_schema():
    locs = []
    for c in CLINICS:
        addr = {"@type": "PostalAddress", "streetAddress": c["street"], "addressLocality": c["city"], "addressRegion": "TO", "addressCountry": "BR"}
        if c["zip"]: addr["postalCode"] = c["zip"]
        loc = {"@type": "MedicalClinic", "name": c["name"], "address": addr}
        if c["phone"]: loc["telephone"] = c["phone"]
        locs.append(loc)
    return {
        "@type": "Physician",
        "@id": SITE + "/#medica",
        "name": "Dra. Renata Cerneiro Bertazzi",
        "alternateName": "Dra. Renata Bertazzi",
        "description": "Médica oftalmologista em Palmas (TO), com atuação em cirurgia de catarata e cirurgia de retina. Membro da Sociedade Brasileira de Retina e Vítreo.",
        "url": SITE + "/",
        "image": SITE + "/img/dra-renata-bertazzi-oftalmologista-palmas.webp",
        "logo": SITE + "/img/logo-dra-renata-bertazzi.png",
        "medicalSpecialty": "Ophthalmologic",
        "sameAs": [IG],
        "address": locs[0]["address"],
        "location": locs,
        "areaServed": [{"@type": "City", "name": n} for n in ["Palmas", "Paraíso do Tocantins", "Porto Nacional"]],
        "memberOf": {"@type": "MedicalOrganization", "name": "Sociedade Brasileira de Retina e Vítreo (SBRV)"},
        "availableService": [{"@type": "MedicalProcedure", "name": n} for n in ["Cirurgia de catarata (facoemulsificação)", "Vitrectomia", "Cirurgia de descolamento de retina", "Injeção intravítrea (anti-VEGF)", "Fotocoagulação a laser da retina", "Mapeamento de retina"]],
        "identifier": [{"@type": "PropertyValue", "propertyID": "CRM-TO", "value": "7132"}, {"@type": "PropertyValue", "propertyID": "RQE", "value": "3562"}],
    }

def faq_schema(faq):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def faq_html(faq):
    items = "\n".join(f"      <details>\n        <summary>{q}</summary>\n        <p>{a}</p>\n      </details>" for q, a in faq)
    return f'<div class="faq">\n{items}\n    </div>'

CTA = f"""<section class="band cta">
  <div class="wrap">
    <div class="stack">
      <h2>Agende sua avaliação</h2>
      <p>Mande uma mensagem pelo Instagram e diga a cidade de sua preferência. A consulta é o primeiro passo para entender o seu caso.</p>
    </div>
    <div class="stack" style="justify-items: start;">
      <span class="handle">@dra.renatabertazzi</span>
      <a class="btn" href="{IG}" target="_blank" rel="noopener">Abrir o Instagram</a>
    </div>
  </div>
</section>"""

# ---------- subpages ----------
for p in PAGES:
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "MedicalWebPage", "@id": url(p["slug"]) + "#pagina", "url": url(p["slug"]), "name": p["title"], "description": p["desc"],
         "inLanguage": "pt-BR", "author": {"@id": SITE + "/#medica"}, "reviewedBy": {"@id": SITE + "/#medica"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": p["h1"], "item": url(p["slug"])}]},
        physician_schema(),
        faq_schema(p["faq"]),
    ]}
    img = ""
    if p["img"]:
        img = f'<figure class="photo-fig page-photo"><img src="{p["img"][0]}" alt="{p["img"][1]}" loading="eager"></figure>'
    rel = "\n".join(f"""      <a class="card rel" href="{r}.html"><span class="tag">Leia também</span><h3>{BYSLUG[r]["h1"]}</h3><p>{BYSLUG[r]["lead"][:120].rsplit(" ",1)[0]}…</p></a>""" for r in p["related"])
    body = f"""<main>
<section class="page-hero">
  <div class="wrap{' has-photo' if img else ''}">
    <div class="stack">
      <nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a> <span aria-hidden="true">›</span> <span>{p["h1"]}</span></nav>
      <span class="eyebrow">{p["eyebrow"]}</span>
      <h1>{p["h1"]}</h1>
      <p class="lead">{p["lead"]}</p>
      <p class="cred">Por <b>Dra. Renata Cerneiro Bertazzi</b>, médica oftalmologista · CRM-TO 7132 · RQE 3562 · Membro da SBRV</p>
      <div class="actions"><a class="btn" href="{IG}" target="_blank" rel="noopener">Agendar avaliação pelo Instagram</a></div>
    </div>
    {img}
  </div>
</section>

<section class="band">
  <div class="wrap">
    <article class="article">
{p["body"]}
    </article>
  </div>
</section>

<section class="band alt">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Dúvidas frequentes</span><h2>Perguntas sobre {p["nav"].lower() if p["nav"] not in ("Catarata","Retina") else ("a cirurgia de catarata" if p["nav"]=="Catarata" else "a cirurgia de retina")}</h2></div>
    {faq_html(p["faq"])}
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="head"><h2>Outros assuntos</h2></div>
    <div class="grid-3">
{rel}
    </div>
  </div>
</section>

{CTA}
</main>
"""
    open(p["slug"] + ".html", "w").write(head(p["title"], p["desc"], p["slug"], schema) + header(p["slug"]) + "\n" + body + "\n" + footer())

# ---------- home ----------
s = open("_home_base.html").read()
main = s[s.index("<main"):s.index("</main>") + 7]

def rep(old, new, count=1):
    global main
    assert old in main, old[:80]
    main = main.replace(old, new, count)

rep('<span class="eyebrow">Médica oftalmologista no Tocantins</span>', '<span class="eyebrow">Oftalmologista em Palmas (TO)</span>')
rep("Consultas, exames e cirurgia de catarata com a Dra. Renata Bertazzi em Palmas, Paraíso do Tocantins e Porto Nacional.",
    "Consultas, exames e cirurgias de catarata e de retina com a Dra. Renata Bertazzi em Palmas, Paraíso do Tocantins e Porto Nacional.")
rep('<a class="btn ghost" href="#catarata">Entender a catarata</a>', '<a class="btn ghost" href="cirurgia-de-catarata-palmas.html">Cirurgia de catarata</a>\n        <a class="btn ghost" href="cirurgia-de-retina-palmas.html">Cirurgia de retina</a>')
rep("médica oftalmologista com atuação dedicada à catarata e às doenças da retina.", "médica oftalmologista com atuação dedicada à catarata e às doenças da retina, no consultório e no centro cirúrgico.")
rep("<li>Cirurgia de catarata por facoemulsificação, com implante de lente intraocular</li>",
    '<li><a href="cirurgia-de-catarata-palmas.html">Cirurgia de catarata</a> por facoemulsificação, com implante de lente intraocular</li>\n        <li><a href="cirurgia-de-retina-palmas.html">Cirurgia de retina</a> (vitrectomia) para descolamento de retina, membrana epirretiniana, buraco macular e hemorragia vítrea</li>')
rep("<li>Avaliação da retina em pacientes com diabetes, pressão alta e miopia alta</li>", '<li><a href="injecao-intravitrea-e-laser-palmas.html">Injeções intravítreas e laser de retina</a> para retinopatia diabética, degeneração macular e roturas da retina</li>\n        <li>Avaliação da retina em pacientes com <a href="retinopatia-diabetica.html">diabetes</a>, pressão alta e miopia alta</li>')
# catarata section CTA after lens table
rep("""        </tbody>
      </table>
    </div>
  </div>
</section>""", """        </tbody>
      </table>
    </div>
    <p style="margin-top:22px;"><a class="more" href="cirurgia-de-catarata-palmas.html">Tudo sobre a cirurgia de catarata: preparo, lentes e recuperação →</a></p>
  </div>
</section>""")
# retina cards -> links
for slug, h3 in [("retinopatia-diabetica", "Retinopatia diabética"), ("degeneracao-macular", "Degeneração macular (DMRI)"), ("descolamento-de-retina", "Descolamento de retina")]:
    i = main.index(f"<h3>{h3}</h3>")
    j = main.index("</p>", i) + 4
    main = main[:j] + f'\n        <a class="more" href="{slug}.html">Saiba mais →</a>' + main[j:]
rep("<h2>A parte do olho que transforma luz em imagem</h2>", "<h2>Retina: diagnóstico, tratamento e cirurgia</h2>")
# retina surgery callout before exams heading
rep("""    <div class="head" style="margin-top: 48px; margin-bottom: 20px;">""", """    <div class="surg">
      <div class="stack">
        <span class="eyebrow">Cirurgia de retina</span>
        <h3>Vitrectomia e cirurgia de descolamento de retina</h3>
        <p class="muted">Quando a retina se descola, sangra ou é puxada por membranas, a cirurgia pode preservar ou recuperar a visão. A Dra. Renata realiza a cirurgia de retina em Palmas, além de <a href=\"injecao-intravitrea-e-laser-palmas.html\">injeções intravítreas e laser</a>.</p>
      </div>
      <a class="btn" href="cirurgia-de-retina-palmas.html">Entenda a cirurgia de retina</a>
    </div>

    <div class="head" style="margin-top: 48px; margin-bottom: 20px;">""")
main = main.replace('id="inicio"', 'id="inicio"')

faq_pairs = re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", main, re.S)
home_schema = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Dra. Renata Bertazzi · Oftalmologista em Palmas", "inLanguage": "pt-BR"},
    physician_schema(),
    faq_schema([(q, re.sub("<[^>]+>", "", a)) for q, a in faq_pairs]),
]}
home_title = "Oftalmologista em Palmas (TO) | Catarata e Retina | Dra. Renata Bertazzi"
home_desc = "Dra. Renata Bertazzi, oftalmologista em Palmas (TO): cirurgia de catarata, cirurgia de retina, injeção intravítrea e laser. Membro da SBRV. Atende no ICOG, Oftalmologia Avançada e OPUS."
open("index.html", "w").write(head(home_title, home_desc, "index", home_schema) + header("index") + "\n" + main + "\n" + footer())

# ---------- sitemap / robots ----------
from datetime import date
today = date.today().isoformat()
urls = [("index", "1.0")] + [(p["slug"], "0.8") for p in PAGES]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{url(sl)}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n" for sl, pr in urls) + "</urlset>\n"
open("sitemap.xml", "w").write(sm)
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
print("ok")
