#!/usr/bin/env python3
"""Gera o manual online do medidor eletromagnético (uma página por modelo) e os QR codes.

Uso:
    python3 manuais-online/eletromagnetico/build.py            # páginas + PDFs + QR codes
    python3 manuais-online/eletromagnetico/build.py --sem-pdf  # mais rápido, sem PDFs

Saída:
    site/manual/eletromagnetico/<modelo>/index.html (+ manual-<modelo>.pdf)  -> publicado no Cloudflare Pages
    manuais-online/eletromagnetico/qrcodes/                                  -> QR codes e etiquetas para imprimir

Fonte técnica: "Manual Eletromagnético KF – 2022" (Techmeter). Conteúdo resumido para o cliente:
instalação, ligações, configuração básica e solução de problemas.
"""
import html
import re, json, shutil, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
CFG = json.loads((AQUI / "modelos.json").read_text(encoding="utf-8"))
SAIDA = RAIZ / "site" / CFG["caminho"]
CHROME = "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome"

ZAP = "5511976435939"
CONTATO = {"zap": "(11) 97643-5939", "tel": "(11) 5071-1630", "tel_link": "+551150711630",
           "suporte": "manutencao@techmeter.com.br", "vendas": "vendas@techmeter.com.br",
           "site": "www.techmeter.com.br", "horario": "Segunda a sexta, das 8h00 às 17h30"}

I_ZAP = '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2.1 1-2.4c.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .5l-.4.6-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.7-.1l.9-1.1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.2.1.6-.1 1.1z"/></svg>'
I_TEL = '<svg viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'
I_PDF = '<svg viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9zM14 3v6h6M12 12v6m-3-3 3 3 3-3"/></svg>'
# teclas como estão no produto (conversor redondo): mesmo desenho de desenhos/gerar_desenhos.py
def _svg_tecla(miolo, nome):
    return (f'<span class="tecla ic" role="img" aria-label="{nome}"><svg viewBox="0 0 64 64" aria-hidden="true">'
            f'<rect x="3" y="3" width="58" height="58" rx="9" fill="#fff" stroke="currentColor" stroke-width="5"/>{miolo}</svg></span>')
_LISTRAS = '<g fill="#fff"><rect x="10" y="20" width="44" height="3"/><rect x="10" y="30" width="44" height="3"/><rect x="10" y="40" width="44" height="3"/></g>'
TECLAS_REAIS = {
    "F": _svg_tecla('<path fill="currentColor" d="M32 9 52 29H12zM12 35h40L32 55z"/>', "Função"),
    "▼": _svg_tecla('<path fill="currentColor" d="M12 12h40v40z"/>' + _LISTRAS, "Para baixo"),
    "▲": _svg_tecla('<path fill="currentColor" d="M52 12v40H12z"/>' + _LISTRAS, "Para cima"),
    "↵": _svg_tecla('<path fill="currentColor" d="M48 14v26H28v10L12 36l16-14v10h12V14z"/>', "Enter"),
}


def teclas_reais(texto):
    """Troca F, ▲, ▼ e ↵ pelos desenhos das teclas reais (só no conversor redondo)."""
    for k, v in TECLAS_REAIS.items():
        texto = texto.replace(f'<span class="tecla">{k}</span>', v)
    return texto.replace("com ▲/▼", "com " + TECLAS_REAIS["▲"] + "/" + TECLAS_REAIS["▼"]) \
                .replace("Com ▲/▼", "Com " + TECLAS_REAIS["▲"] + "/" + TECLAS_REAIS["▼"]) \
                .replace("Com ↵", "Com " + TECLAS_REAIS["↵"])


I_3D = '<svg viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" d="m12 2 9 5v10l-9 5-9-5V7zM12 22V12m9-5-9 5-9-5"/></svg>'
I_MAIL = '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="m3 7 9 6 9-6" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
I_BUSCA = '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="m20 20-4-4" stroke="currentColor" stroke-width="2"/></svg>'


def tabela(cab, linhas, classes=None):
    h = "".join(f"<th>{c}</th>" for c in cab)
    corpo = "".join("<tr>" + "".join(f"<td{(' class=%s' % classes[i]) if classes and classes[i] else ''}>{v}</td>" for i, v in enumerate(l)) + "</tr>" for l in linhas)
    return f'<div class="tabela"><table><tr>{h}</tr>{corpo}</table></div>'


def fig(img, legenda, largura=None):
    w = f' style="width:{largura}"' if largura else ""
    alt = html.escape(re.sub("<[^>]+>", "", legenda))
    return (f'<figure class="fig"><a href="../img/{img}" target="_blank" title="Abrir a figura ampliada">'
            f'<img src="../img/{img}" alt="{alt}" loading="lazy"{w}></a><figcaption>{legenda}</figcaption></figure>')


