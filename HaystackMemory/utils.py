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

    def __save_to_memory(self,
                         result: dict):
        """
        Internal function to store the initial query and the answer of the agent to the memory
        :param result: Transcript of the agent
        """
        if not self.__expiration_is_set:
            self.redis.expire(self.memory_id, self.expiration)
            self.__expiration_is_set = True
        self.redis.rpush(self.memory_id, result["query"])
        self.redis.rpush(self.memory_id, result["answers"][0].answer)

    def chat(self,
             query: str):
        """
        Function to run a query with the given agent. Stores the results in the memory
        :param query: Query to run with the agent
        """
        result = self.agent.run(query)
        self.__save_to_memory(result)
