# bot/base_bot.py
import logging
import sys
from binance import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from datetime import datetime
import os

class BaseTradingBot:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.client = None
        self.logger = self._setup_logging()
        self._initialize_client()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging"""
        os.makedirs('logs', exist_ok=True)
        
        logger = logging.getLogger('TradingBot')
        logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler('logs/trading.log')
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_client(self):
        """Initialize Binance client with error handling"""
        try:
            self.client = Client(
                api_key=self.api_key,
                api_secret=self.api_secret,
                testnet=self.testnet
            )
            self.logger.info("Binance client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Binance client: {str(e)}")
            raise
    
    def validate_symbol(self, symbol: str) -> bool:
        """Validate if symbol exists and is tradable"""
        try:
            exchange_info = self.client.futures_exchange_info()
            valid_symbols = [s['symbol'] for s in exchange_info['symbols']]
            return symbol.upper() in valid_symbols
        except BinanceAPIException as e:
            self.logger.error(f"Error validating symbol {symbol}: {e}")
            return False
    
    def get_account_balance(self) -> dict:
        """Get USDT balance from futures account"""
        try:
            account = self.client.futures_account()
            balances = {
                balance['asset']: float(balance['balance'])
                for balance in account['assets']
                if float(balance['balance']) > 0
            }
            self.logger.info(f"Account balances: {balances}")
            return balances
        except BinanceAPIException as e:
            self.logger.error(f"Error fetching account balance: {e}")
            return {}
    
    def get_symbol_info(self, symbol: str) -> dict:
        """Get symbol information including price filters and lot size"""
        try:
            exchange_info = self.client.futures_exchange_info()
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol.upper():
                    return s
            return {}
        except BinanceAPIException as e:
            self.logger.error(f"Error fetching symbol info: {e}")
            return {}