# ---------------------------------------------------------------- capítulos
VERSOES = [
    ("tm-el-flangeado-carbono.jpg", "Flangeado em aço carbono",
     "Corpo e flanges em aço carbono pintado, revestimento interno de borracha. Indicado para água, saneamento e efluentes."),
    ("tm-el-flangeado-inox-ptfe.jpg", "Flangeado em aço inox",
     "Corpo e flanges em aço inox, revestimento interno de PTFE. Indicado para produtos químicos e líquidos agressivos."),
    ("tm-el-sanitario-triclamp-inox.jpg", "Sanitário tri-clamp",
     "Corpo em aço inox com conexões tri-clamp e revestimento de PFA. Indicado para alimentos, bebidas e indústria farmacêutica."),
]


def cap_conheca(m):
    cards = "".join(
        f'<figure class="versao"><a href="../img/{img}" target="_blank" title="Abrir a foto ampliada">'
        f'<img src="../img/{img}" alt="Medidor eletromagnético Techmeter, versão {html.escape(t)}" loading="lazy"></a>'
        f'<figcaption><b>{t}</b>{d}</figcaption></figure>' for img, t, d in VERSOES)
    remoto = ("<p>Neste modelo o conversor é <b>remoto</b>: fica separado do sensor e é ligado a ele por cabo.</p>"
              if m["conversor"] == "quadrado" else "")
    gal = ""
    if m["galeria"]:
        gal = '<div class="galeria">' + "".join(f'<img src="../img/{g}" alt="Foto do equipamento" loading="lazy">' for g in m["galeria"]) + "</div>"
    return f"""
<p>O medidor eletromagnético mede a <b>vazão de líquidos condutivos</b> (água, efluentes, polpas, químicos) com base na lei de Faraday. Ele <b>não tem partes móveis</b> e não restringe a passagem do fluido, por isso quase não causa perda de carga e exige pouca manutenção.</p>
<h3>Versões</h3>
<p>O medidor eletromagnético Techmeter é fabricado em <b>três versões</b>, todas com o mesmo conversor com display. O que muda é o material do corpo, o revestimento interno e a conexão com a tubulação:</p>
<div class="versoes">{cards}</div>
{remoto}{gal}
<ul>
  <li><b>Condutividade mínima do líquido:</b> 5 µS/cm. Abaixo disso o medidor não funciona (ex.: água destilada, óleos, gases).</li>
  <li><b>Mede nos dois sentidos</b> e totaliza vazão direta, inversa e a diferença.</li>
  <li><b>Saídas:</b> corrente (4-20 mA), pulso ou frequência, alarmes e comunicação RS485 / Modbus.</li>
</ul>"""


def cap_recebimento():
    return """
<ul>
  <li>Transporte e guarde o medidor <b>na embalagem original</b> até o local da instalação. Não levante o equipamento pelo conversor nem pelos cabos.</li>
  <li>Armazene em local coberto, seco e sem vibração: temperatura de <b>-20 a 60 °C</b> e umidade até 80%.</li>
  <li>Confira na plaqueta: modelo, diâmetro (DN), número de série e <b>fator de calibração</b>. Guarde o certificado de calibração.</li>
</ul>"""


