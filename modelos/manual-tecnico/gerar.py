#!/usr/bin/env python3
"""Gera um manual técnico Techmeter em PDF a partir de uma pasta de manual.

Uso:
    python3 modelos/manual-tecnico/gerar.py documentos/manuais/<produto>

A pasta do manual precisa ter:
    manual.json    -> título, modelo, imagem da capa, nome do arquivo final
    conteudo.html  -> capítulos (<h2 class="capitulo">), seções (<h3>) e o texto

Saída: <pasta>/<arquivo>.pdf (e <arquivo>.html para conferência).
"""
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

MODELO = Path(__file__).resolve().parent
CHROME_CANDIDATOS = [
    "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome",
    shutil.which("chromium") or "", shutil.which("chromium-browser") or "",
    shutil.which("google-chrome") or "",
]

# Dados fixos da empresa (fonte: manual LATM 2025 / docs/empresa.md)
EMPRESA = {
    "razao": "K&K DO BRASIL LTDA.",
    "cnpj": "CNPJ: 65.636.888/0001-07",
    "endereco": "Rua Pedrália, 70 - Vila Gumercindo - São Paulo / SP",
    "telefone": "+55 (11) 5071-1630",
    "whatsapp": "+55 (11) 97643-5939",
    "email": "vendas@techmeter.com.br",
    "site": "www.techmeter.com.br",
}

ICONE_TEL = '<svg viewBox="0 0 24 24"><path fill="none" stroke="#4c5866" stroke-width="2" d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'
ICONE_ZAP = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#25a244"/><path fill="#fff" d="M8.5 7.5c.4-.4 1-.4 1.3.1l.8 1.6c.2.4.1.8-.2 1.1l-.5.5c.6 1.3 1.6 2.3 2.9 2.9l.5-.5c.3-.3.7-.4 1.1-.2l1.6.8c.5.3.5.9.1 1.3l-.7.7c-.6.6-1.5.8-2.3.4a9.6 9.6 0 0 1-5-5c-.4-.8-.2-1.7.4-2.3z"/></svg>'
ICONE_MAIL = '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="1.5" fill="none" stroke="#4c5866" stroke-width="2"/><path d="M3 6l9 7 9-7" fill="none" stroke="#4c5866" stroke-width="2"/></svg>'


def bloco_empresa():
    e = EMPRESA
    return f"""
<div class="empresa">
  <div class="razao">{e['razao']}</div>
  <div>{e['cnpj']}</div>
  <div>{html.escape(e['endereco'])}</div>
  <div class="linha"><span>{ICONE_TEL}{e['telefone']}</span><span>{ICONE_ZAP}{e['whatsapp']}</span></div>
  <div class="linha"><span>{ICONE_MAIL}{e['email']}</span></div>
</div>
<div class="marca"><img src="assets/logo-techmeter.png" alt="Techmeter"><span>MEASUREMENT &amp; CONTROL</span></div>"""


def titulos(conteudo):
    """Lista (nível, texto) dos capítulos (h2) e seções (h3) para o sumário."""
    itens = []
    for m in re.finditer(r"<h([23])[^>]*>(.*?)</h\1>", conteudo, re.S):
        texto = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        itens.append((1 if m.group(1) == "2" else 2, texto))
    return itens


def montar(meta, conteudo, paginas=None):
    itens = titulos(conteudo)
    linhas = []
    for i, (nivel, texto) in enumerate(itens):
        pg = paginas[i] if paginas and paginas[i] else ""
        linhas.append(f'<li class="n{nivel}"><span>{html.escape(texto)}</span><span class="pontos"></span><span>{pg}</span></li>')
    sumario = '<h2>Índice</h2><ul class="sumario">' + "".join(linhas) + "</ul>"
    contato = "".join(
        f'<div class="item"><b>{k}</b>{v}</div>' for k, v in [
            ("TELEFONE", EMPRESA["telefone"]), ("WHATSAPP", EMPRESA["whatsapp"]),
            ("E-MAIL", EMPRESA["email"]), ("SITE", EMPRESA["site"].upper()),
            ("ENDEREÇO", html.escape(EMPRESA["endereco"]))])
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>{html.escape(re.sub(r'<[^>]+>', ' ', meta['titulo']))}</title>
<link rel="stylesheet" href="estilo.css"></head><body>

