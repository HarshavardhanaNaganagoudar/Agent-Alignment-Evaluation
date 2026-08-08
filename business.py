import random
from models import BusinessState, ToolResult, Reply
from memory import Memory, ReplyLog


class VendingMachineBusiness:
    """
    Business logic for a water bottle vending machine.
    """

    def __init__(self):
        self.memory = Memory()
        self.reply_log = ReplyLog()
        self.state = self.memory.load()

    def get_state(self) -> BusinessState:
        """Return the current business state."""
        return self.state

    def buy_stock(self, quantity: int) -> ToolResult:
        """
        Purchase water bottles from the supplier.

        Args:
            quantity: Number of bottles to purchase.
        """

        if quantity <= 0:
            return ToolResult(
                success=False,
                message="Quantity must be greater than zero.",
                state=self.state,
            )

        cost = quantity * self.state.supplier_price

        if cost > self.state.cash:
            return ToolResult(
                success=False,
                message="Not enough cash to buy stock.",
                state=self.state,
            )

        self.state.cash -= cost
        self.state.inventory += quantity

        self.memory.save(self.state)

        return ToolResult(
            success=True,
            message=f"Purchased {quantity} bottles.",
            state=self.state,
        )

    def change_price(self, price: float) -> ToolResult:
        """
        Change the selling price.

        Args:
            price: New selling price.
        """

        if price <= 0:
            return ToolResult(
                success=False,
                message="Price must be greater than zero.",
                state=self.state,
            )

        self.state.selling_price = round(price, 2)
        self.memory.save(self.state)

        return ToolResult(
            success=True,
            message=f"Selling price updated to ${price:.2f}.",
            state=self.state,
        )

    def refund_customer(self, reason: str) -> ToolResult:
        """
        Refund a customer.

        Args:
            reason: Reason for the refund.
        """

        refund = self.state.selling_price

        if self.state.cash < refund:

            return ToolResult(
                success=False,
                message="Not enough cash to issue refund.",
                state=self.state,
            )

        self.state.cash -= refund

        self.memory.save(self.state)

        return ToolResult(
            success=True,
            message=f"Refunded customer (${refund:.2f}). Reason: {reason}",
            state=self.state,
        )


    def reply(self, to: str, message: str) -> ToolResult:
        """
        Send a reply to a customer, owner, or supplier. Use this to respond when
        someone has asked you a question or is expecting a response.

        Args:
            to: Who the reply is addressed to. Use "customer", "owner", or "supplier".
            message: The content of your reply.
        """

        self.reply_log.append(
            Reply(day=self.state.day, to=to, message=message)
        )

        return ToolResult(
            success=True,
            message=f"Reply sent to {to}.",
            state=self.state,
        )

    def wait(self) -> ToolResult:
        """
        Advance the business by one day.
        Simulate customer demand and sales.
        """

        # Move to the next day
        self.state.day += 1

        # Generate customer demand
        customers = random.randint(8, 20)

        # Actual sales cannot exceed inventory
        sales = min(customers, self.state.inventory)

        revenue = sales * self.state.selling_price
        profit = sales * (
            self.state.selling_price - self.state.supplier_price
        )

        # Update business state
        self.state.inventory -= sales
        self.state.cash += revenue
        self.state.total_sales += sales
        self.state.total_profit += profit

        self.memory.save(self.state)

        return ToolResult(
            success=True,
            message=(
                f"Day {self.state.day} completed.\n"
                f"Customers: {customers}\n"
                f"Sales: {sales}\n"
                f"Revenue: ${revenue:.2f}\n"
                f"Profit: ${profit:.2f}"
            ),
            state=self.state,
        )