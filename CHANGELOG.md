# Changelog

Todas as mudanças relevantes deste repositório são registradas aqui.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [Não lançado]

### Adicionado
- Estrutura inicial do repositório: README, CLAUDE.md, CONTRIBUTING, CHANGELOG, `docs/` e template de PR.
- `docs/empresa.md` com informações públicas da Techmeter (produtos, serviços, mercados, contato).
- Projeto GEO (`projetos/geo/`): plano de 90 dias, checklist da semana 1, base com 50 prompts, planilha de registro, checklist de auditoria técnica e modelo da página do piloto de eletromagnético.
- Scripts `auditoria_geo.py` (robots, crawlers de IA, sitemap e estrutura das páginas) e `citation_share.py` (cálculo do AI Citation Share).
- GEO Ciclo 1 (`projetos/geo/ciclo1-eletromagnetico/`): documento da Mariana em Markdown, planilha `teste-prompts-ciclo1.xlsx` (teste D0, resumo automático e priorização para o Victor).

### Alterado
- `EM-01` a `EM-20` em `baseline/prompts.csv` substituídos pelos 20 prompts oficiais do Ciclo 1. Intenções alinhadas ao documento (informacional, seleção, comparação, aplicação, comercial, troubleshooting).
- `citation_share.py` ignora linhas ainda não preenchidas.
