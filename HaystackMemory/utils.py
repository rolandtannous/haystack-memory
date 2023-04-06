import redis
from haystack.agents.base import Agent


def chat(query: str, main_agent: Agent, memory_database: list):
    result = main_agent.run(query)
    save_to_memory(result, memory_database)


def save_to_memory(result: dict, memory_database: list):
    memory_database.append(result["query"])
    memory_database.append(result["answers"][0].answer)


class RedisUtils:
    def __init__(self,
                 agent: Agent,
                 memory_id: str,
                 host: str = "localhost",
                 port: int = 6379,
                 db: int = 0,
                 **kwargs):
        self.agent = agent
        self.redis = redis.StrictRedis(host=host, port=port, db=db, **kwargs)
        self.memory_id = memory_id

    def __save_to_memory(self,
                         result: dict):
        self.redis.rpush(self.memory_id, result["query"])
        self.redis.rpush(self.memory_id, result["answers"][0].answer)

    def chat(self,
             query: str):
        result = self.agent.run(query)
        self.__save_to_memory(result)
