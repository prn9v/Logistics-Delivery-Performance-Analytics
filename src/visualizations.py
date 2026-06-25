import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Visualizer:
    def __init__(self, df, output_dir='outputs/charts'):
        """
        Initialize the Visualizer class with a DataFrame and output directory.
        """
        self.df = df
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Apply professional styling
        sns.set_style('whitegrid')
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

    def _get_path(self, filename):
        return os.path.join(self.output_dir, filename)

    def plot_delay_by_weather(self):
        """
        Grouped bar chart: weather_condition vs delay%
        Saves as delay_by_weather.png
        """
        plt.figure(figsize=(10, 6))
        
        # Calculate delay% per weather condition
        weather_delay = self.df.groupby('weather_condition').agg(
            delay_pct=('delayed', lambda x: (x == 'yes').mean() * 100)
        ).reset_index().sort_values(by='delay_pct', ascending=False)
        
        # Use a nice palette
        sns.barplot(data=weather_delay, x='weather_condition', y='delay_pct', palette='viridis')
        
        plt.title('Delay Percentage by Weather Condition', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Weather Condition', fontsize=12)
        plt.ylabel('Delay Percentage (%)', fontsize=12)
        plt.ylim(0, max(weather_delay['delay_pct']) * 1.15)
        
        # Add value labels on top of the bars
        for idx, row in weather_delay.iterrows():
            plt.text(idx, row['delay_pct'] + 1, f"{row['delay_pct']:.1f}%", ha='center', fontweight='semibold')
            
        plt.tight_layout()
        plt.savefig(self._get_path('delay_by_weather.png'), dpi=300)
        plt.close()

    def plot_partner_performance(self):
        """
        Horizontal bar chart: delivery_partner vs delay%
        Saves as partner_delay.png
        """
        plt.figure(figsize=(10, 6))
        
        # Calculate delay% per partner
        partner_delay = self.df.groupby('delivery_partner').agg(
            delay_pct=('delayed', lambda x: (x == 'yes').mean() * 100)
        ).reset_index().sort_values(by='delay_pct', ascending=False)
        
        sns.barplot(data=partner_delay, y='delivery_partner', x='delay_pct', palette='coolwarm')
        
        plt.title('Delay Percentage by Delivery Partner', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Delay Percentage (%)', fontsize=12)
        plt.ylabel('Delivery Partner', fontsize=12)
        
        # Add value labels
        for i, row in enumerate(partner_delay.itertuples()):
            plt.text(row.delay_pct + 0.5, i, f"{row.delay_pct:.1f}%", va='center', fontweight='semibold')
            
        plt.tight_layout()
        plt.savefig(self._get_path('partner_delay.png'), dpi=300)
        plt.close()

    def plot_vehicle_utilization(self):
        """
        Pie chart: orders per vehicle_type
        Saves as vehicle_utilization.png
        """
        plt.figure(figsize=(10, 6))
        
        vehicle_counts = self.df['vehicle_type'].value_counts()
        colors = sns.color_palette('pastel')[0:len(vehicle_counts)]
        
        plt.pie(
            vehicle_counts, 
            labels=vehicle_counts.index, 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=colors,
            textprops={'fontsize': 11, 'fontweight': 'semibold'},
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
        )
        
        plt.title('Vehicle Type Utilization Share', fontsize=14, fontweight='bold', pad=15)
        plt.tight_layout()
        plt.savefig(self._get_path('vehicle_utilization.png'), dpi=300)
        plt.close()

    def plot_distance_vs_time(self):
        """
        Scatter plot: distance_km vs delivery_time_hours, colored by delayed
        Saves as distance_vs_time.png
        """
        plt.figure(figsize=(10, 6))
        
        # Sample down to 2,000 points if the dataset is too dense, to keep it clean and performant
        sample_df = self.df.sample(min(2000, len(self.df)), random_state=42)
        
        sns.scatterplot(
            data=sample_df, 
            x='distance_km', 
            y='delivery_time_hours', 
            hue='delayed', 
            palette={'yes': '#e74c3c', 'no': '#2ecc71'},
            alpha=0.6,
            edgecolor='w',
            linewidth=0.5
        )
        
        plt.title('Distance vs. Actual Delivery Time (Sampled Points)', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Distance (km)', fontsize=12)
        plt.ylabel('Delivery Time (hours)', fontsize=12)
        plt.legend(title='Delayed', title_fontsize='11', loc='upper left')
        
        plt.tight_layout()
        plt.savefig(self._get_path('distance_vs_time.png'), dpi=300)
        plt.close()

    def plot_rating_distribution(self):
        """
        Bar chart: delivery_rating counts
        Saves as rating_distribution.png
        """
        plt.figure(figsize=(10, 6))
        
        rating_counts = self.df['delivery_rating'].value_counts().sort_index().reset_index()
        rating_counts.columns = ['delivery_rating', 'count']
        
        sns.barplot(data=rating_counts, x='delivery_rating', y='count', palette='Blues_d')
        
        plt.title('Distribution of Customer Delivery Ratings', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Rating (Stars)', fontsize=12)
        plt.ylabel('Number of Deliveries', fontsize=12)
        
        # Add labels
        for idx, row in rating_counts.iterrows():
            plt.text(idx, row['count'] + 100, f"{int(row['count']):,}", ha='center', fontweight='semibold')
            
        plt.tight_layout()
        plt.savefig(self._get_path('rating_distribution.png'), dpi=300)
        plt.close()

    def plot_region_orders(self):
        """
        Bar chart: orders per region
        Saves as region_orders.png
        """
        plt.figure(figsize=(10, 6))
        
        region_counts = self.df['region'].value_counts().reset_index()
        region_counts.columns = ['region', 'count']
        
        sns.barplot(data=region_counts, x='region', y='count', palette='muted')
        
        plt.title('Order Volume by Region', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Region', fontsize=12)
        plt.ylabel('Number of Orders', fontsize=12)
        
        for idx, row in region_counts.iterrows():
            plt.text(idx, row['count'] + 50, f"{int(row['count']):,}", ha='center', fontweight='semibold')
            
        plt.tight_layout()
        plt.savefig(self._get_path('region_orders.png'), dpi=300)
        plt.close()

    def plot_delivery_mode_cost(self):
        """
        Box plot: delivery_cost per delivery_mode
        Saves as mode_cost_boxplot.png
        """
        plt.figure(figsize=(10, 6))
        
        sns.boxplot(data=self.df, x='delivery_mode', y='delivery_cost', palette='Set3')
        
        plt.title('Delivery Cost Distribution by Shipping Mode', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Delivery Mode', fontsize=12)
        plt.ylabel('Delivery Cost (INR)', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(self._get_path('mode_cost_boxplot.png'), dpi=300)
        plt.close()

    def plot_delay_heatmap(self):
        """
        Heatmap: pivot of region vs weather_condition with avg delay%
        Saves as delay_heatmap.png
        """
        plt.figure(figsize=(10, 6))
        
        # Create a pivot table: Region vs Weather with Delay%
        pivot_df = self.df.pivot_table(
            index='region', 
            columns='weather_condition', 
            values='delayed', 
            aggfunc=lambda x: (x == 'yes').mean() * 100
        )
        
        sns.heatmap(
            pivot_df, 
            annot=True, 
            fmt=".1f", 
            cmap='YlOrRd', 
            linewidths=0.5,
            cbar_kws={'label': 'Average Delay Percentage (%)'}
        )
        
        plt.title('Regional Delay Heatmap by Weather Conditions (Average Delay %)', fontsize=14, fontweight='bold', pad=15)
        plt.ylabel('Region', fontsize=12)
        plt.xlabel('Weather Condition', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(self._get_path('delay_heatmap.png'), dpi=300)
        plt.close()

    def generate_all(self):
        """
        Generates and saves all 8 charts.
        """
        print("Generating visualizations...")
        self.plot_delay_by_weather()
        print("1/8. delay_by_weather.png saved.")
        self.plot_partner_performance()
        print("2/8. partner_delay.png saved.")
        self.plot_vehicle_utilization()
        print("3/8. vehicle_utilization.png saved.")
        self.plot_distance_vs_time()
        print("4/8. distance_vs_time.png saved.")
        self.plot_rating_distribution()
        print("5/8. rating_distribution.png saved.")
        self.plot_region_orders()
        print("6/8. region_orders.png saved.")
        self.plot_delivery_mode_cost()
        print("7/8. mode_cost_boxplot.png saved.")
        self.plot_delay_heatmap()
        print("8/8. delay_heatmap.png saved.")
        print("All visualizations generated successfully.")
