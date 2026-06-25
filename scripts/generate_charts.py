import sys
import os

# Add src/ to the path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.data_loader import DataLoader
from src.visualizations import Visualizer

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'data', 'Delivery_Logistics.csv')
    output_dir = os.path.join(base_dir, 'outputs', 'charts')
    
    loader = DataLoader(csv_path)
    df = loader.load_data()
    
    visualizer = Visualizer(df, output_dir=output_dir)
    visualizer.generate_all()
    print("All charts generated and saved successfully!")

if __name__ == '__main__':
    main()
