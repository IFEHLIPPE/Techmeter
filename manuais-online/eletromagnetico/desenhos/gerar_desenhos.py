#!/usr/bin/env python3
"""Gera as figuras do manual online do eletromagnético no traço dos desenhos Techmeter.

Fonte: os desenhos de trechos retos em `fonte/` (enviados pelo Felippe em 23/11/2026).
Tudo o que não veio pronto é montado a partir das peças desses desenhos
(medidor, flanges, quebra de tubo, cotas), para manter o mesmo traço.

Uso:
    python manuais-online/eletromagnetico/desenhos/gerar_desenhos.py

Saída: `../img/` (o build.py copia de lá para o site).
"""
import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
FONTE = AQUI / "fonte"
SAIDA = AQUI.parent / "img"
PRETO = 0
TRACO = 4          # espessura das linhas de contorno (px na escala dos desenhos)
FINO = 2           # linhas de cota e de chamada
LARGURA_WEB = 1200


def serif(tam, negrito=False):
    return ImageFont.truetype(str(FONTE / ("NotoSerif-Bold.ttf" if negrito else "NotoSerif-Regular.ttf")), tam)


def sans(tam, negrito=True):
    nome = "LiberationSans-Bold.ttf" if negrito else "LiberationSans-Regular.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/liberation/{nome}", tam)


def mono(tam):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", tam)


def abrir(nome):
    return Image.open(FONTE / nome).convert("L")


def aparar(im, margem=40):
    """Corta o branco em volta e deixa uma margem igual."""
    inv = ImageChops.invert(im)
    caixa = inv.point(lambda v: 255 if v > 40 else 0).getbbox()
    im = im.crop(caixa)
    novo = Image.new("L", (im.width + 2 * margem, im.height + 2 * margem), 255)
    novo.paste(im, (margem, margem))
    return novo


def salvar(im, nome, largura=LARGURA_WEB):
    im = aparar(im)
    if im.width > largura:
        im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
    im = im.quantize(colors=16)
    im.save(SAIDA / nome, optimize=True)
    print("ok", nome, im.size)


def sobrepor(base, peca, x, y):
    """Cola a peça sem o fundo branco (multiplica: branco não apaga nada)."""
    area = base.crop((x, y, x + peca.width, y + peca.height))
    base.paste(ImageChops.multiply(area, peca), (x, y))


def seta(d, x1, y1, x2, y2, tam=26, larg=9):
    """Ponta de seta cheia em (x2, y2), no estilo das cotas."""
    a = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - tam * math.cos(a) + larg * math.sin(a), y2 - tam * math.sin(a) - larg * math.cos(a))
    p2 = (x2 - tam * math.cos(a) - larg * math.sin(a), y2 - tam * math.sin(a) + larg * math.cos(a))
    d.polygon([(x2, y2), p1, p2], fill=PRETO)


def cota_h(d, x1, x2, y, texto, ext_de=None, fonte=None):
    """Cota horizontal com setas nas duas pontas e linhas de extensão."""
    fonte = fonte or serif(46)
    if ext_de is not None:
        for x in (x1, x2):
            d.line([(x, ext_de), (x, y + 22)], fill=PRETO, width=FINO)
    d.line([(x1, y), (x2, y)], fill=PRETO, width=FINO)
    seta(d, x2, y, x1, y); seta(d, x1, y, x2, y)
    d.text(((x1 + x2) / 2, y - 14), texto, font=fonte, fill=PRETO, anchor="mb")


def cota_v(d, x, y1, y2, texto, ext_de=None, fonte=None, lado="esq"):
    fonte = fonte or serif(46)
    if ext_de is not None:
        for y in (y1, y2):
            d.line([(ext_de, y), (x + (-22 if lado == "esq" else 22), y)], fill=PRETO, width=FINO)
    d.line([(x, y1), (x, y2)], fill=PRETO, width=FINO)
    seta(d, x, y2, x, y1); seta(d, x, y1, x, y2)
    d.text((x - 16 if lado == "esq" else x + 16, (y1 + y2) / 2), texto, font=fonte, fill=PRETO,
           anchor="rm" if lado == "esq" else "lm")


