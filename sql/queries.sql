-- SQL Queries for Delivery Performance Analytics (Table Name: deliveries)

-- Query 1: Total orders, avg delivery time, avg rating, total revenue
-- NAME: Query 1: Overall KPIs
SELECT 
    COUNT(*) AS total_orders,
    AVG(delivery_time_hours) AS avg_delivery_time_hours,
    AVG(delivery_rating) AS avg_rating,
    SUM(delivery_cost) AS total_revenue
FROM deliveries;

-- Query 2: Delay percentage by delivery partner (ORDER BY delay% DESC)
-- NAME: Query 2: Delay Percentage by Delivery Partner
SELECT 
    delivery_partner,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN delayed = 'yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS delay_percentage
FROM deliveries
GROUP BY delivery_partner
ORDER BY delay_percentage DESC;

-- Query 3: Top 5 worst weather conditions by avg delivery time
-- NAME: Query 3: Top 5 Worst Weather Conditions by Avg Delivery Time
SELECT 
    weather_condition,
    AVG(delivery_time_hours) AS avg_delivery_time_hours,
    SUM(CASE WHEN delayed = 'yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS delay_percentage
FROM deliveries
GROUP BY weather_condition
ORDER BY avg_delivery_time_hours DESC
LIMIT 5;

-- Query 4: Orders and avg cost by vehicle type
-- NAME: Query 4: Orders and Avg Cost by Vehicle Type
SELECT 
    vehicle_type,
    COUNT(*) AS total_orders,
    AVG(delivery_cost) AS avg_cost
FROM deliveries
GROUP BY vehicle_type
ORDER BY total_orders DESC;

-- Query 5: Cancellation rate by region
-- NAME: Query 5: Cancellation Rate by Region
SELECT 
    region,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN delivery_status = 'cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS cancellation_rate
FROM deliveries
GROUP BY region
ORDER BY cancellation_rate DESC;

-- Query 6: Average delay gap (delivery_time - expected_time) by delivery mode
-- NAME: Query 6: Average Delay Gap by Delivery Mode
SELECT 
    delivery_mode,
    AVG(delivery_time_hours - expected_time_hours) AS avg_delay_gap_hours
FROM deliveries
GROUP BY delivery_mode
ORDER BY avg_delay_gap_hours DESC;

-- Query 7: Partner with highest average rating
-- NAME: Query 7: Partner with Highest Average Rating
SELECT 
    delivery_partner,
    AVG(delivery_rating) AS avg_rating,
    COUNT(*) AS total_orders
FROM deliveries
GROUP BY delivery_partner
ORDER BY avg_rating DESC
LIMIT 1;

-- Query 8: Region-wise revenue breakdown
-- NAME: Query 8: Region-wise Revenue Breakdown
SELECT 
    region,
    SUM(delivery_cost) AS total_revenue,
    AVG(delivery_cost) AS avg_delivery_cost
FROM deliveries
GROUP BY region
ORDER BY total_revenue DESC;
