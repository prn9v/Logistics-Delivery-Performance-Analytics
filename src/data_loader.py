import pandas as pd
import numpy as np
import os

class DataLoader:
    def __init__(self, filepath):
        """
        Initialize DataLoader with the path to the dataset CSV.
        """
        self.filepath = filepath
        
    def load_data(self):
        """
        Loads Delivery_Logistics.csv, performs type fixes and columns calculations,
        and returns a cleaned pandas DataFrame.
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Dataset file not found at: {self.filepath}")
            
        print(f"Loading data from {self.filepath}...")
        df = pd.read_csv(self.filepath)
        
        # 2. Fix the delivery_time_hours and expected_time_hours columns.
        # If they are datetime/timestamp objects (epoch nanoseconds), we convert to numeric float hours.
        for col in ['delivery_time_hours', 'expected_time_hours']:
            if col in df.columns:
                # If df[col] contains datetimes, or is object type, convert to numeric
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    # Extract epoch nanoseconds and divide by 3.6e12
                    df[col] = df[col].astype(np.int64) / 3.6e12
                else:
                    # Coerce conversion to numeric. If strings or other formats, handle them.
                    # First try direct coercion
                    coerced = pd.to_numeric(df[col], errors='coerce')
                    if coerced.isnull().sum() == len(coerced):
                        # If everything is coerced to NaN, it might be a timestamp string format or epoch nanoseconds stored as string
                        try:
                            parsed_dt = pd.to_datetime(df[col], errors='coerce')
                            if parsed_dt.notnull().any():
                                # Conversion succeeded for some, compute from epoch nanoseconds
                                df[col] = parsed_dt.astype(np.int64) / 3.6e12
                            else:
                                df[col] = coerced
                        except Exception:
                            df[col] = coerced
                    else:
                        df[col] = coerced
                        
        # 3. Recalculate delayed column: 'yes' if delivery_time_hours > expected_time_hours, else 'no'
        df['delayed'] = (df['delivery_time_hours'] > df['expected_time_hours']).map({True: 'yes', False: 'no'})
        
        # 4. Add a delay_gap_hours column: delivery_time_hours - expected_time_hours
        df['delay_gap_hours'] = df['delivery_time_hours'] - df['expected_time_hours']
        
        print(f"Data loading and cleaning completed. Loaded {len(df)} rows.")
        return df