def chamada(d, pontos, texto, fonte=None, ancora="lm"):
    """Linha de chamada (polilinha) com um ponto no início e texto no fim."""
    fonte = fonte or serif(44)
    d.line(pontos, fill=PRETO, width=FINO)
    x, y = pontos[0]
    d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=PRETO)
    xt, yt = pontos[-1]
    dx = {"l": 14, "r": -14}.get(ancora[0], 0)
    dy = -12 if ancora[1] == "d" else 0
    d.multiline_text((xt + dx, yt + dy), texto, font=fonte, fill=PRETO, anchor=ancora, spacing=8)


# ------------------------------------------------------------------ peças tiradas dos desenhos
ORIG = abrir("01_valvula_a_montante.png")
# medidor completo (conversor + sensor + pares de flanges), com um toco de tubo de cada lado
MED_CAIXA = (1340, 125, 2060, 920)
MEDIDOR = ORIG.crop(MED_CAIXA)
TUBO_Y = (634, 832)                       # linhas de cima e de baixo do tubo no desenho 01
TUBO_D = TUBO_Y[1] - TUBO_Y[0]            # diâmetro externo do tubo (px)
MED_CY = (TUBO_Y[0] + TUBO_Y[1] + 4) // 2 - MED_CAIXA[1]   # centro do tubo dentro da peça
def _quebra():
    """Símbolo de tubo cortado, no mesmo desenho das pontas dos desenhos originais (ponta esquerda)."""
    D = TUBO_D; im = Image.new("L", (120, D + 12), 255); d = ImageDraw.Draw(im)
    t, m, b = 6, 6 + D // 2, 6 + D
    d.arc([12, t, 108, m + 4], 90, 270, fill=PRETO, width=TRACO)    # folha de cima, lado esquerdo
    d.arc([30, t, 86, m + 4], 270, 90, fill=PRETO, width=TRACO)     # folha de cima, lado direito
    d.arc([10, m - 2, 104, b], 270, 90, fill=PRETO, width=TRACO)    # curva de baixo
    return im
QUEBRA = _quebra()
QUEBRA_X = 58                             # x da ponta dentro do símbolo


def medidor_limpo():
    """Medidor sozinho, sem tubo e sem parafusos (para a figura de dimensões)."""
    m = ORIG.crop((1300, 80, 2050, 1000)).copy()      # mesmo recorte usado no estudo das peças
    d = ImageDraw.Draw(m)
    # tira os parafusos e porcas do lado de dentro dos flanges do medidor
    for x0, x1 in ((236, 292), (503, 559)):
        d.rectangle([x0, 465, x1, 538], fill=255)
        d.rectangle([x0, 772, x1, 845], fill=255)
    d.rectangle([0, 350, 192, 920], fill=255)          # flange do tubo e junta (lado esquerdo)
    d.rectangle([604, 350, 750, 920], fill=255)        # flange do tubo e junta (lado direito)
    # recorta do prensa-cabo ao flange direito do medidor
    return m.crop((145, 40, 604, 842))


def tubo(d, pontos, diam=TUBO_D, inicio=True, fim=True):
    """Desenha um tubo (duas linhas paralelas) seguindo a linha de centro dada."""
    r = diam / 2
    esq, dir_ = [], []
    n = len(pontos)
    for i, (x, y) in enumerate(pontos):
        if i == 0:
            dx, dy = pontos[1][0] - x, pontos[1][1] - y
            nx, ny = -dy, dx; L = math.hypot(nx, ny); nx, ny = nx / L * r, ny / L * r
        elif i == n - 1:
            dx, dy = x - pontos[i - 1][0], y - pontos[i - 1][1]
            nx, ny = -dy, dx; L = math.hypot(nx, ny); nx, ny = nx / L * r, ny / L * r
        else:  # junta em meia-esquadria
            a1 = math.atan2(y - pontos[i - 1][1], x - pontos[i - 1][0])
            a2 = math.atan2(pontos[i + 1][1] - y, pontos[i + 1][0] - x)
            am = (a1 + a2) / 2
            if abs(a2 - a1) > math.pi:
                am += math.pi
            k = r / max(math.cos((a2 - a1) / 2), 0.2)
            nx, ny = -math.sin(am) * k, math.cos(am) * k
        esq.append((x + nx, y + ny)); dir_.append((x - nx, y - ny))
    d.line(esq, fill=PRETO, width=TRACO, joint="curve")
    d.line(dir_, fill=PRETO, width=TRACO, joint="curve")
    return esq, dir_


