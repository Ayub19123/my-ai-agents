import pandas as pd
import os
import re
import gradio as gr
from datetime import datetime

LEDGER_FILE = "Sovereign_Ledger.csv"

# --- CORE LOGIC ---
def parse_signal_from_details(details):
    match = re.search(r"Signal:\s*([\d.]+)", str(details))
    return float(match.group(1)) if match else None

def append_to_ledger(event_type, event_details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Ensure header exists on every write
    file_exists = os.path.exists(LEDGER_FILE)
    
    new_data = pd.DataFrame([[timestamp, event_type, event_details]], 
                            columns=["timestamp", "event", "details"])
    
    if not file_exists:
        new_data.to_csv(LEDGER_FILE, index=False)
    else:
        new_data.to_csv(LEDGER_FILE, mode='a', header=False, index=False)
    return f"🟢 Success: Event '{event_type}' anchored at {timestamp}."

def generate_reflex_insights():
    if not os.path.exists(LEDGER_FILE):
        return "No ledger found. Reflex intelligence cannot be generated yet."
    try:
        # SELF-HEALING SCHEMA: Force column names regardless of file header
        df = pd.read_csv(LEDGER_FILE, names=["timestamp", "event", "details"], header=None if pd.read_csv(LEDGER_FILE, nrows=0).columns[0].startswith('202') else 0)
        
        # Standardize for logic
        df.columns = ["timestamp", "event", "details"]
        
        df["signal_value"] = df["details"].apply(parse_signal_from_details)
        
        lines = ["🟫 SOVEREIGN REFLEX INTELLIGENCE REPORT", "--------------------------------------", ""]
        
        # 1) Event distribution
        lines.append("1) Event distribution:")
        for evt, count in df["event"].value_counts().items():
            lines.append(f"   • {evt}: {count} event(s)")
        
        # 2) Dual-Governance
        manual_seals = len(df[df["event"].str.contains("MANUAL_SEAL", na=False)])
        lines.append(f"\n2) Reflex and seal relationship:\n   • MANUAL_SEAL detected ({manual_seals}). Founder hand confirmed.")
        
        # 3) Persistence
        persistence = len(df[df["details"].str.contains("#persistence", case=False, na=False)])
        lines.append(f"\n3) Stability and persistence:\n   • {persistence} milestone(s) recorded.")
        
        # 4) Temporal span
        lines.append(f"\n4) Temporal evolution:\n   • Ledger span: {df['timestamp'].iloc[0]} → {df['timestamp'].iloc[-1]}")
        lines.append(f"   • Total events recorded: {len(df)}")
        
        return "\n".join(lines)
    except Exception as e:
        return f"[ERROR] Logic fracture: {e}"

# --- UI INTERFACE ---
with gr.Blocks(title="Sovereign Command Center V4.2") as demo:
    gr.Markdown("# 🏛️ Global Agent Assembly Line V4.1")
    
    with gr.Tab("Layer 58: Reflex Intelligence"):
        reflex_output = gr.Textbox(label="Cognitive Output", lines=12)
        btn_reflex = gr.Button("🟫 GENERATE REFLEX INSIGHTS")
        btn_reflex.click(generate_reflex_insights, outputs=reflex_output)

    with gr.Tab("Layer 59: Ledger Expansion"):
        gr.Markdown("### ✍️ Anchor New Events to Sovereign Memory")
        with gr.Row():
            event_input = gr.Dropdown(choices=["AUTO-REFLEX", "MANUAL_SEAL", "STRESS_DETECTED", "PERSISTENCE_MILESTONE"], label="Event Type")
            details_input = gr.Textbox(label="Details (e.g., Signal: 95.0 #persistence)", placeholder="Add signal and motifs...")
        btn_append = gr.Button("🖋️ APPEND TO LEDGER")
        status_output = gr.Textbox(label="Expansion Status")
        btn_append.click(append_to_ledger, inputs=[event_input, details_input], outputs=status_output)

demo.launch()
