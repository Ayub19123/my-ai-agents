import pandas as pd
import os
import re
import gradio as gr

LEDGER_FILE = "Sovereign_Ledger.csv"

def parse_signal_from_details(details):
    match = re.search(r"Signal:\s*([\d.]+)", str(details))
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None

def generate_reflex_insights():
    if not os.path.exists(LEDGER_FILE):
        return "No ledger found. Reflex intelligence cannot be generated yet."

    try:
        # Read CSV normally (your file already has a header)
        df = pd.read_csv(LEDGER_FILE)

        # FORCE column names to match logic (fixes the 'details' KeyError)
        df.columns = ["timestamp", "event", "details"]

        if df.empty:
            return "Ledger is empty. No behavior to analyze yet."

        # Parse timestamps
        try:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
        except Exception:
            pass

        # Extract signal values
        df["signal_value"] = df["details"].apply(parse_signal_from_details)

        lines = []
        lines.append("🟫 SOVEREIGN REFLEX INTELLIGENCE REPORT")
        lines.append("--------------------------------------")
        lines.append("")

        # 1) Event distribution
        lines.append("1) Event distribution:")
        event_counts = df["event"].value_counts()
        for evt, count in event_counts.items():
            lines.append(f"   • {evt}: {count} event(s)")
        lines.append("")

        # 2) Reflex and seal relationship
        auto_reflex_events = df[df["event"].str.contains("AUTO-REFLEX", na=False)]
        manual_seal_events = df[df["event"].str.contains("MANUAL_SEAL", na=False)]

        lines.append("2) Reflex and seal relationship:")
        if not auto_reflex_events.empty:
            avg_signal = auto_reflex_events["signal_value"].dropna().mean()
            if pd.notna(avg_signal):
                lines.append(f"   • AUTO-REFLEX events detected with average signal ≈ {avg_signal:.1f}")
        if not manual_seal_events.empty:
            lines.append(f"   • MANUAL_SEAL events present ({len(manual_seal_events)}). Founder hand confirmed.")
        lines.append("")

        # 3) Stability motifs
        persistence_events = df[df["details"].str.contains("#persistence", case=False, na=False)]
        lines.append("3) Stability and persistence:")
        if not persistence_events.empty:
            lines.append(f"   • {len(persistence_events)} persistence-related milestone(s) recorded.")
            lines.append("   • System demonstrates high uptime awareness.")
        else:
            lines.append("   • No persistence motifs detected.")
        lines.append("")

        # 4) Temporal evolution
        df_sorted = df.sort_values("timestamp")
        first_ts = df_sorted["timestamp"].iloc[0]
        last_ts = df_sorted["timestamp"].iloc[-1]

        lines.append("4) Temporal evolution:")
        lines.append(f"   • Ledger span: {first_ts} → {last_ts}")
        lines.append(f"   • Total events recorded: {len(df_sorted)}")
        lines.append("")

        return "\n".join(lines)

    except Exception as e:
        return f"[REFLEX INTELLIGENCE ERROR] Logic fracture: {e}"

# UI Integration Block
with gr.Blocks(title="Sovereign Command Center V4.1") as demo:
    gr.Markdown("# 🏛️ Global Agent Assembly Line V4.1")
    
    with gr.Tab("Layer 58: Reflex Intelligence"):
        reflex_output = gr.Textbox(label="Cognitive Output", lines=15)
        btn_reflex = gr.Button("🟫 GENERATE REFLEX INSIGHTS")
        btn_reflex.click(generate_reflex_insights, outputs=reflex_output)

demo.launch()
