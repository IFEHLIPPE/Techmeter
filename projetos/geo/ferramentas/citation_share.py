#!/usr/bin/env python3
"""Calcula o AI Citation Share a partir do registro do baseline GEO.

Uso:
    python3 citation_share.py ../baseline/registro.csv
"""
import csv
import sys
from collections import Counter, defaultdict


def sim(valor):
    return valor.strip().lower() in ("sim", "s", "yes", "y", "1")


def main(caminho):
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        linhas = [l for l in csv.DictReader(f) if l.get("prompt_id")]
    if not linhas:
        print("Registro vazio: nenhum teste registrado ainda.")
        return

    por_rodada = defaultdict(lambda: defaultdict(bool))
    por_plataforma = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    fontes = defaultdict(Counter)

    for l in linhas:
        rodada, pid, plat = l["rodada"].strip(), l["prompt_id"].strip(), l["plataforma"].strip()
        apareceu = sim(l["techmeter_apareceu"])
        por_rodada[rodada][pid] |= apareceu
        por_plataforma[rodada][plat][0] += apareceu
        por_plataforma[rodada][plat][1] += 1
        for fonte in l.get("concorrentes_ou_fontes_citadas", "").split(";"):
            if fonte.strip():
                fontes[rodada][fonte.strip()] += 1

    for rodada in sorted(por_rodada, key=lambda r: int(r.lstrip("Dd") or 0)):
        prompts = por_rodada[rodada]
        n, total = sum(prompts.values()), len(prompts)
        print(f"\n=== {rodada} ===")
        print(f"AI Citation Share: {n}/{total} prompts = {n / total:.0%}")
        for plat, (a, t) in sorted(por_plataforma[rodada].items()):
            print(f"  {plat:<12} {a}/{t} = {a / t:.0%}")
        if fontes[rodada]:
            print("  Fontes/concorrentes mais citados:")
            for fonte, qtd in fontes[rodada].most_common(10):
                print(f"    {qtd:>3}x {fonte}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
