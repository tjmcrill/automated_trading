import alpaca_trade_api as tradeapi 
import sys

APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
APCA_API_KEY_ID = "PKVLO8FKEPDMO55XAJZB"
APCA_API_SECRET_KEY = "h05Fou2NL0PQSIcku7tAWsj7dfyIDP8ab2G/eSa8"

api = tradeapi.REST(
    base_url=APCA_API_BASE_URL,
    key_id=APCA_API_KEY_ID,
    secret_key=APCA_API_SECRET_KEY
)

account = api.get_account()

if account.trading_blocked:
    print("Account is currently restricted from trading")

#print("${} is available as buying power.".format(account.buying_power))   

asset = "AAPL"
"""
try:
    aapl_asset = api.get_asset(asset)
    print(aapl_asset)
    if aapl_asset.tradable:
        print("We can trade", asset)
    else:
        print("We cannot trade", asset)    
except:
    print("Error finding",asset)  
"""
all_assets = api.list_assets(status="active")
"""
for asset in all_assets:
    if asset.exchange == "NASDAQ" and asset.tradable == True:
        print(asset)   
"""
def trade_stock(sym,num,side,typ,time):
    api.submit_order(
        symbol = sym,
        qty = num,
        side = side,
        type = typ,
        time_in_force = time
    )
keep_going = True
while(keep_going):
    ans = input("Do you want to buy a stock or sell a stock?(type 'buy' or 'sell'): ")
    print("\n")
    if(ans == 'buy'):
        try:
            symb = input("What stock do you want to buy? Please provide the appropriate symbol: ")
            amount = input("How many of said stock do you want to buy?: ")
            trade_stock(symb,amount,"buy","market","gtc")
            print("\n")
            print("Successfully bought",amount,"shares of",symb,"stock")
        except:
            print("Unexpected error:", sys.exc_info()[0])
    elif(ans == 'sell'):
        symb = input("What stock do you want to sell? Please provide the appropriate symbol: ")    
        amount = input("How many of said stock do you want to sell?: ")
        trade_stock(symb,amount,"sell","market","gtc")
        print("\n")
        print("Successfully sold",amount,"shares of",symb,"stock")

    print("\n")
    val = input("Do you want to make another transaction?(y or n): ")
    if(val=='n'):
        keep_going = False
        print("\n")
        print("Thanks for using my automated trader. Goodbye!")        

    
   