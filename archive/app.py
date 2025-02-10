from praisonaiagents import Agent, Agents, Tools
import os
#os.environ["OPENAI_BASE_URL"] = "http://localhost:11434/v1/"



research_agent = Agent(instructions="You are a research agent to search internet about AI 2024", tools=[Tools.internet_search])
summarise_agent = Agent(instructions="You are a summarize agent to summarise in points")
agents = Agents(agents=[research_agent, summarise_agent])
agents.start()
