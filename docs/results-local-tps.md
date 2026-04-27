# Local Model TPS — RTX 3090 (24GB)

Phase H benchmark throughput on NVIDIA RTX 3090, measured across 59 tests.

| Model | Quant | Params | Avg t/s | Min t/s | Max t/s | Score | % |
|-------|-------|--------|---------|---------|---------|-------|---|
| LFM2.5-350M | Q4_K_M | 350M | 628.3 | 178.9 | 712.2 | 308/1220 | 25.2% |
| Gemma-4-E2B | BF16 | 2B | 101.1 | 98.9 | 111.7 | 981/1220 | 80.4% |
| Gemma-4-E4B | BF16 | 4B | 61.8 | 59.7 | 66.0 | 867/1220 | 71.1% |
| Gemma-4-31B | Q4_K_M | 31B | 28.1 | 25.9 | 33.7 | 927/1220 | 76.0% |

> Gemma-4-E2B is the sweet spot: 101 t/s with 80.4% accuracy — beats models 60x its size.
