# Fluxo de trabalho com Git

## Branches

- `main` — versão estável/oficial. Não se faz commit direto nela.
- Branches de trabalho, a partir da `main`:
  - `feat/<descricao>` — nova funcionalidade ou conteúdo
  - `fix/<descricao>` — correção
  - `docs/<descricao>` — documentação
  - `chore/<descricao>` — manutenção, organização

## Commits

Padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/), em português:

```
<tipo>: <resumo curto no imperativo>
```

Tipos: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `style`.

Exemplos:

```
docs: adiciona apresentação da empresa
feat: cria página inicial do site
fix: corrige link quebrado no README
```

## Pull Requests

1. Crie a branch, faça os commits e dê push.
2. Abra um PR para a `main` usando o template.
3. Revise e faça o merge (preferencialmente *squash*).
4. Atualize o `CHANGELOG.md` se a mudança for relevante.
