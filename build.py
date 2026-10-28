# -*- coding: utf-8 -*-
"""Gera o site estático da Dra. Renata Bertazzi (python3 build.py)."""
import json, html
from datetime import date
from content import PAGES

SITE = "https://drarenatabertazzi.com.br"
IG = "https://www.instagram.com/dra.renatabertazzi/"
DM = "https://ig.me/m/dra.renatabertazzi"   # abre conversa direta no Instagram
BYSLUG = {p["slug"]: p for p in PAGES}

CTA_MAIN = "Agendar consulta de avaliação"
CTA_TALK = "Tirar dúvidas com a equipe"

CLINICS = [
    {"name": "ICOG · Instituto de Catarata e Oftalmologia", "street": "ACSU SO 50, Av. LO 13, Conj. 02, Lote 01 (antiga 501 Sul), ao lado do Hospital Cristo Rei",
     "city": "Palmas", "zip": "77016-010", "phone": "+55-63-3322-2061", "phone_txt": "(63) 3322-2061",
     "maps": "https://www.google.com/maps/search/?api=1&query=ICOG+Instituto+de+Catarata+e+Oftalmologia+Palmas+TO"},
    {"name": "Oftalmologia Avançada", "street": "Quadra 104 Norte, Rua NE 5, nº 11", "city": "Palmas", "zip": "77006-020",
     "phone": "+55-63-3215-3335", "phone_txt": "(63) 3215-3335",
     "maps": "https://www.google.com/maps/search/?api=1&query=Oftalmologia+Avan%C3%A7ada+104+Norte+Palmas+TO"},
    {"name": "OPUS", "street": "Quadra 702 Sul, Av. Joaquim Teotônio Segurado, 15, Conj. 01, Sala 02 · Plano Diretor Sul", "city": "Palmas", "zip": None,
     "phone": None, "phone_txt": None,
     "maps": "https://www.google.com/maps/search/?api=1&query=OPUS+702+Sul+Avenida+Joaquim+Teot%C3%B4nio+Segurado+Palmas+TO"},
]

# ---------- ícones (traço) ----------
I = {
 "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.2-8 9-4.6-.8-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 "id": '<rect x="3" y="5" width="18" height="14" rx="3"/><circle cx="9" cy="11" r="2.4"/><path d="M5.8 16c.6-1.6 1.8-2.4 3.2-2.4s2.6.8 3.2 2.4M14.5 10h4M14.5 13.5h3"/>',
 "award": '<circle cx="12" cy="9" r="5.5"/><path d="M8.6 13.5L7.5 21l4.5-2.5 4.5 2.5-1.1-7.5"/>',
 "hospital": '<path d="M4 21V8l8-5 8 5v13"/><path d="M10 21v-5h4v5M12 8v5M9.5 10.5h5"/>',
 "eye": '<path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "clipboard": '<rect x="5" y="4" width="14" height="17" rx="2.5"/><path d="M9 4.5h6v2.5H9zM8.5 12l2 2 4-4M8.5 17h7"/>',
 "pulse": '<path d="M3 12h4l2.5-6 4 12 2.5-6H21"/>',
 "people": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c.8-3.4 3.2-5.2 6-5.2s5.2 1.8 6 5.2"/><circle cx="17" cy="9" r="2.4"/><path d="M16 14.8c2.4.2 4.2 1.8 5 4.6"/>',
 "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
 "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.3l2.6 2.6L16 9.5"/>',
 "drop": '<path d="M12 3.5s6 6.4 6 10.5a6 6 0 0 1-12 0c0-4.1 6-10.5 6-10.5z"/>',
 "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="2.5"/>',
 "alert": '<path d="M12 4 21 19.5H3z"/><path d="M12 10v4.5M12 17.2v.1"/>',
 "syringe": '<path d="M14 4l6 6M17 7l-9 9-3 1 1-3 9-9M11 8l5 5M4 20l2-2"/>',
 "lens": '<circle cx="12" cy="12" r="8"/><path d="M6 12c2-2.5 10-2.5 12 0"/>',
 "pin": '<path d="M12 21s-6.5-6.2-6.5-11A6.5 6.5 0 0 1 18.5 10c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
}
def ico(name, cls=""):
    return f'<span class="ico {cls}"><svg viewBox="0 0 24 24" aria-hidden="true">{I[name]}</svg></span>'
