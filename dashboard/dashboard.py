import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
import sys

# Add parent directory to path to import src.data_loader
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from src.data_loader import DataLoader

# Initialize the Dash app
app = dash.Dash(__name__, title="Porter-Style Delivery Logistics Dashboard")
server = app.server  # Expose server for potential WSGI deployments

# Load data
csv_path = os.path.join(base_dir, 'data', 'Delivery_Logistics.csv')
loader = DataLoader(csv_path)
df_raw = loader.load_data()

# Unique filter options
regions = sorted(df_raw['region'].unique())
partners = sorted(df_raw['delivery_partner'].unique())
vehicles = sorted(df_raw['vehicle_type'].unique())

# Dark theme layout for Plotly charts
PLOTLY_DARK_TEMPLATE = "plotly_dark"
CHART_BG_COLOR = "#111827"
PLOT_BG_COLOR = "rgba(0,0,0,0)"
TEXT_COLOR = "#9ca3af"

# App Layout
app.layout = html.Div(className="app-container", children=[
    # Header
    html.Header(className="app-header", children=[
        html.Div([
            html.H1("Porter-Style Delivery Logistics Dashboard", className="app-title"),
            html.P("Real-time operational analysis of shipping delays, partner SLAs, and customer satisfaction", className="app-subtitle")
        ]),
        # Status indicator
        html.Div(style={"display": "flex", "alignItems": "center", "gap": "10px"}, children=[
            html.Span(style={"height": "10px", "width": "10px", "backgroundColor": "#10b981", "borderRadius": "50%", "display": "inline-block", "boxShadow": "0 0 8px #10b981"}),
            html.Span("Live Operation Metrics", style={"fontSize": "14px", "fontWeight": "600", "color": "#10b981"})
        ])
    ]),
    
    # Main Grid Layout
    html.Div(className="main-layout", children=[
        # Sidebar for filters
        html.Div(className="sidebar", children=[
            html.H3("Filter Controls", className="sidebar-title"),
            
            # Region filter
            html.Div([
                html.Label("Geographical Region", className="filter-label"),
                dcc.Dropdown(
                    id="region-filter",
                    options=[{"label": "All Regions", "value": "All"}] + [{"label": r.capitalize(), "value": r} for r in regions],
                    value="All",
                    clearable=False,
                    style={"backgroundColor": "#1f2937", "color": "#000000"}
                )
            ]),
            
            # Partner filter
            html.Div([
                html.Label("Delivery Partner (3PL)", className="filter-label"),
                dcc.Dropdown(
                    id="partner-filter",
                    options=[{"label": "All Partners", "value": "All"}] + [{"label": p.upper(), "value": p} for p in partners],
                    value="All",
                    clearable=False,
                    style={"backgroundColor": "#1f2937", "color": "#000000"}
                )
            ]),
            
            # Vehicle type filter
            html.Div([
                html.Label("Vehicle Type", className="filter-label"),
                dcc.Dropdown(
                    id="vehicle-filter",
                    options=[{"label": "All Vehicles", "value": "All"}] + [{"label": v.capitalize(), "value": v} for v in vehicles],
                    value="All",
                    clearable=False,
                    style={"backgroundColor": "#1f2937", "color": "#000000"}
                )
            ]),
            
            # Static Information / Tips
            html.Div(style={"marginTop": "20px", "padding": "15px", "backgroundColor": "#1e293b", "borderRadius": "8px", "border": "1px solid #334155"}, children=[
                html.H5("💡 Analyst Insights", style={"margin": "0 0 8px 0", "color": "#f59e0b", "fontSize": "14px", "fontWeight": "600"}),
                html.P("Filter through different transport fleets and regional hubs to narrow down delivery bottleneck causes.", 
                       style={"margin": 0, "fontSize": "12px", "color": "#cbd5e1", "lineHeight": "1.4"})
            ])
        ]),
        
        # Main Dashboard Panel
        html.Div(className="dashboard-content", children=[
            # KPI Cards Row
            html.Div(className="kpi-row", children=[
                html.Div(className="kpi-card total-orders", children=[
                    html.Div("Total Orders", className="kpi-label"),
                    html.Div(id="kpi-total-orders", className="kpi-value"),
                ]),
                html.Div(className="kpi-card avg-time", children=[
                    html.Div("Avg Delivery Time", className="kpi-label"),
                    html.Div(id="kpi-avg-time", className="kpi-value"),
                ]),
                html.Div(className="kpi-card delay-rate", children=[
                    html.Div("Delay Rate", className="kpi-label"),
                    html.Div(id="kpi-delay-rate", className="kpi-value"),
                ]),
                html.Div(className="kpi-card cancel-rate", children=[
                    html.Div("Cancellation Rate", className="kpi-label"),
                    html.Div(id="kpi-cancel-rate", className="kpi-value"),
                ]),
            ]),
            
            # Row 2: Region Chart and Vehicle Chart
            html.Div(className="chart-grid-2", children=[
                html.Div(className="chart-card", children=[
                    html.H4("Order Volume by Region", className="chart-title"),
                    dcc.Graph(id="chart-region", config={"displayModeBar": False})
                ]),
                html.Div(className="chart-card", children=[
                    html.H4("Vehicle Type Utilization Share", className="chart-title"),
                    dcc.Graph(id="chart-vehicle", config={"displayModeBar": False})
                ])
            ]),
            
            # Row 3: Weather and Partner Delays
            html.Div(className="chart-grid-2", children=[
                html.Div(className="chart-card", children=[
                    html.H4("Delay Rate (%) by Weather Condition", className="chart-title"),
                    dcc.Graph(id="chart-weather", config={"displayModeBar": False})
                ]),
                html.Div(className="chart-card", children=[
                    html.H4("Delay Rate (%) by Delivery Partner", className="chart-title"),
                    dcc.Graph(id="chart-partner", config={"displayModeBar": False})
                ])
            ]),
            
            # Row 4: Distance vs Time and Ratings
            html.Div(className="chart-grid-2", children=[
                html.Div(className="chart-card", children=[
                    html.H4("Distance vs. Transit Time (Sampled)", className="chart-title"),
                    dcc.Graph(id="chart-distance-time", config={"displayModeBar": False})
                ]),
                html.Div(className="chart-card", children=[
                    html.H4("Customer Star Ratings Distribution", className="chart-title"),
                    dcc.Graph(id="chart-ratings", config={"displayModeBar": False})
                ])
            ]),
            
            # Row 5: Heatmap
            html.Div(className="chart-card-full", children=[
                html.H4("Regional Delay Heatmap by Weather Conditions (Average Delay %)", className="chart-title"),
                dcc.Graph(id="chart-heatmap", config={"displayModeBar": False})
            ])
        ])
    ])
])

