from haystack.nodes import PromptTemplate

# This a an example to be used with the memory tools to ensure that the agent is using the memory tools.
# TODO: Further refine the template. Maybe consider few shots
memory_template = PromptTemplate(
    name="memory-shot-react",
    prompt_text="You are a helpful and knowledgeable agent. To achieve your goal of answering complex questions "
                "correctly, you have access to the following tools:\n\n"
                "{tool_names_with_descriptions}\n\n"
                "To answer questions, you'll need to go through multiple steps involving step-by-step thinking and "
                "selecting the appropriate tools and give them the question as input; "
                "tools will respond with observations.\n"
                "Decide if the observations provided by the tool contains information needed to answer questions.\n"
                "When you are ready for a final answer, respond with the Final Answer:\n\n"
                "You should avoid knowledge that is present in your internal knowledge. "
                "You do not use prior knowledge, only the observations provided by the tools available to you"
                "Use the following format:\n\n"
                "Question: the question to be answered\n"
                "Thought: Reason if you have the final answer. "
                "If yes, answer the question. If not, find out the missing information needed to answer it.\n"
                "Tool: pick one of {tool_names}. Always access the Memory tool first \n"
                "Tool Input: the full updated question to be answered\n"
                "Observation: the tool will respond with the observation\n"
                "...\n"
                "Final Answer: the final answer to the question\n\n"
                "Thought, Tool, Tool Input, and Observation steps can be repeated multiple times, "
                "but sometimes we can find an answer in the first pass\n"
                "---\n\n"
                "Question: {query}\n"
                "Thought: Let's think step-by-step, I first need to ",
)
