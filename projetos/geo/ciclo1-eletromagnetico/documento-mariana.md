# GEO Techmeter — Ciclo 1: Medidor de Vazão Eletromagnético

> Conversão em Markdown do arquivo `GEO Ciclo1-Eletromagnetico - Scripts p videos.docx`, enviado por Mariana Costa em 02/10/2026 (original em [`original/`](original/)).
> O documento recebido começa na seção 2–3 e pula as seções 1 e 9–11 (a seção 9 é citada no texto). Os dois últimos títulos `###` foram adicionados na conversão, porque as tabelas não tinham título.

## 2–3. 20 prompts estratégicos e intenções

Os 20 prompts cobrem as 6 intenções e formam o primeiro bloco do baseline de ~50. Felippe e Mariana: cada um deve ser testado no ChatGPT, Google AI Mode/AI Overviews, Gemini e Copilot, em sessão anônima, com o texto exato abaixo.

| # | Prompt (texto exato do teste) | Intenção | Página que deve responder |
|---|---|---|---|
| 1 | Como funciona um medidor de vazão eletromagnético? | Informacional | Hub eletromagnético |
| 2 | Medidor eletromagnético precisa de trecho reto? Quanto? | Informacional | Guia de instalação |
| 3 | Qual a condutividade mínima para usar medidor eletromagnético? | Informacional | Hub + FAQ |
| 4 | Por que o medidor eletromagnético precisa de aterramento? | Informacional | Guia de instalação |
| 5 | Qual medidor de vazão usar para água com sólidos? | Seleção | Hub + aplicação efluentes |
| 6 | Como escolher o revestimento de um medidor eletromagnético? | Seleção | Guia de revestimentos e eletrodos |
| 7 | Como dimensionar um medidor eletromagnético (qual DN escolher)? | Seleção | Guia de dimensionamento |
| 8 | Qual material de eletrodo usar para ácidos e produtos corrosivos? | Seleção | Guia de revestimentos e eletrodos |
| 9 | Qual a diferença entre medidor eletromagnético e ultrassônico? | Comparação | Comparativo eletromagnético × ultrassônico |
| 10 | Medidor eletromagnético ou vortex: qual escolher? | Comparação | Guia de seleção de tecnologia de vazão |
| 11 | Medidor eletromagnético ou hidrômetro Woltmann para rede de água? | Comparação | Aplicação saneamento |
| 12 | Medidor eletromagnético ou turbina para água limpa? | Comparação | Guia de seleção de tecnologia de vazão |
| 13 | Qual medidor usar para vazão de efluentes em ETE? | Aplicação | Aplicação saneamento / efluentes |
| 14 | Como medir vazão de polpa de minerção? | Aplicação | Aplicação minerção |
| 15 | Medidor de vazão para irrigação com outorga de água | Aplicação | Aplicação irrigação / outorga |
| 16 | Medidor eletromagnético sanitário para indústria de alimentos (CIP) | Aplicação | Aplicação alimentos e bebidas |
| 17 | Fabricante brasileiro de medidor de vazão eletromagnético | Comercial | Hub + página institucional |
| 18 | Onde comprar medidor eletromagnético com calibração e suporte técnico no Brasil | Comercial | Hub + página de calibração |
| 19 | Por que meu medidor eletromagnético está marcando vazão errada? | Troubleshooting | Guia de diagnóstico |
| 20 | Medidor eletromagnético oscilando ou marcando vazão com a linha parada: o que fazer? | Troubleshooting | Guia de diagnóstico |

## 4. Principais subtemas

Oito subtemas sustentam o cluster; os três primeiros concentram as perguntas de seleção e troubleshooting, onde a experiência de campo da Techmeter mais diferencia.

