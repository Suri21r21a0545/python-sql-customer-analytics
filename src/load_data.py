from pathlib import Path
import pandas as pd
from database import get_connection

BASE_DIR = Path(__file__).resolve().parents[1]

def main():
    customers = pd.read_csv(BASE_DIR / "data" / "customers.csv")
    orders = pd.read_csv(BASE_DIR / "data" / "orders.csv")

    customers["registration_date"] = pd.to_datetime(customers["registration_date"]).dt.date
    orders["order_date"] = pd.to_datetime(orders["order_date"]).dt.date

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM customers")

    customer_sql = """
        INSERT INTO customers
        (customer_id, name, email, city, registration_date)
        VALUES (%s, %s, %s, %s, %s)
    """

    order_sql = """
        INSERT INTO orders
        (order_id, customer_id, product, category, quantity, unit_price, order_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    for row in customers.itertuples(index=False, name=None):
        cursor.execute(customer_sql, row)

    for row in orders.itertuples(index=False, name=None):
        cursor.execute(order_sql, row)

    connection.commit()
    cursor.close()
    connection.close()

    print(f"Loaded {len(customers)} customers.")
    print(f"Loaded {len(orders)} orders.")

if __name__ == "__main__":
    main()
