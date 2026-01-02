import os
import re
from datetime import datetime

import pandas as pd
import gradio as gr

LEDGER_FILE = "Sovereign_Ledger.csv"


# ---------- Core Utilities ----------

def ensure_ledger_exists():
    """
    Ensure the ledger file exists with the correct header.
    If it doesn't exist, create it with the standard columns.
    """
    if not os.path.exists(LEDGER_FILE):
        df = pd.DataFrame(columns=["Timestamp", "Event", "Details"])
        df.to_csv(LEDGER_FILE, index=False)


def load_ledger():
    """
    Load the ledger and normalize column names to lowercase
    for internal processing, while preserving data.
    """
    ensure_ledger_exists()
    df = pd.read_csv(LEDGER_FILE)

    # Normalize column names but keep structure
    normalized = {c: c.strip().lower() for c in df.columns}
    df = df.rename(columns=normalized)

    # We expect: timestamp, event, details
    # If something is missing, raise a clear error
    expected_cols = {"timestamp", "event", "details"}
    if not expected_cols.issubset(set(df.columns)):
        raise KeyError(
            f"Ledger schema mismatch. Expected columns: {expected_cols}, "
            f"but found: {set(df.columns)}"
        )

    return df


def append_ledger_event(event_type: str, details: str):
    """
    Append a new event to the ledger with the current timestamp.
    """
    ensure_ledger_exists()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = pd.DataFrame(
        [[timestamp, event_type, details]],
        columns=["Timestamp", "Event", "Details"]
    )

    # Append without rewriting header
    new_row.to_csv(LEDGER_FILE, mode="a", header=False, index=False)

    return timestamp


def parse_signal_from_details(details):
    """
    Extracts numerical signal from strings like 'Signal: 92.6'.
    """
    match = re.search(r"Signal:\s*([\d.]+)", str(details))
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None


# ---------- Layer 58: Reflex Intelligence ----------

def generate_reflex_insights():
    """
    Analyze the ledger and generate a reflex intelligence report.
    """
    if not os.path.exists(LEDGER_FILE):
        return "No ledger found. Reflex intelligence cannot be generated yet."

    try:
        df = load_ledger()

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
                lines.append(
                    f"   • AUTO-REFLEX events detected with average signal ≈ {avg_signal:.1f}"
                )
            else:
                lines.append("   • AUTO-REFLEX events detected (signal not consistently parsed).")
        if not manual_seal_events.empty:
            lines.append(
                f"   • MANUAL_SEAL events present ({len(manual_seal_events)}). "
                f"Founder hand confirmed."
            )
        if auto_reflex_events.empty and manual_seal_events.empty:
            lines.append("   • No reflex or seal events recorded yet.")
        lines.append("")

        # 3) Stability and persistence
        persistence_events = df[df["details"].str.contains("#persistence", case=False, na=False)]
        lines.append("3) Stability and persistence:")
        if not persistence_events.empty:
            lines.append(f"   • {len(persistence_events)} persistence-related milestone(s) recorded.")
            lines.append("   • System demonstrates high uptime awareness.")
        else:
            lines.append("   • No persistence motifs detected.")
        lines.append("")

        # 4) Temporal evolution
        try:
            df_sorted = df.sort_values("timestamp")
            first_ts = df_sorted["timestamp"].iloc[0]
            last_ts = df_sorted["timestamp"].iloc[-1]

            lines.append("4) Temporal evolution:")
            lines.append(f"   • Ledger span: {first_ts} → {last_ts}")
            lines.append(f"   • Total events recorded: {len(df_sorted)}")
            lines.append("")
        except Exception:
            lines.append("4) Temporal evolution:")
            lines.append("   • Timestamps could not be fully parsed.")
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        return f"[REFLEX INTELLIGENCE ERROR] Logic fracture: {e}"


# ---------- Layer 59: Ledger Expansion Engine ----------

