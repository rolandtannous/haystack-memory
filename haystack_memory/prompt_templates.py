from haystack.nodes import PromptTemplate

# This a an example to be used with the memory tools to ensure that the agent is using the memory tools.
# TODO: Further refine the template. Maybe consider few shots
memory_template = PromptTemplate(
    name="memory-shot-react",
    prompt_text="You are a helpful agent. To achieve your goal of answering questions "
                "correctly, use step by step thinking and\n"
                "use the following tools to look for answers: {tool_names_with_descriptions}. Give the tool the full "
                "question as input; the tools will respond with observations.\n"
                "Refrain from using prior internal knowledge or tools you don't have access to. You should avoid "
                "searching elsewhere and avoid using external sources.\n"""
                "Only use observations returned by the tools you have been given access to.\n"
                "Use the following format:\n\n"
                "Question: the question to be answered\n"
                "Thought: Break down the problem into smaller steps. Only use the tools you have been given access "
                "to.\n"
                "Tool: use one of the following tools to look for answers: {tool_names_with_descriptions}. Always "
                "access the memory tool first.\n"
                "Tool Input: the full updated question to be answered\n"
                "Observation: the tool will respond with an observation. If the observation is empty pick another "
                "tool to get more information.\n"
                "Final Answer: Your answer to the question. If the observations provided do not contain the answer or "
                "the tools you have access to respond with I don't have an answer, then respond with 'I don't have "
                "enough information to answer the question'\n"
                "Question: {query}\n"
                "Thought: Let's work this out it a step by step. I first need to ",
)
