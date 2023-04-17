# Haystack Memory

Memory for [haystack](https://github.com/deepset-ai/haystack) Agents. Currently, the memory for agents can be used in-memory or using redis. The latter supports a sliding window.

## Installation

- Python pip: ```pip install --upgrade haystack-memory``` . This method will attempt to install the dependencies (farm-haystack>=1.15.0, redis)
- Python pip (skip dependency installation): Use  ```pip install --upgrade haystack-memory --no-deps```
- Using git: ```pip install git+https://github.com/rolandtannous/HaystackAgentBasicMemory.git@main#egg=HaystackAgentBasicMemory```


## Usage

To use memory in your agent, you need two components:
- `MemoryRecallNode`: This node is added to the agent as a tool. It will allow the agent to remember the conversation and make query-memory associations.
- `MemoryUtils`: This class should be used to save the queries and the final agent answers to the conversation memory.
- `chat`: This is a method of the MemoryUtils class. It is used to chat with the agent. It will save the query and the answer to the memory. It also returns the full result and the updated conversation memory for further usage.

```py
from haystack.agents import Agent, Tool
from haystack.nodes import PromptNode
from haystack_memory.prompt_templates import memory_template
from haystack_memory.memory import MemoryRecallNode
from haystack_memory.utils import MemoryUtils

# Initialize the memory and the memory tool so the agent can retrieve the memory
memory_database = []
memory_node = MemoryRecallNode(memory=memory_database)
memory_tool = Tool(name="Memory",
                   pipeline_or_node=memory_node,
                   description="Your memory. Always access this tool first to remember what you have learned.")

prompt_node = PromptNode(model_name_or_path="text-davinci-003", 
                         api_key="<YOUR_OPENAI_KEY>", 
                         max_length=1024,
                         stop_words=["Observation:"])
memory_agent = Agent(prompt_node=prompt_node, prompt_template=memory_template)
memory_agent.add_tool(memory_tool)

# Initialize the utils to save the query and the answers to the memory
memory_utils = MemoryUtils(memory_database=memory_database, agent=memory_agent)
result, conversation_memory = memory_utils.chat("<Your Question>")
```

### Redis

The memory can also be stored in a redis database which makes it possible to use different memories at the same time to be used with multiple agents. Additionally, it supports a sliding window to only utilize the last messages.

```py
from haystack.agents import Agent, Tool
from haystack.nodes import PromptNode
from haystack_memory.memory import RedisMemoryRecallNode
from haystack_memory.prompt_templates import memory_template
from haystack_memory.utils import RedisUtils

# Initialize the memory and the memory tool so the agent can retrieve the memory
redis_memory_node = RedisMemoryRecallNode(memory_id="agent_memory",
                                          host="localhost",
                                          port=6379,
                                          db=0)
memory_tool = Tool(name="Memory",
                   pipeline_or_node=redis_memory_node,
                   description="Your memory. Always access this tool first to remember what you have learned.")
prompt_node = PromptNode(model_name_or_path="text-davinci-003",
                         api_key="<YOUR_OPENAI_KEY>",
                         max_length=1024,
                         stop_words=["Observation:"])
memory_agent = Agent(prompt_node=prompt_node, prompt_template=memory_template)
# Initialize the utils to save the query and the answers to the memory
redis_utils = RedisUtils(agent=memory_agent,
                         memory_id="agent_memory",
                         host="localhost",
                         port=6379,
                         db=0)
result, conversation_memory = redis_utils.chat("<Your Question>")
```


## Examples

Examples can be found in the `examples/` folder. It contains the usage for all memory types.
To open the examples in colab, click on the following links:
- Basic Memory: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rolandtannous/HaystackAgentBasicMemory/blob/main/examples/example_basic_memory.ipynb)
- Redis Memory: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rolandtannous/HaystackAgentBasicMemory/blob/main/examples/example_redis_memory.ipynb)







