# GEO Baseline — marco zero

Base de **50 perguntas estratégicas** que representam dúvidas reais do mercado, testadas nas IAs para medir a presença da Techmeter.
O mesmo conjunto é repetido em **30, 60 e 90 dias**, mantendo o histórico para comparação.

## Arquivos

- [`prompts.csv`](prompts.csv): os 50 prompts. Colunas: `id`, `territorio`, `cluster`, `intencao`, `prompt` e `origem` (`Notion` = exemplo da Mariana, `sugestão` = rascunho para revisar).
- [`registro.csv`](registro.csv): uma linha por **prompt × plataforma × rodada**.

> A base atual é um **rascunho**. Antes de rodar o D0, revisar com a Mariana e, se possível, com vendas e suporte: as melhores perguntas vêm de dúvidas reais de clientes (e-mails, WhatsApp, orçamentos).
> Depois do D0, **não alterar o texto dos prompts**. Prompt novo recebe ID novo, para a comparação continuar válida.

Distribuição atual: 30 de Vazão (20 de Eletromagnético, o piloto), 7 de Nível, 5 de Hidrômetros, 4 de Serviços e 4 de Aplicações.

## Plataformas (sugestão, confirmar com Mariana)

| Plataforma | Onde testar |
|---|---|
| ChatGPT | chatgpt.com, com busca na web ativa |
| Google AI | Visão geral de IA (AI Overviews) e Modo IA na busca do Google |
| Gemini | gemini.google.com |
| Copilot | copilot.microsoft.com |
| Perplexity *(opcional)* | perplexity.ai, que mostra as fontes de forma explícita |

## Regras para o teste ser comparável

1. Use **janela anônima**, deslogado ou numa conta sem histórico, com memória e personalização desativadas.
2. Abra uma **conversa nova para cada prompt**. Não faça pergunta de acompanhamento.
3. Cole o prompt **exatamente** como está em `prompts.csv`.
4. Mantenha idioma pt-BR e localização Brasil sempre iguais.
5. Registre tudo no mesmo dia, ou no máximo na mesma semana, para cada rodada.
6. Se possível, salve um print da resposta em `baseline/prints/<rodada>/<id>-<plataforma>.png`.

## Como preencher `registro.csv`

| Coluna | Como preencher |
|---|---|
| `data` | AAAA-MM-DD |
| `rodada` | `D0`, `D30`, `D60` ou `D90` |
| `prompt_id` | ID do `prompts.csv` (ex.: `EM-03`) |
| `prompt` | Texto do prompt, copiado |
| `plataforma` | `ChatGPT`, `Google AI`, `Gemini`, `Copilot` ou `Perplexity` |
| `techmeter_apareceu` | `Sim` ou `Não` (menção à marca **ou** link para techmeter.com.br) |
| `concorrentes_ou_fontes_citadas` | Marcas e sites citados, separados por `;` (ex.: `Empresa X; site-y.com.br`) |
| `pagina_techmeter_encontrada` | URL da página Techmeter citada, se houver |
| `tipo_intencao` | `educacional`, `comparação`, `seleção`, `aplicação` ou `comercial` |
| `observacoes` | Lacunas e oportunidades (ex.: "resposta cita trecho reto 5D/3D, não temos essa informação no site") |

> Dica: importe o `registro.csv` no Google Sheets para preencher e depois exporte de volta como CSV para o repositório.

## AI Citation Share

```
AI Citation Share = prompts em que a Techmeter aparece ÷ total de prompts monitorados
```

Para calcular automaticamente, por rodada e por plataforma:

```bash
python3 projetos/geo/ferramentas/citation_share.py projetos/geo/baseline/registro.csv
```

Um prompt conta como "apareceu" em uma rodada quando a Techmeter aparece em **pelo menos uma** plataforma. O script também mostra o resultado de cada plataforma separado e as fontes mais citadas.