def add_ledger_entry(event_type, details):
    """
    Gradio-facing function to append a new entry via UI.
    """
    if not event_type or not details:
        return "Please provide both an event type and details before appending."

    try:
        ts = append_ledger_event(event_type.strip(), details.strip())
        return f"✅ Event appended at {ts} | Type: {event_type.strip()}"
    except Exception as e:
        return f"❌ Failed to append event. Logic fracture: {e}"


def get_quick_template(event_type):
    """
    Optional helper: return a suggested details template based on event type.
    """
    templates = {
        "AUTO-REFLEX": "Signal: 92.6 | Status: Optimal | Motifs: #autonomy #reflexloop #selfgoverning",
        "STRESS_DETECTED": "Pulse: Stress Detected | Internal honesty event",
        "MOTIF_BROADCAST": "Sovereign motif broadcast generated | Meaning Engine Active",
        "JOURNAL_ENGINE": "Layer 56 Activated | Narrative Export Ready",
        "TIMELINE_ENGINE": "Layer 57 Activated | Temporal Sovereignty Confirmed",
        "MANUAL_SEAL": "Layer 50 Sealed Manually | Status: Optimal",
    }
    return templates.get(event_type, "")


def fill_template(selected_event):
    """
    Gradio callback: when a preset event is selected, fill the details box.
    """
    return get_quick_template(selected_event)


# ---------- UI: Global Agent Assembly Line V4.2 ----------

with gr.Blocks(title="Sovereign Command Center V4.2") as demo:
    gr.Markdown("# 🏛️ Global Agent Assembly Line V4.2")
    gr.Markdown("### Layer 58: Reflex Intelligence · Layer 59: Ledger Expansion Engine")

    with gr.Tab("Layer 58: Reflex Intelligence"):
        reflex_output = gr.Textbox(
            label="Cognitive Output",
            lines=20,
            interactive=False
        )
        btn_reflex = gr.Button("🟫 GENERATE REFLEX INSIGHTS")
        btn_reflex.click(generate_reflex_insights, outputs=reflex_output)

    with gr.Tab("Layer 59: Ledger Expansion"):
        gr.Markdown("## 🧾 Ledger Expansion Engine")
        gr.Markdown(
            "Use this panel to append new sovereign events to the ledger. "
            "Every entry becomes a permanent relic."
        )

        preset_event = gr.Dropdown(
            label="Preset Event Type (optional)",
            choices=[
                "AUTO-REFLEX",
                "STRESS_DETECTED",
                "MOTIF_BROADCAST",
                "JOURNAL_ENGINE",
                "TIMELINE_ENGINE",
                "MANUAL_SEAL",
            ],
            value=None,
            interactive=True
        )

        custom_event = gr.Textbox(
            label="Event Type (required, can override preset)",
            placeholder="e.g., AUTO-REFLEX, MANUAL_SEAL, MOTIF_BROADCAST",
        )

        details_box = gr.Textbox(
            label="Details (required)",
            lines=4,
            placeholder="Describe the event, signal, status, motifs, or milestone..."
        )

        fill_btn = gr.Button("📋 Fill Details From Preset")
        append_btn = gr.Button("🧾 Append Event To Ledger")
        status_box = gr.Textbox(
            label="Ledger Status",
            lines=2,
            interactive=False
        )

        # When clicking "Fill Details From Preset", populate details based on preset_event
        fill_btn.click(
            fn=fill_template,
            inputs=[preset_event],
            outputs=[details_box]
        )

        # When appending, prefer custom_event if provided; otherwise use preset_event
        def handle_append(preset_evt, custom_evt, details):
            evt = custom_evt.strip() if custom_evt and custom_evt.strip() else preset_evt
            if not evt:
                return "Please select or enter an event type."
            return add_ledger_entry(evt, details)

        append_btn.click(
            fn=handle_append,
            inputs=[preset_event, custom_event, details_box],
            outputs=[status_box]
        )

demo.launch()