def cap_instalacao():
    t_retos = tabela(["Situação antes do medidor", "Trecho reto antes", "Trecho reto depois"], [
        ["Tubulação reta", "10 DN", "3 DN"], ["Curva", "20 DN", "5 DN"], ["Expansão", "25 DN", "5 DN"],
        ["Válvula antes do medidor", "50 DN", "5 DN"], ["Redução", "25 DN", "5 DN"],
        ["Bomba ou manômetro antes do medidor", "50 DN", "5 DN"], ["Mistura de líquidos, derivação em T", "50 DN", "5 DN"]],
        [None, "c", "c"])
    return f"""
<h3>Escolha do local</h3>
<ul>
  <li>Prefira local coberto. Ao ar livre, proteja do sol direto, da chuva e de alagamentos.</li>
  <li>Evite locais com vibração forte, campos magnéticos intensos (motores, inversores, transformadores) e atmosfera corrosiva.</li>
  <li>Deixe espaço livre em volta para manutenção e leitura do display.</li>
</ul>

<h3>Tubo sempre cheio</h3>
<p>O medidor só mede corretamente com o tubo <b>totalmente cheio de líquido</b>. Por isso:</p>
<ul>
  <li>Instale em trecho <b>ascendente</b> ou no <b>ponto mais baixo</b> da tubulação. Nunca no ponto mais alto, onde se acumula ar.</li>
  <li>Em descarga livre, instale o medidor antes de um trecho que mantenha o tubo cheio (ex.: sifão ou trecho que sobe).</li>
  <li>Instale o medidor <b>depois da bomba</b> e as válvulas de controle e de bloqueio <b>depois</b> do medidor.</li>
  <li>Para líquidos com sólidos, a melhor posição é na <b>vertical, com o fluxo de baixo para cima</b>.</li>
</ul>
<div class="figs">
{fig("instalacao-ponto-baixo.png", "No ponto mais baixo da tubulação.")}
{fig("instalacao-ascendente.png", "Em trecho levemente ascendente.")}
</div>

<h3>Trechos retos</h3>
<p>Para a medição ser precisa, mantenha trechos retos de tubulação antes (L1) e depois (L2) do medidor. <b>DN</b> é o diâmetro nominal: num DN50, por exemplo, 10 DN = 500 mm.</p>
{t_retos}
<div class="figs">
{fig("reto-tubulacao-reta.png", "Tubulação reta")}
{fig("reto-curva.png", "Curva")}
{fig("reto-expansao.png", "Expansão (tubulação menor antes do medidor)")}
{fig("reto-reducao.png", "Redução (tubulação maior antes do medidor)")}
{fig("reto-valvula.png", "Válvula antes do medidor")}
{fig("reto-bomba.png", "Bomba antes do medidor")}
{fig("reto-derivacao-t.png", "Derivação em T")}
</div>

<h3>Montagem</h3>
<ul>
  <li>Respeite a <b>seta de sentido do fluxo</b> gravada no medidor.</li>
  <li>O diâmetro da tubulação deve ser igual ao do medidor e os dois devem ficar <b>alinhados</b> (centro com centro).</li>
  <li>Os eletrodos devem ficar na <b>horizontal</b> (o conversor fica para cima ou para o lado, nunca com os eletrodos em cima e embaixo).</li>
  <li>Os flanges devem estar paralelos. Use juntas que não invadam o diâmetro interno.</li>
  <li><b>Não faça solda elétrica</b> perto do medidor instalado: o calor e a corrente danificam o revestimento e os eletrodos.</li>
  <li>Acima de DN200, use uma junta flexível para facilitar a montagem e evitar esforço no medidor.</li>
  <li>Recomenda-se um <b>by-pass</b> com válvulas para retirar o medidor sem parar o processo.</li>
</ul>

<h3>Aterramento</h3>
<p>O aterramento é essencial: sem ele a leitura oscila ou fica errada. A resistência de aterramento deve ser <b>menor que 10 Ω</b>.</p>
<ul>
  <li><b>Tubulação metálica sem revestimento:</b> ligue os flanges do medidor aos flanges da tubulação com cabo de cobre de 6 mm² e ao terra.</li>
  <li><b>Tubulação plástica (PVC, PEAD) ou com revestimento interno:</b> instale <b>anéis de aterramento</b> nos dois lados do medidor, ligados ao terra. Se o medidor já tiver eletrodo de aterramento, os anéis não são necessários.</li>
</ul>
{fig("aterramento-metalico.png", "Aterramento em tubulação metálica sem revestimento.")}
{fig("aterramento-plastico.png", "Aterramento em tubulação plástica ou revestida, com anéis de aterramento.")}
<div class="nota">Em tubulações com <b>proteção catódica</b>, os anéis de aterramento devem ser isolados dos flanges da tubulação. Fale com o suporte Techmeter antes de instalar.</div>"""


def cap_ligacoes(m):
    if m["conversor"] == "redondo":
        bornes = tabela(["Borne", "Ligação"], [
            ["LN+ / LN−", "Alimentação 220 Vca (ou 24 Vcc, conforme o modelo)"],
            ["IOUT / COMM", "Saída de corrente 4-20 mA (IOUT = sinal, COMM = comum) - SAÍDA ATIVA"],
            ["IVIN", "Alimentação 24 Vcc para a saída de corrente a 2 fios (modelo remoto)"],
            ["POUT / COMM", "Saída de pulso ou frequência (coletor aberto) - SAÍDA ATIVA"],
            ["ALM1 / COMM", "Alarme de limite superior - SAÍDA ATIVA"],
            ["ALM2 / COMM", "Alarme de limite inferior - SAÍDA ATIVA"],
            ["TRX+ / TRX−", "RS485 / Modbus (A e B) - SAÍDA ATIVA"]], ["cod", None])
        bloco = f"""
<p>Os bornes ficam sob a <b>tampa traseira</b> do conversor. Os cabos entram pelos prensa-cabos laterais.</p>
{fig("bornes-redondo.png", "Régua de bornes do conversor redondo.", "300px")}
{bornes}"""
    else:
        bornes = tabela(["Borne", "Ligação"], [
            ["L1 / L2 / PE", "Alimentação e terra do conversor"],
            ["SIG1 / SGND / SIG2", "Sinal dos eletrodos (vindo do sensor)"],
            ["DS1 / DS2", "Blindagem do sinal"],
            ["EXT+ / EXT−", "Corrente de excitação das bobinas (para o sensor)"],
            ["IOUT / COM", "Saída de corrente 4-20 mA"],
            ["POUT / COM", "Saída de pulso ou frequência"],
            ["DOUT / CTRL", "Saídas de alarme e de controle"],
            ["TRX+ / TRX−", "RS485 / Modbus (A e B)"]], ["cod", None])
        bloco = f"""
{bornes}
<h3>Cabo entre sensor e conversor</h3>
<ul>
  <li>Use o cabo fornecido com o medidor. Distância máxima: <b>100 m</b> (acima disso, sob consulta).</li>
  <li>Sinal (cabo cinza blindado): fio vermelho em <b>SIG1</b>, branco em <b>SIG2</b> e blindagem em <b>SGND</b>.</li>
  <li>Excitação (cabo preto de 2 vias): ligue em <b>EXT+</b> e <b>EXT−</b>.</li>
  <li>Passe o cabo de sinal longe de cabos de potência, em eletroduto próprio.</li>
  <li>Se o sensor puder ficar submerso, vede bem a caixa de ligação do sensor.</li>
</ul>
{fig("dim-conversor-remoto.png", "Dimensões do conversor remoto (mm).", "380px")}"""
    return f"""
<div class="aviso"><b>Atenção:</b> faça as ligações com a alimentação <b>desligada</b>. Confira na plaqueta se o equipamento é 220 Vca (85 a 265 Vca) ou 24 Vcc antes de energizar.</div>
{bloco}
<h3>Saídas</h3>
<ul>
  <li><b>4-20 mA:</b> carga máxima de 750 Ω. Pode ser ligada a 2, 3 ou 4 fios, conforme o sistema que recebe o sinal.</li>
  <li><b>Pulso / frequência:</b> saída a coletor aberto, até 35 V e 250 mA, com resistor de carga. Para acionar relé, coloque diodo em paralelo com a bobina. Pulso e frequência usam o mesmo borne: escolha um dos dois na configuração.</li>
  <li><b>RS485:</b> cabo par trançado blindado. Use resistor de terminação de 120 Ω só em linhas longas.</li>
  <li><b>Terra do conversor:</b> ligue o borne PE ao terra com cabo de no mínimo 1,5 mm².</li>
</ul>"""


