"""
Wendy's Bot - Automated Order Placement
This bot automates ordering from Wendy's website using Playwright.
"""

import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Browser
from colorama import Fore, Style, init
from dotenv import load_dotenv

# Initialize colorama for colored terminal output
init(autoreset=True)

# Load environment variables
load_dotenv()


class WendysBot:
    """Automated bot for placing orders on Wendy's website."""
    
    def __init__(self, headless=False, slow_mo=1000):
        """
        Initialize the Wendy's bot.
        
        Args:
            headless (bool): Run browser in headless mode
            slow_mo (int): Slow down operations by specified milliseconds
        """
        self.headless = headless
        self.slow_mo = slow_mo
        self.browser = None
        self.page = None
        self.playwright = None
        self.screenshot_dir = "screenshots"
        
        # Create screenshot directory
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
    
    def log(self, message, level="INFO"):
        """Log messages with color coding."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if level == "INFO":
            print(f"{Fore.CYAN}[{timestamp}] ℹ {message}{Style.RESET_ALL}")
        elif level == "SUCCESS":
            print(f"{Fore.GREEN}[{timestamp}] ✓ {message}{Style.RESET_ALL}")
        elif level == "WARNING":
            print(f"{Fore.YELLOW}[{timestamp}] ⚠ {message}{Style.RESET_ALL}")
        elif level == "ERROR":
            print(f"{Fore.RED}[{timestamp}] ✗ {message}{Style.RESET_ALL}")
    
    def take_screenshot(self, name):
        """Take a screenshot for debugging."""
        if self.page:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(self.screenshot_dir, f"{name}_{timestamp}.png")
            self.page.screenshot(path=path)
            self.log(f"Screenshot saved: {path}", "INFO")
    
    def start_browser(self):
        """Start the browser instance."""
        self.log("Starting browser...", "INFO")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo
        )
        context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = context.new_page()
        self.log("Browser started successfully", "SUCCESS")
    
    def close_browser(self):
        """Close the browser and cleanup."""
        if self.browser:
            self.log("Closing browser...", "INFO")
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        self.log("Browser closed", "SUCCESS")
    
    def navigate_to_wendys(self):
        """Navigate to Wendy's website."""
        self.log("Navigating to Wendy's website...", "INFO")
        try:
            self.page.goto("https://www.wendys.com/", wait_until="networkidle")
            self.log("Successfully loaded Wendy's homepage", "SUCCESS")
            self.take_screenshot("homepage")
            return True
        except Exception as e:
            self.log(f"Failed to navigate to Wendy's: {str(e)}", "ERROR")
            self.take_screenshot("navigation_error")
            return False
    
    def start_order(self, delivery_method="pickup", location_zip=None):
        """
        Start an order by selecting delivery method and location.
        
        Args:
            delivery_method (str): 'pickup' or 'delivery'
            location_zip (str): ZIP code for location search
        """
        self.log(f"Starting order with {delivery_method} method...", "INFO")
        
        try:
            # Look for "Order Now" or "Start Order" button
            # Wendy's website structure may vary, so we try multiple selectors
            selectors_to_try = [
                "text=Order Now",
                "text=Start Order",
                "a[href*='order']",
                "button:has-text('Order')",
                "[data-testid='order-now']"
            ]
            
            clicked = False
            for selector in selectors_to_try:
                try:
                    if self.page.locator(selector).first.is_visible(timeout=2000):
                        self.page.click(selector, timeout=5000)
                        self.log(f"Clicked order button: {selector}", "SUCCESS")
                        clicked = True
                        break
                except:
                    continue
            
            if not clicked:
                self.log("Could not find order button, trying direct URL...", "WARNING")
                self.page.goto("https://order.wendys.com/", wait_until="networkidle")
            
            time.sleep(2)
            self.take_screenshot("order_start")
            
            # Handle location input if provided
            if location_zip:
                self.set_location(location_zip, delivery_method)
            
            return True
            
        except Exception as e:
            self.log(f"Error starting order: {str(e)}", "ERROR")
            self.take_screenshot("start_order_error")
            return False
    
    def set_location(self, zip_code, delivery_method="pickup"):
        """
        Set the delivery/pickup location.
        
        Args:
            zip_code (str): ZIP code for location
            delivery_method (str): 'pickup' or 'delivery'
        """
        self.log(f"Setting location to ZIP: {zip_code}", "INFO")
        
        try:
            # Select delivery method
            if delivery_method.lower() == "delivery":
                delivery_selectors = [
                    "text=Delivery",
                    "button:has-text('Delivery')",
                    "[data-testid='delivery-button']"
                ]
                for selector in delivery_selectors:
                    try:
                        if self.page.locator(selector).first.is_visible(timeout=2000):
                            self.page.click(selector)
                            break
                    except:
                        continue
            
            # Find and fill location input
            location_selectors = [
                "input[placeholder*='ZIP']",
                "input[placeholder*='address']",
                "input[name='location']",
                "input[type='search']",
                "input[aria-label*='location']"
            ]
            
            for selector in location_selectors:
                try:
                    if self.page.locator(selector).first.is_visible(timeout=2000):
                        self.page.fill(selector, zip_code)
                        self.log(f"Entered ZIP code: {zip_code}", "SUCCESS")
                        time.sleep(1)
                        
                        # Press Enter or click search button
                        self.page.keyboard.press("Enter")
                        time.sleep(2)
                        break
                except:
                    continue
            
            self.take_screenshot("location_set")
            
            # Select first available restaurant
            time.sleep(2)
            restaurant_selectors = [
                "button:has-text('Start Order')",
                "button:has-text('Select')",
                "[data-testid='select-restaurant']"
            ]
            
            for selector in restaurant_selectors:
                try:
                    if self.page.locator(selector).first.is_visible(timeout=3000):
                        self.page.click(selector.replace(".first", "").strip(), timeout=5000)
                        self.log("Selected restaurant", "SUCCESS")
                        break
                except:
                    continue
            
            time.sleep(2)
            self.take_screenshot("restaurant_selected")
            return True
            
        except Exception as e:
            self.log(f"Error setting location: {str(e)}", "ERROR")
            self.take_screenshot("location_error")
            return False
    
    def add_item_to_cart(self, item_name, customizations=None):
        """
        Add an item to the cart.
        
        Args:
            item_name (str): Name of the item to add
            customizations (dict): Optional customizations for the item
        """
        self.log(f"Adding item to cart: {item_name}", "INFO")
        
        try:
            # Search or browse for the item
            # Try to click on the item
            item_selectors = [
                f"text={item_name}",
                f"button:has-text('{item_name}')",
                f"[aria-label*='{item_name}']",
                f"div:has-text('{item_name}')"
            ]
            
            clicked = False
            for selector in item_selectors:
                try:
                    elements = self.page.locator(selector).all()
                    for element in elements:
                        if element.is_visible():
                            element.click()
                            self.log(f"Clicked on item: {item_name}", "SUCCESS")
                            clicked = True
                            break
                    if clicked:
                        break
                except:
                    continue
            
            if not clicked:
                self.log(f"Could not find item: {item_name}", "WARNING")
                return False
            
            time.sleep(2)
            self.take_screenshot(f"item_{item_name.replace(' ', '_')}")
            
            # Apply customizations if provided
            if customizations:
                self.apply_customizations(customizations)
            
            # Click "Add to Order" or similar button
            add_button_selectors = [
                "button:has-text('Add to Order')",
                "button:has-text('Add to Cart')",
                "button:has-text('Add')",
                "[data-testid='add-to-cart']"
            ]
            
            for selector in add_button_selectors:
                try:
                    if self.page.locator(selector).first.is_visible(timeout=2000):
                        self.page.click(selector)
                        self.log(f"Added {item_name} to cart", "SUCCESS")
                        time.sleep(1)
                        break
                except:
                    continue
            
            self.take_screenshot("item_added")
            return True
            
        except Exception as e:
            self.log(f"Error adding item to cart: {str(e)}", "ERROR")
            self.take_screenshot("add_item_error")
            return False
    
    def apply_customizations(self, customizations):
        """
        Apply customizations to an item.
        
        Args:
            customizations (dict): Dictionary of customization options
        """
        self.log("Applying customizations...", "INFO")
        
        for option, value in customizations.items():
            try:
                # Try to find and click/select the customization option
                option_selector = f"text={option}"
                if self.page.locator(option_selector).first.is_visible(timeout=2000):
                    self.page.click(option_selector)
                    self.log(f"Applied customization: {option} = {value}", "SUCCESS")
            except:
                self.log(f"Could not apply customization: {option}", "WARNING")
    
    def view_cart(self):
        """View the shopping cart."""
        self.log("Opening cart...", "INFO")
        
        try:
            cart_selectors = [
                "button[aria-label*='cart']",
                "button:has-text('Cart')",
                "[data-testid='cart-button']",
                "a[href*='cart']"
            ]
            
            for selector in cart_selectors:
                try:
                    if self.page.locator(selector).first.is_visible(timeout=2000):
                        self.page.click(selector)
                        self.log("Cart opened", "SUCCESS")
                        time.sleep(2)
                        self.take_screenshot("cart_view")
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.log(f"Error viewing cart: {str(e)}", "ERROR")
            return False
    
    def proceed_to_checkout(self):
        """Proceed to checkout."""
        self.log("Proceeding to checkout...", "INFO")
        
        try:
            checkout_selectors = [
                "button:has-text('Checkout')",
                "button:has-text('Continue to Checkout')",
                "button:has-text('Review Order')",
                "[data-testid='checkout-button']"
            ]
            
            for selector in checkout_selectors:
                try:
                    if self.page.locator(selector).first.is_visible(timeout=3000):
                        self.page.click(selector)
                        self.log("Proceeding to checkout", "SUCCESS")
                        time.sleep(3)
                        self.take_screenshot("checkout")
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.log(f"Error proceeding to checkout: {str(e)}", "ERROR")
            self.take_screenshot("checkout_error")
            return False
    
    def place_order(self, order_config):
        """
        Complete order placement workflow.
        
        Args:
            order_config (dict): Configuration containing order details
                - delivery_method: 'pickup' or 'delivery'
                - location: ZIP code
                - items: List of items to order
                - payment_method: Payment method (for future implementation)
        """
        self.log("="*50, "INFO")
        self.log("Starting Wendy's Order Bot", "INFO")
        self.log("="*50, "INFO")
        
        try:
            # Start browser
            self.start_browser()
            
            # Navigate to Wendy's
            if not self.navigate_to_wendys():
                return False
            
            # Start order
            if not self.start_order(
                delivery_method=order_config.get('delivery_method', 'pickup'),
                location_zip=order_config.get('location')
            ):
                return False
            
            # Add items to cart
            items = order_config.get('items', [])
            for item in items:
                item_name = item.get('name')
                customizations = item.get('customizations')
                
                if not self.add_item_to_cart(item_name, customizations):
                    self.log(f"Failed to add item: {item_name}", "WARNING")
                
                time.sleep(2)  # Wait between items
            
            # View cart
            self.view_cart()
            time.sleep(2)
            
            # Proceed to checkout
            self.proceed_to_checkout()
            
            # Note: Actual payment processing is intentionally not automated
            # for security reasons. The bot will navigate to checkout where
            # you can manually complete the order.
            
            self.log("="*50, "SUCCESS")
            self.log("Order ready for checkout!", "SUCCESS")
            self.log("Please complete payment manually", "INFO")
            self.log("="*50, "SUCCESS")
            
            # Keep browser open for manual completion
            input("\nPress Enter to close browser...")
            
            return True
            
        except Exception as e:
            self.log(f"Unexpected error during order: {str(e)}", "ERROR")
            self.take_screenshot("critical_error")
            return False
        
        finally:
            self.close_browser()


if __name__ == "__main__":
    # Example usage
    print(f"{Fore.YELLOW}Wendy's Bot - Automated Ordering System{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*50}{Style.RESET_ALL}\n")
    
    # Create bot instance
    bot = WendysBot(
        headless=os.getenv('HEADLESS_MODE', 'False').lower() == 'true',
        slow_mo=1500 if os.getenv('SLOW_MODE', 'True').lower() == 'true' else 0
    )
    
    # Example order configuration
    order = {
        'delivery_method': 'pickup',
        'location': '10001',  # Replace with your ZIP code
        'items': [
            {'name': "Dave's Single", 'customizations': None},
            {'name': 'Medium Fries', 'customizations': None},
            {'name': 'Frosty', 'customizations': None}
        ]
    }
    
    # Place the order
    bot.place_order(order)
