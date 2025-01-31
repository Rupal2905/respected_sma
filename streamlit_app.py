import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

def get_sma(stock_data, period):
    return stock_data['Close'].rolling(window=period).mean()

def check_continuous_respect_sma(stock_data, sma_list=[34, 50, 55, 89, 100, 144, 200, 233]):
    respected_smas = []

    for period in sma_list:
        sma = get_sma(stock_data, period)
        
        respected_continuously = True
        for i in range(len(stock_data)):
            candle = stock_data.iloc[i]
            current_sma = sma.iloc[i]

            if candle['Open'] < current_sma and candle['High'] < current_sma and candle['Low'] < current_sma and candle['Close'] < current_sma:
                respected_continuously = False
                break  
        if respected_continuously:
            respected_smas.append(period)

    return respected_smas

def display_results(results):
    """Display the results for each stock with its respected SMAs."""
    for stock, smas in results.items():
        if smas:
            st.write(f"**Stock**: {stock}")
            st.write(f"  Respected SMAs: {', '.join(map(str, smas))}")
        else:
            st.write(f"**Stock**: {stock}")
            st.write("  No SMA respected continuously")

def main():
    st.title("SMA Respect Analyzer")

    stock_symbols = ['MAXHEALTH.NS', 'ACC.NS', 'TCS.NS', 'FCL.NS', 'SBIN.NS', 'BEL.NS', 'AXISBANK.NS',
                     'INFY.NS', 'TCS.NS', 'LT.NS',
                     'SRF.NS', 'BAJAJFINSV.NS', 'KOTAKBANK.NS', 'ZOMATO.NS', 'IRFC.NS', 'ADANINENT.NS',
    ]

    # User inputs
    start_date = st.text_input("Enter start date (YYYY-MM-DD):", "2024-01-01")
    end_date = st.text_input("Enter end date (YYYY-MM-DD):", str(datetime.today().date()))
    candle_timeframe = st.selectbox("Select candle time frame:", ['1d', '1wk', '1mo'])

    # Validate inputs
    if not start_date or not end_date:
        st.error("Please provide both start and end dates.")
        return

    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        st.error("Invalid date format. Please use YYYY-MM-DD.")
        return

    if candle_timeframe not in ['1d', '1wk', '1mo']:
        st.error("Invalid candle time frame. Please choose from '1d', '1wk', or '1mo'.")
        return

    extended_start_date = start_date_obj - timedelta(days=365)
    extended_start_date_str = extended_start_date.strftime("%Y-%m-%d")

    # Button to start analysis
    if st.button("Analyze Stock"):
        all_stock_results = {}

        for stock_symbol in stock_symbols:
            stock_data = yf.download(stock_symbol, start=extended_start_date_str, end=end_date, interval=candle_timeframe)

            respected_smas = check_continuous_respect_sma(stock_data)
            all_stock_results[stock_symbol] = respected_smas

        display_results(all_stock_results)

if __name__ == "__main__":
    main()
