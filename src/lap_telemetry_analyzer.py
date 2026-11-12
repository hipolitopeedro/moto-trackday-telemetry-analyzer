#!/usr/bin/env python3
"""
lap_telemetry_analyzer.py
EN: Analyzes motorcycle trackday telemetry logs (CSV) to compute lap times, deltas,
    top speeds, corner apex speeds, peak braking G, and maximum lean angles.
PT: Analisa logs de telemetria de trackday de moto (CSV) para calcular tempos de volta,
    deltas, velocidade máxima, velocidade de apex, frenagem máxima (G) e ângulo de inclinação.
"""

import argparse
import csv
from collections import defaultdict
from typing import Dict, List


def format_lap_time(seconds: float) -> str:
    """Formats seconds into MM:SS.mmm."""
    minutes = int(seconds // 60)
    rem_seconds = seconds - (minutes * 60)
    return f"{minutes:02d}:{rem_seconds:06.3f}"


def analyze_session(csv_path: str) -> None:
    laps: Dict[int, List[Dict[str, float]]] = defaultdict(list)

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lap_num = int(row["lap"])
            laps[lap_num].append(
                {
                    "time_s": float(row["lap_time_s"]),
                    "speed_kmh": float(row["speed_kmh"]),
                    "rpm": float(row["rpm"]),
                    "tps_pct": float(row["tps_pct"]),
                    "brake_bar": float(row["brake_bar"]),
                    "lon_g": float(row["lon_g"]),
                    "lean_deg": float(row["lean_deg"]),
                }
            )

    if not laps:
        print("[WARN] No telemetry records found in CSV.")
        return

    lap_summaries = []
    for lap_num, samples in sorted(laps.items()):
        lap_duration = max(s["time_s"] for s in samples)
        top_speed = max(s["speed_kmh"] for s in samples)
        min_apex_speed = min(s["speed_kmh"] for s in samples)
        max_rpm = max(s["rpm"] for s in samples)
        max_lean_left = abs(min(s["lean_deg"] for s in samples))
        max_lean_right = max(s["lean_deg"] for s in samples)
        max_lean = max(max_lean_left, max_lean_right)
        max_braking_g = abs(min(s["lon_g"] for s in samples))
        full_throttle_pct = (
            sum(1 for s in samples if s["tps_pct"] >= 95.0) / len(samples)
        ) * 100.0

        lap_summaries.append(
            {
                "lap": lap_num,
                "duration": lap_duration,
                "top_speed": top_speed,
                "min_apex": min_apex_speed,
                "max_rpm": max_rpm,
                "max_lean": max_lean,
                "max_lean_l": max_lean_left,
                "max_lean_r": max_lean_right,
                "max_brake_g": max_braking_g,
                "wot_pct": full_throttle_pct,
            }
        )

    best_lap = min(lap_summaries, key=lambda x: x["duration"])
    best_time = best_lap["duration"]

    print("=" * 92)
    print("  MOTORCYCLE TRACKDAY TELEMETRY SESSION ANALYSIS")
    print("=" * 92)

    for s in lap_summaries:
        delta = s["duration"] - best_time
        delta_str = "BEST LAP" if delta == 0.0 else f"+{delta:0.3f}s"
        print(
            f"  Lap {s['lap']:<2} : {format_lap_time(s['duration'])} ({delta_str:<8}) | "
            f"Top: {s['top_speed']:>5.1f} km/h | Apex: {s['min_apex']:>4.1f} km/h | "
            f"Lean: {s['max_lean']:>4.1f} deg (L:{s['max_lean_l']:>4.1f}/R:{s['max_lean_r']:>4.1f}) | "
            f"Brake: {s['max_brake_g']:>4.2f}G"
        )

    print("-" * 92)
    print(
        f"  [FASTEST LAP] Lap {best_lap['lap']} -> {format_lap_time(best_time)} | "
        f"Peak RPM: {int(best_lap['max_rpm'])} | WOT (Full Throttle) Ratio: {best_lap['wot_pct']:.1f}%"
    )
    print("=" * 92)


def main() -> None:
    parser = argparse.ArgumentParser(description="Motorcycle Trackday Telemetry CSV Analyzer")
    parser.add_argument(
        "--log",
        default="data/sample_trackday_session.csv",
        help="Path to telemetry CSV file",
    )
    args = parser.parse_args()
    analyze_session(args.log)


if __name__ == "__main__":
    main()
