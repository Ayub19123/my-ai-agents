from emotion_signal_monitor import EmotionSignalMonitor
from emotion_response_engine import EmotionResponseEngine
from global_emotion_loop import GlobalEmotionLoop

# NEW: Import Economic & Legacy Layers
from market_signal_monitor import MarketSignalMonitor
from capital_strategy_engine import CapitalStrategyEngine
from global_economic_loop import GlobalEconomicLoop
from global_legacy_loop import GlobalLegacyLoop
from legacy_seal_ritual import LegacySeal

# --- 1. EMOTION BAND (Layer 37) ---
monitor = EmotionSignalMonitor()
responder = EmotionResponseEngine()
emo_loop = GlobalEmotionLoop(monitor, responder)

message = {
    "text": "I'm a bit frustrated but hopeful.",
    "agent_id": "demo_agent",
    "channel": "cli"
}

emo_result = emo_loop.run(message)
print(f"🧠 Emotion Signal: {emo_result}")

# --- 2. ECONOMIC BAND (Layer 39) ---
# Analyzing market signals and generating capital strategy
market_monitor = MarketSignalMonitor()
strategy_engine = CapitalStrategyEngine()
econ_loop = GlobalEconomicLoop(market_monitor, strategy_engine)

market_data = {
    "symbol": "SOVEREIGN_ALPHA",
    "price": 100,
    "slope": 0.12,
    "volatility": 0.35,
    "macro_signal": "bullish"
}

econ_result = econ_loop.run(market_data)
print(f"💰 Economic Strategy: {econ_result}")

# --- 3. LEGACY BAND (Layer 40) ---
# Archiving this specific moment in the civilization's history
legacy_loop = GlobalLegacyLoop()
legacy_loop.run()

# PERFORM THE FINAL SEAL
seal_ritual = LegacySeal()
seal_ritual.seal()