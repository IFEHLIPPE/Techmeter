# Manual online — medidor de vazão eletromagnético

Manual para o cliente abrir pelo **QR code colado no equipamento**. Uma página por modelo, pensada para celular:
instalação, ligações, display, configuração básica, alarmes, especificações e suporte. Cada página tem busca,
botão de WhatsApp do suporte e PDF para baixar.

| Modelo | Página publicada |
|---|---|
| TM-EL Flangeado · conversor integrado | `/manual/eletromagnetico/tm-el-integrado/` |
| TM-EL Flangeado · conversor remoto | `/manual/eletromagnetico/tm-el-remoto/` |
| TMTC Tri-Clamp (sanitário) | `/manual/eletromagnetico/tmtc-sanitario/` |
| TMWF Wafer | `/manual/eletromagnetico/tmwf-wafer/` |

## Como atualizar

1. Edite o conteúdo em `build.py` (capítulos) ou os modelos em `modelos.json`.
2. Rode: `python3 manuais-online/eletromagnetico/build.py` (precisa de `qrcode[pil]` e Chromium).
3. O resultado vai para `site/manual/eletromagnetico/` (publicado pelo Cloudflare Pages) e os QR codes para `qrcodes/`.

## Modelo 3D

Modelos com `"modelo_3d": true` mostram o 3D logo abaixo dos botões, só para girar e ver (cores padrão).
É o mesmo configurador de `modelos-3d/medidor-eletromagnetico/`, aberto com `?visualizar`, que esconde o painel de cores.
Se mudar o configurador, rode `python3 modelos-3d/gerar_site.py` antes deste build.

## QR codes

- `qrcodes/<modelo>-etiqueta.png`: etiqueta 60 × 40 mm (300 dpi) pronta para imprimir.
- `qrcodes/<modelo>-qr.svg` / `.png`: só o QR, para usar em outras artes.
- `qrcodes/lista-manuais-*`: QR e etiqueta da página com a lista de todos os modelos (para catálogo, balcão, proposta).
- **O endereço do QR não pode mudar depois de impresso.** Hoje ele aponta para `url_base` em `modelos.json`
  (`https://tm-el-3d.pages.dev`). Se for usar um domínio próprio (ex.: `manual.techmeter.com.br`),
  troque `url_base` e gere de novo **antes** de imprimir.

## Fontes

Conteúdo resumido do "Manual Eletromagnético KF – 2022" (Techmeter). Figuras de instalação, aterramento,
display e bornes extraídas desse manual. Fotos do TM-EL integrado: unidade fotografada na Techmeter.
As senhas do conversor não são publicadas na página (o cliente pede ao suporte).
