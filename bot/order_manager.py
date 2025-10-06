# bot/order_manager.py
from binance import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import logging
from typing import Dict, Optional

class OrderManager:
    def __init__(self, client: Client, logger: logging.Logger):
        self.client = client
        self.logger = logger
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict:
        """Place a market order"""
        try:
            self.logger.info(f"Placing market order: {symbol} {side} {quantity}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='MARKET',
                quantity=quantity
            )
            
            self.logger.info(f"Market order placed successfully: {order}")
            return {
                'status': 'success',
                'order_id': order['orderId'],
                'symbol': order['symbol'],
                'side': order['side'],
                'type': order['type'],
                'quantity': float(order['origQty']),
                'price': None,  # Market orders don't have price
                'timestamp': order['updateTime']
            }
            
        except BinanceOrderException as e:
            error_msg = f"Order error for {symbol}: {e}"
            self.logger.error(error_msg)
            return {'status': 'error', 'message': error_msg}
        except BinanceAPIException as e:
            error_msg = f"API error for {symbol}: {e}"
            self.logger.error(error_msg)
            return {'status': 'error', 'message': error_msg}
        except Exception as e:
            error_msg = f"Unexpected error for {symbol}: {e}"
            self.logger.error(error_msg)
            return {'status': 'error', 'message': error_msg}
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict:
        """Place a limit order"""
        try:
            self.logger.info(f"Placing limit order: {symbol} {side} {quantity} @ {price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce='GTC'  # Good Till Cancelled
            )
            
            self.logger.info(f"Limit order placed successfully: {order}")
            return {
                'status': 'success',
                'order_id': order['orderId'],
                'symbol': order['symbol'],
                'side': order['side'],
                'type': order['type'],
                'quantity': float(order['origQty']),
                'price': float(order['price']),
                'timestamp': order['updateTime']
            }
            
        except BinanceOrderException as e:
            error_msg = f"Order error for {symbol}: {e}"
            self.logger.error(error_msg)
            return {'status': 'error', 'message': error_msg}
        except BinanceAPIException as e:
            error_msg = f"API error for {symbol}: {e}"
            self.logger.error(error_msg)
            return {'status': 'error', 'message': error_msg}
        except Exception as e:
            error_msg = f"Unexpected error for {symbol}: {e}"
            self.logger.error(error_msg)
            return {'status': 'error', 'message': error_msg}
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: float, 
                             price: float, stop_price: float) -> Dict:
        """Place a stop-limit order (Bonus feature)"""
        try:
            self.logger.info(f"Placing stop-limit order: {symbol} {side} {quantity} @ {price}, stop: {stop_price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='STOP_LOSS_LIMIT',
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                timeInForce='GTC'
            )
            
            self.logger.info(f"Stop-limit order placed successfully: {order}")
            return {
                'status': 'success',
                'order_id': order['orderId'],
                'symbol': order['symbol'],
                'side': order['side'],
                'type': order['type'],
                'quantity': float(order['origQty']),
                'price': float(order['price']),
                'stop_price': float(order['stopPrice']),
                'timestamp': order['updateTime']
            }
            
        except BinanceOrderException as e:
            error_msg = f"Stop-limit order error for {symbol}: {e}"
            self.logger.error(error_msg)
            return {'status': 'error', 'message': error_msg}
        except BinanceAPIException as e:
            error_msg = f"API error for stop-limit {symbol}: {e}"
            self.logger.error(error_msg)
            return {'status': 'error', 'message': error_msg}
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict:
        """Check order status"""
        try:
            order_status = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            return {
                'status': 'success',
                'order_status': order_status['status'],
                'executed_quantity': float(order_status['executedQty']),
                'cumulative_quote_qty': float(order_status['cumulativeQuoteQty'])
            }
        except BinanceAPIException as e:
            error_msg = f"Error fetching order status: {e}"
            self.logger.error(error_msg)
            return {'status': 'error', 'message': error_msg}