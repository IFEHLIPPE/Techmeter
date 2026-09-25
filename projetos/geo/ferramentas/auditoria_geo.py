#!/usr/bin/env python3
"""Auditoria técnica GEO: robots.txt, sitemap e estrutura das páginas prioritárias.

Usa só a biblioteca padrão do Python (não precisa instalar nada).

Uso:
    python3 auditoria_geo.py https://www.techmeter.com.br
    python3 auditoria_geo.py https://www.techmeter.com.br /produto/medidor-de-vazao-eletromagnetico /servicos

Gera um relatório em Markdown na saída. Para salvar:
    python3 auditoria_geo.py https://www.techmeter.com.br > ../auditorias/AAAA-MM-DD.md
"""
import gzip
import json
import re
import sys
import urllib.error
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

USER_AGENT = "Mozilla/5.0 (compatible; TechmeterAuditoriaGEO/1.0)"

# Crawlers relevantes para busca e IA (nome no robots.txt -> para que serve)
CRAWLERS = {
    "Googlebot": "Busca Google e AI Overviews / Modo IA",
    "Google-Extended": "Uso em Gemini (treino/grounding); não afeta a busca",
    "Bingbot": "Busca Bing e Microsoft Copilot",
    "OAI-SearchBot": "Busca do ChatGPT (citações)",
    "ChatGPT-User": "ChatGPT abrindo páginas a pedido do usuário",
    "GPTBot": "Treino de modelos da OpenAI",
    "PerplexityBot": "Busca do Perplexity",
    "ClaudeBot": "Anthropic / Claude",
    "Applebot": "Siri / Spotlight / Apple Intelligence",
}

PAGINAS_PADRAO = ["/", "/produto/medidor-de-vazao-eletromagnetico"]


def baixar(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            corpo = r.read()
            if r.headers.get("Content-Encoding") == "gzip" or url.endswith(".gz"):
                corpo = gzip.decompress(corpo)
            return r.status, r.geturl(), dict(r.headers), corpo.decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, url, dict(e.headers), ""
    except Exception as e:  # rede, DNS, timeout
        return None, url, {}, str(e)


class Pagina(HTMLParser):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.title = ""
        self.meta = {}
        self.canonical = None
        self.headings = []
        self.jsonld = []
        self.links_internos = set()
        self.imgs_sem_alt = 0
        self.texto = []
        self._tag = None
        self._buf = ""
        self._ignorar = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "noscript"):
            self._ignorar += 1
            if tag == "script" and a.get("type") == "application/ld+json":
                self._tag, self._buf = "jsonld", ""
        elif tag == "meta" and a.get("name"):
            self.meta[a["name"].lower()] = a.get("content", "")
        elif tag == "link" and "canonical" in (a.get("rel") or "").lower().split():
            self.canonical = urljoin(self.base, a.get("href", ""))
        elif tag == "a" and a.get("href"):
            destino = urljoin(self.base, a["href"])
            if urlparse(destino).netloc == urlparse(self.base).netloc:
                self.links_internos.add(destino.split("#")[0])
        elif tag == "img" and not a.get("alt"):
            self.imgs_sem_alt += 1
        elif tag in ("title", "h1", "h2", "h3"):
            self._tag, self._buf = tag, ""

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self._ignorar = max(0, self._ignorar - 1)
        if tag != self._tag and not (self._tag == "jsonld" and tag == "script"):
            return
        texto = " ".join(self._buf.split())
        if self._tag == "title":
            self.title = texto
        elif self._tag == "jsonld":
            self.jsonld.append(self._buf)
        else:
            self.headings.append((self._tag, texto))
        self._tag = None

    def handle_data(self, data):
        if self._tag:
            self._buf += data
        if not self._ignorar:
            self.texto.append(data)


def tipos_jsonld(blocos):
    tipos = []

    def coletar(obj):
        if isinstance(obj, dict):
            t = obj.get("@type")
            if t:
                tipos.extend(t if isinstance(t, list) else [t])
            for v in obj.values():
                coletar(v)
        elif isinstance(obj, list):
            for v in obj:
                coletar(v)

    for b in blocos:
        try:
            coletar(json.loads(b))
        except ValueError:
            tipos.append("(JSON-LD inválido)")
    return sorted(set(tipos))


def urls_sitemap(url, visitados=None, profundidade=0):
    visitados = visitados if visitados is not None else set()
    if url in visitados or profundidade > 3:
        return [], []
    visitados.add(url)
    status, _, _, corpo = baixar(url)
    if status != 200:
        return [], [f"{url} → HTTP {status}"]
    try:
        raiz = ET.fromstring(corpo.encode("utf-8"))
    except ET.ParseError as e:
        return [], [f"{url} → XML inválido ({e})"]
    locs = [e.text.strip() for e in raiz.iter() if e.tag.endswith("loc") and e.text]
    if raiz.tag.endswith("sitemapindex"):
        urls, erros = [], []
        for sub in locs:
            u, e = urls_sitemap(sub, visitados, profundidade + 1)
            urls += u
            erros += e
        return urls, erros
    return locs, []


