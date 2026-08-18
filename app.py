from business import VendingMachineBusiness
from agent import Agent
from events import EventGenerator


business = VendingMachineBusiness()
event_generator = EventGenerator()
event = event_generator.next_event()

agent = Agent(
    model="gemma4:12b",
    tools=[
        business.buy_stock,
        business.change_price,
        business.wait,
        business.refund_customer,
        business.reply,
        business.add_note,
    ],
)

print("=" * 70)
print("🤖 Aqua Vend Starting")
print("=" * 70)

agent.run(business = business, event = event)

print("\nLoaded Business State")
print(business.get_state())
print("\nAgent is now sleeping...")