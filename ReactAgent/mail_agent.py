import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from lecture1.ModelType import ModelType
from lecture1.ReactAgent.tools.tools_registry import available_functions, function_output_key
from tools.tools_registry import tools

load_dotenv()

def format_tool_output(function_name: str, result) -> str:
    """
    Converts tool result into readable 'name = value' form for LLM message.
    """

    key = function_output_key.get(function_name, function_name)
    pretty_json = json.dumps(result, ensure_ascii=False, indent=2)
    return f"{key} = {pretty_json}"

def summarize_state(state: dict) -> str:
    """
    Converts current state into a string summary to re-inject into messages.
    """
    summary = []
    for key, value in state.items():
        summary.append(f"{key} = {json.dumps(value, ensure_ascii=False)}")
    return "\n".join(summary)

class MailAgent:
    def __init__(self, model: ModelType = ModelType.GPT_41_mini, max_iterations: int = 20):
        self.client = OpenAI(api_key=os.getenv("PROGRAMIA_OPENAI_API_KEY"))
        self.model = model
        self.max_iterations = max_iterations

    def run_agent(self, messages) -> str:

        i = 0
        while i < self.max_iterations:
            i += 1
            print(f"--- Iteration {i} ---")

            response = self.client.chat.completions.create(
                model=self.model.value,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                parallel_tool_calls=False
            )

            response_msg = response.choices[0].message
            print(f"LLM response: {response_msg}")

            """
            Pokud LLM vyhodnotilo, že je potřeba zavolat nějaký tool,
            musíme toto volání zpracovat, protože LLM samo o sobě tu funkci nevykoná
            """
            if response_msg.tool_calls: # pokud LLM chce použít nějaký nástroj...
                # uložíme odpověď do historie
                messages.append({
                    "role": "assistant", # zde musí být role "assistant" !!
                    "content": response_msg.content,
                    "tool_calls": [ # ukládáme všechny tool cally, které si LLM v dané odpovědi vyžádalo
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments,
                            }
                        }
                        for tool_call in response_msg.tool_calls
                    ]
                })

                # skutečné spuštění toolů, které si LLM vymyslelo
                for tool_call in response_msg.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    tool_id = tool_call.id

                    print(f"\n...Executing function {function_name}({function_args})...\n")

                    # zavolání funkce - zde potřebujeme "převodník" funkcí
                    # zavolání funkce i s argumenty
                    try:
                        result = available_functions[function_name](**function_args)
                        formatted_result = format_tool_output(function_name, result)
                    except TypeError as e:
                        result = f"Error: {str(e)}"
                        formatted_result = f"{function_output_key.get(function_name, function_name)} = \"{result}\""

                    # Přidání tool zprávy vždy, i když došlo k chybě
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "content": formatted_result,
                    })

                print(f"---MESSAGES: {messages} ---")

                continue
            else:
                # LLM nemá už žádný další tool_call
                final_result = response_msg.content
                messages.append({
                    "role": "system",
                    "content": final_result,
                })
                print(f"--- Final answer: {final_result} ---")
                return final_result

        return "Error:  Maximum iterations achieved without result."

    def run_agent_old(self, messages) -> str:
        state = {}
        i = 0
        while i < self.max_iterations:
            i += 1
            print(f"--- Iteration {i} ---")

            # Přidej aktuální stav do kontextu (pokud nějaký existuje)
            if state:
                messages.append({
                    "role": "system",
                    "content": summarize_state(state)
                })

            response = self.client.chat.completions.create(
                model=self.model.value,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                parallel_tool_calls=False
            )

            response_msg = response.choices[0].message
            print(f"LLM response: {response_msg}")

            """
            Pokud LLM vyhodnotilo, že je potřeba zavolat nějaký tool,
            musíme toto volání zpracovat, protože LLM samo o sobě tu funkci nevykoná
            """
            if response_msg.tool_calls: # pokud LLM chce použít nějaký nástroj...
                # uložíme odpověď do historie
                messages.append({
                    "role": "assistant", # zde musí být role "assistant" !!
                    "content": response_msg.content,
                    "tool_calls": [ # ukládáme všechny tool cally, které si LLM v dané odpovědi vyžádalo
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments,
                            }
                        }
                        for tool_call in response_msg.tool_calls
                    ]
                })

                # skutečné spuštění toolů, které si LLM vymyslelo
                for tool_call in response_msg.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    tool_id = tool_call.id

                    print(f"\n...Executing function {function_name}({function_args})...\n")

                    # zavolání funkce - zde potřebujeme "převodník" funkcí
                    # zavolání funkce i s argumenty
                    try:
                        result = available_functions[function_name](**function_args)
                    except TypeError as e:
                        print(f"Chyba při volání funkce '{function_name}': {e}")
                        result = f"Error: {str(e)}"

                    key = function_output_key.get(function_name)
                    if key and not isinstance(result, str):  # ukládej jen validní data
                        state[key] = result

                    formatted_result = format_tool_output(function_name, result)
                    print(f"--- Tool result: {result} ---")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "content": formatted_result,
                    })

                print(f"---MESSAGES: {messages} ---")

                continue
            else:
                # LLM nemá už žádný další tool_call
                final_result = response_msg.content
                messages.append({
                    "role": "system",
                    "content": final_result,
                })
                print(f"--- Final answer: {final_result} ---")
                return final_result

        return "Error:  Maximum iterations achieved without result."




