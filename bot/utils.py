# bot/utils.py
import argparse
from typing import Dict, Any

def validate_input(args: Dict[str, Any]) -> tuple:
    """Validate and process command line arguments"""
    symbol = args.get('symbol', '').upper()
    side = args.get('side', '').upper()
    order_type = args.get('order_type', '').upper()
    quantity = args.get('quantity', 0.0)
    
    # Validate symbol
    if not symbol:
        return False, "Symbol is required"
    
    # Validate side
    if side not in ['BUY', 'SELL']:
        return False, "Side must be either 'BUY' or 'SELL'"
    
    # Validate order type
    valid_order_types = ['MARKET', 'LIMIT', 'STOP_LIMIT']
    if order_type not in valid_order_types:
        return False, f"Order type must be one of: {', '.join(valid_order_types)}"
    
    # Validate quantity
    if quantity <= 0:
        return False, "Quantity must be greater than 0"
    
    # Validate price for limit orders
    if order_type in ['LIMIT', 'STOP_LIMIT']:
        price = args.get('price', 0.0)
        if price <= 0:
            return False, "Price is required for limit and stop-limit orders"
    
    # Validate stop price for stop-limit orders
    if order_type == 'STOP_LIMIT':
        stop_price = args.get('stop_price', 0.0)
        if stop_price <= 0:
            return False, "Stop price is required for stop-limit orders"
    
    return True, "Validation successful"

def format_order_output(order_result: Dict) -> str:
    """Format order output for display"""
    if order_result['status'] == 'error':
        return f" Order Failed: {order_result['message']}"
    
    output_lines = [
        " Order Placed Successfully!",
        f"Order ID: {order_result['order_id']}",
        f"Symbol: {order_result['symbol']}",
        f"Side: {order_result['side']}",
        f"Type: {order_result['type']}",
        f"Quantity: {order_result['quantity']}",
    ]
    
    if order_result.get('price'):
        output_lines.append(f"Price: {order_result['price']}")
    
    if order_result.get('stop_price'):
        output_lines.append(f"Stop Price: {order_result['stop_price']}")
    
    return "\n".join(output_lines)