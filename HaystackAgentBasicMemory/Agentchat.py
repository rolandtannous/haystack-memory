from haystack.agents.base import Agent
from HaystackAgentBasicMemory.SaveToMemory import save_to_memory


def chat(query: str, main_agent: Agent, memory_database: list):
    result = main_agent.run(query)
    save_to_memory(result, memory_database)
    return