def svg(name):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[name]}</svg>'

def url(slug):
    return SITE + "/" if slug == "index" else f"{SITE}/{slug}.html"

def head(title, desc, slug, schema, og_img="img/dra-renata-bertazzi-oftalmologista-palmas.webp"):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
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
<meta name="theme-color" content="#fbf8f3">
<link rel="icon" type="image/png" href="img/simbolo.png">
<link rel="apple-touch-icon" href="img/simbolo-grande.png">
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
    links = [("index.html#seguranca", "Segurança", "seguranca"),
             ("index.html#jornada", "Como funciona", "jornada"),
             ("cirurgia-de-catarata-palmas.html", "Catarata", "cirurgia-de-catarata-palmas"),
             ("cirurgia-de-retina-palmas.html", "Retina", "cirurgia-de-retina-palmas"),
             ("index.html#onde-atendo", "Onde atendo", "onde")]
    nav = "\n".join(f'      <a href="{h}"{" aria-current=\"page\"" if k == current else ""}>{t}</a>' for h, t, k in links)
    return f"""<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Dra. Renata Bertazzi, página inicial">
      <img class="mark" src="img/simbolo.png" alt="" width="40" height="40"><span class="bt"><strong>Dra. Renata Bertazzi</strong>
      <span>Oftalmologia | Retina e Catarata</span></span>
    </a>
    <nav class="nav" aria-label="Principal">
{nav}
      <a class="btn" href="{DM}" target="_blank" rel="noopener">Agendar consulta</a>
    </nav>
  </div>
</header>
"""

MBAR = f"""<div class="mbar" role="region" aria-label="Contato rápido">
  <a class="btn soft" href="{DM}" target="_blank" rel="noopener">{svg("chat")} Tirar dúvidas</a>
  <a class="btn" href="{DM}" target="_blank" rel="noopener">Agendar consulta</a>
</div>
"""

def footer():
    names = {"cirurgia-de-catarata-palmas": "Cirurgia de catarata", "cirurgia-de-retina-palmas": "Cirurgia de retina"}
    pages = "\n".join(f'        <li><a href="{p["slug"]}.html">{names.get(p["slug"], p["nav"])}</a></li>' for p in PAGES)
    cl = "\n".join(f'        <li><b>{c["name"]}</b><br>{c["street"]} · {c["city"]} (TO){" · " + c["phone_txt"] if c["phone_txt"] else ""}</li>' for c in CLINICS)
    return f"""<footer class="site-foot">
  <div class="wrap foot-grid">
    <div class="stack">
      <img src="img/logo-dra-renata-bertazzi.png" alt="Dra. Renata Bertazzi · Oftalmologia | Retina e Catarata" class="foot-logo" width="230" height="43" loading="lazy">
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
  <div class="wrap"><p class="foot-note">As informações deste site são educativas e não substituem a consulta médica. Diagnóstico e tratamento dependem de avaliação individual. Responsável técnica: Dra. Renata Cerneiro Bertazzi · CRM-TO 7132 · RQE 3562.</p></div>
</footer>
{MBAR}</body>
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
        "@type": "Physician", "@id": SITE + "/#medica",
        "name": "Dra. Renata Cerneiro Bertazzi", "alternateName": "Dra. Renata Bertazzi",
        "description": "Médica oftalmologista em Palmas (TO): cirurgia de catarata, cirurgia de retina, injeção intravítrea e laser. Membro da Sociedade Brasileira de Retina e Vítreo.",
        "url": SITE + "/", "image": SITE + "/img/dra-renata-bertazzi-oftalmologista-palmas.webp", "logo": SITE + "/img/logo-dra-renata-bertazzi.png",
        "medicalSpecialty": "Ophthalmologic", "sameAs": [IG],
        "address": locs[0]["address"], "location": locs,
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
      <h2>Vamos conversar sobre a sua visão?</h2>
      <p>Mande uma mensagem e diga a cidade de sua preferência. A equipe responde suas dúvidas e encontra o melhor horário para a sua consulta de avaliação.</p>
    </div>
    <div class="actions">
      <a class="btn" href="{DM}" target="_blank" rel="noopener">{CTA_MAIN}</a>
      <a class="btn soft" href="{DM}" target="_blank" rel="noopener">{CTA_TALK}</a>
    </div>
  </div>
</section>"""