| Subtema | Entidades que precisam aparecer | Por que importa para GEO | Prioridade |
|---|---|---|---|
| Instalação | trecho reto a montante/jusante, tubo cheio, posição vertical/horizontal, bolhas, válvulas e bombas, reduções | Gera perguntas de troubleshooting; conteúdo de fabricante costuma ser genérico | P1 |
| Aterramento e ruído elétrico | anéis de aterramento, eletrodo de terra, tubulação plástica/revestida, potencial | Causa frequente de erro de leitura; tema pouco explicado em PT-BR (hipótese) | P1 |
| Revestimentos e eletrodos | PTFE, PFA, borracha, poliuretano, cerâmica; eletrodos 316L, Hastelloy, titânio, tântalo, platina | Decisão de compra técnica; alimenta tabelas de compatibilidade | P1 |
| Princípio de funcionamento | Lei de Faraday, campo magnético, eletrodos, tensão induzida, condutividade | Pergunta informacional mais buscada; porta de entrada do cluster | P1 |
| Dimensionamento | DN, velocidade de escoamento, faixa de vazão, rangeabilidade, perda de carga | Evita erro de especificação; conecta com propostas comerciais | P2 |
| Seleção × outras tecnologias | ultrassônico, vortex, turbina, Woltmann, mássico | Prompts de comparação têm alto potencial de citação | P1 |
| Aplicações por setor | saneamento, efluentes, irrigação/outorga, minerção (polpa), papel e celulose, química, alimentos (CIP) | Liga o cluster ao Cluster 5 e a buscas com intenção de compra | P2 |
| Calibração, comissionamento e manutenção | calibração em bancada, verificação em campo, start-up, parametrização, diagnóstico | Diferencial de serviço da Techmeter; autoridade difícil de copiar | P1 |

## 5. Perguntas frequentes

Estas 15 perguntas entram no FAQ do hub (com dados estruturados FAQPage) e cada resposta deve abrir com 2–4 frases diretas. As marcadas com ★ dependem de dados Techmeter e só podem ser respondidas após validação técnica.

- O que é um medidor de vazão eletromagnético?
- Como funciona um medidor eletromagnético?
- Quais fluidos um medidor eletromagnético consegue medir?
- Medidor eletromagnético mede água destilada, óleo ou gás? (resposta: não para fluidos não condutivos — explicar o porquê)
- Medidor eletromagnético funciona com líquidos com sólidos em suspensão?
- Por que o medidor eletromagnético não tem partes móveis e o que isso muda na manutenção?
- O medidor eletromagnético causa perda de carga?
- O tubo precisa estar sempre cheio?
- Pode ser instalado na vertical?
- Mede vazão nos dois sentidos (bidirecional)?
- ★ Qual a precisão de um medidor eletromagnético Techmeter?
- ★ Quais diâmetros (DN) a Techmeter fornece?
- ★ Quais saídas e protocolos estão disponíveis (4–20 mA, pulso, HART, Modbus etc.)?
- ★ Existe versão remota (conversor separado do sensor) e versão alimentada por bateria?
- ★ Com que frequência calibrar e a Techmeter calibra equipamentos de outras marcas?

## 6. Perguntas técnicas avançadas

Essas perguntas raramente têm boa resposta em português e são onde 30 anos de campo viram autoridade citável. Todas exigem entrevista com a engenharia antes de virar conteúdo.

| Pergunta | Quem responde internamente | Formato sugerido |
|---|---|---|
| Como a excitação da bobina (DC pulsada × AC) afeta estabilidade e resposta com polpas? | Engenharia | Artigo técnico |
| Como o ruído de polpa e o acúmulo nos eletrodos afetam a medição e como mitigar? | Campo / assistência | Artigo + caso real |
| Como aterrar corretamente em tubulação de PVC, PEAD ou aço revestido? | Campo | Guia com diagrama |
| Como detectar tubo vazio ou parcialmente cheio e o que o conversor faz nesse caso? | Engenharia | FAQ + vídeo curto |
| Qual a velocidade de escoamento ideal e o que acontece abaixo de 0,3 m/s ou acima de 10 m/s? | Engenharia (validar faixas) | Tabela no guia de dimensionamento |
| Quando usar redução de diâmetro para aumentar a velocidade, e qual o impacto na perda de carga? | Engenharia | Guia de dimensionamento |
| Como escolher revestimento para água com cloro, polpa abrasiva ou temperatura elevada? | Engenharia | Tabela de compatibilidade |
| Como verificar um medidor em campo sem removê-lo da linha? | Laboratório de calibração | Artigo + vídeo |
| Como funciona a calibração em bancada e o que o certificado deve conter? | Laboratório de calibração | Página de serviço + FAQ |
| Quais são os 5 erros de instalação mais comuns que a Techmeter encontra no start-up? | Campo / comissionamento | Artigo "erros comuns" + Reel |
| Quais requisitos se aplicam ao medidor usado para outorga de uso de água? | Engenharia + regulatório (validar órgão/estado) | Página de aplicação |
| Como integrar o conversor a CLP/SCADA ou telemetria? | Engenharia / integração | Guia técnico |

