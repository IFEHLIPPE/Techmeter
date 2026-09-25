# Piloto — Estrutura GEO da página "Medidor de Vazão Eletromagnético"

Página atual: https://www.techmeter.com.br/produto/medidor-de-vazao-eletromagnetico

> **Princípio:** responder primeiro a pergunta do usuário de forma clara e tecnicamente correta. Depois aprofundar. Evitar texto genérico feito só para encaixar palavras-chave.

A página de produto não deve funcionar só como catálogo. Ela precisa responder às dúvidas de **seleção, especificação, instalação e aplicação**.

## Como escrever para ser citado

- **Resposta direta no início de cada seção.** As 1–2 primeiras frases devem responder sozinhas à pergunta. É esse trecho que as IAs costumam citar.
- **Números concretos e com contexto.** Por exemplo: "condutividade mínima de X µS/cm" em vez de "baixa condutividade".
- **Títulos (H2/H3) em forma de pergunta** quando fizer sentido, iguais às perguntas do baseline.
- **Tabelas** para comparações (revestimentos, eletrodos, fluidos).
- **Experiência própria** da Techmeter: casos, fotos e vídeos de start-up, calibração e diagnóstico. É o que diferencia o conteúdo do resto da internet.
- **Texto no HTML**, não só em PDF, imagem ou carrossel carregado por JavaScript.
- **Autor/revisor técnico e data de atualização** visíveis.

## As 18 seções

Legenda de status: 🔲 a fazer · ✍️ rascunho · 🔎 em revisão técnica · ✅ aprovado

| # | Seção | O que precisa responder | Prompts do baseline | Quem fornece a informação | Status |
|---|---|---|---|---|---|
| 1 | O que é | Definição em 2–3 frases | EM-01 | Marketing | 🔲 |
| 2 | Como funciona | Lei de Faraday, bobinas, eletrodos, sem partes móveis. Um diagrama simples ajuda. | EM-01, EM-07 | Marketing + técnico | 🔲 |
| 3 | Quando usar | Líquidos condutivos, com sólidos, polpas, efluentes; sem perda de carga | EM-05, EM-06, EM-07 | Técnico | 🔲 |
| 4 | Quando não usar | Gases, vapor, hidrocarbonetos/óleos, água desmineralizada e outros fluidos de baixa condutividade | EM-03 | Técnico | 🔲 |
| 5 | Fluidos compatíveis | Tabela de fluido × recomendação | EM-05, EM-06 | Técnico | 🔲 |
| 6 | Condutividade mínima | Valor para os modelos Techmeter (confirmar) e o que acontece abaixo dele | EM-03, EM-04 | Técnico / datasheet | 🔲 |
| 7 | Precisão | Precisão dos modelos Techmeter e em que condições é garantida | EM-13 | Datasheet | 🔲 |
| 8 | Dimensionamento | Faixa de velocidade recomendada, como escolher o DN, exemplo de cálculo | EM-12 | Técnico | 🔲 |
| 9 | Instalação | Tubo sempre cheio, posição vertical/horizontal, pontos altos a evitar, bombas e válvulas | EM-14 | Técnico (fotos reais!) | 🔲 |
| 10 | Trechos retos | Diâmetros a montante e a jusante recomendados pela Techmeter | EM-08 | Técnico / manual | 🔲 |
| 11 | Aterramento | Anéis de aterramento, tubulação plástica ou revestida | EM-09 | Técnico / manual | 🔲 |
| 12 | Revestimentos | Tabela: PTFE, borracha, cerâmica etc. × temperatura × aplicação | EM-10 | Técnico / datasheet | 🔲 |
| 13 | Eletrodos | Tabela: inox 316L, Hastelloy, titânio, tântalo, platina × fluidos | EM-11 | Técnico / datasheet | 🔲 |
| 14 | Aplicações | Saneamento, mineração, papel e celulose, alimentos, química. Cada uma com um caso real. | EM-17, EM-18, EM-19 | Técnico + cases | 🔲 |
| 15 | Erros comuns | Tubo parcialmente cheio, aterramento ruim, ar na linha, DN superdimensionado | EM-15 | Suporte técnico / assistência | 🔲 |
| 16 | FAQ técnico | 8–12 perguntas curtas vindas do baseline e de dúvidas reais de clientes | EM-01…EM-20 | Todos | 🔲 |
| 17 | Modelos Techmeter | Integrado × remoto, faixas de DN, saídas, links para datasheets | EM-16, EM-20 | Comercial / datasheet | 🔲 |
| 18 | CTA | "Solicite dimensionamento / orçamento técnico", com formulário que peça fluido, DN, vazão e condutividade | EM-20 | Marketing | 🔲 |

> Os pontos acima são o **conteúdo técnico esperado** em geral. Os **valores específicos** (condutividade mínima, precisão, trechos retos, materiais, DNs) precisam vir dos **datasheets/manuais da Techmeter** e passar pela revisão da equipe técnica. Não publicar número que não foi validado.

## Mapa atual da página (preencher na semana 1)

Rodar `ferramentas/auditoria_geo.py` e anotar abaixo o que a página tem hoje.

| Seção do modelo | Existe hoje? | Observação |
|---|---|---|
| 1–18 | | |

## Materiais internos a pedir para o time técnico

- [ ] Datasheet e manual dos medidores eletromagnéticos
- [ ] Fotos/vídeos de instalação, start-up, parametrização, calibração e resinagem
- [ ] 2–3 casos reais de aplicação (cliente pode ficar anônimo)
- [ ] Lista de dúvidas mais frequentes que chegam em vendas e suporte
- [ ] Problemas mais comuns em campo (para a seção "Erros comuns")
