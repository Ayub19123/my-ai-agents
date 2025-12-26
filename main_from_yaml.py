import os
import yaml
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# Load secrets from your .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Load Agent Definitions
with open('agents.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize the Professional LLM
def create_llm(model_name):
    return LLM(model=model_name, api_key=GEMINI_API_KEY, temperature=0.7)

# Build Agents from YAML
researcher = Agent(config=config['researcher'], llm=create_llm(config['researcher']['model']))
writer = Agent(config=config['writer'], llm=create_llm(config['writer']['model']))

# Define the 2025 Tasks
task1 = Task(
    description="Summarize the Dec 17, 2025 OpenUSD 1.0 breakthroughs.",
    expected_output="A 3-point summary of the 1.0 release for NVIDIA users.",
    agent=researcher
)
task2 = Task(
    description="Draft a viral LinkedIn post. Use #OpenUSD1 #NVIDIA #DigitalTwins.",
    expected_output="A high-engagement LinkedIn post with emojis.",
    agent=writer
)

# Launch
crew = Crew(agents=[researcher, writer], tasks=[task1, task2], verbose=True)
print("\n🚀 PRO MISSION START: Running YAML-driven Crew...")
result = crew.kickoff()
print("\n########################\n", result)