## 7. Páginas necessárias

São 10 páginas: 1 hub (a página atual reescrita), 5 guias-satélite e 4 páginas de aplicação. Todas linkam para o hub e o hub linka para todas; nenhuma nova página de produto é criada enquanto os modelos não estiverem validados.

| Página | Tipo | Prompts atendidos | Prioridade | Responsável sugerido |
|---|---|---|---|---|
| Medidor de vazão eletromagnético (hub) — reescrita da página atual na estrutura de 22 blocos | Produto + educação | 1, 3, 5, 17, 18 | P1 | Mariana (aprova) · Felippe · Engenharia |
| Como instalar um medidor eletromagnético: trechos retos, aterramento e posição | Guia | 2, 4 | P1 | Felippe + Campo |
| Por que o medidor eletromagnético marca errado: guia de diagnóstico | Guia / troubleshooting | 19, 20 | P1 | Felippe + Assistência |
| Como escolher revestimento e eletrodo | Guia com tabela | 6, 8 | P2 | Engenharia |
| Eletromagnético × ultrassônico: quando usar cada um | Comparativo | 9 | P2 | Felippe |
| Como dimensionar um medidor eletromagnético | Guia | 7 | P2 | Engenharia |
| Medição de vazão em saneamento e efluentes | Aplicação | 11, 13 | P2 | Felippe + Comercial |
| Medição de vazão para irrigação e outorga | Aplicação | 15 | P2 | Felippe + Comercial |
| Medição de vazão de polpa em minerção | Aplicação | 14 | P3 | Engenharia |
| Medidor eletromagnético sanitário para alimentos e bebidas | Aplicação | 16 | P3 — só se houver modelo sanitário no portfólio (VALIDAR) | Engenharia |

Os prompts 10 e 12 (vortex e turbina) ficam para o guia geral de seleção de tecnologia de vazão, que nasce no ciclo do Cluster 1 completo.

## 8. Reaproveitamento em redes sociais

Cada guia do site gera ao menos 4 peças; a regra é publicar a página primeiro e usar as redes para levar tráfego e sinal de autoridade até ela.

| Pauta de origem | LinkedIn | Instagram | Vídeo (YouTube / Reel) | Comercial |
|---|---|---|---|---|
| 5 erros de instalação que vemos no start-up | Post em lista com foto de campo | Carrossel "erro × correção" | Reel de 30–45 s com técnico em campo | Checklist de pré-instalação anexado à proposta |
| Como funciona o eletromagnético | Post explicativo com diagrama | Carrossel em 5 telas | YouTube 3–5 min com sensor em corte | Slide padrão para apresentações |
| Aterramento: por que o medidor oscila | Post "caso real" (validar autorização do cliente) | Carrossel antes/depois | Reel mostrando anéis de aterramento | Resposta pronta para chamados de suporte |
| Revestimento e eletrodo | Tabela resumida em imagem | Carrossel "qual escolher para…" | — | Tabela de seleção para vendedores |
| Eletromagnético × ultrassônico | Post comparativo | Carrossel "quando usar cada um" | YouTube curto lado a lado | Argumento para propostas paradas |
| Calibração em bancada | Bastidores do laboratório | Reel do processo | YouTube do processo completo | Material para renovação de contratos de serviço |

