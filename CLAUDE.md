# Contexto para o Claude

Este repositório é da **Techmeter**. O Claude atua como assistente dedicado da empresa.

## Regras

- Idioma: **português (pt-BR)** em documentação, commits e PRs.
- Sempre que aprender algo novo sobre a empresa, atualizar `docs/empresa.md`.
- Ao concluir/criar tarefas, atualizar `docs/tarefas.md`.
- Decisões relevantes (tecnologia, processo, negócio) vão em `docs/decisoes.md`.
- Mudanças notáveis entram no `CHANGELOG.md` (seção "Não lançado").
- Se a estrutura de pastas mudar, atualizar a árvore no `README.md`.
- Seguir o fluxo de Git descrito em `CONTRIBUTING.md`.
- Não inventar informações sobre a empresa: o que não foi informado fica como `_a definir_`.

## Manuais, catálogos e materiais técnicos (regra de consulta)

Antes de criar ou editar qualquer manual, catálogo ou folheto técnico:

1. **Consulte o modelo** em `modelos/manual-tecnico/` (leia o `README.md`) e gere com `gerar.py`. Não crie layout novo do zero.
2. **Referência visual:** manual LATM 2025 (Canva): fundo azul-claro com ondas, faixas azuis nos títulos, Lato e Montserrat, rodapé K&K do Brasil + logo.
3. **Texto sempre próprio.** Material de fornecedor (por exemplo, Indflow) serve só como **fonte de dados técnicos**: bornes, faixas, menus, registradores. Reescreva com estrutura e palavras da Techmeter. Nunca copie trechos nem só troque o logo.
4. **Nada de inventar dado técnico.** O que não estiver confirmado leva `<span class="validar">VALIDAR: …</span>`. Avise o usuário e não entregue versão final com pendências.
5. **Remova referências ao fornecedor** (nome, site, aplicativo, logomarca no display) ou marque como VALIDAR.
6. **Imagens:** foto do produto sem fundo, em `imagens/`. Imagens de `midia/simulacoes-internas/` só entram com confirmação do usuário.
7. **Dados da empresa** vêm de `docs/empresa.md` e de `EMPRESA` em `gerar.py`. Mantenha os dois iguais.
8. Ao terminar, registre o manual na tabela do `modelos/manual-tecnico/README.md` e no `CHANGELOG.md`.

