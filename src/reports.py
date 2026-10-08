from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from database import get_connection

BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_DIR = BASE_DIR / "reports"
VIS_DIR = BASE_DIR / "visualizations"
REPORT_DIR.mkdir(exist_ok=True)
VIS_DIR.mkdir(exist_ok=True)

QUERIES = {
    "customer_summary": """
        SELECT c.customer_id, c.name, COUNT(DISTINCT o.order_id) AS orders,
               ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue
        FROM customers c JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name ORDER BY revenue DESC
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
    """,
    "repeat_customers": """
        SELECT c.customer_id, c.name, COUNT(DISTINCT o.order_id) AS order_count
        FROM customers c JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name
        HAVING COUNT(DISTINCT o.order_id) > 1
        ORDER BY order_count DESC
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

    data = {name: pd.read_sql(query, connection)
            for name, query in QUERIES.items()}
    connection.close()

    top = data["customer_summary"].head(10)
    plt.figure(figsize=(10, 6))
    plt.bar(top["name"], top["revenue"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Top 10 Customers by Revenue")
    plt.xlabel("Customer")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(VIS_DIR / "top_customers.png", dpi=150)
    plt.close()

    monthly = data["monthly_revenue"]
    plt.figure(figsize=(10, 6))
    plt.plot(monthly["month"], monthly["revenue"], marker="o")
    plt.xticks(rotation=45)
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(VIS_DIR / "monthly_revenue.png", dpi=150)
    plt.close()

    products = data["product_summary"].head(10)
    plt.figure(figsize=(10, 6))
    plt.bar(products["product"], products["revenue"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Top Products by Revenue")
    plt.xlabel("Product")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(VIS_DIR / "top_products.png", dpi=150)
    plt.close()

    cities = data["city_summary"]
    plt.figure(figsize=(10, 6))
    plt.bar(cities["city"], cities["revenue"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Revenue by City")
    plt.xlabel("City")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(VIS_DIR / "city_revenue.png", dpi=150)
    plt.close()

    output = REPORT_DIR / "customer_analytics_report.xlsx"
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        kpi.to_excel(writer, sheet_name="KPIs", index=False)
        for name, df in data.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)

    print(f"Excel report: {output}")
    print(f"Charts: {VIS_DIR}")

if __name__ == "__main__":
    main()
