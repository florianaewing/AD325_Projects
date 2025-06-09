from linked_deque import LinkedDeque


class LedgerEntry:
    def __init__(self, stock_symbol):
        self.stock_symbol = stock_symbol
        self.purchases = LinkedDeque()
        self.total_shares = 0  # Running total of shares

    def add_purchase(self, new_purchase):
        self.purchases.add_to_back(new_purchase)
        self.total_shares += new_purchase.shares  # Update running total

    def remove_purchase(self, shares_to_remove):
        # Adjust purchases to remove the specified number of shares
        current = self.purchases.peek_front()
        while current and shares_to_remove > 0:
            purchase = current.data
            if purchase.shares <= shares_to_remove:
                shares_to_remove -= purchase.shares
                self.total_shares -= purchase.shares
                purchase.shares = 0  # All shares from this purchase are sold
            else:
                purchase.shares -= shares_to_remove
                self.total_shares -= shares_to_remove
                shares_to_remove = 0  # All requested shares are sold
            current = current.next_node
        # Optional: Remove empty purchases from deque

    def display_entry(self):
        output = f"{self.stock_symbol}: "
        current = self.purchases.peek_front()  # Get the front node

        while current:  # Traverse the deque
            purchase = (
                current.data
            )  # Access the StockPurchase object in the node
            if purchase.shares > 0:
                output += f"{purchase.cost_per_share:.1f} ({purchase.shares} shares), "
            current = current.next_node  # Move to the next node

        print(output.strip(", "))

    def get_total_shares(self):
        return self.total_shares  # O(1) lookup now
