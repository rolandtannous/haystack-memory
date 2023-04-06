# haystack-basic-memory

POC Basic memory for [haystack](https://github.com/deepset-ai/haystack) Agents.
This first version is a basic implementation that uses a python list which only persists for the duration of the current session but expires immediately thereafter.</br>
The memory design will be upgraded to persist across sessions in later versions.


## Installation

- Python pip: ```python3 -m pip install``` . This package will attempt to install the dependencies (farm-haystack>=1.15.0)
- Python pip (skip dependency installation: Use  ```python3 -m pip install --no-deps```
- Using git: ```pip install git+https://github.com/rolandtannous/HaystackAgentBasicMemory.git@main#egg=HaystackAgentBasicMemory```


## Usage

The memory is meant to be used with a Haystack agent and is made of two main components:
- MemoryRecallNode tool: To access this method do </br>```from HaystackAgentBasicMemory.MemoryRecallNode import MemoryRecallNode```</br> The method should be initialized with the python list variable that will serve as memory buffer like this:</br> ```memory_node = MemoryRecallNode(memory=memory_database)``` and then defined as and added as an agent tool using the Agent ```Tool``` and  ```add_tool``` methods. The agent's prompt text should also be adjusted n a way such that the agent is instructed/prompted to always check in the Memory first by calling this tool.
- SaveToMemory method: This method is called in the agent chat wrapper method which is also part of the package. This method will append the final answer given by the Agent to the chat memory buffer.

A very simple example of this is:

```
from haystack.agents import Agent, Tool
from haystack.nodes import PromptTemplate, PromptNode
from HaystackAgentBasicMemory.MemoryRecallNode import MemoryRecallNode

memory_database = []
memory_node = MemoryRecallNode(memory_database)
memory_tool = Tool(name="Memory",
                   pipeline_or_node=memory_node,
                   description="Your memory. Always access this tool first to remember what you have learned.")


prompt_node = PromptNode(model_name_or_path="text-davinci-003", api_key=YOUR_OPENAI_KEY, max_length=512, stop_words=["Observation:"])
memory_agent = Agent(prompt_node=prompt_node, prompt_template=AN_AGENT_PROMPT_TEMPLATE)
memory_agent.add_tool(memory_tool)
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