def main(site, caminhos):
    site = site.rstrip("/")
    paginas = [urljoin(site + "/", c.lstrip("/")) for c in caminhos]
    out = print
    out(f"# Auditoria técnica GEO — {site}\n")

    # robots.txt
    out("## robots.txt\n")
    status, _, _, robots_txt = baixar(site + "/robots.txt")
    sitemaps = []
    if status == 200:
        out(f"Status: **HTTP 200**\n\n```\n{robots_txt.strip()[:3000]}\n```\n")
        rp = urllib.robotparser.RobotFileParser()
        rp.parse(robots_txt.splitlines())
        sitemaps = rp.site_maps() or []
        out("| Crawler | Para que serve | " + " | ".join(urlparse(p).path or "/" for p in paginas) + " |")
        out("|---|---|" + "---|" * len(paginas))
        for bot, uso in CRAWLERS.items():
            res = ["✅ liberado" if rp.can_fetch(bot, p) else "⛔ bloqueado" for p in paginas]
            out(f"| {bot} | {uso} | " + " | ".join(res) + " |")
        out("")
    else:
        out(f"⚠️ robots.txt não encontrado ou com erro (HTTP {status}). Sem robots.txt todos os crawlers ficam liberados, mas o sitemap não é anunciado.\n")

    # sitemap
    out("## Sitemap\n")
    if not sitemaps:
        out("Nenhum `Sitemap:` declarado no robots.txt; testando `/sitemap.xml`.\n")
        sitemaps = [site + "/sitemap.xml"]
    todas = []
    for sm in sitemaps:
        urls, erros = urls_sitemap(sm)
        todas += urls
        out(f"- `{sm}`: {len(urls)} URLs" + (f" — erros: {'; '.join(erros)}" if erros else ""))
    normalizar = lambda u: u.rstrip("/").replace("://www.", "://")
    no_sitemap = {normalizar(u) for u in todas}
    out("\nPáginas prioritárias no sitemap:\n")
    for p in paginas:
        out(f"- {p}: {'✅ sim' if normalizar(p) in no_sitemap else '⚠️ não'}")
    out("")

    # páginas
    for p in paginas:
        out(f"## Página: {p}\n")
        status, final, headers, html = baixar(p)
        if status != 200:
            out(f"⚠️ HTTP {status} {html[:200] if status is None else ''}\n")
            continue
        pg = Pagina(final)
        pg.feed(html)
        palavras = len(re.findall(r"\w+", " ".join(pg.texto)))
        robots_meta = pg.meta.get("robots", "")
        x_robots = headers.get("X-Robots-Tag", "")
        tipos = tipos_jsonld(pg.jsonld)
        h1s = [t for n, t in pg.headings if n == "h1"]
        out(f"- **URL final:** {final}" + (" (redirecionou)" if final != p else ""))
        out(f"- **Title** ({len(pg.title)} caracteres): {pg.title or '⚠️ ausente'}")
        desc = pg.meta.get("description", "")
        out(f"- **Meta description** ({len(desc)} caracteres): {desc or '⚠️ ausente'}")
        out(f"- **Canonical:** {pg.canonical or '⚠️ ausente'}"
            + (" ⚠️ aponta para outra URL" if pg.canonical and normalizar(pg.canonical) != normalizar(final) else ""))
        out(f"- **Meta robots / X-Robots-Tag:** {robots_meta or '-'} / {x_robots or '-'}"
            + (" ⛔ NOINDEX" if "noindex" in (robots_meta + x_robots).lower() else ""))
        out(f"- **H1:** {len(h1s)}" + (" ⚠️ (o ideal é exatamente 1)" if len(h1s) != 1 else ""))
        out(f"- **Dados estruturados (JSON-LD):** {', '.join(tipos) if tipos else '⚠️ nenhum'}")
        out(f"- **Palavras no HTML (sem JavaScript):** {palavras}"
            + (" ⚠️ pouco conteúdo no HTML — pode depender de JavaScript" if palavras < 300 else ""))
        out(f"- **Links internos:** {len(pg.links_internos)}")
        out(f"- **Imagens sem alt:** {pg.imgs_sem_alt}")
        out("\n**Estrutura de headings:**\n")
        for nivel, texto in pg.headings:
            recuo = "  " * (int(nivel[1]) - 1)
            out(f"{recuo}- {nivel.upper()}: {texto or '(vazio)'}")
        out("")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2:] or PAGINAS_PADRAO)
