import json
from typing import List, Optional
from datetime import datetime
import argparse
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)


class OrderEntry:
    def __init__(
        self,
        order_number: str,
        asin: str,
        product_name: str,
        order_type: str,
        order_date: str,
        shipped_date: str,
        cancelled_date: Optional[str],
        estimated_tax_value: float,
    ):
        self.order_number = order_number
        self.asin = asin
        self.product_name = product_name
        self.order_type = order_type
        self.order_date = order_date
        self.shipped_date = shipped_date
        self.cancelled_date = cancelled_date
        self.estimated_tax_value = estimated_tax_value

    @classmethod
    def from_dict(cls, data: dict):
        """Create an OrderEntry object from a dictionary."""
        return cls(
            order_number=data.get("Order Number", ""),
            asin=data.get("ASIN", ""),
            product_name=data.get("Product Name", ""),
            order_type=data.get("Order Type", ""),
            order_date=data.get("Order Date", ""),
            shipped_date=data.get("Shipped Date", ""),
            cancelled_date=data.get("Cancelled Date"),
            estimated_tax_value=float(data.get("Estimated Tax Value", 0)),
        )

    def __str__(self):
        return f"Date: {self.order_date}, Order Number: {self.order_number}, Product: {self.product_name}"


class OrderCollection:
    def __init__(self):
        self.orders = []

    def search_by_product_keyword(self, keyword: str) -> List[OrderEntry]:
        """Search for orders where the product name contains a specific keyword."""
        keyword_lower = (
            keyword.lower()
        )  # Convert the keyword to lowercase for case-insensitive comparison.
        filtered_orders = [
            order
            for order in self.orders
            if keyword_lower in order.product_name.lower()
        ]
        return filtered_orders

    def add_order(self, order: OrderEntry):
        """Add a new order to the collection."""
        self.orders.append(order)

    def remove_order(self, order_number: str):
        """Remove an order from the collection by its order number."""
        self.orders = [
            order for order in self.orders if order.order_number != order_number
        ]

    def get_order_by_number(self, order_number: str) -> Optional[OrderEntry]:
        """Retrieve an order by its order number."""
        for order in self.orders:
            if order.order_number == order_number:
                return order
        return None

    def total_costs(self, orders: List[OrderEntry] = None) -> float:
        """Calculate the total cost of all orders."""
        if orders is None:
            return sum((order.estimated_tax_value) for order in self.orders)
        return sum((order.estimated_tax_value) for order in orders)

    def load_orders_from_file(self, filename: str):
        """Load orders from a JSON file and add them to the collection."""
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for entry in data:
                    self.add_order(OrderEntry.from_dict(entry))
            print(Fore.GREEN + f"Successfully loaded orders from {filename}")
        except FileNotFoundError:
            print(Fore.RED + f"No file found with the name {filename}")
        except json.JSONDecodeError:
            print(
                Fore.RED
                + "Error decoding JSON from the file. Please check the file format."
            )
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")

    def filter_orders_by_date(self, start_date: str, end_date: str) -> List[OrderEntry]:
        """Filter orders by a date range."""
        start = datetime.strptime(start_date, "%m/%d/%Y")
        end = datetime.strptime(end_date, "%m/%d/%Y")
        filtered_orders = [
            order
            for order in self.orders
            if datetime.strptime(order.order_date, "%m/%d/%Y") >= start
            and datetime.strptime(order.order_date, "%m/%d/%Y") <= end
        ]
        return filtered_orders

    def cancelled_orders(self, start_date: str, end_date: str) -> List[OrderEntry]:
        """Filter orders by a date range."""
        start = datetime.strptime(start_date, "%m/%d/%Y")
        end = datetime.strptime(end_date, "%m/%d/%Y")
        filtered_orders = [
            order
            for order in self.orders
            if datetime.strptime(order.order_date, "%m/%d/%Y") >= start
            and datetime.strptime(order.order_date, "%m/%d/%Y") <= end
            and order.cancelled_date is not None
        ]
        return filtered_orders

    def noncancelled_orders(self, start_date: str, end_date: str) -> List[OrderEntry]:
        """Filter orders by a date range."""
        start = datetime.strptime(start_date, "%m/%d/%Y")
        end = datetime.strptime(end_date, "%m/%d/%Y")
        filtered_orders = [
            order
            for order in self.orders
            if datetime.strptime(order.order_date, "%m/%d/%Y") >= start
            and datetime.strptime(order.order_date, "%m/%d/%Y") <= end
            and order.cancelled_date is None
        ]
        return filtered_orders


