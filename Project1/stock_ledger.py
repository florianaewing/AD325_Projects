from stock_purchase import StockPurchase
from ledger_entry import LedgerEntry
from linked_deque import LinkedDeque

class Stock_Ledger:
    def __init__(self):
        self.entries = {}
<<<<<<< Updated upstream
=======
        self.total_profit = 0.0
>>>>>>> Stashed changes

    def buy(self, stock_symbol, shares_bought, price_per_share):
        if stock_symbol not in self.entries:
            self.entries[stock_symbol] = LedgerEntry(stock_symbol)
        new_purchase = StockPurchase(stock_symbol, price_per_share, shares_bought)
        self.entries[stock_symbol].add_purchase(new_purchase)

    def sell(self, stock_symbol, shares_sold, price_per_share):
        if stock_symbol in self.entries:
            entry = self.entries[stock_symbol]
            total_shares = entry.get_total_shares()

            if total_shares < shares_sold:
                print(f"Error: Not enough shares to sell {shares_sold} shares of {stock_symbol}")
                return

<<<<<<< Updated upstream
            # Logic to remove shares from purchases
=======
            # Logic to remove shares from purchases and calculate profit/loss
>>>>>>> Stashed changes
            remaining_shares_to_sell = shares_sold
            current = entry.purchases.peek_front()

            while current and remaining_shares_to_sell > 0:
                purchase = current.data
                if purchase.shares <= remaining_shares_to_sell:
<<<<<<< Updated upstream
                    remaining_shares_to_sell -= purchase.shares
                    purchase.shares = 0  # All shares from this purchase are sold
                else:
=======
                    # Calculate profit for this purchase
                    profit = (price_per_share - purchase.cost_per_share) * purchase.shares
                    self.total_profit += profit  # Update total profit
                    remaining_shares_to_sell -= purchase.shares
                    purchase.shares = 0  # All shares from this purchase are sold
                else:
                    # Calculate profit for partially sold shares
                    profit = (price_per_share - purchase.cost_per_share) * remaining_shares_to_sell
                    self.total_profit += profit  # Update total profit
>>>>>>> Stashed changes
                    purchase.shares -= remaining_shares_to_sell
                    remaining_shares_to_sell = 0  # All requested shares are sold

                current = current.next_node

        print(f"Selling {shares_sold} shares of {stock_symbol} at {price_per_share}")
<<<<<<< Updated upstream
=======

    def display_total_net_profit_loss(self):
        # Display the total profit or loss
        if self.total_profit > 0:
            print(f"Total Profit: ${self.total_profit:.2f}")
        elif self.total_profit < 0:
            print(f"Total Loss: ${-self.total_profit:.2f}")
        else:
            print("No Profit or Loss.")
>>>>>>> Stashed changes
        
        
################################################################################
# EXTRA CREDIT:

   

################################################################################
        
    def display_ledger(self):
        print()
        print("---- Stock Ledger ----")
        for entry in self.entries.values():
            entry.display_entry()
        print()

    def contains(self, stock_symbol):
        return stock_symbol in self.entries

    def get_entry(self, stock_symbol):
        return self.entries.get(stock_symbol, None)
