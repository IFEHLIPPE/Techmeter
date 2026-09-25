# Auditoria técnica GEO

Checklist da seção 4 do projeto, com o **como verificar** de cada item.
Resultados de cada rodada vão em `auditorias/AAAA-MM-DD.md`.

## Automatizado (script)

```bash
cd projetos/geo && mkdir -p auditorias
python3 ferramentas/auditoria_geo.py https://www.techmeter.com.br \
  / /produto/medidor-de-vazao-eletromagnetico /servicos /contato \
  > auditorias/$(date +%F).md
```

O script verifica robots.txt, quais crawlers de busca/IA estão liberados, o sitemap, e em cada página: title, description, canonical, noindex, H1, headings, JSON-LD, volume de texto no HTML, links internos e imagens sem `alt`.

## Checklist

| # | Item | Como verificar | Status |
|---|---|---|---|
| 1 | robots.txt | Script, ou abrir `techmeter.com.br/robots.txt`. Nenhuma página importante deve estar em `Disallow`. | 🔲 |
| 2 | sitemap.xml | Script. O sitemap deve existir, ser declarado no robots.txt e conter as páginas prioritárias. | 🔲 |
| 3 | Indexação das páginas prioritárias | Search Console → **Inspeção de URL** para cada página. Busca rápida: `site:techmeter.com.br eletromagnético`. | 🔲 |
| 4 | Canonicals e duplicadas | Script (canonical apontando para outra URL). Verificar versões com/sem `www`, `http`/`https`, barra final e parâmetros. Todas devem redirecionar (301) para uma só. | 🔲 |
| 5 | Conteúdo importante em HTML | Script ("palavras no HTML"). Também: Chrome → Ver código-fonte (Ctrl+U) e procurar o texto técnico. Se só aparece com JavaScript, muitos crawlers de IA não enxergam. | 🔲 |
| 6 | Estrutura de headings | Script. Deve ter um H1 por página e H2/H3 seguindo as seções (ver [modelo do piloto](piloto-eletromagnetico/estrutura-pagina.md)). | 🔲 |
| 7 | Links internos | Script (contagem). Produto ↔ aplicações ↔ serviços ↔ artigos devem se linkar entre si. | 🔲 |
| 8 | Dados estruturados | Script (tipos JSON-LD) + [Teste de pesquisa aprimorada](https://search.google.com/test/rich-results). Relevantes: `Organization`, `Product`, `BreadcrumbList`, `Article`, `VideoObject`. | 🔲 |
| 9 | Google Search Console | Confirmar acesso, propriedade verificada, sitemap enviado, páginas indexadas x não indexadas, erros. | 🔲 |
| 10 | Bing Webmaster Tools | Configurar/revisar (dá para importar do Search Console). Enviar sitemap. Ver relatório **AI Performance**. O Bing alimenta o Copilot. | 🔲 |
| 11 | Acesso de crawlers (inclui OAI-SearchBot) | Script (tabela de crawlers). Verificar também se CDN/firewall (ex.: Cloudflare) não bloqueia bots de IA. Isso o robots.txt não mostra. | 🔲 |
| 12 | Lista de erros para o developer | Consolidar os ⚠️/⛔ encontrados na tabela abaixo. | 🔲 |

### Crawlers que importam para GEO

| Crawler | Controla | Recomendação inicial |
|---|---|---|
| `Googlebot` | Busca Google **e** AI Overviews / Modo IA | Liberado |
| `Bingbot` | Busca Bing **e** Copilot | Liberado |
| `OAI-SearchBot` | Aparecer/ser citado na busca do ChatGPT | Liberado |
| `ChatGPT-User` | ChatGPT abrindo páginas quando o usuário pede | Liberado |
| `PerplexityBot` | Busca do Perplexity | Liberado |
| `Google-Extended` | Uso do conteúdo em Gemini (não afeta a busca Google) | Decisão da Mariana |
| `GPTBot`, `ClaudeBot` etc. | Treino de modelos | Decisão da Mariana (liberar tende a ajudar a marca a ser "conhecida" pelos modelos) |

> Os liberados/bloqueados de treino são uma **decisão de negócio**. Quando for tomada, registrar em `docs/decisoes.md`.

## Erros encontrados → developer

| Prioridade | Página / área | Problema | Correção sugerida | Status |
|---|---|---|---|---|
| | | | | |
