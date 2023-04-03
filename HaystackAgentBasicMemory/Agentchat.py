from haystack.agents.base import  Agent
from HaystackAgentBasicMemory.SaveToMemory import SaveToMemory


def chat(input: str, Mainagent: Agent, memory_database: list):
    result = Mainagent.run(input)
    SaveToMemory(result, memory_database)
    return