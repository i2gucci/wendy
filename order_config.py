"""
Order configuration and menu helper for Wendy's Bot
"""


# Wendy's popular menu items (simplified)
MENU_ITEMS = {
    "burgers": [
        "Dave's Single",
        "Dave's Double",
        "Dave's Triple",
        "Baconator",
        "Son of Baconator",
        "Bourbon Bacon Cheeseburger",
        "Jr. Bacon Cheeseburger",
        "Jr. Cheeseburger",
        "Crispy Chicken Sandwich",
        "Spicy Chicken Sandwich",
        "Asiago Ranch Chicken Club"
    ],
    "chicken": [
        "10 Pc. Chicken Nuggets",
        "6 Pc. Chicken Nuggets",
        "4 Pc. Chicken Nuggets",
        "Homestyle Chicken Sandwich",
        "Spicy Chicken Sandwich"
    ],
    "sides": [
        "Small Fries",
        "Medium Fries",
        "Large Fries",
        "Cheese Fries",
        "Chili Cheese Fries",
        "Small Chili",
        "Medium Chili",
        "Large Chili",
        "Baked Potato"
    ],
    "drinks": [
        "Small Frosty",
        "Medium Frosty",
        "Large Frosty",
        "Small Coke",
        "Medium Coke",
        "Large Coke",
        "Small Lemonade",
        "Medium Lemonade",
        "Large Lemonade"
    ],
    "breakfast": [
        "Breakfast Baconator",
        "Honey Butter Chicken Biscuit",
        "Sausage Biscuit",
        "Bacon Biscuit",
        "Egg & Cheese Biscuit"
    ]
}


# Pre-configured combo meals
COMBO_MEALS = {
    "daves_single_combo": {
        "name": "Dave's Single Combo",
        "items": [
            {"name": "Dave's Single", "customizations": None},
            {"name": "Medium Fries", "customizations": None},
            {"name": "Medium Coke", "customizations": None}
        ]
    },
    "baconator_combo": {
        "name": "Baconator Combo",
        "items": [
            {"name": "Baconator", "customizations": None},
            {"name": "Medium Fries", "customizations": None},
            {"name": "Medium Coke", "customizations": None}
        ]
    },
    "spicy_chicken_combo": {
        "name": "Spicy Chicken Combo",
        "items": [
            {"name": "Spicy Chicken Sandwich", "customizations": None},
            {"name": "Medium Fries", "customizations": None},
            {"name": "Medium Coke", "customizations": None}
        ]
    },
    "nuggets_combo": {
        "name": "10 Piece Nuggets Combo",
        "items": [
            {"name": "10 Pc. Chicken Nuggets", "customizations": None},
            {"name": "Medium Fries", "customizations": None},
            {"name": "Medium Coke", "customizations": None}
        ]
    }
}


class OrderBuilder:
    """Helper class to build orders programmatically."""
    
    def __init__(self):
        self.items = []
        self.delivery_method = "pickup"
        self.location = None
    
    def set_delivery_method(self, method):
        """Set delivery method (pickup or delivery)."""
        if method.lower() in ['pickup', 'delivery']:
            self.delivery_method = method.lower()
        return self
    
    def set_location(self, location):
        """Set location (ZIP code)."""
        self.location = str(location)
        return self
    
    def add_item(self, item_name, customizations=None):
        """Add a single item to the order."""
        self.items.append({
            "name": item_name,
            "customizations": customizations
        })
        return self
    
    def add_combo(self, combo_name):
        """Add a pre-configured combo meal."""
        if combo_name in COMBO_MEALS:
            combo = COMBO_MEALS[combo_name]
            self.items.extend(combo["items"])
        return self
    
    def build(self):
        """Build and return the order configuration."""
        return {
            "delivery_method": self.delivery_method,
            "location": self.location,
            "items": self.items
        }
    
    def show_menu(self, category=None):
        """Display available menu items."""
        if category and category in MENU_ITEMS:
            print(f"\n{category.upper()}:")
            for item in MENU_ITEMS[category]:
                print(f"  - {item}")
        else:
            print("\n=== WENDY'S MENU ===")
            for cat, items in MENU_ITEMS.items():
                print(f"\n{cat.upper()}:")
                for item in items:
                    print(f"  - {item}")
    
    def show_combos(self):
        """Display available combo meals."""
        print("\n=== COMBO MEALS ===")
        for combo_id, combo in COMBO_MEALS.items():
            print(f"\n{combo['name']} (ID: {combo_id}):")
            for item in combo['items']:
                print(f"  - {item['name']}")


def create_custom_order(delivery_method, location, items):
    """
    Create a custom order configuration.
    
    Args:
        delivery_method (str): 'pickup' or 'delivery'
        location (str): ZIP code
        items (list): List of item dictionaries
    
    Returns:
        dict: Order configuration
    """
    return {
        "delivery_method": delivery_method,
        "location": location,
        "items": items
    }


def create_quick_order(combo_name, location, delivery_method="pickup"):
    """
    Create a quick order using a pre-configured combo.
    
    Args:
        combo_name (str): Name of the combo from COMBO_MEALS
        location (str): ZIP code
        delivery_method (str): 'pickup' or 'delivery'
    
    Returns:
        dict: Order configuration
    """
    if combo_name not in COMBO_MEALS:
        raise ValueError(f"Combo '{combo_name}' not found")
    
    combo = COMBO_MEALS[combo_name]
    return {
        "delivery_method": delivery_method,
        "location": location,
        "items": combo["items"]
    }
