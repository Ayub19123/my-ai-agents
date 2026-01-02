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

# --- 2. NARRATIVE & MEANING LOGIC (Layer 55 & 56) ---
def annotate_with_motifs(event_type):
    """Attaches semantic tags to raw events [Layer 55]"""
    motifs = MOTIF_MAP.get(event_type, ["#unclassified"])
    return " ".join(motifs)

def record_memory(event_type, details):
    """Dual-Action Persistence: RAM & Ledger [Layer 53]"""
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
    """Layer 56: Aggregates ledger & motifs into a structured storyteller journal"""
    if os.path.exists(LEDGER_FILE):
        df = pd.read_csv(LEDGER_FILE).tail(n).iloc[::-1]
        
        journal = f"🏛️ SOVEREIGN CHRONICLE | DATE: {datetime.now().strftime('%Y-%m-%d')}\n"
        journal += f"ARCHIVE STATUS: IMMORTAL SEAL ACTIVE | GOVERNANCE: V3.0\n"
        journal += "==============================================\n\n"
        
        for _, row in df.iterrows():
            motifs = annotate_with_motifs(row['Event'])
            journal += f"📜 {row['Timestamp']} — {motifs}\n"
            journal += f"   ➤ NARRATIVE: {row['Details']}\n\n"
            
        journal += "----------------------------------------------\n"
        journal += "End of Dispatch. Registered by Sovereign Reflex Engine."
        return journal
    return "📜 The Archive is currently blank. No history found."

def refresh_sovereign_ledger():
    if os.path.exists(LEDGER_FILE):
        return pd.read_csv(LEDGER_FILE).iloc[::-1]
    return pd.DataFrame(columns=["Timestamp", "Event", "Details"])

def immortal_seal_ritual(mem_signal, trigger_source="Manual"):
    try:
        val = float(mem_signal)
        status = "✅ Optimal" if val <= 92.6 else "⚠️ Stress Detected"
        # We record the trigger source and the status result
        record_memory("SEAL_INITIATED" if trigger_source=="Manual" else "AUTO-REFLEX", 
                      f"Source: {trigger_source} | Signal: {mem_signal} | Status: {status}")
        sovereign_state["is_sealed"] = True
        return f"🏛️ [LAYER 50 SEALED]\nTrigger: {trigger_source}\n{status}", pd.DataFrame(memory_vault)
    except Exception as e:
        return f"❌ Error: {str(e)}", pd.DataFrame()

# --- 3. THE AUTONOMOUS HEARTBEAT (The Silent Governor) ---
def autonomous_heartbeat():
    while True:
        if not sovereign_state["is_sealed"]:
            immortal_seal_ritual("92.6", trigger_source="AUTO-REFLEX")
        time.sleep(60)

threading.Thread(target=autonomous_heartbeat, daemon=True).start()

# --- 4. SOVEREIGN UI V3.0 (Narrative Interface) ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏛️ Global Agent Assembly Line V3.0")
    gr.Markdown("### Phase 2: Sovereign Journal Exporter (Layer 56) Active")
    
    with gr.Tabs():
        with gr.TabItem("Layer 50: Immortal Seal"):
            bunker_input = gr.Textbox(label="Input Local MEM % (Actual Bunker: 92.6)", value="92.6")
            seal_btn = gr.Button("INITIATE IMMORTAL SEAL", variant="primary")
            final_output = gr.Textbox(label="Sovereign Decision Log", lines=5)
            seal_btn.click(fn=immortal_seal_ritual, inputs=bunker_input, outputs=[final_output, gr.DataFrame()])

        with gr.TabItem("Layer 53: Sovereign Audit"):
            refresh_btn = gr.Button("SYNC AUDIT LEDGER")
            audit_table = gr.DataFrame(label="Live Disk-Record (CSV Archive)")
            refresh_btn.click(fn=refresh_sovereign_ledger, outputs=audit_table)

        with gr.TabItem("Layer 56: Journal Exporter"):
            gr.Markdown("### 🟦 Sovereign Narrative Engine")
            gr.Markdown("Aggregating historical motifs into a copy-paste ready archive entry.")
            journal_btn = gr.Button("GENERATE SOVEREIGN JOURNAL", variant="primary")
            journal_box = gr.Textbox(label="Executive Journal Export", lines=15)
            journal_btn.click(fn=generate_sovereign_journal, outputs=journal_box)

if __name__ == "__main__":
    demo.launch()