<section class="capa">
  <img class="produto" src="{meta['imagem_capa']}" alt="">
  <div class="tipo">{html.escape(meta.get('tipo', 'MANUAL'))}</div>
  <hr>
  <h1>{meta['titulo']}</h1>
  <div class="modelo" style="top: {201 + 10.2 * (meta['titulo'].count('<br>') + 1):.1f}mm">MODELO: {html.escape(meta['modelo'])}</div>
  <div class="rodape-capa">{bloco_empresa()}</div>
</section>

<div class="rodape"><img class="ondas" src="assets/ondas.png" alt="">{bloco_empresa()}</div>
<table class="pagina">
  <thead><tr><td><div class="espaco-topo"></div></td></tr></thead>
  <tfoot><tr><td><div class="espaco-base"></div></td></tr></tfoot>
  <tbody><tr><td><div class="conteudo">
{sumario}
{conteudo}
  </div></td></tr></tbody>
</table>

<section class="contracapa">
  <div class="caixa"><h2>Contato</h2>{contato}</div>
  <div class="marca"><img src="assets/logo-techmeter.png" alt="Techmeter"><span>MEASUREMENT &amp; CONTROL</span></div>
</section>
</body></html>"""


def imprimir(html_path, pdf_path):
    chrome = next((c for c in CHROME_CANDIDATOS if c and Path(c).exists()), None)
    if not chrome:
        sys.exit("Chromium/Chrome não encontrado.")
    subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--allow-file-access-from-files", f"--print-to-pdf={pdf_path}", html_path.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)


def paginas_dos_titulos(pdf_path, itens):
    """Descobre em que página cada título caiu (pdftotext separa páginas com \\f)."""
    txt = subprocess.run(["pdftotext", "-layout", str(pdf_path), "-"], capture_output=True, text=True).stdout
    pags = [re.sub(r"\s+", " ", p).upper() for p in txt.split("\f")]
    res, inicio = [], 2  # pula capa e índice
    for _, texto in itens:
        alvo = re.sub(r"\s+", " ", texto).upper()
        achou = next((i for i in range(inicio, len(pags)) if alvo in pags[i]), None)
        res.append(achou + 1 if achou is not None else None)
        if achou is not None:
            inicio = achou
    return res


def main(pasta):
    pasta = Path(pasta).resolve()
    meta = json.loads((pasta / "manual.json").read_text(encoding="utf-8"))
    conteudo = (pasta / "conteudo.html").read_text(encoding="utf-8")
    build = pasta / "build"
    if build.exists():
        shutil.rmtree(build)
    shutil.copytree(MODELO / "assets", build / "assets")
    shutil.copy(MODELO / "estilo.css", build / "estilo.css")
    for extra in meta.get("arquivos", []) + [meta["imagem_capa"]]:
        destino = build / extra
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(pasta / extra, destino)

    html_path, pdf_path = build / "manual.html", build / "manual.pdf"
    html_path.write_text(montar(meta, conteudo), encoding="utf-8")
    imprimir(html_path, pdf_path)                       # 1ª passada: descobrir páginas
    paginas = paginas_dos_titulos(pdf_path, titulos(conteudo))
    html_path.write_text(montar(meta, conteudo, paginas), encoding="utf-8")
    imprimir(html_path, pdf_path)                       # 2ª passada: índice numerado

    final = pasta / f"{meta['arquivo']}.pdf"
    shutil.copy(pdf_path, final)
    faltando = [t for (_, t), p in zip(titulos(conteudo), paginas) if p is None]
    print(f"PDF gerado: {final}")
    if faltando:
        print("Aviso: títulos sem página no índice:", faltando)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
