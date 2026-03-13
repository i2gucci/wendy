"""
Example script showing different ways to use the Wendy's Bot
"""

from wendys_bot import WendysBot
from order_config import OrderBuilder, create_quick_order, COMBO_MEALS
import os


def example_1_simple_order():
    """Example 1: Simple order with individual items."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Simple Order with Individual Items")
    print("="*60)
    
    # Create bot instance
    bot = WendysBot(headless=False, slow_mo=1500)
    
    # Define order
    order = {
        'delivery_method': 'pickup',
        'location': '10001',  # Replace with your ZIP code
        'items': [
            {'name': "Dave's Single", 'customizations': None},
            {'name': 'Medium Fries', 'customizations': None},
            {'name': 'Small Frosty', 'customizations': None}
        ]
    }
    
    # Place order
    bot.place_order(order)


def example_2_combo_meal():
    """Example 2: Using pre-configured combo meals."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Order Using Pre-Configured Combo")
    print("="*60)
    
    # Create bot instance
    bot = WendysBot(headless=False, slow_mo=1500)
    
    # Use quick order function with a combo
    order = create_quick_order(
        combo_name='baconator_combo',
        location='10001',  # Replace with your ZIP code
        delivery_method='pickup'
    )
    
    # Place order
    bot.place_order(order)


def example_3_order_builder():
    """Example 3: Using OrderBuilder for flexible order creation."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Using OrderBuilder")
    print("="*60)
    
    # Build order using OrderBuilder
    builder = OrderBuilder()
    
    order = (builder
        .set_delivery_method('pickup')
        .set_location('10001')  # Replace with your ZIP code
        .add_item("Baconator")
        .add_item("Large Fries")
        .add_item("Medium Frosty")
        .add_item("10 Pc. Chicken Nuggets")
        .build()
    )
    
    # Create bot and place order
    bot = WendysBot(headless=False, slow_mo=1500)
    bot.place_order(order)


def example_4_multiple_combos():
    """Example 4: Ordering multiple items for a group."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Multiple Combos for a Group")
    print("="*60)
    
    # Build large order
    builder = OrderBuilder()
    
    order = (builder
        .set_delivery_method('pickup')
        .set_location('10001')  # Replace with your ZIP code
        .add_combo('daves_single_combo')
        .add_combo('spicy_chicken_combo')
        .add_combo('nuggets_combo')
        .add_item('Large Fries')  # Extra fries
        .add_item('Large Frosty')  # Extra frosty
        .build()
    )
    
    # Create bot and place order
    bot = WendysBot(headless=False, slow_mo=1500)
    bot.place_order(order)


def example_5_delivery_order():
    """Example 5: Delivery order."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Delivery Order")
    print("="*60)
    
    # Create bot instance
    bot = WendysBot(headless=False, slow_mo=1500)
    
    # Define delivery order
    order = {
        'delivery_method': 'delivery',
        'location': '10001',  # Replace with your address/ZIP
        'items': [
            {'name': "Baconator", 'customizations': None},
            {'name': 'Large Fries', 'customizations': None},
            {'name': 'Medium Coke', 'customizations': None}
        ]
    }
    
    # Place order
    bot.place_order(order)


def show_menu():
    """Display the menu."""
    print("\n" + "="*60)
    print("WENDY'S MENU REFERENCE")
    print("="*60)
    
    builder = OrderBuilder()
    builder.show_menu()
    builder.show_combos()


if __name__ == "__main__":
    print("Wendy's Bot - Example Scripts")
    print("="*60)
    print("\nAvailable examples:")
    print("1. Simple order with individual items")
    print("2. Order using pre-configured combo meal")
    print("3. Using OrderBuilder for flexible order creation")
    print("4. Multiple combos for a group order")
    print("5. Delivery order")
    print("6. Show menu and combos")
    print("0. Exit")
    
    while True:
        choice = input("\nEnter example number (0-6): ").strip()
        
        if choice == "1":
            example_1_simple_order()
        elif choice == "2":
            example_2_combo_meal()
        elif choice == "3":
            example_3_order_builder()
        elif choice == "4":
            example_4_multiple_combos()
        elif choice == "5":
            example_5_delivery_order()
        elif choice == "6":
            show_menu()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
