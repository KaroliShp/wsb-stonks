import requests
import time
import random

def fetch_intraday_quote(ticker, FINNHUB_API_KEY):
    """
    Get current market price and percentage diff from today's open for a single stock ticker
    """
    r = requests.get(f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}')
    """
    dict with keys
    o - Open price of the day
    h - High price of the day
    l - Low price of the day
    c - Current price
    pc - Previous close price
    """
    res = r.json()
    # print(r.json())
    try:
        current = res["c"]
        up_down_by = (res["c"] - res["o"]) * 100 / res["o"]
    except ZeroDivisionError:
        current = "N/A"
        up_down_by = "N/A"
    except Exception as e:
        print(f"exception in fetch_intraday_quote() with ticker {ticker}")
        print(e)
        current = "N/A"
        up_down_by = "N/A"
    return {'stock_name': ticker, "current": current, "intraday_perc_change": up_down_by}


def get_top_k_ticker_data(db_client, FINNHUB_API_KEY, K=10):
    """
    Fetches top-k most mentioned stock tickers,
    calls API to get current market price and percentage diff from today's open,
    writes the update to DB.
    """
    top_tickers_data = db_client.find_all('top-stocks-global', {})[:K]
    while top_tickers_data == []:
        print("retrying - in case of collision, top-tickers were temporarily cleaned by main job")
        # get random value between 0.3 and 0.7 seconds for backoff with random jitter
        r = abs(random.random()-0.3)
        time.sleep(r)
        top_tickers_data = db_client.find_all('top-stocks-global', {})[:K]
    # print(top_tickers_data)
    top_tickers_list =  [obj["stock_name"] for obj in top_tickers_data]
    return [fetch_intraday_quote(t, FINNHUB_API_KEY) for t in top_tickers_list]