def cap_display(m):
    figura = fig("display-redondo.png", "Display e teclas do conversor redondo, na ordem em que aparecem no produto.") if m["conversor"] == "redondo" else fig("display-quadrado.png", "Display e teclas do conversor quadrado.")
    return f"""
{figura}
<p>A tela mostra a vazão instantânea na linha de cima e, na linha de baixo, o item escolhido: totalizador direto, inverso ou diferença, velocidade, porcentagem da faixa, data e hora.</p>
{tabela(["Tecla", "Na tela de medição", "No menu de configuração"], [
    ['<span class="tecla">F</span> Função', "Com ↵: abre o menu · com ▲/▼: ajusta o contraste", "Com ▲/▼: move o cursor para a direita / esquerda"],
    ['<span class="tecla">▼</span> Para baixo', "Troca o item da linha de baixo", "Diminui o dígito / página abaixo"],
    ['<span class="tecla">▲</span> Para cima', "Troca o item da linha de cima", "Aumenta o dígito / página acima"],
    ['<span class="tecla">↵</span> Enter', "—", "Entra e sai dos itens. Segurar 2 s volta para a medição"]])}
<p>Para usar a tecla <b>Função</b>, mantenha-a pressionada e então aperte a outra tecla. No menu, se nenhuma tecla for usada por alguns segundos, o conversor volta sozinho para a tela de medição.</p>"""


