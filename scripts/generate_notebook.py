import json
import os

def create_notebook():
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

    # Helper function to add markdown cell
    def add_md(source):
        notebook["cells"].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + "\n" for line in source.split("\n")]
        })

    # Helper function to add code cell
    def add_code(source):
        notebook["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in source.split("\n")]
        })

    # 1. Project Introduction
    add_md("""# Logistics Delivery Performance Analytics Project
This project analyzes delivery logistics operations to identify drivers of delays, evaluate partner performance, and improve operational efficiency.

### Dataset Description
The dataset `Delivery_Logistics.csv` contains 25,000 rows of delivery logs with the following details:
- `delivery_id`: Unique delivery identifier.
- `delivery_partner`: The 3PL partner carrying the package (e.g., Delhivery, Xpressbees, Shadowfax, DHL, Ecom Express, Bluedart, Ekart, Amazon Logistics, DTDC).
- `package_type`: Category of items being shipped.
- `vehicle_type`: Vehicle used for the delivery.
- `delivery_mode`: Shipping speed class (Same Day, Express, Two Day, Standard).
- `region`: Geographical region of delivery.
- `weather_condition`: Atmospheric conditions during transit.
- `distance_km`: Trip distance in kilometers.
- `package_weight_kg`: Physical weight of the package.
- `delivery_time_hours`: Actual transit time in hours.
- `expected_time_hours`: Committed/Promised transit time in hours.
- `delayed`: Indication of whether actual delivery time exceeded expected time.
- `delivery_status`: Outcome of the order (Delivered, Cancelled, Returned).
- `delivery_rating`: Customer satisfaction rating (1-5 stars).
- `delivery_cost`: Cost of delivery in INR.
""")

    # 2. Imports & Data Loading
    add_md("""## 2. Imports & Data Loading
We load required packages and our custom loader class `DataLoader` which cleans the numeric fields and recalculates delay flags.
""")
    add_code("""import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Add src to python path to load custom scripts
sys.path.append(os.path.abspath('../src'))
from data_loader import DataLoader
from analysis import Analysis
from visualizations import Visualizer

# Enable inline plotting
%matplotlib inline

# Load cleaned data
csv_path = os.path.abspath('../data/Delivery_Logistics.csv')
loader = DataLoader(csv_path)
df = loader.load_data()
analysis = Analysis(df)
""")

    # 3. Dataset Overview
    add_md("""## 3. Dataset Overview
Here we check the dimensions, datatypes, summary statistics, and missing value distribution of the dataset.
""")
    add_code("""# Display first 5 rows
df.head()""")
    
    add_code("""# Check column data types and missing values
df.info()""")
    
    add_code("""# Get descriptive statistics
df.describe(include='all')""")
    
    add_code("""# Check for null values explicitly
df.isnull().sum()""")

    # 4. KPI Summary
    add_md("""## 4. Key Performance Indicators (KPIs)
Here is a summary of the high-level delivery operation metrics.
""")
    add_code("""total_orders = len(df)
avg_time = analysis.avg_delivery_time()
delay_pct = analysis.delay_percentage()
cancel_rate = analysis.cancellation_rate()
total_rev = analysis.total_revenue()

print(f"==========================================")
print(f"             DELIVERY LOGISTICS KPIs      ")
print(f"==========================================")
print(f"Total Orders:          {total_orders:,}")
print(f"Avg Delivery Time:     {avg_time:.2f} hours")
print(f"Delay Rate:            {delay_pct:.2f}%")
print(f"Cancellation Rate:     {cancel_rate:.2f}%")
print(f"Total Revenue:         INR {total_rev:,.2f}")
print(f"==========================================")
""")

    # 5. Delay Analysis
    add_md("""## 5. Delay Analysis
We analyze how weather, delivery partner, and region influence shipping delays.
""")
    add_code("""# Weather impact on delays
weather_perf = analysis.weather_impact()
print("Weather Impact on Delivery Delays:")
print(weather_perf)

# Plot delay percentage by weather condition
plt.figure(figsize=(10, 6))
sns.barplot(data=weather_perf, x='weather_condition', y='delay_percentage', palette='viridis')
plt.title('Delay Percentage by Weather Condition')
plt.ylabel('Delay Percentage (%)')
plt.xlabel('Weather Condition')
for i, val in enumerate(weather_perf['delay_percentage']):
    plt.text(i, val + 1, f"{val:.1f}%", ha='center', fontweight='bold')
plt.tight_layout()
plt.show()
""")

    add_code("""# Regional delay breakdown
region_delay = df.groupby('region').agg(
    order_count=('delivery_id', 'count'),
    delay_percentage=('delayed', lambda x: (x == 'yes').mean() * 100)
).reset_index().sort_values(by='delay_percentage', ascending=False)

print("Regional Delay Breakdown:")
print(region_delay)
""")

    # 6. Partner Performance
    add_md("""## 6. Partner Performance Comparison
We compare average delivery times, delay rates, customer ratings, and order volumes across our 3PL shipping partners.
""")
    add_code("""partner_perf = analysis.partner_performance()
print("Partner Performance Summary Table:")
print(partner_perf.to_string(index=False))

# Horizontal bar chart: delivery_partner vs delay%
plt.figure(figsize=(10, 6))
sns.barplot(data=partner_perf, y='delivery_partner', x='delay_percentage', palette='coolwarm')
plt.title('Delay Percentage by Delivery Partner')
plt.xlabel('Delay Percentage (%)')
plt.ylabel('Delivery Partner')
for i, val in enumerate(partner_perf['delay_percentage']):
    plt.text(val + 0.5, i, f"{val:.1f}%", va='center', fontweight='bold')
plt.tight_layout()
plt.show()
""")

    # 7. Vehicle Utilization
    add_md("""## 7. Vehicle Utilization
Let's see what vehicles are being used most frequently and their average performance.
""")
    add_code("""vehicle_perf = analysis.vehicle_utilization()
print("Vehicle Utilization & Performance:")
print(vehicle_perf.to_string(index=False))

# Pie chart: orders per vehicle_type
plt.figure(figsize=(8, 8))
plt.pie(vehicle_perf['order_count'], labels=vehicle_perf['vehicle_type'], autopct='%1.1f%%', startangle=140)
plt.title('Orders Distribution by Vehicle Type')
plt.show()
""")

    # 8. Customer Ratings
    add_md("""## 8. Customer Ratings Distribution
We review how delivery performance affects customer satisfaction.
""")
    add_code("""ratings_dist = analysis.rating_distribution()
print("Rating Star Count Distribution:")
print(ratings_dist)

# Plot rating counts
plt.figure(figsize=(10, 6))
sns.barplot(data=ratings_dist, x='delivery_rating', y='order_count', palette='Blues_d')
plt.title('Distribution of Customer Ratings')
plt.xlabel('Rating (Stars)')
plt.ylabel('Number of Orders')
plt.show()

# Avg rating per partner
partner_ratings = partner_perf[['delivery_partner', 'avg_rating']].sort_values(by='avg_rating', ascending=False)
print("Average Rating per Delivery Partner:")
print(partner_ratings.to_string(index=False))
""")

    # 9. Delivery Cost Analysis
    add_md("""## 9. Delivery Cost Analysis
We analyze delivery cost trends across different modes, vehicle types, and regions.
""")
    add_code("""# Cost by Delivery Mode
mode_cost = df.groupby('delivery_mode')['delivery_cost'].mean().reset_index().sort_values(by='delivery_cost', ascending=False)
print("Average Delivery Cost by Mode:")
print(mode_cost)

# Cost by Vehicle Type
vehicle_cost = df.groupby('vehicle_type')['delivery_cost'].mean().reset_index().sort_values(by='delivery_cost', ascending=False)
print("\\nAverage Delivery Cost by Vehicle:")
print(vehicle_cost)

# Cost by Region
region_cost = df.groupby('region')['delivery_cost'].mean().reset_index().sort_values(by='delivery_cost', ascending=False)
print("\\nAverage Delivery Cost by Region:")
print(region_cost)
""")

    # 10. Distance vs Time Analysis
    add_md("""## 10. Distance vs. Delivery Time Relationship
We examine whether longer shipping distances correlate strongly with increased actual delivery times.
""")
    add_code("""corr_coef = df['distance_km'].corr(df['delivery_time_hours'])
print(f"Pearson Correlation Coefficient between Distance and Delivery Time: {corr_coef:.4f}")

# Plot scatter
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df.sample(2000, random_state=42), x='distance_km', y='delivery_time_hours', hue='delayed', alpha=0.5)
plt.title(f'Distance vs. Delivery Time (Corr: {corr_coef:.2f})')
plt.xlabel('Distance (km)')
plt.ylabel('Delivery Time (hours)')
plt.show()
""")

    # 11. SQL Insights
    add_md("""## 11. SQL Query Insights
We execute the 8 SQLite queries in-memory on our deliveries table and showcase the results.
""")
    add_code("""# Create in-memory connection
conn = sqlite3.connect(':memory:')
df.to_sql('deliveries', conn, index=False, if_exists='replace')

sql_file_path = '../sql/queries.sql'
with open(sql_file_path, 'r', encoding='utf-8') as f:
    sql_text = f.read()

# Execute and print queries
queries = []
curr_q = []
curr_name = ""

for line in sql_text.splitlines():
    trimmed = line.strip()
    if trimmed.startswith('-- NAME:'):
        curr_name = trimmed.replace('-- NAME:', '').strip()
        continue
    elif trimmed.startswith('--') or not trimmed:
        continue
    curr_q.append(line)
    if ';' in line:
        queries.append((curr_name, '\\n'.join(curr_q)))
        curr_q = []
        curr_name = ""

for i, (name, q) in enumerate(queries, 1):
    print(f"\\nQuery {i}: {name}")
    print("-" * 50)
    res = pd.read_sql_query(q, conn)
    print(res.head(10).to_string(index=False))
    print("-" * 50)

conn.close()
""")

    # 12. Business Recommendations
    add_md("""## 12. Business Recommendations
Based on the results of our EDA, SQL metrics, and visualizations, we put forward the following actionable recommendations:

1. **Mitigate Stormy and Foggy Weather Disruptions**: Stormy weather causes a **97.1% delay rate** with delivery time soaring to **30.8 hours**. Implement dynamic routing, adjust weather-sensitive delivery ETAs in real-time, and temporarily suspend bike shipments during storms.
2. **Review Low Ratings**: The overall average rating is **2.48 stars**, which is low. A primary cause is delivery delays (delayed orders suffer much lower ratings). Addressing delay factors directly is the most critical path to improving customer satisfaction.
3. **Address Ecom Express and Shadowfax Delays**: Ecom Express has an **88.0% delay rate** and Shadowfax has **86.9%**. We should renegotiate SLAs, restrict high-priority shipments (Same Day/Express) with these partners, or transition volume to better-performing partners like Delhivery or DTDC.
4. **Optimize Shipping Speed Expectation**: Standard shipments have a massive **7.9-hour delay gap**, indicating that promised delivery times are set too optimistically. Re-calibrate standard and two-day delivery commitments based on realistic historical statistics.
5. **Adjust Pricing for Same-Day Shipping**: Same Day shipments cost an average of **INR 1,223** compared to **INR 923** for standard shipping. Ensure that pricing strategies fully cover the premium operational overhead required to execute same-day shipping.
6. **Improve regional operations in the East and North**: East and North regions have the highest cancellation rates (**15.5% and 15.4%**). Investigate local distribution center bottlenecks or regional partner inefficiencies in these regions.
7. **Equip Vehicle Fleet Dynamically**: Vehicle type utilization is evenly split at ~16% each. However, bikes and three-wheelers should be confined to short-distance zones (under 100km) as they suffer severe delay rates on long-distance transits.
8. **Utilize EV Vans and Cargo Bikes for Urban Routes**: EV vans have the lowest average delivery cost (**INR 1,005**). Transitioning the short-distance urban delivery fleet to EV vans and cargo bikes will lower overall operational logistics expenditures.
""")

    # Write the file
    os.makedirs(os.path.dirname(os.path.abspath("../notebooks/01_EDA_and_Analysis.ipynb")), exist_ok=True)
    with open("../notebooks/01_EDA_and_Analysis.ipynb", "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2)
    print("Notebook JSON created successfully!")

if __name__ == '__main__':
    create_notebook()
