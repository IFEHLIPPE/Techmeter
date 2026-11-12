#!/usr/bin/env python3
"""Gera os gráficos de perda de carga (SVG) e insere no conteudo.html.

Os pontos foram medidos no gráfico "Head loss for fully open valve" da ficha do
fornecedor e redesenhados na mesma escala (eixos como no original).

Uso: python3 documentos/catalogos/valvula-solenoide-g80/graficos.py
"""
import math
import re
from pathlib import Path

PASTA = Path(__file__).resolve().parent

# Grade do gráfico original (em pixels relativos ao canto superior esquerdo da área do gráfico)
W, H = 246, 151
X_GRADE = [0, 41, 67, 84, 99, 111, 121, 126, 130, 134, 160, 175, 196, 213, 228, 240, 246]
X_ROTULOS = {0: "1", 41: "2", 67: "3", 84: "4", 99: "5", 134: "10", 160: "15", 175: "20", 196: "30", 213: "40", 228: "50"}
Y_GRADE = [0, 4, 7, 12, 19, 26, 36, 49, 72, 108, 113, 116, 120, 125, 130, 137, 144, 151]
Y_ROTULOS = {0: "1", 12: ",7", 26: ",5", 36: ",4", 49: ",3", 72: ",2", 108: ",1", 116: ",08", 144: ",04"}
ZONA = (0, 23, 197, 80)  # x0, y0, x1, y1

# Linhas: dois pontos medidos (x, y) por diâmetro
GRAFICOS = {
    "pequenas": [("3/4\"", (130.0, 1), (33.5, 145), "esq"), ("1\"", (146.0, 1), (53.0, 145), "dir")],
    "grandes": [("1-1/2\"", (198.0, 2), (124.0, 146), "esq"), ("2\"", (212.5, 2), (134.0, 146), "dir")],
}

AZUL, GRADE, ZONA_COR, TEXTO = "#1d2b4f", "#c9d4e0", "#dcebf8", "#4a4f57"


def no_quadro(p, q):
    """Estende a reta p-q até as bordas superior e inferior e recorta nas laterais."""
    (x1, y1), (x2, y2) = p, q
    k = (x2 - x1) / (y2 - y1)
    pts = []
    for y in (0, H):
        x = x1 + (y - y1) * k
        if x < 0:
            y = y1 + (0 - x1) / k; x = 0
        elif x > W:
            y = y1 + (W - x1) / k; x = W
        pts.append((x, y))
    return pts, k


def svg(linhas):
    s = [f'<svg viewBox="-34 -10 292 196" width="100%" font-family="Lato, Arial, sans-serif" role="img">']
    s.append(f'<rect x="{ZONA[0]}" y="{ZONA[1]}" width="{ZONA[2]-ZONA[0]}" height="{ZONA[3]-ZONA[1]}" fill="{ZONA_COR}"/>')
    for x in X_GRADE:
        s.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{GRADE}" stroke-width=".6"/>')
    for y in Y_GRADE:
        s.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{GRADE}" stroke-width=".6"/>')
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#9aa6b5" stroke-width=".8"/>')
    for x, t in X_ROTULOS.items():
        s.append(f'<text x="{x}" y="{H+9}" font-size="6.4" fill="{TEXTO}" text-anchor="middle">{t}</text>')
    for y, t in Y_ROTULOS.items():
        s.append(f'<text x="-3" y="{y+2.2}" font-size="6.4" fill="{TEXTO}" text-anchor="end">{t}</text>')
    s.append(f'<text x="{W/2}" y="{H+20}" font-size="7.2" fill="{AZUL}" text-anchor="middle" font-weight="700">Q (m³/h)</text>')
    s.append(f'<text transform="translate(-24 {H/2}) rotate(-90)" font-size="7.2" fill="{AZUL}" text-anchor="middle" font-weight="700">ΔH (kgf/cm²)</text>')
    s.append(f'<text x="{W-3}" y="100" font-size="5.6" fill="{AZUL}" text-anchor="end" letter-spacing=".4" font-weight="700">ZONA DE TRABALHO</text>')
    s.append(f'<text x="{W-3}" y="107" font-size="5.6" fill="{AZUL}" text-anchor="end" letter-spacing=".4" font-weight="700">RECOMENDADA</text>')
    for nome, p, q, lado in linhas:
        (a, b), k = no_quadro(p, q)
        s.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#d7261e" stroke-width="1.6" stroke-linecap="round"/>')
        ang = math.degrees(math.atan2(-1, -k))  # acompanha a reta, lendo de baixo para cima
        yl = 58 if lado == "esq" else 70
        xl = p[0] + (yl - p[1]) * k + (-7 if lado == "esq" else 7)
        s.append(f'<text transform="translate({xl:.1f} {yl}) rotate({ang:.1f})" font-size="7" fill="{AZUL}" font-weight="700" text-anchor="middle">{nome}</text>')
    s.append("</svg>")
    return "".join(s)


