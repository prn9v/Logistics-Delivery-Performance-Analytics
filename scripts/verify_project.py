import os
import sys
import pandas as pd

# Add src to the path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.data_loader import DataLoader
from src.analysis import Analysis

def verify_all():
    print("=" * 60)
    print("             LOGISTICS ANALYTICS PROJECT VERIFICATION            ")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    errors = 0
    
    # 1. Check Directory Structure
    dirs = [
        'data',
        'notebooks',
        'src',
        'sql',
        'dashboard',
        'outputs/charts',
        'outputs/report'
    ]
    
    print("\n[1] Checking Directory Structure:")
    for d in dirs:
        p = os.path.join(base_dir, d)
        if os.path.exists(p) and os.path.isdir(p):
            print(f"  [OK] {d}/ exists")
        else:
            print(f"  [FAIL] {d}/ is missing")
            errors += 1
            
    # 2. Check Key Files
    files = [
        'data/Delivery_Logistics.csv',
        'notebooks/01_EDA_and_Analysis.ipynb',
        'src/data_loader.py',
        'src/analysis.py',
        'src/visualizations.py',
        'sql/queries.sql',
        'sql/run_sql.py',
        'dashboard/dashboard.py',
        'dashboard/assets/style.css',
        'outputs/report/insights_report.md',
        'requirements.txt',
        'README.md'
    ]
    
    print("\n[2] Checking Key Files:")
    for f in files:
        p = os.path.join(base_dir, f)
        if os.path.exists(p) and os.path.isfile(p):
            print(f"  [OK] {f} exists")
        else:
            print(f"  [FAIL] {f} is missing")
            errors += 1
            
    # 3. Check CSV Dimensions
    csv_path = os.path.join(base_dir, 'data/Delivery_Logistics.csv')
    if os.path.exists(csv_path):
        print("\n[3] Checking Dataset Dimensions:")
        df_raw = pd.read_csv(csv_path)
        rows, cols = df_raw.shape
        print(f"  - Rows: {rows} (Target: 25,000)")
        print(f"  - Columns: {cols}")
        if rows == 25000:
            print("  [OK] Dataset has exactly 25,000 rows")
        else:
            print("  [FAIL] Dataset does not have 25,000 rows")
            errors += 1
    else:
        print("\n[3] Dataset CSV missing, skipping size check.")
        errors += 1
        
    # 4. Check DataLoader Class
    print("\n[4] Testing DataLoader class:")
    try:
        loader = DataLoader(csv_path)
        df_cleaned = loader.load_data()
        print("  [OK] Loader ran successfully")
        
        # Verify columns are floats and delay gap exists
        for col in ['delivery_time_hours', 'expected_time_hours', 'delay_gap_hours']:
            if pd.api.types.is_numeric_dtype(df_cleaned[col]):
                print(f"  [OK] Column '{col}' is numeric float")
            else:
                print(f"  [FAIL] Column '{col}' is not numeric float")
                errors += 1
                
        # Check delayed calculation correctness
        correct_delayed = (df_cleaned['delivery_time_hours'] > df_cleaned['expected_time_hours']).map({True: 'yes', False: 'no'})
        if (df_cleaned['delayed'] == correct_delayed).all():
            print("  [OK] Delayed flag recalculated correctly")
        else:
            print("  [FAIL] Delayed flag recalculation mismatch")
            errors += 1
    except Exception as e:
        print(f"  [FAIL] DataLoader raised an exception: {e}")
        errors += 1
        
    # 5. Check Analysis Methods
    print("\n[5] Testing Analysis class methods:")
    try:
        analysis = Analysis(df_cleaned)
        
        # 1. avg_delivery_time
        adt = analysis.avg_delivery_time()
        print(f"  [OK] avg_delivery_time(): {adt:.2f} hours (Type: {type(adt).__name__})")
        
        # 2. delay_percentage
        dp = analysis.delay_percentage()
        print(f"  [OK] delay_percentage(): {dp:.2f}% (Type: {type(dp).__name__})")
        
        # 3. cancellation_rate
        cr = analysis.cancellation_rate()
        print(f"  [OK] cancellation_rate(): {cr:.2f}% (Type: {type(cr).__name__})")
        
        # 4. total_revenue
        tr = analysis.total_revenue()
        print(f"  [OK] total_revenue(): INR {tr:,.2f} (Type: {type(tr).__name__})")
        
        # 5. orders_by_region
        obr = analysis.orders_by_region()
        print(f"  [OK] orders_by_region(): returned {len(obr)} rows (Type: DataFrame)")
        
        # 6. partner_performance
        pp = analysis.partner_performance()
        print(f"  [OK] partner_performance(): returned {len(pp)} rows (Type: DataFrame)")
        
        # 7. vehicle_utilization
        vu = analysis.vehicle_utilization()
        print(f"  [OK] vehicle_utilization(): returned {len(vu)} rows (Type: DataFrame)")
        
        # 8. weather_impact
        wi = analysis.weather_impact()
        print(f"  [OK] weather_impact(): returned {len(wi)} rows (Type: DataFrame)")
        
        # 9. delivery_mode_analysis
        dma = analysis.delivery_mode_analysis()
        print(f"  [OK] delivery_mode_analysis(): returned {len(dma)} rows (Type: DataFrame)")
        
        # 10. package_type_analysis
        pta = analysis.package_type_analysis()
        print(f"  [OK] package_type_analysis(): returned {len(pta)} rows (Type: DataFrame)")
        
        # 11. rating_distribution
        rd = analysis.rating_distribution()
        print(f"  [OK] rating_distribution(): returned {len(rd)} rows (Type: DataFrame)")
        
        # 12. top_delayed_partners
        tdp = analysis.top_delayed_partners()
        print(f"  [OK] top_delayed_partners(): returned {len(tdp)} rows (Type: DataFrame)")
        
    except Exception as e:
        print(f"  [FAIL] Analysis class raised an exception: {e}")
        errors += 1
        
    # 6. Check Charts
    print("\n[6] Checking Saved PNG Charts:")
    charts = [
        'delay_by_weather.png',
        'partner_delay.png',
        'vehicle_utilization.png',
        'distance_vs_time.png',
        'rating_distribution.png',
        'region_orders.png',
        'mode_cost_boxplot.png',
        'delay_heatmap.png'
    ]
    for c in charts:
        p = os.path.join(base_dir, 'outputs/charts', c)
        if os.path.exists(p) and os.path.isfile(p):
            print(f"  [OK] Chart saved: {c} ({os.path.getsize(p)} bytes)")
        else:
            print(f"  [FAIL] Chart missing: {c}")
            errors += 1
            
    print("\n" + "=" * 60)
    if errors == 0:
        print("SUCCESS: All verification tests passed successfully!")
    else:
        print(f"FAILURE: Verification complete with {errors} errors.")
    print("=" * 60)
    
    return errors == 0

if __name__ == '__main__':
    verify_all()
