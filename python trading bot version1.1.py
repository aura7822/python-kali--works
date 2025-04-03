import ccxt
import time
from datetime import datetime
import smtplib
import numpy as np

api_key = "api_key"
api_secret = "api_secret"

exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})
symbol = 'BTC/USDT'
budget = 100  
price_drop = 0.99  # Buy trigger
price_increase = 1.01  # Sell trigger
stop_loss = 0.95  
take_profit_threshold = 1.05  
ma_period = 5  
last_price = None
holding = False
buy_price = 0  
trade_log = []  
price_history = []  

def send_email_alert(subject, body):
    try:
        sender_email = "your_email@gmail.com"
        receiver_email = "receiver_email@gmail.com"
        password = "your_password"  # Security risk! Use environment variables instead.

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        print("Email alert sent successfully!")
    except Exception as e:
        print(f"Failed to send email alert: {e}")

def log_trade(action, amount, price, timestamp):
    trade_log.append({
        "action": action,
        "amount": amount,
        "price": price,
        "timestamp": timestamp
    })
    print(f"{action.capitalize()} {amount:.6f} BTC at {price:.2f} USDT on {timestamp}")
    
    send_email_alert(
        subject=f"Trade Alert: {action.capitalize()} {symbol}",
        body=f"Action: {action.capitalize()}\nAmount: {amount:.6f} BTC\nPrice: {price:.2f} USDT\nTime: {timestamp}"
    )

def calculate_moving_average(prices, period):
    if len(prices) < period:
        return None
    return np.mean(prices[-period:])

def manage_risk(current_price):
    global holding, buy_price
    if current_price <= buy_price * stop_loss:
        print("Stop-loss triggered!")
        holding = False
        return "sell"
    elif current_price >= buy_price * take_profit_threshold:
        print("Take profit triggered!")
        holding = False
        return "sell"
    return None

print("Starting advanced trading bot...")

try:
    while True:
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']
        price_history.append(current_price)
        
        moving_average = calculate_moving_average(price_history, ma_period)
        print(f"Current Price: {current_price:.2f} USDT, Moving Average ({ma_period} periods): {moving_average:.2f}" if moving_average else "Calculating moving average...")
        if last_price is not None and not holding and current_price < last_price * price_drop:
            if len(price_history) > ma_period and current_price < moving_average:
                amount_to_buy = budget / current_price
                buy_price = current_price
                holding = True
                log_trade("buy", amount_to_buy, current_price, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if holding:
            action = manage_risk(current_price)
            if action == "sell":
                log_trade("sell", amount_to_buy, current_price, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        last_price = current_price
        time.sleep(10)  # Wait before next check

except Exception as e:
    print(f"An error occurred: {e}")
print("\nTrade Log Summary:")
for trade in trade_log:
    print(trade)