def cap_configuracao():
    return f"""
<div class="nota">O medidor sai da Techmeter <b>calibrado e configurado</b> com os dados do pedido (diâmetro, faixa, unidade e saídas). Altere a configuração só se precisar.</div>

<h3>Antes de configurar</h3>
<ul>
  <li>Confira o aterramento e se o tubo está <b>cheio</b>.</li>
  <li>Na primeira partida, deixe o líquido em contato com os eletrodos por <b>até 48 horas</b> para estabilizar a leitura antes de fazer o ajuste de zero.</li>
</ul>

<h3>Como entrar no menu</h3>
<ol>
  <li>Na tela de medição, aperte <span class="tecla">F</span> + <span class="tecla">↵</span>. Aparece <b>Parameter Setting</b>.</li>
  <li>Aperte <span class="tecla">↵</span> e digite a <b>senha</b> com as setas (<span class="tecla">F</span> + seta move o cursor).</li>
  <li>Aperte <span class="tecla">F</span> + <span class="tecla">↵</span> para entrar.</li>
  <li>Use <span class="tecla">▲</span> <span class="tecla">▼</span> para escolher o parâmetro e <span class="tecla">↵</span> para editar e confirmar.</li>
  <li>Para sair, segure <span class="tecla">↵</span> por 2 segundos.</li>
</ol>
<p>A senha de acesso é informada pela Techmeter junto com o equipamento. Se não tiver, fale com o suporte.</p>

<h3>Parâmetros mais usados</h3>
{tabela(["Nº", "No display", "O que faz", "Opções"], [
    ["5", "Sensor Size", "Diâmetro do medidor (já vem de fábrica)", "3 a 3.000 mm"],
    ["6", "Flow Range", "Fundo de escala: vazão que corresponde a 20 mA e a 100%", "0 a 99.999"],
    ["—", "Flow Unit", "Unidade da vazão", "L/s, L/min, L/h, m³/s, m³/min, m³/h"],
    ["7", "Flow Rspns", "Amortecimento: valores maiores deixam a leitura mais estável e mais lenta", "Seleção"],
    ["8", "Flow Direct", "Inverte o sentido do fluxo sem mexer na ligação", "Direto / inverso"],
    ["9", "Flow Zero", "Ajuste de zero, com o tubo cheio e o líquido parado", "± mm/s"],
    ["10", "Flow Cutoff", "Corte de vazão baixa: abaixo deste valor o medidor mostra zero", "0 a 99% da escala"],
    ["12", "Total Unit", "Resolução do totalizador", "0,001 L a 1 m³"],
    ["14", "Analog Type", "Tipo de saída de corrente", "4-20 mA ou 0-10 mA"],
    ["15", "Pulse Type", "Saída de frequência ou de pulso", "Freq. / pulso"],
    ["16", "Pulse Unit", "Volume de cada pulso", "0,001 L a 1 m³"],
    ["17", "Frequen Max", "Frequência que corresponde a 100% da escala", "1 a 5.000 Hz"],
    ["18", "Mtsensor Ena", "Liga o alarme de tubo vazio", "Habilitar / desabilitar"],
    ["21 a 24", "Alm High / Low", "Alarmes de vazão alta e baixa, em % da escala", "0 a 199,9%"],
    ["2 e 3", "Com Address / Baud Rate", "Endereço e velocidade da RS485", "0 a 99 · 600 a 14.400 bps"],
    ["4", "Com Protocol", "Protocolo de comunicação", "Tipo 1 (RS485) / Tipo 2 (Modbus)"]],
    ["cod", "cod", None, None])}
<div class="aviso"><b>Não altere</b> o fator do sensor (<b>Sensor Fact</b>) nem o modo de excitação: eles vêm da calibração e estão anotados na plaqueta e no certificado. Alterar esses valores tira o medidor de calibração.</div>

<h3>Exemplos</h3>
<details><summary>Escolher a unidade e o fundo de escala</summary><div>
<p>Escolha uma unidade em que a vazão máxima caiba em 5 dígitos. Se o display mostrar <b>overflow</b>, a unidade está pequena demais. Exemplo: em DN200, 1 m/s equivale a 113.097 L/h (6 dígitos); use m³/h (113,10 m³/h).</p>
<p>Defina <b>Flow Range</b> com a vazão máxima do processo, com uma folga. A saída 4-20 mA e a porcentagem seguem esse valor.</p></div></details>
<details><summary>Configurar a saída de pulso para um totalizador ou CLP</summary><div>
<p>Em <b>Pulse Type</b> escolha <b>Pulso</b> e em <b>Pulse Unit</b> o volume de cada pulso (ex.: 1 pulso = 0,01 m³). Mantenha a frequência de pulsos abaixo de 3.000 Hz na vazão máxima: se o volume do pulso for pequeno demais para a vazão, aumente o valor.</p></div></details>
<details><summary>Fazer o ajuste de zero</summary><div>
<p>Com o tubo <b>cheio e o líquido parado</b> (válvulas fechadas), entre em <b>Flow Zero</b> e ajuste o valor até a vazão indicada ficar em zero. Anote o valor ajustado.</p></div></details>
<details><summary>Zerar o totalizador</summary><div>
<p>No menu, vá até <b>Clr Total Rec</b>, digite a senha de zerar totalizador e confirme com <span class="tecla">F</span> + <span class="tecla">↵</span>. Os totais voltam a zero.</p></div></details>"""


def cap_problemas():
    return f"""
<h3>Alarmes no display</h3>
{tabela(["Mensagem", "Significado"], [
    ["FQH · UPPER ALARM", "Vazão acima do limite de alarme alto"],
    ["FQL · LOWER ALARM", "Vazão abaixo do limite de alarme baixo"],
    ["FGP · LIQUID ALARM", "Tubo vazio ou parcialmente cheio"],
    ["SYS · SYSTEM ALARM", "Falha na excitação das bobinas"]], ["cod", None])}
<h3>O que verificar</h3>
<details><summary>Display apagado</summary><div><ul>
<li>Confira se há alimentação nos bornes e se a tensão é a do equipamento (220 Vca ou 24 Vcc).</li>
<li>Verifique o fusível do conversor.</li></ul></div></details>
<details><summary>Alarme de tubo vazio (FGP)</summary><div><ul>
<li>Confirme se o tubo está realmente cheio (ar na linha, medidor em ponto alto, descarga livre).</li>
<li>Confira as ligações do sinal (SIG1, SIG2, SGND) no modelo remoto.</li>
<li>O líquido pode ter condutividade baixa, ou os eletrodos podem estar sujos. Fale com o suporte.</li></ul></div></details>
<details><summary>Alarme de excitação (SYS)</summary><div><ul>
<li>No modelo remoto, confira se os fios EXT+ e EXT− estão bem ligados.</li>
<li>Se a ligação estiver correta, o conversor ou as bobinas precisam de assistência.</li></ul></div></details>
<details><summary>Leitura oscilando ou diferente do esperado</summary><div><ul>
<li>Verifique o <b>aterramento</b> (causa mais comum).</li>
<li>Confira se o tubo está cheio e se há bolhas de ar.</li>
<li>Confira os trechos retos e se há bomba ou válvula muito perto do medidor.</li>
<li>Confira se o fator do sensor e o zero estão iguais aos da plaqueta / certificado.</li>
<li>Aumente o amortecimento (<b>Flow Rspns</b>) se o processo for pulsante.</li></ul></div></details>
<div class="nota">O conversor não tem peças que o usuário possa consertar. Não abra a parte eletrônica: fale com a assistência técnica Techmeter.</div>"""


