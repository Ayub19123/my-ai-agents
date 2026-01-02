import pandas as pd
import os
import re

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
        # Adjust column names if your CSV already has headers
        df = pd.read_csv(LEDGER_FILE, header=None, names=["timestamp", "event", "details"])

        if df.empty:
            return "Ledger is empty. No behavior to analyze yet."

        # Parse timestamps if possible
        try:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
        except Exception:
            pass  # If parse fails, still continue with basic analysis

        # Extract signal values (where present)
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
        auto_reflex_events = df[df["event"] == "AUTO-REFLEX"]
        manual_seal_events = df[df["event"] == "MANUAL_SEAL"]
        seal_initiated_events = df[df["event"] == "SEAL_INITIATED"]

        if not auto_reflex_events.empty or not seal_initiated_events.empty or not manual_seal_events.empty:
            lines.append("2) Reflex and seal relationship:")
            if not auto_reflex_events.empty:
                avg_signal = auto_reflex_events["signal_value"].dropna().mean()
                if pd.notna(avg_signal):
                    lines.append(f"   • AUTO-REFLEX events detected with average signal ≈ {avg_signal:.1f}")
                else:
                    lines.append("   • AUTO-REFLEX events detected (signal not consistently parsed).")
            if not seal_initiated_events.empty:
                lines.append(f"   • SEAL_INITIATED events present ({len(seal_initiated_events)}).")
            if not manual_seal_events.empty:
                lines.append(f"   • MANUAL_SEAL events present ({len(manual_seal_events)}).")
            lines.append("")
        else:
            lines.append("2) Reflex and seal relationship:")
            lines.append("   • No reflex or seal events detected yet.")
            lines.append("")

        # 3) Stability motifs (based on your details text)
        persistence_events = df[df["details"].str.contains("#persistence", case=False, na=False)]
        if not persistence_events.empty:
            lines.append("3) Stability and persistence:")
            lines.append(f"   • {len(persistence_events)} persistence-related milestone(s) recorded.")
            lines.append("   • System demonstrates uptime awareness and milestone tracking.")
            lines.append("")
        else:
            lines.append("3) Stability and persistence:")
            lines.append("   • No explicit persistence milestones detected yet.")
            lines.append("")

        # 4) Temporal evolution
        if "timestamp" in df.columns:
            try:
                df_sorted = df.sort_values("timestamp")
                first_ts = df_sorted["timestamp"].iloc[0]
                last_ts = df_sorted["timestamp"].iloc[-1]
                lines.append("4) Temporal evolution:")
                lines.append(f"   • Ledger span: {first_ts} → {last_ts}")
                lines.append(f"   • Total recorded events: {len(df_sorted)}")
                lines.append("")
            except Exception:
                pass

        # 5) Founder influence
        if not manual_seal_events.empty:
            lines.append("5) Founder influence:")
            lines.append("   • Manual seal detected: founder explicitly intervened in system state.")
            lines.append("   • System history reflects dual-governance: autonomous reflex + manual authority.")
            lines.append("")
        else:
            lines.append("5) Founder influence:")
            lines.append("   • No manual governance events explicitly recorded yet.")
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        return f"[REFLEX INTELLIGENCE ERROR] Failed to generate insights: {e}"