# Curva do 3": gráfico log-log real, medido na ficha do fornecedor (perda em m.c.a.,
# convertida para kgf/cm² dividindo por 10). Reta de (15,6 m³/h; 0,01) a (87 m³/h; 1,0).
def svg_3pol():
    x0, x1, y0, y1 = 10, 200, 0.01, 1.0
    def X(q): return W * (math.log10(q) - math.log10(x0)) / (math.log10(x1) - math.log10(x0))
    def Y(h): return H * (math.log10(y1) - math.log10(h)) / (math.log10(y1) - math.log10(y0))
    s = ['<svg viewBox="-34 -10 292 196" width="100%" font-family="Lato, Arial, sans-serif" role="img">']
    for d in (10, 100):
        for m in range(1, 10):
            q = d * m
            if x0 <= q <= x1:
                s.append(f'<line x1="{X(q):.1f}" y1="0" x2="{X(q):.1f}" y2="{H}" stroke="{GRADE}" stroke-width=".6"/>')
    for d in (0.01, 0.1):
        for m in range(1, 10):
            h = d * m
            if y0 <= h <= y1:
                s.append(f'<line x1="0" y1="{Y(h):.1f}" x2="{W}" y2="{Y(h):.1f}" stroke="{GRADE}" stroke-width=".6"/>')
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#9aa6b5" stroke-width=".8"/>')
    for q in (10, 20, 30, 40, 50, 100, 200):
        s.append(f'<text x="{X(q):.1f}" y="{H+9}" font-size="6.4" fill="{TEXTO}" text-anchor="middle">{q}</text>')
    for h, t in ((1, "1"), (0.4, ",4"), (0.2, ",2"), (0.1, ",1"), (0.04, ",04"), (0.02, ",02"), (0.01, ",01")):
        s.append(f'<text x="-3" y="{Y(h)+2.2:.1f}" font-size="6.4" fill="{TEXTO}" text-anchor="end">{t}</text>')
    s.append(f'<text x="{W/2}" y="{H+20}" font-size="7.2" fill="{AZUL}" text-anchor="middle" font-weight="700">Q (m³/h)</text>')
    s.append(f'<text transform="translate(-24 {H/2}) rotate(-90)" font-size="7.2" fill="{AZUL}" text-anchor="middle" font-weight="700">ΔH (kgf/cm²)</text>')
    a, b = (X(15.6), Y(0.01)), (X(87), Y(1.0))
    s.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#d7261e" stroke-width="1.6" stroke-linecap="round"/>')
    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    mx, my = a[0] + (b[0] - a[0]) * 0.55 - 7, a[1] + (b[1] - a[1]) * 0.55 - 4
    s.append(f'<text transform="translate({mx:.1f} {my:.1f}) rotate({ang:.1f})" font-size="7" fill="{AZUL}" font-weight="700" text-anchor="middle">3"</text>')
    s.append("</svg>")
    return "".join(s)


def main():
    arq = PASTA / "conteudo.html"
    txt = arq.read_text(encoding="utf-8")
    for chave, linhas in GRAFICOS.items():
        txt = re.sub(rf"<!--grafico:{chave}-->.*?<!--/grafico-->",
                     f"<!--grafico:{chave}-->{svg(linhas)}<!--/grafico-->", txt, flags=re.S)
    txt = re.sub(r"<!--grafico:3pol-->.*?<!--/grafico-->", f"<!--grafico:3pol-->{svg_3pol()}<!--/grafico-->", txt, flags=re.S)
    arq.write_text(txt, encoding="utf-8")
    print("Gráficos atualizados em", arq)


if __name__ == "__main__":
    main()