# =================== páginas internas ===================
for p in PAGES:
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "MedicalWebPage", "@id": url(p["slug"]) + "#pagina", "url": url(p["slug"]), "name": p["title"], "description": p["desc"],
         "inLanguage": "pt-BR", "author": {"@id": SITE + "/#medica"}, "reviewedBy": {"@id": SITE + "/#medica"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": p["h1"], "item": url(p["slug"])}]},
        physician_schema(), faq_schema(p["faq"])]}
    img = f'<figure class="page-photo"><img src="{p["img"][0]}" alt="{p["img"][1]}"></figure>' if p["img"] else ""
    rel = "\n".join(f'      <a class="card rel" href="{r}.html"><span class="tag">Leia também</span><h3>{BYSLUG[r]["h1"]}</h3><p>{BYSLUG[r]["lead"][:118].rsplit(" ",1)[0]}…</p><span class="more">Ler mais →</span></a>' for r in p["related"])
    faqtitle = {"Catarata": "a cirurgia de catarata", "Retina": "a cirurgia de retina"}.get(p["nav"], p["nav"].lower())
    body = f"""<main>
<section class="page-hero">
  <div class="wrap{' has-photo' if img else ''}">
    <div class="stack">
      <nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a> <span aria-hidden="true">›</span> <span>{p["h1"]}</span></nav>
      <span class="eyebrow">{p["eyebrow"]}</span>
      <h1>{p["h1"]}</h1>
      <p class="lead">{p["lead"]}</p>
      <p class="cred">Por <b>Dra. Renata Cerneiro Bertazzi</b>, médica oftalmologista · CRM-TO 7132 · RQE 3562 · Membro da SBRV</p>
      <div class="actions"><a class="btn" href="{DM}" target="_blank" rel="noopener">{CTA_MAIN}</a><a class="btn soft" href="{DM}" target="_blank" rel="noopener">{CTA_TALK}</a></div>
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
    <div class="head"><span class="eyebrow">Dúvidas frequentes</span><h2>Perguntas sobre {faqtitle}</h2></div>
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

# =================== página inicial ===================
HOME_FAQ = [
    ("A primeira consulta já define a cirurgia?", "Não necessariamente. A primeira consulta serve para examinar seus olhos com calma, entender suas queixas e explicar as opções. Quando há indicação de cirurgia, os exames e o planejamento são feitos em seguida, sem pressa."),
    ("A cirurgia de catarata dói?", "Na maioria dos casos a anestesia é feita com colírio, às vezes com sedação leve. O paciente fica acordado, tranquilo, e pode sentir apenas uma leve pressão no olho."),
    ("Vou conseguir tirar dúvidas depois da cirurgia?", "Sim. Você sai com as orientações por escrito, os retornos já programados e um canal direto com a equipe para dúvidas no pós-operatório."),
    ("Tenho diabetes e enxergo bem. Preciso examinar a retina?", "Sim. A retinopatia diabética pode avançar sem sintomas. O exame anual de fundo de olho é a forma de encontrar alterações a tempo de tratar."),
    ("Como faço para agendar?", "Envie uma mensagem pelo Instagram @dra.renatabertazzi informando a cidade de sua preferência. A equipe responde e combina o melhor horário."),
]

clinic_cards = []
for c in CLINICS:
    phone = f'<a href="tel:{c["phone"].replace("-", "")}">{c["phone_txt"]}</a>' if c["phone"] else ""
    clinic_cards.append(f"""      <div class="card place">
        {ico("pin", "b")}
        <div class="clinic" style="border:0;padding:0;"><b>{c["name"]}</b><p>{c["street"]} · {c["city"]} (TO){(" · CEP " + c["zip"]) if c["zip"] else ""}</p>
          <p class="links">{phone}<a href="{c["maps"]}" target="_blank" rel="noopener">Ver no mapa</a></p></div>
      </div>""")

treat = [
    ("cirurgia-de-catarata-palmas", "lens", "", "Cirurgia de catarata", "Facoemulsificação com implante de lente intraocular, escolhida junto com você."),
    ("cirurgia-de-retina-palmas", "eye", "b", "Cirurgia de retina", "Vitrectomia para descolamento de retina, membranas, buraco macular e hemorragia."),
    ("injecao-intravitrea-e-laser-palmas", "syringe", "p", "Injeção intravítrea e laser", "Tratamentos rápidos, com colírio anestésico, para DMRI, diabetes e roturas da retina."),
    ("retinopatia-diabetica", "drop", "", "Retinopatia diabética", "Exame anual e tratamento para quem tem diabetes, mesmo enxergando bem."),
    ("degeneracao-macular", "target", "b", "Degeneração macular", "Diagnóstico com OCT e tratamento da DMRI para preservar a visão central."),
    ("descolamento-de-retina", "alert", "p", "Descolamento de retina", "Clarões, moscas novas ou sombra na visão pedem avaliação no mesmo dia."),
]
treat_cards = "\n".join(f'      <a class="card" href="{s}.html">{ico(i, c)}<h3>{t}</h3><p>{d}</p><span class="more">Saiba mais →</span></a>' for s, i, c, t, d in treat)

# ---------- depoimentos (preenchidos em depoimentos.json) ----------
_dep = json.load(open("depoimentos.json", encoding="utf-8")).get("depoimentos", [])
if _dep:
    _cards = "\n".join(
        f'      <figure class="quote" style="margin:0;"><p>{html.escape(d["texto"])}</p><footer>{html.escape(d.get("nome", ""))}{(" · " + html.escape(d["contexto"])) if d.get("contexto") else ""}</footer></figure>'
        for d in _dep)
    DEPO = f"""<section class="band sand" id="depoimentos">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">O que os pacientes dizem</span>
      <h2>A experiência de quem passou por aqui.</h2>
    </div>
    <div class="quotes">
{_cards}
    </div>
    <p class="ethics">Relatos publicados com autorização dos pacientes. Eles falam da experiência de atendimento, não de resultados: cada caso é único e depende de avaliação individual.</p>
  </div>