def ponta(base, x, y, angulo=0, espelhar=False):
    """Cola o símbolo de tubo cortado com o centro em (x, y)."""
    q = QUEBRA.transpose(Image.FLIP_LEFT_RIGHT) if espelhar else QUEBRA
    dx = (q.width - QUEBRA_X if espelhar else QUEBRA_X) - q.width / 2   # ponta em relação ao centro
    if angulo:
        q = q.rotate(angulo, expand=True, fillcolor=255, resample=Image.BICUBIC)
    a = math.radians(-angulo)
    cx, cy = x - dx * math.cos(a), y - dx * math.sin(a)
    sobrepor(base, q, int(cx - q.width / 2), int(cy - q.height / 2))


def seta_fluxo(d, x, y, comp=120, angulo=0):
    a = math.radians(angulo)
    x2, y2 = x + comp * math.cos(a), y + comp * math.sin(a)
    d.line([(x, y), (x2 - 30 * math.cos(a), y2 - 30 * math.sin(a))], fill=PRETO, width=9)
    seta(d, x, y, x2, y2, tam=42, larg=18)


# ------------------------------------------------------------------ 1. trechos retos
def legenda_retos(im, novo_l1, novo_l2):
    """Troca os números da legenda 'L1⩾ 50DN; L2⩾5DN' reaproveitando as letras do desenho."""
    a = im.crop((1130, 1195, 1900, 1290))
    gl = {  # recortes das letras na legenda original (x0, x1)
        "L": (1143, 1184), "1": (1191, 1219), "≥": (1231, 1288), "5": (1319, 1354), "0": (1362, 1398),
        "D": (1405, 1456), "N": (1463, 1517), ";": (1525, 1537), "2": (1615, 1650),
    }
    def letra(c):
        if c in gl:
            x0, x1 = gl[c]
            return im.crop((x0, 1195, x1 + 1, 1290))
        # algarismo que não existe na legenda: desenha na mesma fonte serifada
        f = serif(77); w = int(f.getlength(c)) + 2
        g = Image.new("L", (w, 95), 255)
        ImageDraw.Draw(g).text((0, 72), c, font=f, fill=PRETO, anchor="ls")
        return g.crop((0, 0, w, 95))
    seq = ["L", "1", "≥", " "] + list(novo_l1) + ["D", "N", ";", " ", "L", "2", "≥"] + list(novo_l2) + ["D", "N"]
    pecas = [letra(c) if c != " " else Image.new("L", (24, 95), 255) for c in seq]
    larg = sum(p.width for p in pecas) + 7 * (len(pecas) - 1)
    faixa = Image.new("L", (larg, 95), 255)
    x = 0
    for p in pecas:
        faixa.paste(p, (x, 0)); x += p.width + 7
    d = ImageDraw.Draw(im)
    d.rectangle([1100, 1195, 1950, 1290], fill=255)
    im.paste(faixa, (int(1515 - larg / 2), 1195))
    _ = a


def trecho_reto():
    im = ORIG.copy()
    d = ImageDraw.Draw(im)
    d.rectangle([205, 420, 1385, 945], fill=255)        # tira válvula, flanges e parafusos (mantém seta e ponta)
    d.line([(150, TUBO_Y[0] + 2), (1386, TUBO_Y[0] + 2)], fill=PRETO, width=TRACO)
    d.line([(150, TUBO_Y[1] + 2), (1386, TUBO_Y[1] + 2)], fill=PRETO, width=TRACO)
    legenda_retos(im, "10", "3")
    return im


def trechos():
    salvar(trecho_reto(), "reto-tubulacao-reta.png")
    for orig, nome in [("02_duas_curvas.png", "reto-curva.png"), ("06_tubulacao_menor.png", "reto-expansao.png"),
                       ("01_valvula_a_montante.png", "reto-valvula.png"), ("05_tubulacao_maior.png", "reto-reducao.png"),
                       ("03_bomba_a_montante.png", "reto-bomba.png"), ("07_derivacao_T.png", "reto-derivacao-t.png")]:
        salvar(abrir(orig), nome)