def cap_especificacoes(m):
    gerais = tabela(["Característica", "Especificação"], [
        ["Princípio", "Indução eletromagnética (lei de Faraday)"],
        ["Precisão", "±0,5% do valor medido (velocidade ≥ 1 m/s)"],
        ["Velocidade do fluido", "0,3 a 15 m/s (fundo de escala)"],
        ["Condutividade mínima", "5 µS/cm"],
        ["Pressão nominal", "1,6 MPa (até 4,0 MPa sob pedido)"],
        ["Revestimento", "PTFE, borracha, poliuretano e outros"],
        ["Eletrodos", "Aço inox 316L, Hastelloy B/C, titânio, tântalo, platina-irídio"],
        ["Alimentação", "85 a 265 Vca, 45 a 63 Hz ou 24 Vcc · potência < 20 W"],
        ["Saídas", "4-20 mA ou 0-10 mA · pulso/frequência até 5.000 Hz · 2 alarmes · RS485 / Modbus"],
        ["Temperatura ambiente", "Conversor: -10 a 60 °C · sensor: -40 a 80 °C"],
        ["Temperatura do fluido", "Até 70 °C (integrado) · até 80 a 150 °C conforme revestimento (remoto)"],
        ["Grau de proteção", "IP65 · IP68 no sensor remoto com revestimento de borracha ou poliuretano"]])
    dim = ""
    if m["dimensoes"] == "flangeado":
        if m["conversor"] == "redondo":
            fig_dim = fig("dim-flangeado.png", 'L = comprimento entre flanges · D = diâmetro do flange · H = altura total. '
                          '<span class="validar">VALIDAR: os valores de H vieram do sensor remoto; confirmar a altura total do integrado.</span>', "380px")
        else:
            fig_dim = fig("dim-flangeado-remoto.png", "L = comprimento entre flanges · D = diâmetro do flange · H = altura do sensor.", "520px")
        linhas = [["15", "200", "95", "220", "8"], ["20", "200", "105", "220", "10"], ["25", "200", "115", "223", "12"],
                  ["32", "200", "140", "240", "13"], ["40", "200", "150", "250", "14"], ["50", "200", "165", "263", "15"],
                  ["65", "200", "185", "283", "18"], ["80", "200", "200", "290", "20"], ["100", "250", "235", "318", "25"],
                  ["125", "250", "270", "350", "28"], ["150", "300", "300", "380", "30"], ["200", "350", "340", "430", "50"],
                  ["250", "450", "405", "495", "70"], ["300", "500", "460", "547", "95"], ["350", "550", "520", "602", "120"],
                  ["400", "600", "580", "665", "140"], ["500", "600", "715", "783", "200"], ["600", "600", "840", "897", "280"]]
        dim = f"""<details open><summary>Dimensões (mm) e peso</summary><div>
{fig_dim}
{tabela(["DN", "L", "D", "H", "Peso (kg)"], linhas, ["cod", "c", "c", "c", "c"])}
<p>Flanges conforme GB/T 9119 (PN40 até DN150, PN16 de DN200 a DN600). Outras normas e diâmetros sob consulta.</p></div></details>"""
    elif m["dimensoes"] == "triclamp":
        linhas = [["10", "179", "70", "172", "2,5"], ["15", "179", "70", "172", "2,5"], ["20", "179", "70", "172", "2,6"], ["25", "189", "83", "172", "2,6"],
                  ["40", "196", "95", "172", "3,0"], ["50", "214", "105", "172", "3,6"], ["65", "220", "115", "200", "4,5"], ["80", "240", "135", "200", "5,2"],
                  ["100", "252", "146", "200", "7,0"], ["125", "276", "170", "200", "9,6"], ["150", "310", "204", "256", "12,8"], ["200", "336", "230", "256", "22,0"]]
        dim = f"""<details open><summary>Dimensões (mm) e peso</summary><div>
{fig("dim-triclamp.png", "H = altura · W = largura · L = comprimento.", "320px")}
{tabela(["DN", "H", "W", "L", "Peso (kg)"], linhas, ["cod", "c", "c", "c", "c"])}</div></details>"""
    else:
        dim = "<p>Dimensões do modelo wafer: consulte a Techmeter.</p>"
    return gerais + dim


def cap_suporte():
    c = CONTATO
    return f"""
<p>Dúvidas na instalação ou na configuração? Fale com a assistência técnica Techmeter.</p>
{tabela(["Canal", "Contato"], [
    ["WhatsApp", c["zap"]], ["Telefone", c["tel"]], ["Suporte técnico", c["suporte"]],
    ["Comercial", c["vendas"]], ["Atendimento", c["horario"]]])}
<p>Para agilizar, tenha em mãos o <b>modelo e o número de série</b> da plaqueta e, se possível, fotos da instalação e do display.</p>
<p>A Techmeter também faz <b>calibração em laboratório próprio</b>, start-up e manutenção em todo o Brasil.</p>"""


