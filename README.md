# Techmeter

> Repositório central da **Techmeter** — documentação da empresa, tarefas e projetos.

A Techmeter (São Paulo/SP, desde 1991) é especialista em **medição e controle de vazão**: medidores de vazão (eletromagnéticos, vórtex, turbina, rotâmetros), transmissores de nível e serviços de calibração em laboratório próprio. Site: https://www.techmeter.com.br/

⚠️ *Em construção: as informações são complementadas conforme a empresa for apresentada.*

## Sobre a empresa

Ver [`docs/empresa.md`](docs/empresa.md).

## Estrutura do repositório

```
.
├── README.md                 # Visão geral (este arquivo)
├── CLAUDE.md                 # Contexto e regras para o assistente (Claude)
├── CONTRIBUTING.md           # Fluxo de trabalho com Git (branches, commits, PRs)
├── CHANGELOG.md              # Histórico de mudanças relevantes
├── docs/
│   ├── empresa.md            # Quem somos, produtos, clientes, equipe
│   ├── tarefas.md            # Backlog e status das tarefas
│   └── decisoes.md           # Registro de decisões importantes
├── projetos/
│   └── geo/                  # Projeto GEO — Otimização para Mecanismos Generativos
│       ├── README.md         # Plano, frentes, KPIs e cronograma de 90 dias
│       ├── semana-1.md       # Checklist da primeira semana
│       ├── auditoria-tecnica.md
│       ├── baseline/         # 50 prompts + registro dos testes (D0/D30/D60/D90)
│       ├── ferramentas/      # Scripts: auditoria técnica e AI Citation Share
│       └── piloto-eletromagnetico/
└── .github/
    └── pull_request_template.md
```

Cada projeto tem sua pasta em `projetos/`.

## Projetos ativos

| Projeto | Responsáveis | Status |
|---|---|---|
| [GEO — Otimização para Mecanismos Generativos](projetos/geo/README.md) | Mariana (estratégia) · Felippe (operacional) | 🔄 Semana 1 — diagnóstico |

## Como trabalhamos

- Tarefas ficam em [`docs/tarefas.md`](docs/tarefas.md) (ou em Issues do GitHub).
- Toda mudança vai por branch + Pull Request — ver [`CONTRIBUTING.md`](CONTRIBUTING.md).
- Mudanças relevantes são registradas no [`CHANGELOG.md`](CHANGELOG.md).