Conteúdo de campo (fotos, vídeos, casos) precisa de autorização do cliente e revisão técnica antes de publicar.

## 12. Pesquisa de termos: ferramentas e termos no Brasil

Nenhuma ferramenta mostra "o que as pessoas perguntam às IAs" com volume real; para Google e Bing há dados de volume, e para IAs o melhor dado disponível hoje é o relatório de citações do Bing mais o baseline manual de prompts. A lista de termos abaixo vem do autocompletar do Google e do Bing (Brasil, pt-BR, coletado em 30/09/2026): mostra o que as pessoas digitam, mas não tem volume — o volume deve ser puxado no Planejador de Palavras-chave.

### Ferramentas recomendadas

| Ferramenta | Mede | Custo | Uso no projeto | Prioridade |
|---|---|---|---|---|
| Google Search Console | Consultas reais que já trazem impressões e cliques ao site da Techmeter | Gratuito | Fonte nº 1: mostra termos que a Techmeter já disputa | P1 |
| Planejador de Palavras-chave (Google Ads) | Volume mensal estimado por termo, filtro Brasil | Gratuito com conta Ads (faixas amplas sem campanha ativa) | Volume dos termos da lista abaixo | P1 |
| Bing Webmaster Tools — Keyword Research | Volume de busca no Bing por país | Gratuito | Volume no Bing (base do Copilot) | P1 |
| Bing Webmaster Tools — AI Performance | Citações de páginas do site no Copilot e resumos de IA do Bing, com as "grounding queries" que levaram à citação | Gratuito | Único dado oficial de citação em IA disponível hoje (análise) | P1 |
| Google Trends | Interesse relativo ao longo do tempo e por estado | Gratuito | Sazonalidade e comparação entre termos (ex.: eletromagnético × ultrassônico) | P2 |
| Semrush ou Ahrefs (base Brasil) | Volume, dificuldade, concorrentes, perguntas relacionadas | Pago | Mapear termos em que concorrentes ranqueiam e a Techmeter não | P2 — avaliar teste gratuito |
| Ferramentas de monitoramento de IA (ex.: Semrush AI Toolkit, Ahrefs Brand Radar, Otterly, Peec AI) | Menções da marca em respostas de IA para prompts definidos | Pago | Automatizar o baseline no futuro; dados são estimativas | P3 — só após o baseline manual |

O Search Console não separa hoje o tráfego de AI Overviews/AI Mode do restante da busca (HIPÓTESE a reconfirmar na configuração), por isso o baseline manual continua necessário para o Google.

### Termos pesquisados no Brasil — medidor de vazão eletromagnético

| Termo (como digitado) | Intenção | Oportunidade para a Techmeter |
|---|---|---|
| medidor de vazão eletromagnético | Informacional / comercial | Termo principal do hub |
| medidor eletromagnético de vazão | Informacional / comercial | Variante: usar no texto do hub |
| medidor de vazão magnético | Informacional / comercial | Sinônimo: citar no hub e no FAQ |
| medidor de vazão magnético indutivo | Informacional | Sinônimo técnico: citar no "O que é" |
| sensor de vazão eletromagnético / tubo medidor eletromagnético de vazão | Informacional | Explicar sensor × conversor |
| medidor de vazão eletromagnético funcionamento | Informacional | Seção "Como funciona" (prompt 1) |
| como funciona medidor de vazão eletromagnético / medidor de vazão magnético como funciona | Informacional | Idem; bom tema para vídeo |
| medidor de vazão eletromagnético pdf | Informacional | Oferecer guia/datasheet em PDF, com resumo em HTML |
| medidor de vazão eletromagnético de inserção | Seleção | Tipo de sensor: VALIDAR se a Techmeter oferece |
| medidor de vazão eletromagnético tipo carretel / carretel | Seleção | Tipo de sensor: explicar inserção × carretel |
| medidor de vazão eletromagnético a bateria | Seleção | VALIDAR versão bateria (item 9 da seção 9) |
| medidor de vazão eletromagnético dn 25 / dn50 / dn150 / 2" / 6" | Comercial (específico) | Tabela de DN no hub; pesquisa de quem já sabe o que compra |
| medidor de vazão eletromagnético preço | Comercial | CTA de orçamento com dados do processo; não publicar preço sem decisão comercial |
| medidor de vazão eletromagnético para água | Aplicação | Página de saneamento |
| medidor de vazão eletromagnético para esgoto | Aplicação | Página de saneamento/efluentes (prompt 13) |
| medidor de vazão para efluentes / tratamento de efluentes | Aplicação | Idem |
| medidor de vazão outorga | Aplicação | Página de irrigação/outorga (prompt 15) |
| medidor de vazão eletromagnético + marca (Conaut, Siemens, Endress+Hauser, ifm, Yokogawa, Rosemount/Emerson, Incontrol) | Comercial (concorrente) | Concorrentes que o mercado já associa ao termo; usar na análise GEO, não em conteúdo |

