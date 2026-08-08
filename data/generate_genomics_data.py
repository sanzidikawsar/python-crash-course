"""Generate a small synthetic plant-gene FASTA for the session-1 Part-4 taste.

Reproducible (seeded). Writes data/genomics/plant_genes.fasta with six clean
open reading frames — start codon ATG, no in-frame stop until the end — so
Biopython's .translate() gives a tidy protein.

A real biological signal is baked in on purpose: monocot genes (rice, maize,
sorghum) are built GC-rich and dicot genes (Arabidopsis, soybean, tomato)
GC-poor, mirroring the genuine monocot/dicot GC-content difference. The GC bar
chart in the notebook therefore shows something true, which is the charm.
"""

from pathlib import Path

import numpy as np

SEED = 7
OUT = Path(__file__).resolve().parent / "genomics" / "plant_genes.fasta"

# Non-stop codons, split by GC richness (no TAA/TAG/TGA anywhere).
HIGH_GC = ["GCC", "GGC", "CGC", "CCG", "GAG", "CAG", "GCG", "GGG",
           "CCC", "GTG", "CTG", "TCC", "ACC", "AGC"]
LOW_GC = ["AAA", "TTT", "ATA", "AAT", "TTA", "TAT", "ATT", "AAG",
          "AGA", "TCA", "ACA", "CAA", "TTG", "AAC"]

# Approximate GC of the two codon pools, used to hit a realistic target GC by
# mixing them. Real plant CDS: monocots ~58-62% GC, dicots ~42-46%.
GC_HIGH, GC_LOW = 0.81, 0.17

# (id, description, target GC fraction, codon count)
GENES = [
    ("OsWRKY13", "Oryza sativa (rice) WRKY transcription factor", 0.60, 40),
    ("ZmNAC7", "Zea mays (maize) NAC stress factor", 0.62, 46),
    ("SbMYB3", "Sorghum bicolor (sorghum) MYB regulator", 0.58, 34),
    ("AtDREB1A", "Arabidopsis thaliana (thale cress) DREB cold factor", 0.44, 44),
    ("GmbZIP1", "Glycine max (soybean) bZIP factor", 0.42, 38),
    ("SlHSF2", "Solanum lycopersicum (tomato) heat-shock factor", 0.46, 42),
]


def build_orf(rng, target_gc, n_codons):
    p_high = min(max((target_gc - GC_LOW) / (GC_HIGH - GC_LOW), 0.0), 1.0)
    codons = []
    for _ in range(n_codons):
        pool = HIGH_GC if rng.random() < p_high else LOW_GC
        codons.append(rng.choice(pool))
    return "ATG" + "".join(codons) + "TAA"


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    lines = []
    for gene_id, desc, target_gc, n in GENES:
        seq = build_orf(rng, target_gc, n)
        lines.append(f">{gene_id} {desc}")
        lines.append(seq)
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT} ({len(GENES)} sequences)")


if __name__ == "__main__":
    main()
