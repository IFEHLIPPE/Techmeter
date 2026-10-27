# Mídia

Fotos e imagens da Techmeter usadas no site, nas redes e nos materiais comerciais.

## Estrutura

```
midia/
└── fotos-produtos/
    └── AAAA-MM-DD-<descricao>/
        ├── original/                    # foto como foi tirada
        ├── <nome>-sem-fundo.png         # recorte com fundo transparente
        └── <nome>-fundo-branco.jpg      # fundo branco com sombra suave (site/catálogo)
```

## Como as fotos são tratadas

- Recorte automático do fundo com IA (rembg, modelo BiRefNet).
- Ajuste leve de contraste, cor e nitidez.
- Ampliação 2x e enquadramento quadrado com margem.

> Ampliar não recupera detalhe que a foto não tem. Para resultado de catálogo, o ideal é fotografar com o celular na **resolução máxima**, com boa luz e enviar o **arquivo original** (não pelo WhatsApp, que comprime).