Termos para excluir (anunciantes e análise): "medidor eletromagnético fantasma", "app", "K2" e "medidor de campo eletromagnético" são buscas de detectores de campo/caça-fantasmas, não de vazão. Devem entrar como palavras-chave negativas nas campanhas do Google Ads.

Termos vizinhos no autocompletar de "medidor de vazão": ultrassônico (inclusive portátil), água, coriolis, ar, ar comprimido e vortex — confirmam as pautas de comparação (prompts 9 e 10) e os próximos clusters.

### Próximo passo

- Colar esta lista no Planejador de Palavras-chave (local: Brasil, idioma: português) e registrar volume e concorrência — Felippe (P1)
- Exportar as consultas dos últimos 16 meses do Search Console que contenham "vazão", "eletromagnético" ou "magnético" — Felippe (P1)
- Cadastrar o site no Bing Webmaster Tools (importando do Search Console) e ativar o relatório AI Performance — Felippe (P1)
- Revisar a lista final e escolher o termo principal do hub — Mariana (P1)

Método: autocompletar do Google (hl=pt-BR, gl=br) e do Bing (mercado pt-BR), consultado em 30/09/2026 com as sementes "medidor de vazão eletromagnético", "medidor eletromagnético", "medidor de vazão", "medidor de vazão magnético", "como funciona medidor de vazão" e variações. O autocompletar muda com o tempo e com o histórico do usuário.

### Perguntas do usuário priorizadas (⭐)

| Pri. | Pergunta do usuário | Intenção |
|---|---|---|
| ⭐⭐⭐ | Qual medidor de vazão usar para líquidos com sólidos em suspensão? | Escolha |
| ⭐⭐⭐ | Qual medidor de vazão é indicado para efluentes? | Escolha |
| ⭐⭐⭐ | Qual medidor usar para produtos químicos corrosivos? | Escolha |
| ⭐⭐⭐ | Qual medidor de vazão não causa perda de carga? | Escolha |
| ⭐⭐⭐ | Qual medidor de vazão não possui partes móveis? | Escolha |
| ⭐⭐⭐ | Eletromagnético ou ultrassônico: qual é melhor? | Comparação |
| ⭐⭐⭐ | Quando devo usar um medidor de vazão eletromagnético? | Escolha |
| ⭐⭐⭐ | Quando não devo usar um medidor eletromagnético? | Escolha |
| ⭐⭐⭐ | Medidor eletromagnético pode medir água com sólidos? | Aplicação |
| ⭐⭐⭐ | Medidor eletromagnético pode medir esgoto? | Aplicação |
| ⭐⭐⭐ | Medidor eletromagnético pode medir produtos químicos? | Aplicação |
| ⭐⭐⭐ | Como escolher um medidor de vazão eletromagnético? | Compra |
| ⭐⭐ | Qual a condutividade mínima para usar um eletromagnético? | Especificação |
| ⭐⭐ | Água desmineralizada pode ser medida por eletromagnético? | Aplicação |
| ⭐⭐ | Medidor eletromagnético mede óleo? | Aplicação |
| ⭐⭐ | Medidor eletromagnético mede gases ou vapor? | Aplicação |
| ⭐⭐ | Como escolher o revestimento do medidor eletromagnético? | Especificação |
| ⭐⭐ | Como escolher o material dos eletrodos? | Especificação |
| ⭐⭐ | PTFE ou borracha: qual revestimento escolher? | Comparação |
| ⭐⭐ | Qual medidor usar para fluido corrosivo com particulados? | Problema real |
| ⭐⭐ | O medidor eletromagnético precisa de trecho reto? | Instalação |
| ⭐⭐ | O tubo precisa estar totalmente cheio? | Instalação |
| ⭐⭐ | Como instalar corretamente um medidor eletromagnético? | Instalação |
| ⭐⭐ | Como dimensionar o diâmetro do medidor? | Dimensionamento |
| ⭐⭐ | Qual a precisão de um medidor eletromagnético? | Especificação |
| ⭐ | Por que um medidor eletromagnético pode apresentar leitura errada? | Diagnóstico |
| ⭐ | É necessário aterramento? | Instalação |
| ⭐ | Medidor eletromagnético precisa de calibração? | Manutenção |
| ⭐ | Com que frequência deve ser calibrado? | Manutenção |
| ⭐ | Qual a vida útil de um medidor eletromagnético? | Compra/manutenção |

