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
- `midia/fotos-produtos/`: 3 fotos do medidor com mostrador, recortadas (PNG sem fundo e JPG fundo branco).
- `midia/fotos-produtos/2026-11-03-conversor-compacto-ip67/`: imagem do conversor compacto com as cotas do desenho técnico (Ø104, 205, Ø80, Ø64, 8 furos Ø5 mm; medidas corrigidas em 05/11).
- `midia/simulacoes-internas/`: simulação interna da membrana LATM numa caixa de painel (não publicar).
- `modelos/manual-tecnico/`: modelo de manual técnico Techmeter (capa, índice automático, rodapé, contracapa) e gerador de PDF.
- `documentos/manuais/tm-smart/`: manual do TM-Smart (rascunho, com pendências marcadas como VALIDAR). Capa refeita para ficar fiel ao manual LATM 2025. Membrana oficial TM-Smart aplicada na imagem do produto e nova figura do painel frontal.
- `midia/fotos-produtos/2026-11-tm-smart/`: arte da membrana TM-Smart e montagens do produto.
- `modelos-3d/medidor-eletromagnetico/`: configurador 3D do medidor eletromagnético TM-EL, com troca de cor do cabeçote, das tampas e da base.
- `site/`: versão pública do configurador 3D para o Cloudflare Pages, gerada por `modelos-3d/gerar_site.py`.
- `documentos/catalogos/valvula-solenoide-g80/`: catálogo da válvula solenoide G80 no modelo Techmeter, em português, com especificações, materiais, gráficos de perda de carga redesenhados, dimensões com peso, códigos de pedido e bobina.
- `documentos/manuais/radar-80g/`: manual do radar 80G refeito em português no modelo Techmeter, com o protocolo RS485 Modbus incorporado.

### Alterado
- `EM-01` a `EM-20` em `baseline/prompts.csv` substituídos pelos 20 prompts oficiais do Ciclo 1. Intenções alinhadas ao documento (informacional, seleção, comparação, aplicação, comercial, troubleshooting).
- `citation_share.py` ignora linhas ainda não preenchidas.
