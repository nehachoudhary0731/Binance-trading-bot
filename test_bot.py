# test_bot.py
import os
from dotenv import load_dotenv
from bot.base_bot import BaseTradingBot

def test_connection():
    """Test basic connection to Binance Testnet"""
    load_dotenv()
    
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        print(" Please set API keys in .env file")
        return
    
    try:
        bot = BaseTradingBot(api_key, api_secret, testnet=True)
        print(" Successfully connected to Binance Testnet")
        
        # Test account balance
        balances = bot.get_account_balance()
        print(f" Account balances: {balances}")
        
        # Test symbol validation
        is_valid = bot.validate_symbol('BTCUSDT')
        print(f" BTCUSDT validation: {is_valid}")
        
        is_invalid = bot.validate_symbol('INVALIDPAIR')
        print(f" INVALIDPAIR validation: {is_invalid}")
        
    except Exception as e:
        print(f" Connection test failed: {e}")

if __name__ == "__main__":
    test_connection()