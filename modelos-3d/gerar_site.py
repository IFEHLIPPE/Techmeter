#!/usr/bin/env python3
"""Gera a pasta `site/` (publicada no Cloudflare Pages) a partir do configurador 3D.

Uso:
    python3 modelos-3d/gerar_site.py

Só o que estiver em `site/` vai para a internet. O resto do repositório não é publicado.
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
fonte = (RAIZ / "modelos-3d/medidor-eletromagnetico/configurador.html").read_text(encoding="utf-8")
fim_cabeca = fonte.index("<main")
pagina = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Modelo 3D interativo do medidor de vazão eletromagnético Techmeter. Gire, aproxime e escolha as cores.">
<style>body{{margin:0}}[hidden]{{display:none!important}}</style>
{fonte[:fim_cabeca].strip()}
</head>
<body>
{fonte[fim_cabeca:].strip()}
</body>
</html>
"""
destino = RAIZ / "site"
destino.mkdir(exist_ok=True)
(destino / "index.html").write_text(pagina, encoding="utf-8")
print("Gerado:", destino / "index.html")
