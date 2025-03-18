import yaml
import importlib
from langgraph.prebuilt import create_react_agent
from src.models.models import query_llm

class ResponseChain:
    def __init__(self):
        self.agent_config_path = 'src/config/agents/agents.yaml'
        self.tools_config_path = 'src/config/tools/tools_config.yaml'
        self.agent_config = None
        self.tools_list = []
        self.loaded_tools = {}  # Store dynamically imported tools
        self.system_message = ""
        self.query_generator_chain = None

    def load_configs(self):
        """Load agent and tool configurations from YAML files."""
        # Load Agent Configuration
        with open(self.agent_config_path, 'r') as file:
            self.agent_config = yaml.safe_load(file)

        # Load Tools Configuration
        with open(self.tools_config_path, 'r') as file:
            config = yaml.safe_load(file)
            # print(config)
            self.tools_list = config.get("response_generator", [])  # Get tools from YAML

        # Dynamically load tools
        self.loaded_tools = self.load_tools_dynamically()

        # print("TOOLS LOADED:")
        # print(list(self.loaded_tools.values()))

    def load_tools_dynamically(self):
        """Dynamically load tools from the tools list."""
        tools_dict = {}
        for tool_name in self.tools_list:
            try:
                # Construct the module path dynamically
                module_path = f"src.tools.{tool_name}"
                module = importlib.import_module(module_path)

                # Retrieve the class and instantiate it
                tool_class = getattr(module, tool_name)
                tools_dict[tool_name] = tool_class  # Store instantiated tool
                print(f"Loaded tool: {tool_name}")
            except (ModuleNotFoundError, AttributeError) as e:
                print(f"Error loading tool {tool_name}: {e}")
            print(tools_dict)

        return tools_dict

    def setup_response_system(self):
        """Set up the MongoDB query generation system message."""
        if not self.agent_config:
            raise ValueError("Agent configuration is not loaded.")

        role = self.agent_config['response_generator']['role']
        goal = self.agent_config['response_generator']['goal']
        backstory = self.agent_config['response_generator']['backstory']

        self.system_message = (
            f"Your Role: {role}\n"
            f"Your main goal: {goal}\n"
            f"Backstory: {backstory}"
        )

    def create_response_generator_chain(self):
        """Create the query generator chain using the system message and loaded tools."""
        if not self.system_message:
            raise ValueError("System message for MongoDB is not set up.")

        self.query_generator_chain = create_react_agent(
            query_llm,
            list(self.loaded_tools.values()),  # Pass dynamically loaded tool instances
            state_modifier=self.system_message
        )

    def get_response_generator_chain(self):
        """Return the query generator chain."""
        if self.query_generator_chain is None:
            raise ValueError("Query generator chain has not been created.")
        return self.query_generator_chain

if __name__ == "__main__":
    response_agent = ResponseChain()
    response_agent.load_configs()
    response_agent.setup_response_system()
    response_agent.create_response_generator_chain()

    chain = response_agent.get_response_generator_chain()
    print("Query generator chain created successfully.")
