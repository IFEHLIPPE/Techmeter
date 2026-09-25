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
└── .github/
    └── pull_request_template.md
```

Novos projetos/códigos entram em pastas próprias na raiz (ex.: `site/`, `app/`, `scripts/`) e são listados aqui.

## Como trabalhamos

- Tarefas ficam em [`docs/tarefas.md`](docs/tarefas.md) (ou em Issues do GitHub).
- Toda mudança vai por branch + Pull Request — ver [`CONTRIBUTING.md`](CONTRIBUTING.md).
- Mudanças relevantes são registradas no [`CHANGELOG.md`](CHANGELOG.md).