# ------------------------------------------------------------------ 2. posição na tubulação
def posicao_baixo():
    W, H = 2600, 1250
    im = Image.new("L", (W, H), 255); d = ImageDraw.Draw(im)
    cy_baixo, cy_alto = 880, 330
    xm = 1300                                         # centro do medidor
    m0 = xm - MEDIDOR.width // 2
    pts_esq = [(300, cy_alto), (520, cy_alto), (820, cy_baixo), (m0 + 6, cy_baixo)]
    pts_dir = [(m0 + MEDIDOR.width - 6, cy_baixo), (1780, cy_baixo), (2080, cy_alto), (2460, cy_alto)]
    tubo(d, pts_esq); tubo(d, pts_dir)
    sobrepor(im, MEDIDOR, m0, cy_baixo - MED_CY)
    ponta(im, 300, cy_alto); ponta(im, 2460, cy_alto, espelhar=True)
    seta_fluxo(d, 90, cy_alto, 190)
    return im


def posicao_subida():
    W, H = 2600, 1250
    ang = -9                                          # graus (sobe para a direita)
    a = math.radians(ang)
    peca = MEDIDOR.rotate(-ang, expand=True, fillcolor=255, resample=Image.BICUBIC)
    xm, ym = 1300, 760
    # meia-largura do medidor ao longo do tubo
    meia = MEDIDOR.width / 2 - 6
    p1 = (xm - meia * math.cos(a), ym + meia * math.sin(-a) * -1)
    p1 = (xm - meia * math.cos(a), ym - meia * math.sin(a))
    p2 = (xm + meia * math.cos(a), ym + meia * math.sin(a))
    im = Image.new("L", (W, H), 255); d = ImageDraw.Draw(im)
    x0 = 330; y0 = ym - (xm - x0) * math.tan(a)
    x3 = 2460; y3 = ym + (x3 - xm) * math.tan(a)
    tubo(d, [(x0, y0), p1]); tubo(d, [p2, (x3, y3)])
    # a peça gira em torno do centro; o centro do tubo na peça fica deslocado do centro da imagem
    dy = MED_CY - MEDIDOR.height / 2
    cx = xm - dy * math.sin(a) * -1
    cx = xm + dy * math.sin(a); cyp = ym - dy * math.cos(a)
    sobrepor(im, peca, int(cx - peca.width / 2), int(cyp - peca.height / 2))
    ponta(im, x0, y0, angulo=-ang); ponta(im, x3, y3, angulo=-ang, espelhar=True)
    seta_fluxo(d, x0 - 190 * math.cos(a), y0 - 190 * math.sin(a), 190, angulo=ang)
    return im


def posicao():
    salvar(posicao_baixo(), "instalacao-ponto-baixo.png", 1000)
    salvar(posicao_subida(), "instalacao-ascendente.png", 1000)


# ------------------------------------------------------------------ 3. aterramento
# posições na peça MEDIDOR (x a partir da esquerda da peça; y em relação ao centro do tubo)
FL_TUBO_E, JUNTA_E, FL_MED_E = 115, 145, 175      # centro do flange do tubo, da junta e do flange do medidor
FL_MED_D, JUNTA_D, FL_TUBO_D = 540, 570, 602
FL_TOPO, FL_BASE = -185, 183


def simbolo_terra(d, x, y):
    for i, w in enumerate((60, 40, 20)):
        d.line([(x - w, y + i * 16), (x + w, y + i * 16)], fill=PRETO, width=TRACO)


def medidor_na_linha(W=2400, H=1300, xm=1300, cy=620):
    W_TXT = 2780                     # largura total (o texto do terra passa do fim do tubo)
    im = Image.new("L", (W_TXT, H), 255); d = ImageDraw.Draw(im)
    m0 = xm - MEDIDOR.width // 2
    tubo(d, [(420, cy), (m0 + 6, cy)]); tubo(d, [(m0 + MEDIDOR.width - 6, cy), (W - 150, cy)])
    sobrepor(im, MEDIDOR, m0, cy - MED_CY)
    ponta(im, 420, cy); ponta(im, W - 150, cy, espelhar=True)
    seta_fluxo(d, 200, cy, 190)
    return im, d, m0, cy


