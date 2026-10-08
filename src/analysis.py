import pandas as pd
from database import get_connection

QUERIES = {
    "customer_summary": """
        SELECT c.customer_id, c.name,
               COUNT(DISTINCT o.order_id) AS orders,
               ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name
        ORDER BY revenue DESC
    """,
    "product_summary": """
        SELECT product, SUM(quantity) AS units_sold,
               ROUND(SUM(quantity * unit_price), 2) AS revenue
        FROM orders GROUP BY product ORDER BY revenue DESC
    """,
    "category_summary": """
        SELECT category, SUM(quantity) AS units_sold,
               ROUND(SUM(quantity * unit_price), 2) AS revenue
        FROM orders GROUP BY category ORDER BY revenue DESC
    """,
    "city_summary": """
        SELECT c.city, COUNT(DISTINCT c.customer_id) AS customers,
               ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue
        FROM customers c JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.city ORDER BY revenue DESC
    """,
    "monthly_revenue": """
        SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
               ROUND(SUM(quantity * unit_price), 2) AS revenue
        FROM orders
        GROUP BY DATE_FORMAT(order_date, '%Y-%m') ORDER BY month
    """
}

def main():
    connection = get_connection()

    kpi = pd.read_sql("""
        SELECT
          (SELECT COUNT(*) FROM customers) AS total_customers,
          (SELECT COUNT(*) FROM orders) AS total_orders,
          (SELECT ROUND(SUM(quantity * unit_price), 2) FROM orders) AS total_revenue,
          (SELECT ROUND(SUM(quantity * unit_price) /
                        COUNT(DISTINCT order_id), 2) FROM orders) AS average_order_value
    """, connection)

    print("\n=== KPIs ===")
    print(kpi.to_string(index=False))

    for name, query in QUERIES.items():
        print(f"\n=== {name.upper()} ===")
        print(pd.read_sql(query, connection).head(10).to_string(index=False))

    connection.close()

if __name__ == "__main__":
    main()
