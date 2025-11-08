import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# --- 1. Data Loading and Preparation ---
# Using a sample dataset for demonstration. 
# REPLACE THIS with your actual sales/transaction data (e.g., loading a CSV file).
# df = pd.read_csv('your_sales_data.csv')
# Make sure your dataset has columns like 'Sales', 'Profit', 'Date', 'Category', 'Region'

# Using a robust sample dataset for visualization richness
df = px.data.gapminder()
# We'll use 'year' as Date, 'country' as Region, 'pop' as Quantity/Sales, and 'gdpPercap' as Profit/Margin.

# Create basic calculated fields (measures)
df['Profit Margin'] = df['gdpPercap'] * 0.1 # Placeholder margin
df['Total Sales'] = df['pop'] * df['gdpPercap'] # Placeholder total sales

# --- 2. Dashboard Component Layout ---
app = dash.Dash(_name_)

# Define the overall layout structure
app.layout = html.Div(style={'backgroundColor': '#f9f9f9', 'padding': '20px'}, children=[
    
    html.H1(
        children='CodTech Task 3: Interactive Sales Performance Dashboard',
        style={
            'textAlign': 'center',
            'color': '#111827',
            'paddingBottom': '20px'
        }
    ),
    
    # KPI Section (Cards)
    html.Div(className='row', children=[
        # Card 1: Total Sales
        html.Div(
            children=[
                html.H3('Total Global Sales (Example)', style={'color': '#1f77b4'}),
                html.H2(f"${df['Total Sales'].sum():,.0f}", style={'color': '#1f77b4'})
            ], 
            style={'width': '30%', 'display': 'inline-block', 'padding': '10px', 'marginRight': '3%', 'border': '1px solid #ddd', 'borderRadius': '5px', 'backgroundColor': 'white'}
        ),
        # Card 2: Average Profit Margin
        html.Div(
            children=[
                html.H3('Average Profit Margin (Example)', style={'color': '#2ca02c'}),
                html.H2(f"{df['Profit Margin'].mean():.2f}%", style={'color': '#2ca02c'})
            ],
            style={'width': '30%', 'display': 'inline-block', 'padding': '10px', 'marginRight': '3%', 'border': '1px solid #ddd', 'borderRadius': '5px', 'backgroundColor': 'white'}
        ),
        # Card 3: Actionable Insight Note
        html.Div(
            children=[
                html.H3('Key Insight', style={'color': '#d62728'}),
                html.P('Filter data below to identify regions with negative profit margins.', style={'fontSize': '14px', 'color': '#d62728'})
            ],
            style={'width': '30%', 'display': 'inline-block', 'padding': '10px', 'border': '1px solid #ddd', 'borderRadius': '5px', 'backgroundColor': 'white'}
        )
    ]),

    html.Hr(),

    # Interactive Filter Section
    html.Div(style={'padding': '20px', 'backgroundColor': 'white', 'marginBottom': '20px', 'borderRadius': '5px'}, children=[
        html.Label("Select Region/Country for Filtering:", style={'fontWeight': 'bold', 'paddingRight': '15px'}),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': i, 'value': i} for i in df['country'].unique()],
            value=df['country'].unique()[0:5],  # Default selection
            multi=True,
            style={'width': '100%'}
        )
    ]),

    # Visualization Section
    html.Div(className='row', children=[
        # Visual 1: Trend Analysis (Line Chart)
        html.Div(style={'width': '49%', 'display': 'inline-block', 'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '5px'}, children=[
            dcc.Graph(id='trend-chart')
        ]),
        # Visual 2: Regional/Categorical Breakdown (Bar Chart)
        html.Div(style={'width': '49%', 'display': 'inline-block', 'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '5px'}, children=[
            dcc.Graph(id='breakdown-chart')
        ])
    ])
])

# --- 3. Dashboard Interactivity (Callback Functions) ---

@app.callback(
    [Output('trend-chart', 'figure'),
     Output('breakdown-chart', 'figure')],
    [Input('region-dropdown', 'value')]
)
def update_graph(selected_countries):
    """Updates both charts based on the selected regions/countries."""
    
    # Filter the DataFrame based on the dropdown selection
    filtered_df = df[df['country'].isin(selected_countries)]
    
    # 1. Trend Chart (Time-Series)
    trend_fig = px.line(
        filtered_df, 
        x='year', 
        y='Total Sales', 
        color='country',
        title='Sales Trend Over Time by Selected Region'
    )
    trend_fig.update_layout(
        xaxis_title='Year', 
        yaxis_title='Total Sales',
        plot_bgcolor='white'
    )

    # 2. Breakdown Chart (Regional/Categorical Breakdown)
    # Calculate aggregated sales per region/continent
    breakdown_data = filtered_df.groupby('continent')['Total Sales'].sum().reset_index()
    
    breakdown_fig = px.bar(
        breakdown_data, 
        x='continent', 
        y='Total Sales', 
        color='continent',
        title='Total Sales by Continent (Actionable Insight: Focus on low-sales continents)'
    )
    breakdown_fig.update_layout(
        xaxis_title='Continent', 
        yaxis_title='Total Sales',
        plot_bgcolor='white'
    )
    
    return trend_fig, breakdown_fig

# --- 4. Run the Application ---

if _name_ == '_main_':
    # Setting debug=True allows for automatic refreshing during development
    print("Dashboard starting at http://127.0.0.1:8050/")
    app.run_server(debug=True)