</section>"""
else:
    DEPO = ""

HOME = f"""<main id="inicio">

<section class="hero">
  <div class="wrap">
    <div class="hero-photo">
      <div class="frame"><img src="img/dra-renata-bertazzi-oftalmologista-palmas.webp" alt="Dra. Renata Bertazzi, oftalmologista em Palmas, sorrindo em seu consultório" width="960" height="1280" fetchpriority="high"></div>
      <div class="seal"><b>+500</b><span>cirurgias realizadas</span></div>
    </div>
    <div class="hero-text">
      <div class="hero-name">
        <strong>Dra. Renata Bertazzi</strong>
        <span>Médica oftalmologista · Catarata e Retina · Palmas (TO)</span>
      </div>
      <ul class="creds" aria-label="Credenciais">
        <li class="key">{svg("id")} CRM-TO 7132</li>
        <li class="key">{svg("shield")} RQE 3562 · Oftalmologia</li>
        <li>{svg("award")} Membro da SBRV</li>
        <li>{svg("hospital")} Cirurgias no Oftalmologia Avançada</li>
      </ul>
      <h1>Cirurgia com rigor técnico e o cuidado que você merece em cada etapa.</h1>
      <p class="lead">Da primeira consulta ao último retorno, você é acompanhado pela mesma médica, com explicações claras e tempo para todas as suas dúvidas.</p>
      <div class="actions">
        <a class="btn" href="{DM}" target="_blank" rel="noopener">{CTA_MAIN}</a>
        <a class="btn soft" href="{DM}" target="_blank" rel="noopener">{svg("chat")} {CTA_TALK}</a>
      </div>
    </div>
  </div>
</section>

<section class="trust" aria-label="Em números">
  <div class="wrap">
    <div><b>+500</b><span>cirurgias realizadas</span></div>
    <div><b>RQE 3562</b><span>especialista registrada em Oftalmologia</span></div>
    <div><b>SBRV</b><span>membro da Sociedade Brasileira de Retina e Vítreo</span></div>
    <div><b>3 clínicas</b><span>em Palmas, com atendimento à região</span></div>
  </div>
</section>

