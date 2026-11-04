# Modelo — Manual técnico Techmeter

Modelo padrão para **manuais de operação e catálogos técnicos** da Techmeter. A identidade visual segue o manual **LATM 2025**, feito no Canva: fundo azul-claro com ondas, títulos em faixa azul, fontes Lato e Montserrat, e rodapé com dados da K&K do Brasil e o logo.

## Como gerar um manual novo

1. Crie uma pasta em `documentos/manuais/<produto>/` com:
   - `manual.json` com os dados da capa:
     ```json
     {
       "titulo": "TÍTULO DO PRODUTO<br>SEGUNDA LINHA",
       "modelo": "CÓDIGO",
       "tipo": "MANUAL",
       "imagem_capa": "imagens/produto.png",
       "arquivo": "manual-<produto>",
       "arquivos": []
     }
     ```
   - `conteudo.html` com o texto, usando os elementos da tabela abaixo.
   - `imagens/` com a foto do produto **sem fundo** (PNG transparente) e as demais figuras.
2. Gere o PDF:
   ```bash
   python3 modelos/manual-tecnico/gerar.py documentos/manuais/<produto>
   ```
   O resultado é `documentos/manuais/<produto>/<arquivo>.pdf`. O índice com números de página é feito automaticamente.

Requisitos: Python 3, Chromium/Chrome e `pdftotext` (poppler-utils).

## Elementos do conteúdo

| Elemento | Uso |
|---|---|
| `<h2 class="capitulo">` | Capítulo: faixa azul centralizada, entra no índice. Acrescente `nova-pagina` para forçar uma página nova. |
| `<h3>` | Seção: faixa azul à esquerda, entra no índice |
| `<h4>` | Subtítulo em negrito, fora do índice |
| `<table class="dados">` | Tabelas: bornes, menus, registradores, especificações. Use `<td class="cod">` para códigos. |
| `<div class="figura">…<div class="legenda">` | Figura com legenda ("Figura N: …") |
| `<div class="aviso">` | Alerta de segurança, com borda vermelha |
| `<div class="nota">` | Observação, com borda azul |
| `<span class="tecla">✓</span>` | Ícone de tecla |
| `<span class="validar">VALIDAR: …</span>` | Marca amarela de **pendência**. Precisa sumir antes da versão final. |

## Arquivos

| Arquivo | O que é |
|---|---|
| `estilo.css` | Visual: cores, fontes, capa, rodapé, tabelas |
| `gerar.py` | Monta capa, índice, conteúdo e contracapa e imprime o PDF |
| `assets/logo-techmeter.png` | Logo extraído do manual LATM 2025 (baixa resolução). **Trocar pelo vetor oficial quando houver.** |
| `assets/ondas.png` | Ondas da identidade visual (manual LATM 2025) |
| `assets/fontes/` | Lato e Montserrat (licença SIL Open Font) |

Os dados da empresa (razão social, CNPJ, endereço, telefones e e-mail) ficam em `EMPRESA`, no início de `gerar.py`.

## Manuais feitos com este modelo

| Manual | Pasta |
|---|---|
| LATM — caixa de campo (firmware 2.00) | `documentos/manuais/latm-caixa-campo/` |
