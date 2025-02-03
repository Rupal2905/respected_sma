import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

def get_sma(stock_data, period):
    return stock_data['Close'].rolling(window=period).mean()

def check_continuous_respect_sma(stock_data, sma_list=[34, 50, 55, 89, 100, 144, 200, 233], candle_timeframe='1d'):
    respected_smas = []

    for period in sma_list:
        sma = get_sma(stock_data, period)
        respected_continuously = True
        touch_count = 0

        for i in range(1, len(stock_data)):
            candle = stock_data.iloc[i]
            current_sma = sma.iloc[i]

            if candle['Open'] < current_sma and candle['High'] < current_sma and candle['Low'] < current_sma and candle['Close'] < current_sma:
                respected_continuously = False
                break

        if respected_continuously:
            for i in range(1, len(stock_data)):
                candle = stock_data.iloc[i]
                current_sma = sma.iloc[i]

                if candle['Low'] < current_sma and candle['High'] > current_sma:
                    touch_count += 1

            if touch_count > 0:
                respected_smas.append((period, touch_count))
            else:
                respected_smas.append((period, 0))  

    return respected_smas

def main():
    st.title("Stock Analysis - SMA Respect Checker")

    stock_symbols_input =  st.selectbox("Select symbol", ['MAXHEALTH.NS', 'ZOMATO.NS', 'AARTIIND.NS', 'ABB.NS', 'ABBOTINDIA.NS', 'ABCAPITAL.NS',
                                                         'ABFRL.NS', 'ACC.NS', 'ADANIENSOL.NS', 'ADANIENT.NS', 'ADANIGREEN.NS', 'INDIGO.NS',
                                                         'ALKEM.NS', 'AMBUJACEM.NS', 'ANGELONE.NS', 'APLAPOLLO.NS', 'ASTRAL.NS', 'ATGL.NS',
                                                         'BRITANNIA.NS', 'CANBK.NS', 'CIPLA.NS', 'COALINDIA.NS', 'DABUR.NS', 'IGL.NS', ])
    stock_symbols = stock_symbols_input.split(",") 
    stock_symbols = [symbol.strip() for symbol in stock_symbols]

    start_date = st.date_input("Start date", datetime(2024, 1, 1))
    end_date = st.date_input("End date", datetime.today())
    candle_timeframe = st.selectbox("Select candle time frame", ['1d','1wk', '1mo'])

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    extended_start_date = start_date - timedelta(days=365)
    extended_start_date_str = extended_start_date.strftime("%Y-%m-%d")

    if st.button("Analyze Stocks"):
        all_stock_results = []
        for stock_symbol in stock_symbols:
            stock_data = yf.download(stock_symbol, start=extended_start_date_str, end=end_date_str, interval=candle_timeframe)

            respected_smas = check_continuous_respect_sma(stock_data, candle_timeframe=candle_timeframe)

            for sma, count in respected_smas:
                all_stock_results.append({
                    "Stock Symbol": stock_symbol,
                    "Respected SMA": sma,
                    "Touch Count": count
                })

        if all_stock_results:
            df_results = pd.DataFrame(all_stock_results)
            st.dataframe(df_results)  
        else:
            st.write("No SMAs respected continuously for the selected stocks.")

if __name__ == "__main__":
    main()

