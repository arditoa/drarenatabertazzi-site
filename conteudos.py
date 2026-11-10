# -*- coding: utf-8 -*-
"""Seção 'Conteúdos' (vídeos e orientações). Os itens ficam em conteudos.json."""
import json, html, re
from content import PAGES

BYSLUG = {p["slug"]: p for p in PAGES}
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="rgba(24,41,74,.72)"/><path d="M10 8l6 4-6 4z" fill="#fff"/></svg>'


def _yt_id(u):
    m = re.search(r"(?:youtu\.be/|v=|shorts/|embed/)([A-Za-z0-9_-]{11})", u or "")
    return m.group(1) if m else None


def _data(d):
    a, m, dd = d.split("-")
    return f"{int(dd)} {MESES[int(m) - 1]} {a}"


def carregar():
    raw = json.load(open("conteudos.json", encoding="utf-8")).get("itens", [])
    itens = []
    for it in raw:
        it = dict(it)
        pg = BYSLUG.get(it.get("pagina"))
        if pg:
            it.setdefault("titulo", pg["h1"])
            it.setdefault("resumo", pg["lead"][:150].rsplit(" ", 1)[0] + "…")
            if pg.get("img"):
                it.setdefault("capa", pg["img"][0])
        if it.get("pagina"):
            it["href"] = it["pagina"] + ".html"
        elif it.get("link"):
            it["href"] = it["link"]
        if it.get("youtube"):
            yid = _yt_id(it["youtube"])
            it["yt"] = yid
            if yid:
                it.setdefault("capa", f"https://i.ytimg.com/vi/{yid}/hqdefault.jpg")
        itens.append(it)
    itens.sort(key=lambda x: x.get("data", ""), reverse=True)
    return itens


def card(it):
    e = html.escape
    tema = e(it.get("tema", ""))
    tipo = "Vídeo" if it["tipo"] == "video" else "Leitura"
    meta = f'<span class="tag">{tipo}{" · " + tema if tema else ""}</span>'
    when = f'<span class="when">{_data(it["data"])}</span>' if it.get("data") else ""
    capa = it.get("capa")
    title = e(it["titulo"])
    resumo = e(it.get("resumo", ""))

    if it["tipo"] == "video" and it.get("arquivo"):
        poster = f' poster="{capa}"' if capa else ""
        media = f'<div class="c-media"><video src="{it["arquivo"]}" controls muted playsinline preload="none"{poster} aria-label="{title}"></video></div>'
        foot = ""
    elif it["tipo"] == "video" and it.get("yt"):
        media = (f'<div class="c-media"><iframe src="https://www.youtube-nocookie.com/embed/{it["yt"]}" title="{title}" loading="lazy" '
                 f'allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>')
        foot = ""
    elif it["tipo"] == "video" and it.get("instagram"):
        img = f'<img src="{capa}" alt="" loading="lazy">' if capa else '<span class="c-blank"></span>'
        media = f'<a class="c-media" href="{it["instagram"]}" target="_blank" rel="noopener" aria-label="Assistir no Instagram: {title}">{img}<span class="play">{PLAY}</span></a>'
        foot = f'<a class="more" href="{it["instagram"]}" target="_blank" rel="noopener">Assistir no Instagram →</a>'
    else:
        href = it.get("href", "#")
        ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        img = f'<img src="{capa}" alt="" loading="lazy">' if capa else '<span class="c-blank"></span>'
        media = f'<a class="c-media" href="{href}"{ext} tabindex="-1" aria-hidden="true">{img}</a>'
        foot = f'<a class="more" href="{href}"{ext}>Ler orientação →</a>'

    return (f'      <article class="c-card" data-tema="{tema}">{media}<div class="c-body">{meta}<h3>{title}</h3>'
            f'<p>{resumo}</p><div class="c-foot">{foot}{when}</div></div></article>')


def conteudos_home(svg):
    itens = carregar()[:3]
    if not itens:
        return ""
    cards = "\n".join(card(i) for i in itens)
    return f"""<section class="band alt" id="conteudos">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">Conteúdos</span>
      <h2>Vídeos e orientações para cuidar da sua visão</h2>
      <p>Explicações curtas e claras sobre catarata, retina e o dia a dia da cirurgia.</p>
    </div>
    <div class="c-grid">
{cards}
    </div>
    <p style="margin-top:22px"><a class="btn soft" href="conteudos.html">Ver todos os conteúdos</a></p>
  </div>
</section>"""


def build_conteudos(head, header, footer, url, SITE, physician_schema, CTA):
    itens = carregar()
    temas = []
    for i in itens:
        t = i.get("tema")
        if t and t not in temas:
            temas.append(t)
    chips = '<button type="button" class="chip" aria-pressed="true" data-f="">Todos</button>' + "".join(
        f'<button type="button" class="chip" aria-pressed="false" data-f="{html.escape(t)}">{html.escape(t)}</button>' for t in temas)
    cards = "\n".join(card(i) for i in itens)
    slug = "conteudos"
    title = "Conteúdos: vídeos e orientações sobre catarata e retina | Dra. Renata Bertazzi"
    desc = "Vídeos e orientações da Dra. Renata Bertazzi, oftalmologista em Palmas (TO), sobre catarata, retina, diabetes e cirurgia ocular."
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url(slug) + "#pagina", "url": url(slug), "name": title, "description": desc, "inLanguage": "pt-BR",
         "author": {"@id": SITE + "/#medica"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Conteúdos", "item": url(slug)}]},
        physician_schema()]}
    body = f"""<main>
<section class="page-hero">
  <div class="wrap">
    <div class="stack">
      <nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a> <span aria-hidden="true">›</span> <span>Conteúdos</span></nav>
      <span class="eyebrow">Vídeos e orientações</span>
      <h1>Conteúdos para entender e cuidar da sua visão</h1>
      <p class="lead">Explicações da Dra. Renata sobre catarata, retina, diabetes e cirurgia, em linguagem simples. Novos vídeos são publicados aqui e no Instagram.</p>
      <p class="cred">Por <b>Dra. Renata Carneiro Bertazzi</b>, médica oftalmologista · CRM-TO 7132 · RQE 3562 · Membro da SBRV</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="chips" role="group" aria-label="Filtrar por tema">{chips}</div>
    <div class="c-grid" id="c-lista">
{cards}
    </div>
    <p class="ethics">Os conteúdos são educativos e não substituem a consulta. Cada caso depende de avaliação individual.</p>
  </div>
</section>

{CTA}
</main>
<script>
document.querySelectorAll('.chip').forEach(function(b){{b.addEventListener('click',function(){{
  var f=b.dataset.f;document.querySelectorAll('.chip').forEach(function(x){{x.setAttribute('aria-pressed',x===b?'true':'false');}});
  document.querySelectorAll('#c-lista .c-card').forEach(function(c){{c.hidden=!!f&&c.dataset.tema!==f;}});
}});}});
</script>
"""
    open(slug + ".html", "w").write(head(title, desc, slug, schema) + header(slug) + "\n" + body + "\n" + footer())
