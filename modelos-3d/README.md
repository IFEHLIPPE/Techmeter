# Modelos 3D

Modelos 3D interativos de produtos Techmeter, feitos para abrir no navegador.

| Modelo | Arquivo | O que faz |
|---|---|---|
| Medidor de vazão eletromagnético TM-EL (DN50, conversor integrado) | `medidor-eletromagnetico/configurador.html` | Gira, aproxima e troca a cor do **cabeçote**, das **tampas** e da **base** (sensor, flanges e pescoço) |

## Como é feito

- Um único arquivo HTML com three.js (carregado da internet, via cdnjs). Precisa de conexão para abrir.
- O modelo é desenhado por código, a partir de fotos do equipamento. As proporções são aproximadas: **não usar como desenho dimensional**.
- Etiquetas, plaqueta e display são desenhados no próprio arquivo, com os dados da unidade fotografada (TM-EL-500, DN50, 316L, borracha, IP65).
- Para acrescentar cores ou combinações, edite as listas `CORES` e `COMBOS` no início do script.