<section class="band" id="sobre">
  <div class="wrap grid-2">
    <figure class="about-photo" style="margin:0;"><img src="img/dra-renata-bertazzi-congresso-sbrv.webp" alt="Dra. Renata Bertazzi no congresso da Sociedade Brasileira de Retina e Vítreo" loading="lazy"><figcaption>No congresso da Sociedade Brasileira de Retina e Vítreo (SBRV).</figcaption></figure>
    <div class="stack">
      <span class="eyebrow">Sobre a médica</span>
      <h2>Experiência no centro cirúrgico. Escuta no consultório.</h2>
      <p class="muted">A Dra. Renata Cerneiro Bertazzi é médica oftalmologista com atuação dedicada à catarata e às doenças da retina, no consultório e no centro cirúrgico. Já realizou mais de 500 cirurgias e atende pacientes de Palmas e da região central do Tocantins.</p>
      <ul class="ticks">
        <li><a href="cirurgia-de-catarata-palmas.html">Cirurgia de catarata</a> por facoemulsificação</li>
        <li><a href="cirurgia-de-retina-palmas.html">Cirurgia de retina</a> (vitrectomia) e tratamento do descolamento de retina</li>
        <li><a href="injecao-intravitrea-e-laser-palmas.html">Injeções intravítreas e laser</a> para retinopatia diabética e degeneração macular</li>
      </ul>
      <div class="cred-box">
        <div class="cred-num"><b>5%</b><span>dos oftalmologistas do país</span></div>
        <div><b>Membro da SBRV</b><p>A Dra. Renata passou pela prova de admissão da Sociedade Brasileira de Retina e Vítreo. Estima-se que apenas 5% dos oftalmologistas do país sejam membros.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="band alt" id="seguranca">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">Como cuidamos da sua segurança</span>
      <h2>Cada etapa é planejada para você operar tranquilo.</h2>
      <p>Segurança não é um detalhe do dia da cirurgia. Ela começa na primeira consulta e segue até a sua alta.</p>
    </div>
    <div class="safe-list">
      <div class="safe">{ico("clipboard")}<div><h3>Avaliação completa antes de operar</h3><p>Exames dos olhos que medem cada detalhe, como a biometria, o mapeamento de retina e a tomografia (OCT), e uma revisão da sua saúde geral: pressão, glicemia, alergias e remédios em uso.</p></div></div>
      <div class="safe">{ico("hospital", "b")}<div><h3>Centro cirúrgico preparado</h3><p>As cirurgias são feitas em centro cirúrgico com equipamentos modernos, material esterilizado e estrutura de apoio para qualquer imprevisto.</p></div></div>
      <div class="safe">{ico("people", "p")}<div><h3>Equipe que trabalha junta</h3><p>Médico anestesista e equipe de enfermagem acostumados com cirurgia ocular. Todos sabem o que fazer em cada momento, e isso se traduz em calma para você.</p></div></div>
      <div class="safe">{ico("pulse")}<div><h3>Monitoramento contínuo</h3><p>Durante todo o procedimento, seus batimentos, sua pressão e a oxigenação são acompanhados em tempo real.</p></div></div>
    </div>
    <div class="checklist">
      <h3>Checklist de cirurgia segura</h3>
      <p>Antes de começar, a equipe para e confere, em voz alta, os pontos essenciais. É um protocolo recomendado pela Organização Mundial da Saúde.</p>
      <ul>
        <li>{svg("check")}<span>Sua identidade e o procedimento planejado</span></li>
        <li>{svg("check")}<span>O olho a ser operado, marcado com antecedência</span></li>
        <li>{svg("check")}<span>A lente intraocular certa, com o grau calculado nos exames</span></li>
        <li>{svg("check")}<span>Alergias, remédios em uso e cuidados especiais</span></li>
      </ul>
    </div>
    <div class="strip" aria-label="Preparo antes de cada cirurgia">
      <figure><img src="img/preparo-instrumental-cirurgico.webp" alt="Dra. Renata conferindo a caixa de instrumentos cirúrgicos"><figcaption>Conferência do instrumental</figcaption></figure>
      <figure><img src="img/preparo-facoemulsificador.webp" alt="Dra. Renata preparando o facoemulsificador"><figcaption>Preparo do equipamento</figcaption></figure>
      <figure><img src="img/microscopio-cirurgico-catarata.webp" alt="Dra. Renata ajustando o microscópio cirúrgico"><figcaption>Ajuste do microscópio</figcaption></figure>
      <figure><video src="img/bastidores-sala-cirurgica.mp4" autoplay muted loop playsinline preload="metadata" aria-label="Vídeo da Dra. Renata preparando a sala cirúrgica"></video><figcaption>Sala preparada para você</figcaption></figure>
    </div>
  </div>
