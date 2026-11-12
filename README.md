# Motorcycle Trackday Telemetry & Pit-Lane Setup Analyzer

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Telemetry](https://img.shields.io/badge/Motorsport-Telemetry_%26_Physics-E10600?style=for-the-badge)

> **Live Interactive Telemetry & Pit-Lane Dashboard (GitHub Pages):** [https://hipolitopeedro.github.io/moto-trackday-telemetry-analyzer/](https://hipolitopeedro.github.io/moto-trackday-telemetry-analyzer/)
>
> **English:** Personal motorsport engineering project built for **Motorcycle Trackdays**. Includes a GPS/IMU telemetry analyzer (lap times, sector splits, corner apex speeds, braking G-force, and lean angle estimation) and a pit-lane mechanical setup calculator (hot/cold tire pressure thermodynamics, suspension sag validation, and sprocket gearing top-speed simulator).
>
> **Português:** Projeto pessoal voltado para **Trackday de Motos**. Inclui um analisador de telemetria GPS/IMU (tempos de volta, parciais de setor, velocidade mínima de apex, força G de frenagem e estimativa de ângulo de inclinação / *lean angle*) e uma calculadora mecânica de box (compensação térmica de calibragem de pneus a frio/quente, validação de *Sag* de suspensão e simulação de relação coroa/pinhão).

---

## Included Tools / Ferramentas Inclusas

| File | Description (EN) | Descrição (PT-BR) |
| :--- | :--- | :--- |
| [`src/lap_telemetry_analyzer.py`](src/lap_telemetry_analyzer.py) | Parses session telemetry CSV logs (`RPM`, `Speed_kmh`, `Throttle_TPS`, `Brake_Bar`, `Lat_G`, `Lon_G`, `Lean_Angle_Deg`) to compute lap times, fastest lap delta, max lean angles (L/R), and corner apex speeds. | Processa logs CSV de telemetria da sessão para calcular tempos de volta, *delta* para a volta mais rápida, inclinação máxima (esq/dir), zonas de frenagem e velocidades de *apex*. |
| [`src/tire_pressure_suspension_calc.py`](src/tire_pressure_suspension_calc.py) | Pit-lane setup utility: calculates cold-to-hot tire pressure adjustments, evaluates front/rear Suspension Sag (Static & Rider Sag in mm), and simulates final drive gearing changes (sprocket teeth vs. top speed per gear). | Utilitário de acerto de box: calcula ajuste de pressão de pneus (frio vs. quente na manta/pista), avalia o *Sag* da suspensão dianteira/traseira e simula trocas de relação (pinhão/coroa vs. velocidade final por marcha). |
| [`data/sample_trackday_session.csv`](data/sample_trackday_session.csv) | Sample multi-lap motorcycle trackday telemetry dataset for testing and analysis. | Dataset de exemplo com múltiplas voltas de telemetria em trackday para testes. |

---

## Quick Start / Como Executar

### 1. Analyze Trackday Session Telemetry / Analisar Telemetria de Sessão
```bash
python src/lap_telemetry_analyzer.py --log data/sample_trackday_session.csv
```

**Sample Output / Exemplo de Saída:**
```text
==============================================================================
  MOTORCYCLE TRACKDAY TELEMETRY REPORT | Track: Curvelo / Circuito dos Cristais
==============================================================================
  Lap 1 : 01:38.450 (+1.650s) | Top Speed: 238.4 km/h | Max Lean: 51.2 deg | Min Apex: 74.5 km/h
  Lap 2 : 01:36.800 (BEST)    | Top Speed: 243.1 km/h | Max Lean: 54.0 deg | Min Apex: 78.2 km/h
  Lap 3 : 01:37.210 (+0.410s) | Top Speed: 241.8 km/h | Max Lean: 53.4 deg | Min Apex: 76.9 km/h
```

### 2. Pit-Lane Setup Calculator (Tire Pressure, Suspension Sag & Gearing)
```bash
python src/tire_pressure_suspension_calc.py \
    --target-hot-psi-front 33.0 \
    --target-hot-psi-rear 27.0 \
    --ambient-temp-c 24 \
    --hot-tire-temp-c 80 \
    --front-sprocket 15 \
    --rear-sprocket 45 \
    --max-rpm 13500
```
