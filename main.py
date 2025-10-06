# main.py
#!/usr/bin/env python3
import argparse
import os
from dotenv import load_dotenv
from bot.base_bot import BaseTradingBot
from bot.order_manager import OrderManager
from bot.utils import validate_input, format_order_output

def setup_environment():
    """Load environment variables"""
    load_dotenv()
    
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        print("❌ Error: Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables")
        print("Create a .env file with your Binance Testnet credentials")
        exit(1)
    
    return api_key, api_secret

def main():
    """Main CLI application"""
    parser = argparse.ArgumentParser(description='Binance Futures Trading Bot')
    
    # Required arguments
    parser.add_argument('symbol', help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('side', choices=['buy', 'sell'], help='Order side')
    parser.add_argument('order_type', choices=['market', 'limit', 'stop_limit'], 
                       help='Order type')
    parser.add_argument('quantity', type=float, help='Order quantity')
    
    # Optional arguments
    parser.add_argument('--price', type=float, help='Limit price (for limit orders)')
    parser.add_argument('--stop-price', type=float, help='Stop price (for stop-limit orders)')
    
    args = parser.parse_args()
    
    # Convert to dictionary for validation
    args_dict = {
        'symbol': args.symbol,
        'side': args.side,
        'order_type': args.order_type,
        'quantity': args.quantity,
        'price': args.price,
        'stop_price': args.stop_price
    }
    
    # Validate input
    is_valid, validation_msg = validate_input(args_dict)
    if not is_valid:
        print(f"❌ Validation Error: {validation_msg}")
        return
    
    try:
        # Initialize bot
        api_key, api_secret = setup_environment()
        bot = BaseTradingBot(api_key, api_secret, testnet=True)
        order_manager = OrderManager(bot.client, bot.logger)
        
        # Validate symbol
        if not bot.validate_symbol(args.symbol):
            print(f"❌ Error: Invalid symbol {args.symbol}")
            return
        
        # Display account balance
        print("📊 Checking account balance...")
        balances = bot.get_account_balance()
        if balances:
            print("Account Balances:")
            for asset, balance in balances.items():
                print(f"  {asset}: {balance}")
        
        # Place order based on type
        print(f"\n🚀 Placing {args.order_type} order...")
        
        if args.order_type == 'market':
            result = order_manager.place_market_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity
            )
        
        elif args.order_type == 'limit':
            result = order_manager.place_limit_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
                price=args.price
            )
        
        elif args.order_type == 'stop_limit':
            result = order_manager.place_stop_limit_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
                price=args.price,
                stop_price=args.stop_price
            )
        
        # Display result
        print("\n" + "="*50)
        print(format_order_output(result))
        print("="*50)
        
        # If order was successful, show status
        if result['status'] == 'success':
            print("\n📈 Checking order status...")
            status = order_manager.get_order_status(args.symbol, result['order_id'])
            if status['status'] == 'success':
                print(f"Order Status: {status['order_status']}")
                print(f"Executed Quantity: {status['executed_quantity']}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()