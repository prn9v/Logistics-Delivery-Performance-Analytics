import csv
import random
import os

def generate_dataset(output_path, num_rows=25000):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    partners = ['delhivery', 'xpressbees', 'shadowfax', 'dhl', 'ecom express', 'bluedart', 'ekart', 'amazon logistics', 'dtdc']
    packages = ['electronics', 'groceries', 'clothing', 'cosmetics', 'automobile parts', 'furniture', 'books', 'medical', 'food']
    vehicles = ['bike', 'van', 'truck', 'ev van', 'cargo bike', 'three wheeler']
    modes = ['same day', 'express', 'two day', 'standard']
    regions = ['north', 'south', 'east', 'west', 'central']
    weather_conds = ['clear', 'rainy', 'foggy', 'cold', 'stormy', 'windy']
    statuses = ['delivered', 'cancelled', 'returned']
    status_weights = [0.75, 0.15, 0.10]
    
    headers = [
        'delivery_id', 'delivery_partner', 'package_type', 'vehicle_type', 
        'delivery_mode', 'region', 'weather_condition', 'distance_km', 
        'package_weight_kg', 'delivery_time_hours', 'expected_time_hours', 
        'delayed', 'delivery_status', 'delivery_rating', 'delivery_cost'
    ]
    
    random.seed(42)  # For reproducibility
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for i in range(num_rows):
            delivery_id = float(100000 + i)
            partner = random.choice(partners)
            package = random.choice(packages)
            vehicle = random.choice(vehicles)
            mode = random.choice(modes)
            region = random.choice(regions)
            weather = random.choice(weather_conds)
            
            # Distance: 5 to 500 km
            distance = round(random.uniform(5.0, 500.0), 2)
            
            # Package weight: 0.5 to 50 kg
            weight = round(random.uniform(0.5, 50.0), 2)
            
            # Expected time: 2 to 48 hours, correlated to distance
            # Let's base expected time roughly on distance and mode
            base_expected = (distance / 15.0) + 2.0  # standard base
            if mode == 'same day':
                expected = random.uniform(2.0, 12.0)
            elif mode == 'express':
                expected = random.uniform(6.0, 24.0)
            else:
                expected = random.uniform(12.0, 48.0)
            
            # Cap expected time at [2.0, 48.0]
            expected = max(2.0, min(48.0, round(expected, 2)))
            
            # Delivery time: 2 to 72 hours, influenced by weather, partner, and vehicle
            # Delay factor increases with stormy/rainy weather and certain partners
            delay_factor = 1.0
            if weather == 'stormy':
                delay_factor += random.uniform(0.2, 0.6)
            elif weather == 'rainy':
                delay_factor += random.uniform(0.1, 0.4)
            elif weather == 'foggy':
                delay_factor += random.uniform(0.15, 0.35)
                
            if partner in ['ecom express', 'shadowfax']:
                delay_factor += random.uniform(0.05, 0.2)
                
            if vehicle in ['bike', 'three wheeler'] and distance > 200:
                delay_factor += random.uniform(0.2, 0.5)
                
            # Random variation
            delay_factor *= random.uniform(0.7, 1.3)
            
            # Calculate actual delivery time
            delivery_time = expected * delay_factor
            # Add some baseline random noise
            delivery_time += random.uniform(-1.0, 2.0)
            
            # Ensure it fits in [2.0, 72.0]
            delivery_time = max(2.0, min(72.0, round(delivery_time, 2)))
            
            # Delayed flag
            delayed = 'yes' if delivery_time > expected else 'no'
            
            # Delivery status (weighted: 75% delivered, 15% cancelled, 10% returned)
            status = random.choices(statuses, weights=status_weights, k=1)[0]
            
            # Rating: 1 to 5. Correlated to delay and status
            if status in ['cancelled', 'returned']:
                rating = random.choice([1, 2])
            else:
                if delayed == 'yes':
                    # delayed deliveries get lower ratings on average
                    rating = random.choices([1, 2, 3, 4], weights=[0.2, 0.3, 0.4, 0.1], k=1)[0]
                else:
                    rating = random.choices([3, 4, 5], weights=[0.1, 0.4, 0.5], k=1)[0]
            
            # Cost: 100 to 2000 INR
            # Base cost on distance, weight, and mode
            cost_factor = 1.0
            if mode == 'same day':
                cost_factor = 1.5
            elif mode == 'express':
                cost_factor = 1.25
                
            base_cost = 100.0 + (distance * 2.5) + (weight * 5.0)
            cost = base_cost * cost_factor * random.uniform(0.9, 1.1)
            cost = max(100.0, min(2000.0, round(cost, 2)))
            
            writer.writerow([
                delivery_id, partner, package, vehicle, mode, region, weather,
                distance, weight, delivery_time, expected, delayed, status,
                rating, cost
            ])

if __name__ == '__main__':
    print("Generating synthetic dataset...")
    generate_dataset('data/Delivery_Logistics.csv', 25000)
    print("Dataset generation completed! Saved to 'data/Delivery_Logistics.csv'.")
