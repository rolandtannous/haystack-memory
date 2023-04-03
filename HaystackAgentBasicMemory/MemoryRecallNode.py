from haystack.nodes.base import BaseComponent


class MemoryRecallNode(BaseComponent):
    def __init__(self, memory: list):
        super(MemoryRecallNode, self).__init__()
        self.memory = memory
    outgoing_edges = 1

    def run(
        self,
        query: [str] = None,
        **kwargs
    ):
        return f"{self.memory}"

    def run_batch(
        self,
        query: str = None,
        **kwargs
    ):
        pass



