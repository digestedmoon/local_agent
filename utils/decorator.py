import inspect
from ollama import Tool


class RegisteredTool:
    def __init__(self, func, schema):
        self.func = func
        self.schema = schema


def tool(func):
    signature = inspect.signature(func)

    properties = {}
    required = []

    for param in signature.parameters.values():
        annotation = param.annotation
        annotation_name = getattr(annotation, "__name__", str(annotation))

        json_type = {
            "str": "string",
            "int": "integer",
            "float": "number",
            "bool": "boolean",
        }.get(annotation_name, "string")

        properties[param.name] = Tool.Function.Parameters.Property(
            type=json_type
        )

        if param.default is inspect.Parameter.empty:
            required.append(param.name)

    schema = Tool(
        function=Tool.Function(
            name=func.__name__,
            description=func.__doc__ or "No description provided.",
            parameters=Tool.Function.Parameters(
                properties=properties,
                required=required,
            ),
        )
    )

    return RegisteredTool(func, schema)

if __name__ == "__main__" : 
    @tool
    def get_weather(location: str, unit: str = "celsius") -> str:
        """Fetches the current weather for a given location."""
        return f"Weather in {location} is 22° {unit}"

    # Accessing the generated schema for Ollama:
    print(f"\n{get_weather.schema}")

    # Calling the original Python function:
    result = get_weather.func("London", unit="fahrenheit")
    print (f"\n{result}")