# Wendy's Bot 🍔

An automated bot for placing orders on the Wendy's website using Python and Playwright.

## 🌐 Landing Page

Open [index.html](index.html) in your browser to see the beautiful Wendy's-themed landing page with complete documentation, examples, and menu information!

## Features

- ✅ Automated browser navigation to Wendy's website
- 🎯 Location-based restaurant selection (pickup or delivery)
- 🍔 Add items to cart with customizations
- 🛒 Cart management and checkout navigation
- 📸 Automatic screenshots for debugging
- 🎨 Colorful terminal output with status logging
- 🔧 Flexible order configuration system
- 📦 Pre-configured combo meals
- 🏗️ OrderBuilder pattern for easy order creation

## Prerequisites

- Python 3.8 or higher
- Windows, macOS, or Linux
- Internet connection

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

4. **Configure environment (optional):**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` to customize settings:
   - `HEADLESS_MODE`: Set to `True` for headless browser (default: `False`)
   - `SLOW_MODE`: Set to `False` for faster execution (default: `True`)
   - `SCREENSHOT_ON_ERROR`: Enable error screenshots (default: `True`)

## Quick Start

### Basic Usage

```python
from wendys_bot import WendysBot

# Create bot instance
bot = WendysBot(headless=False, slow_mo=1500)

# Define your order
order = {
    'delivery_method': 'pickup',  # or 'delivery'
    'location': '10001',          # Your ZIP code
    'items': [
        {'name': "Dave's Single", 'customizations': None},
        {'name': 'Medium Fries', 'customizations': None},
        {'name': 'Small Frosty', 'customizations': None}
    ]
}

# Place the order
bot.place_order(order)
```

### Using OrderBuilder

```python
from wendys_bot import WendysBot
from order_config import OrderBuilder

# Build order
order = (OrderBuilder()
    .set_delivery_method('pickup')
    .set_location('10001')
    .add_item("Baconator")
    .add_item("Large Fries")
    .add_item("Medium Frosty")
    .build()
)

# Place order
bot = WendysBot(headless=False, slow_mo=1500)
bot.place_order(order)
```

### Using Pre-Configured Combos

```python
from wendys_bot import WendysBot
from order_config import create_quick_order

# Use a pre-configured combo
order = create_quick_order(
    combo_name='baconator_combo',
    location='10001',
    delivery_method='pickup'
)

bot = WendysBot(headless=False, slow_mo=1500)
bot.place_order(order)
```

## Available Combos

- `daves_single_combo` - Dave's Single with fries and drink
- `baconator_combo` - Baconator with fries and drink
- `spicy_chicken_combo` - Spicy Chicken Sandwich with fries and drink
- `nuggets_combo` - 10 Piece Nuggets with fries and drink

## Running Examples

The project includes several example scripts:

```bash
python examples.py
```

This will show an interactive menu with different ordering scenarios:
1. Simple order with individual items
2. Order using pre-configured combo meal
3. Using OrderBuilder for flexible order creation
4. Multiple combos for a group order
5. Delivery order
6. Show menu and combos

## Project Structure

```
food-bot/
├── wendys_bot.py          # Main bot implementation
├── order_config.py        # Order configuration and menu helpers
├── examples.py            # Example usage scripts
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
├── .gitignore            # Git ignore rules
├── screenshots/          # Auto-generated screenshots (created at runtime)
└── README.md             # This file
```

## Configuration Options

### Bot Parameters

- `headless` (bool): Run browser in headless mode (default: `False`)
- `slow_mo` (int): Slow down operations by milliseconds (default: `1500`)

### Order Configuration

```python
order = {
    'delivery_method': 'pickup',  # 'pickup' or 'delivery'
    'location': '10001',          # ZIP code
    'items': [
        {
            'name': 'Item Name',
            'customizations': {
                'option': 'value'
            }
        }
    ]
}
```

## Menu Items

The bot includes a reference to popular Wendy's menu items:

### Burgers
- Dave's Single, Double, Triple
- Baconator, Son of Baconator
- Jr. Bacon Cheeseburger
- And more...

### Chicken
- Chicken Nuggets (4, 6, 10 piece)
- Crispy/Spicy Chicken Sandwich
- Asiago Ranch Chicken Club

### Sides
- Fries (Small, Medium, Large)
- Chili
- Baked Potato

### Drinks
- Frosty (Small, Medium, Large)
- Soft drinks
- Lemonade

## Important Notes

⚠️ **Security & Payment:**
- The bot intentionally does NOT automate payment processing for security reasons
- The bot will navigate to checkout where you should manually complete payment
- Never store payment credentials in code or configuration files

⚠️ **Usage Disclaimer:**
- This bot is for educational and personal use only
- Use responsibly and in accordance with Wendy's terms of service
- The bot may break if Wendy's updates their website structure
- Always verify your order before completing payment

⚠️ **Website Changes:**
- Wendy's website structure may change over time
- The bot includes multiple selectors to handle variations
- Screenshots are automatically saved for debugging if issues occur

## Troubleshooting

### Bot can't find elements

The Wendy's website may have changed. Check the screenshots in the `screenshots/` folder to see what the bot is encountering.

### Browser doesn't start

Make sure Playwright browsers are installed:
```bash
playwright install chromium
```

### Items not found

Verify the exact item names on Wendy's website. The bot searches for text matches, so names must be accurate.

### Slow performance

You can speed up the bot by:
- Reducing `slow_mo` parameter
- Setting `SLOW_MODE=False` in `.env`

## Customization

### Adding New Menu Items

Edit `order_config.py` and add items to the `MENU_ITEMS` dictionary:

```python
MENU_ITEMS = {
    "burgers": [
        "Your New Burger Name",
        # ... existing items
    ]
}
```

### Creating New Combos

Add combo configurations in `order_config.py`:

```python
COMBO_MEALS = {
    "your_combo": {
        "name": "Your Combo Name",
        "items": [
            {"name": "Item 1", "customizations": None},
            {"name": "Item 2", "customizations": None}
        ]
    }
}
```

## Advanced Usage

### Custom Wait Times

```python
bot = WendysBot(headless=False, slow_mo=2000)  # Slower for debugging
```

### Headless Mode

```python
bot = WendysBot(headless=True, slow_mo=0)  # Fast headless execution
```

### Taking Manual Screenshots

```python
bot.take_screenshot("my_custom_screenshot")
```

## Contributing

Feel free to enhance this bot:
- Add more robust element selectors
- Implement customization options
- Add support for promotional codes
- Improve error handling

## License

This project is for educational purposes. Use at your own risk and responsibility.

## Support

If you encounter issues:
1. Check the `screenshots/` folder for visual debugging
2. Review terminal output for error messages
3. Verify menu item names match Wendy's current offerings
4. Ensure your ZIP code is valid and has nearby Wendy's locations

---

**Enjoy your automated Wendy's orders!** 🍟🍔🥤
