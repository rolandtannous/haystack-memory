from typing import List
import redis
from haystack.agents.base import Agent


class MemoryUtils:
    def __init__(self,
                 agent: Agent,
                 working_memory: List[str],
                 sensory_memory: List[str]):
        self.working_memory = working_memory
        self.sensory_memory = sensory_memory
        self.agent = agent

    def __save_to_working_memory(self, result: dict):
        self.working_memory.append(result["query"])
        self.__transfer_sensory_memory()
        self.working_memory.append(result["answers"][0].answer)

    def __transfer_sensory_memory(self):
        if self.sensory_memory:
            for i in self.sensory_memory:
                self.working_memory.append(i)

    def __initialize_sensory_memory(self):
        self.sensory_memory.clear()

    def chat(self, query: str):
        result = self.agent.run(query)
        self.__save_to_working_memory(result)
        self.__initialize_sensory_memory()
        return result


class RedisUtils:
    def __init__(self,
                 agent: Agent,
                 sensory_memory: List[str],
                 memory_id: str,
                 host: str = "localhost",
                 port: int = 6379,
                 db: int = 0,
                 expiration: int = 3600,
                 **kwargs):
        """
        :param agent: Agent which will be used to run the queries. Make sure that the agent has a RedisMemoryRecallNode
        :param memory_id: ID of the memory to be used. Has to be the same ID as the one used in the RedisMemoryRecallNode
        :param host: Redis host
        :param port: Redis port
        :param db:  Redis db
        :param expiration: Expiration time of the memory in seconds
        :param kwargs: kwargs to be passed to redis.StrictRedis
        """
        self.agent = agent
        self.expiration = expiration
        self.__expiration_is_set = False
        self.redis = redis.StrictRedis(host=host,
                                       port=port,
                                       db=db,
                                       **kwargs)
        self.memory_id = memory_id
        self.sensory_memory = sensory_memory

    def __transfer_sensory_memory(self, result: dict):
        if not self.__expiration_is_set:
            self.redis.expire(self.memory_id, self.expiration)
            self.__expiration_is_set = True
        if self.sensory_memory:
            for i in self.sensory_memory:
                self.redis.rpush(self.memory_id, result["query"])

    def __initialize_sensory_memory(self):
        self.sensory_memory.clear()

    def __save_to_working_memory(self,
                                 result: dict):
        """
        Internal function to store the initial query and the answer of the agent to the memory
        :param result: Transcript of the agent
        """
        if not self.__expiration_is_set:
            self.redis.expire(self.memory_id, self.expiration)
            self.__expiration_is_set = True
        self.redis.rpush(self.memory_id, result["query"])
        self.__transfer_sensory_memory(result)
        self.redis.rpush(self.memory_id, result["answers"][0].answer)

    def chat(self,
             query: str):
        """
        Function to run a query with the given agent. Stores the results in the memory
        :param query: Query to run with the agent
        """
        result = self.agent.run(query)
        self.__save_to_working_memory(result)
        self.__initialize_sensory_memory()
        return result
