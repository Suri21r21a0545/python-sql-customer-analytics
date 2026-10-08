USE customer_analytics;

SELECT COUNT(*) AS total_customers FROM customers;

SELECT COUNT(*) AS total_orders FROM orders;

SELECT ROUND(SUM(quantity * unit_price), 2) AS total_revenue
FROM orders;

SELECT ROUND(SUM(quantity * unit_price) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM orders;

SELECT c.customer_id, c.name,
       COUNT(DISTINCT o.order_id) AS orders,
       ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY revenue DESC;

SELECT product,
       SUM(quantity) AS units_sold,
       ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
GROUP BY product
ORDER BY revenue DESC;

SELECT category,
       SUM(quantity) AS units_sold,
       ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
GROUP BY category
ORDER BY revenue DESC;

SELECT c.city,
       COUNT(DISTINCT c.customer_id) AS customers,
       ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY revenue DESC;

SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
       ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;

SELECT c.customer_id, c.name,
       COUNT(DISTINCT o.order_id) AS order_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(DISTINCT o.order_id) > 1
ORDER BY order_count DESC;
