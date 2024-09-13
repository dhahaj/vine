import json
from typing import List, Optional
from datetime import datetime

class OrderEntry:
    def __init__(self, order_number: str, asin: str, product_name: str, order_type: str,
                 order_date: str, shipped_date: str, cancelled_date: Optional[str], estimated_tax_value: float):
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
            estimated_tax_value=float(data.get("Estimated Tax Value", 0))
        )

    def __str__(self):
        return f"Date: {self.order_date}, Order Number: {self.order_number}, Product: {self.product_name}"

class OrderCollection:
    def __init__(self):
        self.orders = []

    def add_order(self, order: OrderEntry):
        """Add a new order to the collection."""
        self.orders.append(order)

    def remove_order(self, order_number: str):
        """Remove an order from the collection by its order number."""
        self.orders = [order for order in self.orders if order.order_number != order_number]

    def get_order_by_number(self, order_number: str) -> Optional[OrderEntry]:
        """Retrieve an order by its order number."""
        for order in self.orders:
            if order.order_number == order_number:
                return order
        return None

    def load_orders_from_file(self, filename: str):
        """Load orders from a JSON file and add them to the collection."""
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                for entry in data:
                    self.add_order(OrderEntry.from_dict(entry))
        except FileNotFoundError:
            print(f"No file found with the name {filename}")
        except json.JSONDecodeError:
            print("Error decoding JSON from file.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def filter_orders_by_date(self, start_date: str, end_date: str) -> List[OrderEntry]:
        """Filter orders by a date range."""
        start = datetime.strptime(start_date, "%m/%d/%Y")
        end = datetime.strptime(end_date, "%m/%d/%Y")
        filtered_orders = [
            order for order in self.orders
            if datetime.strptime(order.order_date, "%m/%d/%Y") >= start
            and datetime.strptime(order.order_date, "%m/%d/%Y") <= end
            # and order.cancelled_date is None
        ]
        return filtered_orders
    
    def cancelled_orders(self, start_date: str, end_date: str) -> List[OrderEntry]:
        """Filter orders by a date range."""
        start = datetime.strptime(start_date, "%m/%d/%Y")
        end = datetime.strptime(end_date, "%m/%d/%Y")
        filtered_orders = [
            order for order in self.orders
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
            order for order in self.orders
            if datetime.strptime(order.order_date, "%m/%d/%Y") >= start
            and datetime.strptime(order.order_date, "%m/%d/%Y") <= end
            and order.cancelled_date is None
        ]
        return filtered_orders

def list(data: List[OrderEntry]):
    """Print a list of orders."""
    for order in data:
        print(order)

# Example usage
if __name__ == "__main__":
    order_collection = OrderCollection()
    order_collection.load_orders_from_file("book1.json")
    filtered_orders = order_collection.filter_orders_by_date("03/30/2024", "09/12/2024")
    # i=0
    # for order in filtered_orders:
    #     print(order)
    #     i=i+1
    # print(f"Found {i} orders in the specified date range.")
    
    cancelled_order = order_collection.cancelled_orders("03/30/2024", "09/12/2024")
    not_cancelled = order_collection.noncancelled_orders("03/30/2024", "09/12/2024")
    
    list(cancelled_order)
    
    i = len(cancelled_order)
    j = len(not_cancelled)
    k= len(filtered_orders)
    print(f"{i} cancelled orders, {j} non cancelled orders, {k} ")
