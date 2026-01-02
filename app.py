import gradio as gr
import pandas as pd
import threading
import time
import os
from datetime import datetime

# --- 1. CONFIG & MOTIF DICTIONARY ---
LEDGER_FILE = "Sovereign_Ledger.csv"
MOTIF_MAP = {
    "AUTO-REFLEX": ["#autonomy", "#reflexloop", "#selfgoverning"],
    "SEAL_INITIATED": ["#activation", "#sovereignmoment", "#finality"],
    "Pulse": ["#heartbeat", "#persistence", "#monitoring"],
    "STRESS_DETECTED": ["#resilience", "#load", "#pressureevent"],
    "GUARDIAN_ALERT": ["#selfhealing", "#auditloop", "#stabilitywatch"]
}

memory_vault = []
sovereign_state = {"is_sealed": False, "logs": "", "df": pd.DataFrame()}

# --- 2. LOGIC ENGINES (Layers 53-57) ---
def annotate_with_motifs(event_type):
    motifs = MOTIF_MAP.get(event_type, ["#unclassified"])
    return " ".join(motifs)

def record_memory(event_type, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"Timestamp": timestamp, "Event": event_type, "Details": details}
    memory_vault.append(entry)
    ledger_df = pd.DataFrame([entry])
    if not os.path.isfile(LEDGER_FILE):
        ledger_df.to_csv(LEDGER_FILE, index=False)
    else:
        ledger_df.to_csv(LEDGER_FILE, mode='a', header=False, index=False)
    return pd.DataFrame(memory_vault)

def generate_sovereign_journal(n=10):
    """Layer 56: Executive Narrative summary"""
    if os.path.exists(LEDGER_FILE):
        df = pd.read_csv(LEDGER_FILE).tail(n).iloc[::-1]
        journal = f"🏛️ SOVEREIGN CHRONICLE | {datetime.now().strftime('%Y-%m-%d')}\n"
        journal += "==============================================\n\n"
        for _, row in df.iterrows():
            motifs = annotate_with_motifs(row['Event'])
            journal += f"📜 {row['Timestamp']} — {motifs}\n"
            journal += f"   ➤ NARRATIVE: {row['Details']}\n\n"
        return journal
    return "Archive Empty."

def generate_sovereign_timeline():
    """Layer 57: Visual Temporal Sequence Mapper"""
    if os.path.exists(LEDGER_FILE):
        df = pd.read_csv(LEDGER_FILE).iloc[::-1] # Newest First
        timeline_html = "<div style='height: 450px; overflow-y: scroll; border: 1px solid #333; padding: 20px; border-radius: 12px; background-color: #1a1a1a;'>"
        for _, row in df.iterrows():
            motifs = annotate_with_motifs(row['Event'])
            color = "#00ff88" if "Optimal" in str(row['Details']) else "#00d4ff"
            timeline_html += f"""
            <div style='margin-bottom: 25px; padding-left: 20px; border-left: 3px solid {color};'>
                <div style='color: #666; font-size: 0.85em; font-family: monospace;'>[{row['Timestamp']}]</div>
                <div style='color: {color}; font-weight: bold; font-size: 1.1em;'>{row['Event']} <span style='color: #555; font-weight: normal;'>{motifs}</span></div>
                <div style='color: #ddd; margin-top: 5px; font-size: 0.95em;'>{row['Details']}</div>
            </div>
            """
        timeline_html += "</div>"
        return timeline_html
    return "⌛ Timeline waiting for anchor data."

def refresh_sovereign_ledger():
    if os.path.exists(LEDGER_FILE):
        return pd.read_csv(LEDGER_FILE).iloc[::-1]
    return pd.DataFrame(columns=["Timestamp", "Event", "Details"])

def immortal_seal_ritual(mem_signal, trigger_source="Manual"):
    try:
        val = float(mem_signal)
        status = "✅ Optimal" if val <= 92.6 else "⚠️ Stress Detected"
        record_memory("SEAL_INITIATED" if trigger_source=="Manual" else "AUTO-REFLEX", 
                      f"Source: {trigger_source} | Signal: {mem_signal} | Status: {status}")
        sovereign_state["is_sealed"] = True
        return f"🏛️ [LAYER 50 SEALED]\nTrigger: {trigger_source}\n{status}", pd.DataFrame(memory_vault)
    except Exception as e:
        return f"❌ Error: {str(e)}", pd.DataFrame()

# --- 3. THE AUTONOMOUS HEARTBEAT ---
def autonomous_heartbeat():
    while True:
        if not sovereign_state["is_sealed"]:
            immortal_seal_ritual("92.6", trigger_source="AUTO-REFLEX")
        time.sleep(60)

threading.Thread(target=autonomous_heartbeat, daemon=True).start()

# --- 4. SOVEREIGN UI V4.0 ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏛️ Global Agent Assembly Line V4.0")
    gr.Markdown("### Phase 2: Temporal Sovereignty (Layer 57) Active")
    
    with gr.Tabs():
        with gr.TabItem("Layer 50: Immortal Seal"):
            bunker_input = gr.Textbox(label="Input Local MEM %", value="92.6")
            seal_btn = gr.Button("INITIATE IMMORTAL SEAL", variant="primary")
            final_output = gr.Textbox(label="Sovereign Decision Log", lines=5)
            seal_btn.click(fn=immortal_seal_ritual, inputs=bunker_input, outputs=[final_output, gr.DataFrame()])

        with gr.TabItem("Layer 53: Audit"):
            refresh_btn = gr.Button("SYNC AUDIT LEDGER")
            audit_table = gr.DataFrame(label="CSV Archive")
            refresh_btn.click(fn=refresh_sovereign_ledger, outputs=audit_table)

        with gr.TabItem("Layer 56: Journal"):
            journal_btn = gr.Button("GENERATE SOVEREIGN JOURNAL", variant="primary")
            journal_box = gr.Textbox(label="Narrative Export", lines=10)
            journal_btn.click(fn=generate_sovereign_journal, outputs=journal_box)

        with gr.TabItem("Layer 57: Timeline"):
            gr.Markdown("### 🟥 Sovereign Temporal View")
            timeline_btn = gr.Button("REFRESH TIMELINE VIEW", variant="primary")
            timeline_display = gr.HTML(label="Visual History")
            timeline_btn.click(fn=generate_sovereign_timeline, outputs=timeline_display)

if __name__ == "__main__":
    demo.launch()
