import alpaca_trade_api as tradeapi 
import argparse
import os
import sys

APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(
    base_url=APCA_API_BASE_URL,
    key_id=os.environ.get("APCA_API_KEY_ID"),
    secret_key=os.environ.get("APCA_API_SECRET_KEY"),
)

account = api.get_account()
conn = tradeapi.stream2.StreamConn()

def buy_method():
    try:
        print('\n')
        symb = input('Enter the symbol of the stock you wish to buy: ')
        amnt = input("Enter the # of shares you wish to purchase: ")
        print('\n')
        trade_stock(symb,amnt,"buy","market","gtc")
        print('\n')
        print("Successfully bought",amnt,"shares of",symb,"stock")
        print('\n')
    except: 
        print("Unexpected error:", sys.exc_info()[0])       


def sell_method():
    try:
        print('\n')
        symb = input('Enter the symbol of the stock you wish to sell: ')
        amnt = input("Enter the # of shares you wish to sell: ")
        print('\n')
        trade_stock(symb,amnt,"sell","market","gtc")
        print('\n')
        print("Successfully sold",amnt,"shares of",symb,"stock")
        print('\n')
    except: 
        print("Unexpected error:", sys.exc_info()[0])   
                

def check_market():
    print('\n')
    clock = api.get_clock()
    print('The market is {}'.format('open.' if clock.is_open else 'closed.'))    
    print('\n')

def buy_power():
    print('\n')
    print('${} is available as buying power.'.format(account.buying_power))
    print('\n')   

def check_symbols():
    print('\n')
    active_assets = api.list_assets(status='active')
    nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ']
    amex_assets = [b for b in active_assets if b.exchange == 'AMEX']
    nyse_assets = [c for c in active_assets if c.exchange == 'NYSE']
    arca_assets = [d for d in active_assets if d.exchange == 'ARCA']
    print('Stock Exchange Asset Menu\n')
    ans = input('1. NASDAQ\n'
        '2. AMEX\n'
        '3. NYSE\n'
        '4. ARCA\n'
        '5. All Assets\n'    
        '\nEnter an input: ')
    if(ans == '1'):
        for asset in nasdaq_assets:
            print('\n')
            print(asset)
    
    elif(ans == '2'):
        for asset in amex_assets:
            print('\n')
            print(asset)   

    elif(ans == '3'):
        for asset in nyse_assets:
            print('\n')
            print(asset)  

    elif(ans == '4'):
        for asset in arca_assets:
            print('\n')
            print(asset)                         

    elif(ans == '5'):
        for asset in active_assets:
            print('\n')
            print(asset)  
    print('\n')         
                    

def trade_stock(sym,num,side,typ,time):
    api.submit_order(
        symbol = sym,
        qty = num,
        side = side,
        type = typ,
        time_in_force = time
    )

@conn.on(r'account_updates')
async def on_msg(conn, channel, data):
    # Track the cash balance in our account.
    print("Update for account. Cash balance: {}".format(data['cash']))    

def main():
    wantCont = True
    while (wantCont):
        print('Automated Trader Menu:\n')
        ans = input('1. Check your current buying power\n'
        '2. Check if the market is open\n'
        '3. List all tradeable assets on any exchange\n'
        '4. Buy shares of a specific stock\n'
        '5. Sell shares of a specific stock\n'
        '99. Exit\n'    
        '\nEnter an input: ')   

        if (ans == '1'):
            buy_power()

        elif(ans == '2'):
            check_market()

        elif(ans == '3'):
            check_symbols()

        elif(ans == '4'):
            buy_method()

        elif(ans == '5'):
            sell_method()

        elif(ans == '99'):
            print('Thank you for using the trader!')
            break


if __name__ == '__main__':
    main()
    
    
   