# ---------------------------------------------------------------- página
def pagina(m, base_url):
    caps = [
        ("conheca", "Conheça o equipamento", cap_conheca(m)),
        ("recebimento", "Recebimento e armazenamento", cap_recebimento()),
        ("instalacao", "Instalação", cap_instalacao()),
        ("ligacoes", "Ligações elétricas", cap_ligacoes(m)),
        ("display", "Display e teclas", cap_display(m)),
        ("configuracao", "Configuração", cap_configuracao()),
        ("problemas", "Alarmes e solução de problemas", cap_problemas()),
        ("especificacoes", "Especificações", cap_especificacoes(m)),
        ("suporte", "Suporte técnico", cap_suporte()),
    ]
    indice = "".join(f'<a href="#{i}"><b>{n}</b>{t}</a>' for n, (i, t, _) in enumerate(caps, 1))
    secoes = "".join(f'<section class="cap" id="{i}"><h2><b>{n}</b>{t}</h2><div class="corpo">{c}</div></section>' for n, (i, t, c) in enumerate(caps, 1))
    if m["conversor"] == "redondo":
        secoes = teclas_reais(secoes)
    foto = (f'<img src="../img/{m["foto"]}" alt="{html.escape(m["nome"])}">' if m["foto"]
            else '<div class="placeholder">Foto em breve</div>')
    msg = f"Olá! Preciso de suporte com o medidor eletromagnético {m['curto']}."
    a3d = f'<a href="#ver-3d">{I_3D}Ver em 3D</a>' if m["modelo_3d"] else ""
    v3d = ('<div class="v3d so-tela" id="ver-3d"><iframe src="../../../index.html?visualizar" loading="lazy" '
           'title="Modelo 3D do medidor. Arraste para girar."></iframe>'
           '<p>Modelo 3D ilustrativo. Arraste para girar.</p></div>') if m["modelo_3d"] else ""
    url = f"{base_url}/{CFG['caminho']}/{m['slug']}/"
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Manual {html.escape(m['curto'])} · Techmeter</title>
<meta name="description" content="Manual do medidor de vazão eletromagnético {html.escape(m['nome'])}: instalação, ligações e configuração.">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#14204a">
<meta name="color-scheme" content="light">
<link rel="stylesheet" href="../estilo.css">
</head><body>
<header class="topo"><img src="../img/logo-techmeter.png" alt="TechMeter"><div class="t">Manual do produto<small>{html.escape(m['curto'])}</small></div><button type="button" id="ir-indice">Índice</button></header>
<main class="pagina">
  <div class="capa">
    <div><div class="eyebrow">Medidor de vazão eletromagnético</div><h1>{html.escape(m['nome'])}</h1><p>{html.escape(m['resumo'])}</p></div>
    <div class="foto">{foto}</div>
  </div>
  <nav class="acoes">
    <a class="zap" href="https://wa.me/{ZAP}?text={html.escape(msg).replace(' ', '%20')}" target="_blank" rel="noopener">{I_ZAP}Suporte no WhatsApp</a>
    <a href="tel:{CONTATO['tel_link']}">{I_TEL}{CONTATO['tel']}</a>
    <a href="manual-{m['slug']}.pdf" download>{I_PDF}Baixar PDF</a>
    {a3d}
  </nav>
  {v3d}
  <div class="busca"><label for="busca" class="so-tela" style="position:absolute;left:-9999px">Buscar no manual</label>{I_BUSCA}<input id="busca" type="search" placeholder="Buscar no manual (ex.: aterramento, senha, 4-20 mA)" autocomplete="off"><p class="vazio" id="busca-vazio" hidden>Nada encontrado. Tente outra palavra ou fale com o suporte.</p></div>
  <nav class="indice" aria-label="Índice">{indice}</nav>
  {secoes}
  <footer class="rodape"><b>Techmeter</b> · K&amp;K do Brasil Ltda. · Rua Pedrália, 70 – Vila Gumercindo – São Paulo/SP<br>{CONTATO['site']} · {CONTATO['vendas']}<br><a href="../">Ver outros modelos</a></footer>