def aterramento_metalico():
    im, d, m0, cy = medidor_na_linha()
    f = serif(66)
    # jumper de cobre por cima de cada par de flanges (flange do tubo -> flange do medidor)
    for xa, xb in ((FL_TUBO_E, FL_MED_E), (FL_MED_D, FL_TUBO_D)):
        d.arc([m0 + xa, cy + FL_TOPO - 80, m0 + xb, cy + FL_TOPO + 80], 180, 360, fill=PRETO, width=TRACO + 2)
    # flange do medidor ao terra
    xt = m0 + FL_MED_E
    d.line([(xt, cy + FL_BASE), (xt, cy + FL_BASE + 150)], fill=PRETO, width=TRACO)
    simbolo_terra(d, xt, cy + FL_BASE + 150)
    xm_e = m0 + (FL_TUBO_E + FL_MED_E) // 2
    chamada(d, [(xm_e, cy + FL_TOPO - 80), (xm_e - 160, cy + FL_TOPO - 260), (780, cy + FL_TOPO - 260)],
            "Cabo de cobre 6 mm²\n(nos dois lados)", f, "rm")
    chamada(d, [(xt + 64, cy + FL_BASE + 166), (xt + 420, cy + FL_BASE + 166)], "Terra: resistência < 10 Ω", f)
    chamada(d, [(700, cy + TUBO_D // 2), (700, cy + TUBO_D // 2 + 170), (680, cy + TUBO_D // 2 + 170)],
            "Tubulação metálica\nsem revestimento", f, "rm")
    return im


def aterramento_plastico():
    im, d, m0, cy = medidor_na_linha()
    f = serif(66)
    # anéis de aterramento no lugar das juntas, com a orelha descendo para o cabo
    for xj in (JUNTA_E, JUNTA_D):
        x = m0 + xj
        d.rectangle([x - 9, cy + FL_TOPO + 20, x + 9, cy + FL_BASE + 70], fill=PRETO)
        d.line([(x, cy + FL_BASE + 70), (x, cy + FL_BASE + 170)], fill=PRETO, width=TRACO)
    xa, xb = m0 + JUNTA_E, m0 + JUNTA_D
    yb = cy + FL_BASE + 170
    d.line([(xa, yb), (xb, yb)], fill=PRETO, width=TRACO)
    xt = (xa + xb) // 2
    d.line([(xt, yb), (xt, yb + 60)], fill=PRETO, width=TRACO)
    simbolo_terra(d, xt, yb + 60)
    chamada(d, [(xa, cy + FL_TOPO + 30), (xa - 160, cy + FL_TOPO - 200), (760, cy + FL_TOPO - 200)],
            "Anel de aterramento\n(nos dois lados)", f, "rm")
    chamada(d, [(xt + 64, yb + 76), (xt + 420, yb + 76)], "Terra: resistência < 10 Ω", f)
    chamada(d, [(700, cy + TUBO_D // 2), (700, cy + TUBO_D // 2 + 170), (680, cy + TUBO_D // 2 + 170)],
            "Tubulação plástica\nou revestida", f, "rm")
    return im


def aterramento():
    salvar(aterramento_metalico(), "aterramento-metalico.png", 1100)
    salvar(aterramento_plastico(), "aterramento-plastico.png", 1100)


# ------------------------------------------------------------------ 4. display e teclas (conversor redondo)
def icone_tecla(d, x, y, s, tipo):
    """Teclas como no produto: [▲▼] Função, [◥] para baixo, [◢] para cima, [↵] Enter."""
    d.rounded_rectangle([x, y, x + s, y + s], radius=10, outline=PRETO, width=TRACO)
    k = s / 64
    P = lambda pts: [(x + px * k, y + py * k) for px, py in pts]
    if tipo == "F":
        d.polygon(P([(32, 9), (52, 29), (12, 29)]), fill=PRETO)
        d.polygon(P([(12, 35), (52, 35), (32, 55)]), fill=PRETO)
    elif tipo in ("baixo", "cima"):
        tri = [(12, 12), (52, 12), (52, 52)] if tipo == "baixo" else [(52, 12), (52, 52), (12, 52)]
        d.polygon(P(tri), fill=PRETO)
        for i in range(3):
            d.rectangle([x + 10 * k, y + (20 + i * 10) * k, x + 54 * k, y + (23 + i * 10) * k], fill=255)
    else:
        d.polygon(P([(48, 14), (48, 40), (28, 40), (28, 50), (12, 36), (28, 22), (28, 32), (40, 32), (40, 14)]), fill=PRETO)


def display():
    W, H = 2500, 1700
    im = Image.new("L", (W, H), 255); d = ImageDraw.Draw(im)
    cx, cy, R = 760, 760, 600
    # tampa: anel externo, anel da rosca e visor
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=PRETO, width=TRACO + 1)
    d.ellipse([cx - R + 40, cy - R + 40, cx + R - 40, cy + R - 40], outline=PRETO, width=TRACO)
    for i in range(72):                                  # serrilhado da tampa
        a = i * math.pi / 36
        d.line([(cx + (R - 4) * math.cos(a), cy + (R - 4) * math.sin(a)),
                (cx + (R - 34) * math.cos(a), cy + (R - 34) * math.sin(a))], fill=PRETO, width=FINO)
    r2 = R - 110
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=PRETO, width=TRACO)
    # logomarca
    lw, lh = 360, 84
    d.rounded_rectangle([cx - lw / 2, cy - 400, cx + lw / 2, cy - 400 + lh], radius=8, outline=PRETO, width=TRACO)
    d.text((cx, cy - 400 + lh / 2), "TechMeter", font=sans(56), fill=PRETO, anchor="mm")
    # LCD
    x0, y0, x1, y1 = cx - 380, cy - 270, cx + 380, cy + 140
    d.rounded_rectangle([x0 - 22, y0 - 22, x1 + 22, y1 + 22], radius=16, outline=PRETO, width=TRACO)
    d.rectangle([x0, y0, x1, y1], outline=PRETO, width=FINO + 1)
    d.text((x1 - 190, y0 + 150), "12.50", font=mono(150), fill=PRETO, anchor="rs")
    d.text((x1 - 30, y0 + 150), "m³/h", font=mono(56), fill=PRETO, anchor="rs")
    d.line([(x0 + 30, y0 + 210), (x1 - 30, y0 + 210)], fill=PRETO, width=FINO)
    d.text((x0 + 40, y0 + 330), "Σ 000184.6 m³", font=mono(70), fill=PRETO, anchor="ls")
    # teclas
    s, gap = 104, 54
    tipos = ["F", "baixo", "cima", "enter"]
    xs = [cx - (4 * s + 3 * gap) / 2 + i * (s + gap) for i in range(4)]
    yk = cy + 250
    for x, t in zip(xs, tipos):
        icone_tecla(d, x, yk, s, t)
    # chamadas do LCD
    f = serif(68); xl = 1480
    chamada(d, [(x1 - 330, y0 + 28), (xl, y0 + 28)], "Vazão instantânea", f)
    chamada(d, [(x1 - 20, y0 + 122), (x1 + 120, y0 + 150), (xl, y0 + 150)], "Unidade", f)
    chamada(d, [(x1 - 120, y0 + 305), (xl, y0 + 330)], "Totalizador, velocidade,\n% da faixa, data e hora", f)
    # chamadas das teclas, em escada
    nomes = ["Função", "Para baixo", "Para cima", "Enter"]
    for i in range(3, -1, -1):
        xk = xs[i] + s / 2
        yl = yk + s + 110 + (3 - i) * 100
        chamada(d, [(xk, yk + s + 6), (xk, yl), (xl, yl)], nomes[i], f)
    return im


# ------------------------------------------------------------------ 5. dimensões (flangeado)
def dimensoes():
    m = medidor_limpo()
    W, H = m.width + 700, m.height + 420
    im = Image.new("L", (W, H), 255); d = ImageDraw.Draw(im)
    ox, oy = 360, 80
    sobrepor(im, m, ox, oy)
    # medidas na peça limpa: flanges de x=50 a x=455; flange de y=430 a y=798; topo do conversor em y=15
    fx0, fx1 = ox + 50, ox + 455
    fy0, fy1 = oy + 430, oy + 798
    topo = oy + 15
    cota_h(d, fx0, fx1, fy1 + 170, "L", ext_de=fy1 + 10)
    cota_v(d, fx1 + 160, fy0, fy1, "D", ext_de=fx1 + 10, lado="dir")
    cota_v(d, fx0 - 170, topo, fy1, "H", ext_de=fx0 - 10)
    # linha de centro do tubo
    yc = (fy0 + fy1) // 2
    for x in range(fx0 - 60, fx1 + 60, 60):
        d.line([(x, yc), (x + 34, yc)], fill=PRETO, width=FINO)
    return im


def main():
    SAIDA.mkdir(exist_ok=True)
    trechos()
    posicao()
    aterramento()
    salvar(display(), "display-redondo.png", 1100)
    salvar(dimensoes(), "dim-flangeado.png", 700)


if __name__ == "__main__":
    main()