def list(data: List[OrderEntry]):
    """Print a list of orders."""
    for order in data:
        print(
            Fore.BLUE + 'Date: ',
            order.order_date,
            Fore.MAGENTA + 'ASIN: ',
            order.asin,
            Fore.LIGHTYELLOW_EX + "Product: ",
            order.product_name,
            Fore.CYAN + "Cost: ",
            order.estimated_tax_value
        )


import re
from datetime import datetime


def is_valid_date(date_str):
    """Check if the date string is in MM/DD/YYYY format and is a valid date."""
    try:
        datetime.strptime(date_str, "%m/%d/%Y")
        return True
    except ValueError:
        return False


def prompt_for_date(prompt_text):
    """Prompt the user for a date and validate the input."""
    while True:
        date_input = input(prompt_text)
        if is_valid_date(date_input):
            return date_input
        else:
            print(Fore.YELLOW + "Invalid date format. Please use MM/DD/YYYY.")


def main():
    order_collection = OrderCollection()
    while True:
        print(Fore.CYAN + "\nOrder Management System")
        print("1. Load orders from a JSON file")
        print("2. List all orders")
        print("3. Filter orders by date")
        print("4. Search orders by product keyword")
        print("5. List cancelled orders")
        print("6. List non-cancelled orders")
        print("7. Exit")
        choice = input(Fore.BLUE + "Enter your choice (1-7): ")

        if choice == "1":
            filename = input("Enter the filename to load orders from: ")
            order_collection.load_orders_from_file(filename)

        elif choice == "2":
            if order_collection.orders:
                print("Listing all orders:")
                list(order_collection.orders)
                print(
                    Fore.LIGHTCYAN_EX + "Number of orders: ",
                    len(order_collection.orders),
                )
                print(Fore.BLUE + "Total: $", order_collection.total_costs())
            else:
                print("No orders loaded.")

        elif choice == "3":
            start_date = prompt_for_date("Enter start date (MM/DD/YYYY): ")
            end_date = prompt_for_date("Enter end date (MM/DD/YYYY): ")
            filtered_orders = order_collection.filter_orders_by_date(
                start_date, end_date
            )
            if filtered_orders:
                print("Filtered orders:")
                list(filtered_orders)
            else:
                print("No orders found within the specified dates.")

        elif choice == "4":
            keyword = input("Enter a keyword to search in product names: ")
            if keyword:
                keyword_search_results = order_collection.search_by_product_keyword(
                    keyword
                )
                print("Orders matching the keyword search:")
                list(keyword_search_results)
            else:
                print("No keyword provided.")

        elif choice == "5":
            start_date = prompt_for_date("Enter start date (MM/DD/YYYY): ")
            end_date = prompt_for_date("Enter end date (MM/DD/YYYY): ")
            cancelled_orders = order_collection.cancelled_orders(start_date, end_date)
            list(cancelled_orders)

        elif choice == "6":
            start_date = prompt_for_date("Enter start date (MM/DD/YYYY): ")
            end_date = prompt_for_date("Enter end date (MM/DD/YYYY): ")
            non_cancelled_orders = order_collection.noncancelled_orders(
                start_date, end_date
            )
            list(non_cancelled_orders)

        elif choice == "7":
            print(Fore.GREEN + "Exiting the program.")
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