</main>
<script src="../app.js"></script>
</body></html>"""


def pagina_inicial(base_url):
    def card(m):
        img = f'<img src="img/{m["foto"]}" alt="">' if m["foto"] else "<div></div>"
        return f'<a class="modelo" href="{m["slug"]}/">{img}<div><b>{html.escape(m["curto"])}</b>{html.escape(m["resumo"])}</div></a>'
    cards = "".join(card(m) for m in CFG["modelos"])
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Manuais · Medidor eletromagnético · Techmeter</title><meta name="theme-color" content="#14204a">
<meta name="color-scheme" content="light">
<link rel="stylesheet" href="estilo.css">
<style>@font-face{{font-family:Lato;src:url(fontes/Lato-Regular.ttf)}}@font-face{{font-family:Lato;font-weight:700;src:url(fontes/Lato-Bold.ttf)}}@font-face{{font-family:Montserrat;font-weight:100 900;src:url("fontes/Montserrat[wght].ttf")}}</style>
</head><body>
<header class="topo"><img src="img/logo-techmeter.png" alt="TechMeter"><div class="t">Manuais do produto<small>Medidor de vazão eletromagnético</small></div></header>
<main class="pagina">
  <h1 style="font:800 24px Montserrat;color:var(--ink);margin:6px 0 4px">Escolha o seu modelo</h1>
  <p style="color:var(--soft)">O modelo está na plaqueta do equipamento e na etiqueta do QR code.</p>
  <div class="modelos">{cards}</div>
  <footer class="rodape"><b>Techmeter</b> · {CONTATO['site']} · WhatsApp {CONTATO['zap']}</footer>
</main></body></html>"""


# ---------------------------------------------------------------- QR codes
def qrcodes(base_url):
    import qrcode, qrcode.image.svg
    from PIL import Image, ImageDraw, ImageFont
    dest = AQUI / "qrcodes"; dest.mkdir(exist_ok=True)
    F = RAIZ / "modelos/manual-tecnico/assets/fontes"
    def fb(s):
        f = ImageFont.truetype(str(F / "Montserrat[wght].ttf"), s); f.set_variation_by_axes([800]); return f
    fl = lambda s: ImageFont.truetype(str(F / "Lato-Regular.ttf"), s)
    logo = Image.open(AQUI / "img/logo-techmeter.png").convert("RGBA")
    itens = [(m["slug"], f"{base_url}/{CFG['caminho']}/{m['slug']}/", m["curto"].split(" ", 1), ("MANUAL DO", "PRODUTO"))
             for m in CFG["modelos"]]
    # página com a lista de todos os modelos
    itens.append(("lista-manuais", f"{base_url}/{CFG['caminho']}/", ["Eletromagnéticos", "Todos os modelos"], ("MANUAIS", "TECHMETER")))
    for slug, url, linhas, titulo in itens:
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=2, box_size=20)
        qr.add_data(url); qr.make(fit=True)
        img = qr.make_image(fill_color="#14204a", back_color="white").convert("RGB")
        img.save(dest / f"{slug}-qr.png")
        qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, border=2).save(str(dest / f"{slug}-qr.svg"))
        # etiqueta 60 x 40 mm a 300 dpi
        W, H = 709, 472
        e = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(e)
        d.rectangle([0, 0, W - 1, H - 1], outline="#14204a", width=4)
        q = img.resize((400, 400), Image.NEAREST); e.paste(q, (W - 420, 36))
        lg = logo.copy(); lg.thumbnail((250, 70)); e.paste(lg, (28, 34), lg)
        d.text((28, 140), titulo[0], font=fb(30), fill="#d01f1f")
        d.text((28, 176), titulo[1], font=fb(30), fill="#d01f1f")
        y = 240
        for linha in linhas:
            tam = 28
            while tam > 16 and d.textlength(linha, font=fb(tam)) > W - 420 - 40: tam -= 1
            d.text((28, y), linha, font=fb(tam), fill="#14204a"); y += 36
        d.text((28, 340), "Aponte a câmera", font=fl(22), fill="#333c4f")
        d.text((28, 368), "do celular", font=fl(22), fill="#333c4f")
        d.text((W // 2, H - 26), url.replace("https://", ""), font=fl(17), fill="#667085", anchor="mm")
        e.save(dest / f"{slug}-etiqueta.png", dpi=(300, 300))
    print("QR codes em", dest)


def main():
    base_url = CFG["url_base"].rstrip("/")
    if SAIDA.exists(): shutil.rmtree(SAIDA)
    (SAIDA / "img").mkdir(parents=True)
    shutil.copytree(RAIZ / "modelos/manual-tecnico/assets/fontes", SAIDA / "fontes")
    for f in (AQUI / "img").iterdir(): shutil.copy(f, SAIDA / "img" / f.name)
    shutil.copy(RAIZ / "modelos/manual-tecnico/assets/logo-techmeter.png", SAIDA / "img/logo-techmeter.png")
    shutil.copy(RAIZ / "modelos/manual-tecnico/assets/logo-techmeter.png", AQUI / "img/logo-techmeter.png")
    shutil.copy(AQUI / "estilo.css", SAIDA / "estilo.css"); shutil.copy(AQUI / "app.js", SAIDA / "app.js")
    (SAIDA / "index.html").write_text(pagina_inicial(base_url), encoding="utf-8")
    for m in CFG["modelos"]:
        p = SAIDA / m["slug"]; p.mkdir()
        (p / "index.html").write_text(pagina(m, base_url), encoding="utf-8")
        if "--sem-pdf" not in sys.argv and Path(CHROME).exists():
            subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                            "--allow-file-access-from-files", f"--print-to-pdf={p / ('manual-' + m['slug'] + '.pdf')}",
                            (p / "index.html").as_uri()], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
        print("ok", m["slug"])
    qrcodes(base_url)


if __name__ == "__main__":
    main()
