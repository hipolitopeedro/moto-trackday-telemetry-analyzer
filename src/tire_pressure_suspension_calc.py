#!/usr/bin/env python3
"""
tire_pressure_suspension_calc.py
EN: Pit-lane engineering tool for motorcycle trackdays:
    1. Cold-to-Hot tire pressure calculator (Gay-Lussac's thermodynamic law).
    2. Suspension Sag evaluator (Static Sag & Rider Sag in mm).
    3. Final drive sprocket gearing & theoretical top speed calculator.
PT: Ferramenta de engenharia de pista para trackday de motos:
    1. Cálculo termodinâmico de pressão de pneus (frio vs. quente).
    2. Avaliação de Sag de suspensão (Estático e com Piloto em mm).
    3. Simulador de relação (pinhão/coroa) e velocidade máxima teórica.
"""

import argparse
import math

ATM_PSI = 14.696


def calculate_cold_tire_pressure(target_hot_psi: float, ambient_c: float, hot_tire_c: float) -> float:
    """
    Uses Gay-Lussac's Law on absolute pressures: P_cold_abs = P_hot_abs * (T_cold_K / T_hot_K)
    """
    t_cold_k = ambient_c + 273.15
    t_hot_k = hot_tire_c + 273.15
    p_hot_abs = target_hot_psi + ATM_PSI
    p_cold_abs = p_hot_abs * (t_cold_k / t_hot_k)
    return round(p_cold_abs - ATM_PSI, 1)


def evaluate_suspension_sag(free_mm: float, static_mm: float, rider_mm: float, end: str) -> str:
    """
    Calculates Static Sag and Rider Sag from unloaded (free) measurement.
    Trackday typical targets:
      Front Fork : Static 20-25mm | Rider 30-35mm
      Rear Shock : Static 8-12mm  | Rider 25-30mm
    """
    static_sag = free_mm - static_mm
    rider_sag = free_mm - rider_mm

    if end.lower() == "front":
        ideal_range = (28.0, 36.0)
    else:
        ideal_range = (24.0, 32.0)

    if rider_sag < ideal_range[0]:
        advice = "TOO STIFF (Reduce preload or softer spring)"
    elif rider_sag > ideal_range[1]:
        advice = "TOO SOFT (Increase preload or stiffer spring)"
    else:
        advice = "OPTIMAL TRACKDAY BASELINE"

    return f"Static Sag: {static_sag:.1f} mm | Rider Sag: {rider_sag:.1f} mm -> [{advice}]"


def calculate_top_speed_kmh(
    max_rpm: int,
    primary_ratio: float,
    sixth_gear_ratio: float,
    front_sprocket: int,
    rear_sprocket: int,
    tire_width_mm: int = 180,
    tire_aspect_pct: int = 55,
    wheel_inches: int = 17,
) -> float:
    """Calculates theoretical top speed in 6th gear based on sprocket ratio and rear tire size."""
    final_drive_ratio = rear_sprocket / front_sprocket
    overall_ratio = primary_ratio * sixth_gear_ratio * final_drive_ratio

    sidewall_mm = tire_width_mm * (tire_aspect_pct / 100.0)
    wheel_diameter_mm = (wheel_inches * 25.4) + (2.0 * sidewall_mm)
    circumference_m = (math.pi * wheel_diameter_mm) / 1000.0

    wheel_rpm = max_rpm / overall_ratio
    speed_m_per_min = wheel_rpm * circumference_m
    return round((speed_m_per_min * 60.0) / 1000.0, 1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Motorcycle Trackday Pit-Lane Setup Calculator")
    parser.add_argument("--target-hot-psi-front", type=float, default=33.0, help="Target hot front PSI")
    parser.add_argument("--target-hot-psi-rear", type=float, default=27.0, help="Target hot rear PSI")
    parser.add_argument("--ambient-temp-c", type=float, default=24.0, help="Ambient pit temperature (C)")
    parser.add_argument("--hot-tire-temp-c", type=float, default=80.0, help="Operating tire temperature (C)")
    parser.add_argument("--front-sprocket", type=int, default=15, help="Front countershaft sprocket teeth")
    parser.add_argument("--rear-sprocket", type=int, default=44, help="Rear wheel sprocket teeth")
    parser.add_argument("--max-rpm", type=int, default=14000, help="Engine redline RPM")
    args = parser.parse_args()

    cold_front = calculate_cold_tire_pressure(
        args.target_hot_psi_front, args.ambient_temp_c, args.hot_tire_temp_c
    )
    cold_rear = calculate_cold_tire_pressure(
        args.target_hot_psi_rear, args.ambient_temp_c, args.hot_tire_temp_c
    )

    print("==========================================================================")
    print("  MOTORCYCLE TRACKDAY PIT-LANE SETUP CALCULATOR")
    print("==========================================================================")
    print("\n[1] TIRE PRESSURE COMPENSATION (COLD TO HOT)")
    print(f"    Ambient Temp: {args.ambient_temp_c:.1f} C | Expected Track Tire Temp: {args.hot_tire_temp_c:.1f} C")
    print(f"    Front Tire  : Target Hot = {args.target_hot_psi_front:.1f} PSI -> Set Cold at {cold_front:.1f} PSI")
    print(f"    Rear Tire   : Target Hot = {args.target_hot_psi_rear:.1f} PSI -> Set Cold at {cold_rear:.1f} PSI")

    print("\n[2] SUSPENSION SAG REFERENCE CHECK")
    print("    Front Fork  : " + evaluate_suspension_sag(120.0, 97.0, 87.0, "front"))
    print("    Rear Shock  : " + evaluate_suspension_sag(550.0, 540.0, 522.0, "rear"))

    print("\n[3] FINAL DRIVE SPROCKET GEARING & TOP SPEED SIMULATOR")
    ratio = round(args.rear_sprocket / args.front_sprocket, 2)
    top_speed = calculate_top_speed_kmh(
        max_rpm=args.max_rpm,
        primary_ratio=1.65,
        sixth_gear_ratio=1.15,
        front_sprocket=args.front_sprocket,
        rear_sprocket=args.rear_sprocket,
    )
    print(f"    Sprockets   : {args.front_sprocket}T Front / {args.rear_sprocket}T Rear (Ratio: {ratio})")
    print(f"    Redline     : {args.max_rpm} RPM -> Theoretical 6th Gear Top Speed: {top_speed} km/h")
    print("==========================================================================")


if __name__ == "__main__":
    main()
