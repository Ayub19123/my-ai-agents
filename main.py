#!/usr/bin/env python3
"""
main.py - CrewAI example with .env support, tracing toggle, and output saving
"""
import os
import sys
import logging
import json
from dotenv import load_dotenv

load_dotenv()
os.environ.pop("OPENAI_API_KEY", None)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TRACING_ENV = os.getenv("CREWAI_TRACING_ENABLED", "false").lower()
CREW_TRACING = TRACING_ENV in ("1", "true", "yes", "on")

if not GEMINI_API_KEY:
    sys.stderr.write(
        "ERROR: GEMINI_API_KEY environment variable is not set.\n"
        "Please create a .env file (see .env.example) or set GEMINI_API_KEY in your environment.\n"
    )
    sys.exit(2)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("my-ai-agents")

try:
    from crewai import Agent, Task, Crew, LLM
except Exception:
    logger.error("Failed to import crewai. Install requirements: pip install -r requirements.txt")
    raise

gemini_llm = LLM(
    model="gemini/gemini-2.5-flash-lite",
    api_key=GEMINI_API_KEY,
    temperature=0.7,
)

researcher = Agent(
    role="Senior Research Analyst",
    goal="Identify the 3 most critical breakthroughs in the Dec 17, 2025 OpenUSD 1.0 release",
    backstory="You are a tech scout for industrial digitalization and 3D standards.",
    verbose=True,
    llm=gemini_llm,
    allow_delegation=False,
)

writer = Agent(
    role="Tech Content Strategist",
    goal="Write a viral LinkedIn post about OpenUSD 1.0 becoming the 'HTML of the 3D Web'",
    backstory="You specialize in turning technical milestones into industry-leading social content.",
    verbose=True,
    llm=gemini_llm,
    allow_delegation=False,
)

task1 = Task(
    description=(
        "Summarize the impact of the newly ratified OpenUSD Core Spec 1.0. "
        "Focus on how it ends data fragmentation for digital twins."
    ),
    expected_output="A 3-point summary of the 1.0 release and its impact on NVIDIA Omniverse users.",
    agent=researcher,
)

task2 = Task(
    description=(
        "Draft a high-engagement LinkedIn post. Explain that OpenUSD is now a production-ready open standard "
        "for the global 3D economy. Use #OpenUSD1 #NVIDIA #DigitalTwins."
    ),
    expected_output="A viral LinkedIn post with emojis and technical authority.",
    agent=writer,
)


def main():
    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        verbose=True,
        memory=False,
        tracing=CREW_TRACING,
    )

    logger.info("🚀 MISSION START: Researching the December 2025 OpenUSD 1.0 Milestone...")
    try:
        result = crew.kickoff()
    except Exception as exc:
        logger.exception("Crew kickoff failed: %s", exc)
        raise

    # Normalize result to string for saving/printing
    if isinstance(result, (bytes, dict, list)):
        try:
            result_str = json.dumps(result, indent=2, ensure_ascii=False)
        except Exception:
            result_str = str(result)
    else:
        result_str = str(result)

    print("\n\n########################")
    print("## YOUR LINKEDIN POST ##")
    print("########################\n")
    print(result_str)

    # Save output
    out_dir = "outputs"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "linkedin_post.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result_str)
    logger.info("Saved LinkedIn post to: %s", out_path)


if __name__ == "__main__":
    main()