### Top 10: o que a Techmeter precisa responder

| # | Pergunta prioritária | O que a Techmeter precisa responder | Destino |
|---|---|---|---|
| 1 | Qual medidor de vazão usar para líquidos com sólidos em suspensão? | Eletromagnético pode ser uma ótima opção quando o líquido é condutivo; sólidos em suspensão não impedem necessariamente a medição. Seleção de revestimento/eletrodos deve considerar abrasividade e processo. (Endress+Hauser) | Página + FAQ + artigo |
| 2 | Qual medidor de vazão usar para efluentes? | Eletromagnéticos são amplamente aplicáveis a água e efluentes condutivos, inclusive com sólidos, respeitando as condições do processo. (Techmeter) | Landing + artigo |
| 3 | Qual medidor usar para produtos químicos corrosivos? | Não basta escolher “eletromagnético”: é necessário analisar compatibilidade química do revestimento e dos eletrodos. | FAQ + artigo técnico |
| 4 | Qual medidor de vazão não causa perda de carga? | Como o eletromagnético possui passagem livre, sem elemento mecânico obstruindo o fluxo, a perda de carga gerada pelo instrumento é praticamente nula. (Techmeter) | FAQ + comparativo |
| 5 | Qual medidor de vazão não possui partes móveis? | Eletromagnéticos são uma das tecnologias sem partes móveis no caminho do fluido, reduzindo desgaste mecânico e necessidade de manutenção associada a essas partes. (Endress+Hauser) | FAQ + post |
| 6 | Medidor eletromagnético ou ultrassônico: qual escolher? | A resposta deve depender do processo: condutividade, necessidade de instalação não invasiva, diâmetro, fluido, precisão, custo e condições de instalação. | Artigo comparativo + vídeo |
| 7 | Quando usar um medidor de vazão eletromagnético? | Quando há líquido condutivo e busca-se medição contínua, passagem plena, ausência de partes móveis e baixa perda de carga. | Página principal |
| 8 | Quando NÃO usar um medidor eletromagnético? | Gases, vapor e líquidos com condutividade inferior ao limite do equipamento não são aplicações adequadas. (Techmeter) | FAQ + artigo |
| 9 | Medidor eletromagnético pode medir esgoto ou água com sólidos? | Sim, dependendo da condutividade e das características do processo. Aplicações com lodos, polpas e suspensões são comuns para essa tecnologia. (Endress+Hauser) | FAQ + case/aplicação |
| 10 | Como escolher um medidor de vazão eletromagnético? | Fluido, condutividade, vazão, diâmetro, pressão, temperatura, revestimento, eletrodos, conexão, sinal/automação e condições de instalação precisam entrar na especificação. | Guia principal / conteúdo pilar |