# Define Callbacks
@app.callback(
    [
        Output("kpi-total-orders", "children"),
        Output("kpi-avg-time", "children"),
        Output("kpi-delay-rate", "children"),
        Output("kpi-cancel-rate", "children"),
        Output("chart-region", "figure"),
        Output("chart-vehicle", "figure"),
        Output("chart-weather", "figure"),
        Output("chart-partner", "figure"),
        Output("chart-distance-time", "figure"),
        Output("chart-ratings", "figure"),
        Output("chart-heatmap", "figure")
    ],
    [
        Input("region-filter", "value"),
        Input("partner-filter", "value"),
        Input("vehicle-filter", "value")
    ]
)
def update_dashboard(selected_region, selected_partner, selected_vehicle):
    # Apply filtering
    filtered_df = df_raw.copy()
    
    if selected_region != "All":
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
        
    if selected_partner != "All":
        filtered_df = filtered_df[filtered_df['delivery_partner'] == selected_partner]
        
    if selected_vehicle != "All":
        filtered_df = filtered_df[filtered_df['vehicle_type'] == selected_vehicle]
        
    # 1. Recalculate KPIs
    total_orders = len(filtered_df)
    if total_orders > 0:
        avg_time = filtered_df['delivery_time_hours'].mean()
        delay_rate = (filtered_df['delayed'] == 'yes').mean() * 100
        cancel_rate = (filtered_df['delivery_status'] == 'cancelled').mean() * 100
        
        kpi_orders_str = f"{total_orders:,}"
        kpi_time_str = f"{avg_time:.2f} hrs"
        kpi_delay_str = f"{delay_rate:.1f}%"
        kpi_cancel_str = f"{cancel_rate:.1f}%"
    else:
        kpi_orders_str = "0"
        kpi_time_str = "N/A"
        kpi_delay_str = "0.0%"
        kpi_cancel_str = "0.0%"
        
    # Helper to apply clean styling to plotly layouts
    def clean_layout(fig):
        fig.update_layout(
            paper_bgcolor=CHART_BG_COLOR,
            plot_bgcolor=PLOT_BG_COLOR,
            font_color=TEXT_COLOR,
            margin=dict(l=40, r=20, t=20, b=40),
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                bordercolor="rgba(0,0,0,0)"
            ),
            xaxis=dict(showgrid=True, gridcolor="#1f2937", linecolor="#374151"),
            yaxis=dict(showgrid=True, gridcolor="#1f2937", linecolor="#374151"),
            template=PLOTLY_DARK_TEMPLATE
        )
        return fig

    # 2. Chart - Orders by Region
    if total_orders > 0:
        region_df = filtered_df['region'].value_counts().reset_index()
        region_df.columns = ['region', 'count']
        fig_region = px.bar(
            region_df, x='region', y='count',
            color='count', color_continuous_scale='Purples'
        )
        fig_region.update_coloraxes(showscale=False)
    else:
        fig_region = go.Figure()
    clean_layout(fig_region)

    # 3. Chart - Vehicle Utilization
    if total_orders > 0:
        vehicle_df = filtered_df['vehicle_type'].value_counts().reset_index()
        vehicle_df.columns = ['vehicle_type', 'count']
        fig_vehicle = px.pie(
            vehicle_df, names='vehicle_type', values='count',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_vehicle.update_traces(textposition='inside', textinfo='percent+label')
    else:
        fig_vehicle = go.Figure()
    clean_layout(fig_vehicle)
    fig_vehicle.update_layout(margin=dict(l=20, r=20, t=20, b=20))

    # 4. Chart - Delay by Weather
    if total_orders > 0:
        weather_df = filtered_df.groupby('weather_condition').agg(
            delay_pct=('delayed', lambda x: (x == 'yes').mean() * 100)
        ).reset_index().sort_values(by='delay_pct', ascending=False)
        fig_weather = px.bar(
            weather_df, x='weather_condition', y='delay_pct',
            color='delay_pct', color_continuous_scale='OrRd'
        )
        fig_weather.update_coloraxes(showscale=False)
        fig_weather.update_yaxes(title="Delay Rate (%)")
    else:
        fig_weather = go.Figure()
    clean_layout(fig_weather)

    # 5. Chart - Delay by Partner
    if total_orders > 0:
        partner_df = filtered_df.groupby('delivery_partner').agg(
            delay_pct=('delayed', lambda x: (x == 'yes').mean() * 100)
        ).reset_index().sort_values(by='delay_pct', ascending=True)
        fig_partner = px.bar(
            partner_df, y='delivery_partner', x='delay_pct',
            orientation='h', color='delay_pct', color_continuous_scale='Bluered'
        )
        fig_partner.update_coloraxes(showscale=False)
        fig_partner.update_xaxes(title="Delay Rate (%)")
    else:
        fig_partner = go.Figure()
    clean_layout(fig_partner)

    # 6. Chart - Distance vs Delivery Time
    if total_orders > 0:
        # Sample down to max 1500 points for browser performance
        sample_size = min(1500, len(filtered_df))
        sample_df = filtered_df.sample(sample_size, random_state=42)
        fig_dist_time = px.scatter(
            sample_df, x='distance_km', y='delivery_time_hours',
            color='delayed', color_discrete_map={'yes': '#ef4444', 'no': '#10b981'},
            labels={'distance_km': 'Distance (km)', 'delivery_time_hours': 'Delivery Time (hours)'},
            opacity=0.6
        )
    else:
        fig_dist_time = go.Figure()
    clean_layout(fig_dist_time)

    # 7. Chart - Ratings
    if total_orders > 0:
        ratings_df = filtered_df['delivery_rating'].value_counts().sort_index().reset_index()
        ratings_df.columns = ['rating', 'count']
        fig_ratings = px.bar(
            ratings_df, x='rating', y='count',
            color='count', color_continuous_scale='Blues'
        )
        fig_ratings.update_coloraxes(showscale=False)
        fig_ratings.update_xaxes(tickvals=[1,2,3,4,5], title="Rating (Stars)")
    else:
        fig_ratings = go.Figure()
    clean_layout(fig_ratings)

    # 8. Chart - Heatmap (Region vs Weather delay%)
    if total_orders > 0:
        # If filtered too deep, we might have empty combinations. Fill na with 0.
        pivot_df = filtered_df.pivot_table(
            index='region',
            columns='weather_condition',
            values='delayed',
            aggfunc=lambda x: (x == 'yes').mean() * 100
        ).fillna(0.0)
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale='YlOrRd',
            colorbar=dict(title="Delay %"),
            hovertemplate="Region: %{y}<br>Weather: %{x}<br>Delay Rate: %{z:.1f}%<extra></extra>"
        ))
    else:
        fig_heatmap = go.Figure()
    clean_layout(fig_heatmap)
    
    return (
        kpi_orders_str, kpi_time_str, kpi_delay_str, kpi_cancel_str,
        fig_region, fig_vehicle, fig_weather, fig_partner,
        fig_dist_time, fig_ratings, fig_heatmap
    )

if __name__ == '__main__':
    # Default local dev port
    app.run(debug=True, host="127.0.0.1", port=8050)
