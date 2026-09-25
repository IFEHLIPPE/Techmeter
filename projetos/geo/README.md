# Projeto GEO — Otimização para Mecanismos Generativos

> **Objetivo:** fazer a Techmeter se tornar uma fonte técnica cada vez mais fácil de encontrar, entender e citar em respostas de mecanismos generativos (ChatGPT, Google AI, Gemini, Copilot e outras buscas com IA).

| | |
|---|---|
| **Gestão e estratégia** | Mariana |
| **Responsável operacional** | Felippe |
| **Duração inicial** | 90 dias |
| **Piloto** | Medição de Vazão Eletromagnética |
| **Fonte** | Página do Notion "Projeto GEO — Otimização para Mecanismos Generativos" |

> GEO não substitui SEO. O projeto combina fundamentos técnicos de SEO, arquitetura de informação, conteúdo original, autoridade técnica e acompanhamento de presença em mecanismos generativos.

## Arquivos deste projeto

| Arquivo | Para que serve |
|---|---|
| [`semana-1.md`](semana-1.md) | Checklist da primeira semana (Felippe) com status |
| [`baseline/README.md`](baseline/README.md) | Metodologia do baseline: como rodar e registrar os prompts |
| [`baseline/prompts.csv`](baseline/prompts.csv) | Base dos 50 prompts estratégicos (abre no Excel/Google Sheets) |
| [`baseline/registro.csv`](baseline/registro.csv) | Planilha de registro dos testes (D0, D30, D60, D90) |
| [`auditoria-tecnica.md`](auditoria-tecnica.md) | Checklist da auditoria técnica + como verificar cada item |
| [`ferramentas/auditoria_geo.py`](ferramentas/auditoria_geo.py) | Script que automatiza parte da auditoria (robots, sitemap, página) |
| [`piloto-eletromagnetico/estrutura-pagina.md`](piloto-eletromagnetico/estrutura-pagina.md) | Modelo das 18 seções da nova página de eletromagnético |

## 1. Frentes do projeto

| Frente | O que será feito | Responsabilidade |
|---|---|---|
| Diagnóstico GEO | Mapear como a Techmeter aparece hoje nas principais IAs e buscas generativas | Felippe executa; Mariana acompanha |
| Infraestrutura | Indexação, robots.txt, sitemap, Search Console, Bing Webmaster, crawlers, estrutura técnica | Felippe + developer |
| Arquitetura de conteúdo | Organizar os territórios de autoridade | Mariana define; Felippe estrutura |
| Conteúdo GEO | Transformar páginas comerciais em conteúdos técnicos úteis, estruturados e citáveis | Felippe executa; Mariana e time técnico validam |
| Autoridade técnica | Cases, aplicações, vídeos, testes, start-up, comissionamento, conhecimento interno | Marketing + equipe técnica |
| Medição | Prompts, citações, páginas encontradas, tráfego de IA e leads | Felippe |
| Otimização contínua | Atualizar páginas com base em perguntas e lacunas encontradas | Mariana + Felippe |

## 2. Territórios de autoridade

1. **Medição de Vazão** — Eletromagnético · Vortex · Mássico termal · Turbina · Rotâmetro e outras
2. **Medição de Nível** — Radar · Ultrassônico · Hidrostático
3. **Hidrômetros** — Woltmann · Tangencial · Multijato · Unijato
4. **Serviços técnicos** — Calibração · Manutenção · Start-Up e Comissionamento · Suporte técnico
5. **Aplicações industriais** — Saneamento · Irrigação · Papel e celulose · Mineração · Química · Alimentos e bebidas · Energia · Óleo e gás

## 3. Conteúdo técnico como matéria-prima

Cada atividade técnica gera vários ativos:
vídeo técnico → Reel → YouTube → página técnica → FAQ → artigo → LinkedIn → case → imagens técnicas → atualização da página do produto.

Priorizar registros reais de: parametrização, calibração, resinagem, testes finais, instalação, comissionamento, start-up, diagnóstico de problemas e aplicações reais.

## 4. Piloto — Medição de Vazão Eletromagnética

- [ ] Auditoria da página atual
- [ ] Levantamento das perguntas reais sobre eletromagnéticos
- [ ] Análise das fontes que hoje aparecem nas respostas generativas
- [ ] Nova arquitetura de conteúdo ([modelo](piloto-eletromagnetico/estrutura-pagina.md))
- [ ] FAQ técnico
- [ ] Conteúdo de instalação e aplicação
- [ ] Conteúdo sobre limitações e quando não utilizar
- [ ] Revisão técnica interna
- [ ] Implementação no site
- [ ] Novo teste dos mesmos prompts após publicação

## 5. KPIs

**SEO / site:** impressões orgânicas · cliques orgânicos · queries relevantes · páginas indexadas · leads das páginas trabalhadas.

**GEO:** prompts monitorados · respostas em que a Techmeter aparece · citações/menções · páginas Techmeter usadas como fonte · concorrentes/fontes recorrentes · evolução em 30/60/90 dias.

**Indicador interno — AI Citation Share**

```
AI Citation Share = prompts em que a Techmeter aparece ÷ total de prompts monitorados
```

Exemplo: 6 aparições em 50 prompts = 12%. Métrica interna de acompanhamento, **não** promessa de posicionamento.

## 6. Cronograma de 90 dias

### Dias 1–15 — Diagnóstico
- [ ] Construir os 50 prompts *(rascunho pronto em `baseline/prompts.csv` — revisar com Mariana)*
- [ ] Rodar baseline
- [ ] Executar auditoria técnica
- [ ] Criar mapa de autoridade
- [ ] Escolher lacunas prioritárias do piloto

### Dias 16–45 — Construção
- [ ] Reestruturar cluster de eletromagnético
- [ ] Produzir FAQs e conteúdos técnicos
- [ ] Implementar melhorias técnicas
- [ ] Criar links internos
- [ ] Transformar materiais internos em ativos digitais

### Dias 46–75 — Expansão
- [ ] Repetir metodologia para outros clusters
- [ ] Priorizar Vortex / Mássico Termal / Nível conforme resultados e estratégia comercial
- [ ] Publicar cases e aplicações
- [ ] Consolidar rotina de conteúdo técnico

### Dias 76–90 — Medição e próxima fase
- [ ] Rodar novamente os prompts
- [ ] Comparar baseline inicial x 90 dias
- [ ] Analisar páginas e conteúdos que ganharam presença
- [ ] Identificar lacunas
- [ ] Definir segundo ciclo GEO

## 7. Rotina de gestão

- **Felippe:** executa pesquisas, testes, documentação e produção; mantém a base atualizada; traz achados, problemas e oportunidades.
- **Mariana:** define prioridades e estratégia; aprova direcionamento de conteúdo; conecta GEO com campanhas, site, growth e posicionamento; aciona equipe técnica e developer.

**Revisão semanal** (curta), com três perguntas:
1. O que avançou?
2. O que aprendemos?
3. Qual é a próxima ação de maior impacto?

## Referências oficiais

- Google — [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- OpenAI — [Publishers and Developers FAQ](https://help.openai.com/en/articles/12627856-publishers-and-developers-faq)
- OpenAI — [Overview of OpenAI crawlers](https://platform.openai.com/docs/bots)
- Bing Webmaster — [Bing Webmaster Tools](https://www.bing.com/webmasters) (relatório AI Performance)
