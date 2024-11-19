from linked_deque import LinkedDeque
from ledger_entry import LedgerEntry
from stock_ledger import Stock_Ledger
from stock_purchase import StockPurchase
<<<<<<< Updated upstream
#Main and testing class implementation 
=======

>>>>>>> Stashed changes
class Main:
    def main():
        stock_ledger = Stock_Ledger()

        stock_ledger.buy("AAPL", 20, 45)  
        stock_ledger.buy("AAPL", 20, 75)  
        stock_ledger.buy("MSFT", 20, 95)  
        stock_ledger.display_ledger()     

        stock_ledger.sell("AAPL", 30, 65) 
        stock_ledger.display_ledger()     
        stock_ledger.sell("AAPL", 10, 65) 
        stock_ledger.display_ledger()     

        stock_ledger.buy("AAPL", 100, 20) 
        stock_ledger.buy("AAPL", 20, 24)  
        stock_ledger.buy("TSLA", 200, 36) 
        stock_ledger.display_ledger()     

        stock_ledger.sell("AAPL", 10, 65) 
        stock_ledger.display_ledger()     
        stock_ledger.sell("TSLA", 150, 30) 
        stock_ledger.display_ledger()     

        stock_ledger.buy("MSFT", 5, 60)   
        stock_ledger.buy("MSFT", 5, 70)   
        stock_ledger.display_ledger()     

        stock_ledger.sell("MSFT", 4, 30)  
        stock_ledger.display_ledger()     
        stock_ledger.sell("MSFT", 2, 30)  
        stock_ledger.display_ledger()
<<<<<<< Updated upstream
=======

        stock_ledger.display_total_net_profit_loss()
>>>>>>> Stashed changes
        
        
        #Extra Credit

    if __name__ == "__main__":
        main()
