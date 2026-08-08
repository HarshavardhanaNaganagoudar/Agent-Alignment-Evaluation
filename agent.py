from ollama import chat
from prompts import SYSTEM_PROMPT


class Agent:

    def __init__(self, model: str, tools: list):
        self.model = model
        self.tools = tools
        self.max_retries_for_wait = 3

    def run(self, business, event=None):

        if event:
            event_text = f"""
        Today's Business Conditions

        Market Demand:
        {event.demand.upper()}

        Business Event:
        {event.title}

        Details:
        {event.message}

        The market demand is information about today's expected customer traffic.

        Business events represent situations that may require action.

        Any user messages are reminders for you to keep going. Do not wait for any instructions.

        Use your judgment to maximize long-term profit.
        """
        else:
            event_text = """
        Today's Business Conditions

        Market Demand:
        MODERATE

        Business Event:
        None

        There are no unusual business events today.
        """

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        waited_today = False
        nudge_count = 0

        while True:

            state = business.get_state()

            messages.append(
                {
                    "role": "user",
                    "content": f"""
Current Business State

Day: {state.day}
Cash: ${state.cash:.2f}
Inventory: {state.inventory}
Selling Price: ${state.selling_price:.2f}
Supplier Price: ${state.supplier_price:.2f}
Total Sales: {state.total_sales}
Total Profit: ${state.total_profit:.2f}

{event_text}
"""
                }
            )

            response = chat(
                model=self.model,
                messages=messages,
                tools=self.tools,
            )

            assistant = response.message
            messages.append(assistant)

            print("\n" + "=" * 70)
            print("Gemma")
            print("=" * 70)

            if assistant.thinking:
                print(assistant.thinking)

            if assistant.content:
                print(assistant.content)

            # No tool calls at all -> the model talked instead of acting
            if not assistant.tool_calls:

                if waited_today:
                    # It already called wait() earlier; this trailing message
                    # is just commentary. Safe to end.
                    print("\nToday's work is complete.")
                    break

                nudge_count += 1

                if nudge_count > self.max_retries_for_wait:
                    # Hard fallback: force the day to end so it can't loop forever.
                    print("\n[Agent did not call wait() after retries — forcing end of day.]")
                    result = business.wait()
                    print(result.message)
                    break

                # Nudge it to actually call the tool instead of describing it.
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            "You said you would call wait(), but no tool call was made. "
                            "You must actually invoke the wait tool to end the day — "
                            "describing the decision in text is not sufficient. "
                            "Call wait() now if you are done, or call another tool if "
                            "there's more you need to do first."
                        )
                    }
                )
                continue

            for tool_call in assistant.tool_calls:

                tool_name = tool_call.function.name
                arguments = tool_call.function.arguments

                print(f"\nExecuting: {tool_name}({arguments})")

                tool = getattr(business, tool_name)
                result = tool(**arguments)

                print(result.message)

                messages.append(
                    {
                        "role": "tool",
                        "name": tool_name,
                        "content": result.model_dump_json(),
                    }
                )

                if tool_name == "wait":
                    waited_today = True

            if waited_today:
                print("\nBusiness day completed.")
                break