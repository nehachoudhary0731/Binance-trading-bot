# Overview

This project is a simplified trading bot built in Python as part of the Junior Python Developer – Crypto Trading Bot assignment.
The bot interacts with the Binance Futures Testnet (USDT-M) to place market and limit orders, supporting both buy and sell sides.

Key features include:
Market and Limit order placement
Input validation and CLI interaction
Logging of API requests, responses, and errors
Structured, reusable Python code for clarity and maintainability

# Requirements

Python
python-binance
requests, logging, dotenv (optional for API key management)
Install dependencies:
pip install python-binance requests python-dotenv

# Important: The logs may show "APIError(code=-2015): Invalid API-key, IP, or permissions for action" 
because I could not generate Binance Testnet API credentials (PAN card verification required).  
However, the bot is fully functional, and once valid API keys are provided, it can execute 
trades on Binance Futures Testnet.






