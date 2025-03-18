from src.agentic_core.chains.response_generator_chain import ResponseChain
import yaml
from langgraph.graph import MessagesState

#Initalizing

response_chain_obj = ResponseChain()
response_chain_obj.load_configs()
response_chain_obj.setup_response_system()
response_chain_obj.create_response_generator_chain()


# Load YAML from a file
with open('src/config/agents/tasks.yaml', 'r') as file:
    task_config = yaml.safe_load(file)

async def response_generator_agent(state: MessagesState):
    plan = state["messages"]
    prompt =  plan #"\n".join(f"{i+1}. {step}" for i, step in enumerate(plan))
    description = task_config['generate_response_task']['description']
    expected_output = task_config['generate_response_task']['expected_output']

    task = f"description : {description}\n expected output: {expected_output}".format(input=prompt)

    agent_response = await response_chain_obj.get_response_generator_chain().ainvoke(
        {"messages": [("user", task)]}
    )
    # print(agent_response)

    return {"messages": [str(agent_response)]}