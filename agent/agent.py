from ollama import chat
from models import Message
from utils import from_ollama
from agent.context import ContextManager
from agent.models_info import inspect_model
from agent.tokenizer import create_tokenizer


class Agent:
    def __init__(self, model, system_prompt, messages=None, tools=None):
        self.model = model
        
        self.system_prompt = system_prompt
        
        self.messages = messages if messages is not None else [
            Message(
                role="system",
                content=self.system_prompt
            )
        ]

        self.tools = tools or {}

        self.tool_schemas = [
            tool.schema
            for tool in self.tools.values()
        ]

        self.model_info= inspect_model(model)

        self.tokenizer = create_tokenizer(self.model_info)

        self.contextmanager = ContextManager(tokenizer=self.tokenizer,context_window=self.model_info.context_window,max_output_tokens=2048,safety_margin=256,)

        
    def run(self, user_input):

        self.messages.append(
            Message(
                role="user",
                content=user_input
            )
        )

        while True:
            
            context = self.contextmanager.build_context(self.messages)
            
            # Convert YOUR Message objects -> dictionaries
            ollama_messages = [
                message.model_dump(exclude_none=True)
                for message in context
            ]

            response = chat(
                model=self.model,
                messages=ollama_messages,
                tools=self.tool_schemas,
            )
            print(f"\nThinking: {response.message.thinking}")

            # Convert Ollama Message -> YOUR Message
            message = from_ollama(response.message)
            
            self.messages.append(message)

            if not message.tool_calls:
                return message.content

            #shows how many tool call we are going with
            for tool_call in message.tool_calls:
                print(f"\n{tool_call}")

            for tool_call in message.tool_calls:
                
                print(f"\nProcedding with '{tool_call.function.name}'")
                result = self.execute_tool(tool_call)
                print(f"\nResult of toolcall('{tool_call.function.name}') = {str(result)} ")
                self.messages.append(
                    Message(
                        role="tool",
                        tool_name=tool_call.function.name,
                        content=str(result),
                    )
                )

    def execute_tool(self, tool_call):
        tool_name = tool_call.function.name
        arguments = tool_call.function.arguments

        tool = self.tools[tool_name]
        try:
            return tool.func(**arguments)
        except Exception as e:
            return f"Tool execution failed: {type(e).__name__}: {e}" 