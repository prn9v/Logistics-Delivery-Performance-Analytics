import pandas as pd

class Analysis:
    def __init__(self, df):
        """
        Initialize the Analysis class with a cleaned DataFrame.
        """
        self.df = df

    def avg_delivery_time(self):
        """
        Returns the overall average delivery time in hours.
        """
        return float(self.df['delivery_time_hours'].mean())

    def delay_percentage(self):
        """
        Returns the percentage of orders where delayed == 'yes'.
        """
        delayed_count = (self.df['delayed'] == 'yes').sum()
        total_count = len(self.df)
        return float((delayed_count / total_count) * 100) if total_count > 0 else 0.0

    def cancellation_rate(self):
        """
        Returns the percentage of orders where delivery_status == 'cancelled'.
        """
        cancelled_count = (self.df['delivery_status'] == 'cancelled').sum()
        total_count = len(self.df)
        return float((cancelled_count / total_count) * 100) if total_count > 0 else 0.0

    def total_revenue(self):
        """
        Returns the sum of delivery_cost.
        """
        return float(self.df['delivery_cost'].sum())

    def orders_by_region(self):
        """
        Returns the count of orders per region as a DataFrame.
        """
        res = self.df.groupby('region').size().reset_index(name='order_count')
        return res.sort_values(by='order_count', ascending=False)

    def partner_performance(self):
        """
        Returns a DataFrame with per delivery_partner:
        avg delivery_time, delay%, avg rating, order count.
        """
        # Calculate delay% manually per partner to be accurate
        def get_delay_pct(group):
            return (group['delayed'] == 'yes').mean() * 100

        res = self.df.groupby('delivery_partner').agg(
            avg_delivery_time=('delivery_time_hours', 'mean'),
            delay_percentage=('delayed', lambda x: (x == 'yes').mean() * 100),
            avg_rating=('delivery_rating', 'mean'),
            order_count=('delivery_id', 'count')
        ).reset_index()
        return res.sort_values(by='order_count', ascending=False)

    def vehicle_utilization(self):
        """
        Returns a DataFrame with count and avg delivery_time per vehicle_type.
        """
        res = self.df.groupby('vehicle_type').agg(
            order_count=('delivery_id', 'count'),
            avg_delivery_time=('delivery_time_hours', 'mean')
        ).reset_index()
        return res.sort_values(by='order_count', ascending=False)

    def weather_impact(self):
        """
        Returns a DataFrame with avg delivery_time and delay% per weather_condition.
        """
        res = self.df.groupby('weather_condition').agg(
            avg_delivery_time=('delivery_time_hours', 'mean'),
            delay_percentage=('delayed', lambda x: (x == 'yes').mean() * 100)
        ).reset_index()
        return res.sort_values(by='delay_percentage', ascending=False)

    def delivery_mode_analysis(self):
        """
        Returns a DataFrame with avg time, avg cost, delay% per delivery_mode.
        """
        res = self.df.groupby('delivery_mode').agg(
            avg_delivery_time=('delivery_time_hours', 'mean'),
            avg_delivery_cost=('delivery_cost', 'mean'),
            delay_percentage=('delayed', lambda x: (x == 'yes').mean() * 100)
        ).reset_index()
        return res.sort_values(by='avg_delivery_time', ascending=False)

    def package_type_analysis(self):
        """
        Returns a DataFrame with avg cost, avg weight, count per package_type.
        """
        res = self.df.groupby('package_type').agg(
            avg_delivery_cost=('delivery_cost', 'mean'),
            avg_package_weight=('package_weight_kg', 'mean'),
            order_count=('delivery_id', 'count')
        ).reset_index()
        return res.sort_values(by='order_count', ascending=False)

    def rating_distribution(self):
        """
        Returns the count per delivery_rating as a DataFrame.
        """
        res = self.df.groupby('delivery_rating').size().reset_index(name='order_count')
        return res.sort_values(by='delivery_rating')

    def top_delayed_partners(self):
        """
        Returns the top 5 partners by delay%.
        """
        perf = self.partner_performance()
        return perf.sort_values(by='delay_percentage', ascending=False).head(5)