</section>

<section class="band" id="jornada">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">Sua jornada, passo a passo</span>
      <h2>Você sabe o que vai acontecer em cada etapa.</h2>
    </div>
    <ol class="journey">
      <li><span class="num">1</span><div><h3>Primeira consulta, sem pressa</h3><p>Exame completo e uma conversa de verdade: o que você sente, o que espera enxergar e quais são as opções. Você sai entendendo o seu caso.</p></div></li>
      <li><span class="num">2</span><div><h3>Preparo e planejamento</h3><p>Exames específicos, escolha da lente ou da técnica junto com você e todas as orientações para o dia da cirurgia, por escrito.</p></div></li>
      <li><span class="num">3</span><div><h3>Dia do procedimento</h3><p>Você é recebido pela equipe, tem as dúvidas de última hora respondidas e é acompanhado do começo ao fim. Em geral, volta para casa no mesmo dia.</p></div></li>
      <li><span class="num">4</span><div><h3>Pós-operatório próximo</h3><p>Retornos já programados e acompanhamento com a mesma médica até a alta.</p><span class="note">Canal direto com a equipe para dúvidas no pós-operatório</span></div></li>
    </ol>
  </div>
</section>

<section class="feature" aria-label="Cuidado durante a cirurgia">
  <div class="wrap">
    <img src="img/cirurgia-catarata-cuidado-paciente.webp" alt="Durante a cirurgia de catarata, uma mão segura a mão do paciente enquanto a médica opera ao microscópio" loading="lazy">
    <div class="stack">
      <span class="eyebrow">Durante a cirurgia</span>
      <h2>Você fica acordado. E não fica sozinho.</h2>
      <p>Na cirurgia de catarata, a anestesia costuma ser feita com colírio. A equipe conversa com você, explica o que está acontecendo e garante que você se sinta seguro do começo ao fim.</p>
    </div>
  </div>
</section>

<section class="band" id="tratamentos">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">Tratamentos</span>
      <h2>Catarata e retina, do diagnóstico à cirurgia.</h2>
    </div>
    <div class="grid-3">
{treat_cards}
    </div>
    <div class="alert" role="note">
      <h3>Procure atendimento no mesmo dia se notar:</h3>
      <p>Clarões de luz que surgem de repente, muitos pontos ou "moscas" novas na visão, ou uma sombra que parece uma cortina cobrindo parte do que você vê.</p>
    </div>
  </div>
</section>

{DEPO}

<section class="band alt" id="onde-atendo">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">Onde atendo</span>
      <h2>Três clínicas em Palmas, perto de você.</h2>
      <p>Pacientes de Paraíso do Tocantins, Porto Nacional e região são atendidos em Palmas.</p>
    </div>
    <div class="clinic-grid">
{chr(10).join(clinic_cards)}
    </div>
  </div>
</section>

<section class="band" id="duvidas">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Dúvidas frequentes</span><h2>Perguntas que os pacientes costumam fazer.</h2></div>
    {faq_html(HOME_FAQ)}
  </div>
</section>

{CTA}
</main>
"""

home_schema = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Dra. Renata Bertazzi · Oftalmologista em Palmas", "inLanguage": "pt-BR"},
    physician_schema(), faq_schema(HOME_FAQ)]}
home_title = "Oftalmologista em Palmas (TO) | Catarata e Retina | Dra. Renata Bertazzi"
home_desc = "Dra. Renata Bertazzi, oftalmologista em Palmas (TO): cirurgia de catarata, cirurgia de retina, injeção intravítrea e laser. CRM-TO 7132, RQE 3562, membro da SBRV."
open("index.html", "w").write(head(home_title, home_desc, "index", home_schema) + header("index") + "\n" + HOME + "\n" + footer())

# =================== sitemap / robots ===================
today = date.today().isoformat()
urls = [("index", "1.0")] + [(p["slug"], "0.8") for p in PAGES]
open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{url(sl)}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n" for sl, pr in urls) + "</urlset>\n")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
print("ok")
