import redis
from haystack.nodes.base import BaseComponent


class MemoryRecallNode(BaseComponent):
    def __init__(self, memory: list):
        super(MemoryRecallNode, self).__init__()
        self.memory = memory

    outgoing_edges = 1

    def run(
            self,
            **kwargs
    ):
        return f"{self.memory}"

    def run_batch(
            self,
            query: str = None,
            **kwargs
    ):
        pass


class RedisMemoryRecallNode(BaseComponent):
    """
    Memory implementation using Redis to be used as a Tool in a haystack Agent
    """

    def __init__(self,
                 memory_id: str,
                 host: str = "localhost",
                 port: int = 6379,
                 db: int = 0,
                 window_size: int = 10,
                 **kwargs):
        """
        :param memory_id: ID of the unique memory to be used
        :param host: Redis Host
        :param port: Redis Port
        :param db:  Redis DB
        :param window_size: Sliding window size to return the last N items. This is done to avoid too large messages
        :param kwargs: Additional kwargs to be passed to redis.StrictRedis
        """
        super(RedisMemoryRecallNode, self).__init__()
        self.window_size = window_size
        self.redis = redis.StrictRedis(host=host,
                                       port=port,
                                       db=db,
                                       decode_responses=True,
                                       **kwargs)
        self.memory_id = memory_id

    outgoing_edges = 1

    def run(
            self,
            **kwargs
    ):
        if self.redis.llen(self.memory_id) == 0:
            return {"results": "No memory found"}, "output_1"
        memory = self.redis.lrange(self.memory_id, self.window_size * -1, -1)
        memory_string = ",".join(memory)
        return {"results": memory_string}, "output_1"

    def run_batch(self,
                  **kwargs):
        return NotImplementedError("Batch mode not implemented for RedisMemoryRecallNode")
