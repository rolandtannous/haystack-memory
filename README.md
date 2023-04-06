# haystack-basic-memory

POC Basic memory for [haystack](https://github.com/deepset-ai/haystack) Agents.
This first version is a basic implementation that uses a python list which only persists for the duration of the current session but expires immediately thereafter.</br>
The memory design will be upgraded to persist across sessions in later versions.


## Installation

- Python pip: ```python3 -m pip install``` . This package will attempt to install the dependencies (farm-haystack>=1.15.0)
- Python pip (skip dependency installation: Use  ```python3 -m pip install --no-deps```
- Using git: ```pip install git+https://github.com/rolandtannous/HaystackAgentBasicMemory.git@main#egg=HaystackAgentBasicMemory```


## Usage

To use memory in your agent, you need two parts:
- `MemoryRecallNode`: This node is passed to the agent to be used as a tool. It will be passed to the agent to let it remember the conversation.
- `MemoryUtils`: This class has to be used to save the query and the answers to the memory.

```py
from haystack.agents import Agent, Tool
from haystack.nodes import PromptNode
from HaystackMemory.prompt_templates import memory_template
from HaystackMemory.memory import MemoryRecallNode
from HaystackMemory.utils import MemoryUtils

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
memory_utils.chat("<Your Question>")
```

### Redis

The memory can also be stored in a redis database which makes it possible to use different memories at the same time to be used with multiple agents. Additionally, it supports a sliding window to only utilize the last messages.

```py
from haystack.agents import Agent, Tool
from haystack.nodes import PromptNode
from HaystackMemory.memory import RedisMemoryRecallNode
from HaystackMemory.prompt_templates import memory_template
from HaystackMemory.utils import RedisUtils

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
redis_utils.chat("<Your Question>")
```


## Examples

### Python script example
A working example file ```example.py``` is included with this repository. 
The example illustrates how to activate and use this basic agent memory using the seven wonders dataset, an ElasticSearch Document Store, and two tools: a Generative QA pipeline and the MemoryRecall Tool. The example also contains the adjusted prompt necessary to make the Agent access the memory looking for potential answers.</br>
The Generative QA pipeline uses OpenAI's `text-embedding-ada-002` as a retriever model, and `text-davinci-003` as a generative model.

An example `PromptTemplate` used for the `Agent` can be imported from `HaystackMemory/prompt_templates`

### Jupyter notebook/ google colab example
A notebook version of the example file code is also included in the repository 
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rolandtannous/HaystackAgentBasicMemory/blob/main/Example.ipynb)

## Credits
Credits to [Stefano Fiorruci](https://github.com/anakin87) whose chatgpt implementation example was the basis of our basic memory template. 







