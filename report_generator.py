import os
import time
from google import genai

def generate_clinical_summary(reps, min_angle, max_angle, avg_angle):
    api_key = os.environ.get("GEMINI_API_KEY", "")
    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an expert orthopedic kinematic analyst.
    Evaluate the following movement capture telemetry:
    - Exercise: Lower Limb Knee Flexion / Squat Kinematics
    - Valid Repetitions: {reps}
    - Minimum Joint Flexion Angle: {min_angle:.1f} degrees (Target <= 95 deg)
    - Maximum Extension Angle: {max_angle:.1f} degrees
    - Mean Planar Angle: {avg_angle:.1f} degrees

    Generate a concise clinical rehabilitation evaluation (under 130 words) formatted as:
    1. Biomechanical Range of Motion Assessment
    2. Depth & Symmetry Evaluation
    3. Actionable Kinematic Corrections

    Tone: Rigorous, clinical, data-driven. Do NOT use the words 'AI', 'Artificial Intelligence', or 'LLM'.
    """

    # Cycle through available candidate models if one experiences high demand
    models_to_try = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-3.8-flash"]

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            print("\n" + "=" * 55)
            print(" REHABOPTICS: AUTOMATED CLINICAL REPORT")
            print("=" * 55)
            print(response.text)
            print("=" * 55 + "\n")
            return
        except Exception as e:
            print(f"[Notice] {model_name} busy or unavailable. Trying alternative engine...")
            time.sleep(1)

    # Deterministic local fallback so your demo never fails on camera
    print("\n" + "=" * 55)
    print(" REHABOPTICS: AUTOMATED CLINICAL REPORT (LOCAL TELEMETRY)")
    print("=" * 55)
    print(f"1. Biomechanical ROM: Recorded min angle of {min_angle:.1f}° and max angle of {max_angle:.1f}° across {reps} counted repetitions.")
    depth_eval = "Satisfactory eccentric range achieved below target 95° threshold." if min_angle <= 95 else "Sub-optimal depth; joint flexion restricted above 95° threshold."
    print(f"2. Depth & Symmetry: {depth_eval}")
    print("3. Kinematic Corrections: Focus on controlled eccentric pacing and stabilizing the knee-ankle vector throughout the turnaround phase.")
    print("=" * 55 + "\n")
