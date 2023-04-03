import os
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import OpenAIAnswerGenerator
from haystack.nodes import EmbeddingRetriever
from haystack.pipelines import GenerativeQAPipeline
from haystack.agents import Agent, Tool
from HaystackAgentBasicMemory.MemoryRecallNode import MemoryRecallNode
from HaystackAgentBasicMemory.Agentchat import chat
from haystack.pipelines import Pipeline
from haystack.nodes import PromptTemplate, PromptNode
from datasets import load_dataset
# import logging
#
# logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
# logging.getLogger("haystack").setLevel(logging.INFO)

openai_api_key = "<your_open_ai_key>"

# define a simple list variable to hold our memory
# memory_database = []
memory_database = []
# full_transcript = []
# from haystack.utils import launch_es
# launch_es()

# Get the host where Elasticsearch is running, default to localhost
host = os.environ.get("ELASTICSEARCH_HOST", "localhost")

# creating elastic search document store
document_store = ElasticsearchDocumentStore(
    host=host,
    username="",
    password="",
    index="document-small-test",
    search_fields=["title", "text"],
    embedding_field="embedding",
    excluded_meta_data=["embedding"],
    embedding_dim=1536)


# loading dataset several wonders of the world dataset
# dataset = load_dataset("bilgeyucel/seven-wonders", split="train")

#writing dataset content to elastic search document store index
# document_store.write_documents(dataset)

# defining embeddings Retriever as openAi text-embedding-ada-002
retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="text-embedding-ada-002",
    api_key=openai_api_key,
    top_k=3,
)
# updating vector embeddings in document store index using Retriever
# document_store.update_embeddings(retriever=retriever)

# define generator node using OpenAIAnswerGenerator haystack node and text-davinci-003 model
generator = OpenAIAnswerGenerator(api_key=openai_api_key,
                                  model="text-davinci-003",
                                  temperature=0.2, top_k=1)


# Define search tool generative QA pipeline
open_ai_search_engine = GenerativeQAPipeline(retriever=retriever, generator=generator)

# Build search tool generative QA pipeline and add retriever and generator as pipeline nodes
pipe = Pipeline()
pipe.add_node(component=open_ai_search_engine.get_node("Retriever"), name="Retriever", inputs=["Query"])
pipe.add_node(component=open_ai_search_engine.get_node("Generator"), name="Generator", inputs=["Retriever"])




# define agent prompt
agent_prompt = PromptTemplate(
    name="memory-shot-react",
    prompt_text="You are a helpful and knowledgeable agent. To achieve your goal of answering complex questions "
                "correctly, you have access to the following tools:\n\n"
                "{tool_names_with_descriptions}\n\n"
                "To answer questions, you'll need to go through multiple steps involving step-by-step thinking and "
                "selecting the appropriate tools and give them the question as input; tools will respond with observations.\n"
                "Decide if the observations provided by the tool contains information needed to answer questions.\n"
                "When you are ready for a final answer, respond with the Final Answer:\n\n"
                "You should avoid knowledge that is present in your internal knowledge. You do not use prior knowledge, only the observations provided by the tools available to you"
                "Use the following format:\n\n"
                "Question: the question to be answered\n"
                "Thought: Reason if you have the final answer. If yes, answer the question. If not, find out the missing information needed to answer it.\n"
                "Tool: pick one of {tool_names}. Always access the Memory tool first \n"
                "Tool Input: the full updated question to be answered\n"
                "Observation: the tool will respond with the observation\n"
                "...\n"
                "Final Answer: the final answer to the question\n\n"
                "Thought, Tool, Tool Input, and Observation steps can be repeated multiple times, but sometimes we can find an answer in the first pass\n"
                "---\n\n"
                "Question: {query}\n"
                "Thought: Let's think step-by-step, I first need to ",

)

# create agent prompt node
prompt_node = PromptNode(model_name_or_path="text-davinci-003", api_key=openai_api_key,
                         stop_words=["Observation:"])
# declare agent
memory_agent = Agent(prompt_node=prompt_node, prompt_template=agent_prompt)

# define Agent tools and add them to agent's tools list
recall_node = MemoryRecallNode(memory=memory_database)
memory_tool = Tool(name="Memory",
                           pipeline_or_node=recall_node,
                           description="Your memory. Always access this tool first to remember what you have learned.")
search_tool = Tool(name="DocumentStore_QA",
                           pipeline_or_node=pipe,
                           description="Access this tool to find out missing information needed to answer questions",
                           output_variable="answers")
memory_agent.add_tool(search_tool)
memory_agent.add_tool(memory_tool)


# loop through chat wrapper function
while True:
    user_input = input("\nchat with me (or 'quit' to exit): ")

    if user_input == "quit":
        break
    else:
        # call the chat wrapper function defined from the HaystackAgentBasicMemory library
        chat(user_input, memory_agent, memory_database)

# print("printing memory content")
# print(memory_database)
# printing("printing full conversation transcript")
# print(transcript)

