import os
import argparse
import pandas as pd
import alpaca_trade_api as ata
import datetime as dt
from pytz import timezone

os.environ['APCA_API_KEY_ID']='PKHQNEDZG5JJQ68YGNJZ'
os.environ['APCA_API_SECRET_KEY']='W5hkYXrA6rvnaqKwfFV4d71/Vm9304fujseAxdW0'

def main(symbol,date,start,ticks,cond):
    print("hello")
    full_date = date+" "+start
    st = dt.datetime.strptime(full_date, '%Y-%m-%d %H:%M:%S')
    st = timezone('US/Eastern').localize(st)
    st = int(st.timestamp())*1000
    trades = ata.REST().polygon.historic_trades(symbol, date, offset=st, limit=ticks)
    trades.df.reset_index(level=0, inplace=True)
    #convert exchange numeric codes to names for readability
    exchanges = ata.REST().polygon.exchanges()
    ex_lst = [[e.id,e.name,e.type] for e in exchanges]
    dfe = pd.DataFrame(ex_lst,columns=['exchange','exch','excode'])
    trades.df['exchange'] = trades.df['exchange'].astype(int)
    df = pd.merge(trades.df,dfe,how='left',on='exchange')
    df = df[df.exchange!=0]
    df.drop('exchange', axis=1, inplace=True)
    if cond:
        #convert sale condition numeric codes to names for readability
        conditions = ata.REST().polygon.condition_map()
        c = conditions.__dict__['_raw']
        c = {int(k):v for k,v in c.items()}
        df['condition1'] = df['condition1'].map(c)
        df['condition2'] = df['condition2'].map(c)
        df['condition3'] = df['condition3'].map(c)
        df['condition4'] = df['condition4'].map(c)
    else:
        df.drop(['condition1','condition2','condition3','condition4'], axis=1, inplace=True)
    print(df.to_string())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', type=str, default='SPY', help='symbol you want to get data for')
    parser.add_argument('--date', type=str, default='2018-09-19', help='date you want to get data for')
    parser.add_argument('--start', type=str, default='09:30:00', help='start time you want to get data for')
    parser.add_argument('--ticks', type=int, default=10000, help='number of ticks to retrieve')
    parser.add_argument('--conditions', action='store_true', default=False)
    args = parser.parse_args()
    main(args.symbol,args.date,args.start,args.ticks,args.conditions)