# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Binance Testnet Configuration
    TESTNET_BASE_URL = "https://testnet.binancefuture.com"
    API_KEY = os.getenv('BINANCE_API_KEY', '')
    API_SECRET = os.getenv('BINANCE_API_SECRET', '')
    
    # Trading Configuration
    DEFAULT_SYMBOL = 'BTCUSDT'
    DEFAULT_QUANTITY = 0.001
    
    # Logging Configuration
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/trading.log'