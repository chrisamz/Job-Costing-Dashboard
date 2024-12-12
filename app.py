import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import sqlite3

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Job Costing Dashboard"

# Load and preprocess data
def load_data():
    conn = sqlite3.connect('data/job_costing.db')
    materials = pd.read_sql("SELECT * FROM materials", conn)
    labor = pd.read_sql("SELECT * FROM labor", conn)
    overhead = pd.read_sql("SELECT * FROM overhead", conn)
    conn.close()

    # Combine datasets
    materials['category'] = 'Materials'
    labor['category'] = 'Labor'
    overhead['category'] = 'Overhead'

    # Normalize columns
    labor['cost'] = labor['hours_worked'] * labor['hourly_rate']
    all_data = pd.concat([
        materials[['project_id', 'date', 'cost', 'category']],
        labor[['project_id', 'date', 'cost', 'category']],
        overhead[['project_id', 'date', 'cost', 'category']]
    ])

    all_data['date'] = pd.to_datetime(all_data['date'])
    return all_data

data = load_data()
projects = data['project_id'].unique()

# Layout of the app
app.layout = html.Div([
    html.H1("Job Costing Dashboard", style={'textAlign': 'center'}),

    # Filters
    html.Div([
        html.Label("Select Project:"),
        dcc.Dropdown(
            id="project-dropdown",
            options=[{"label": f"Project {p}", "value": p} for p in projects],
            value=projects[0],
            multi=False
        ),

        html.Label("Date Range:"),
        dcc.DatePickerRange(
            id="date-picker",
            start_date=data['date'].min(),
            end_date=data['date'].max(),
            display_format="YYYY-MM-DD"
        ),
    ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),

    # Summary Cards
    html.Div(id="summary-cards", style={'display': 'flex', 'justifyContent': 'space-around'}),

    # Visualizations
    html.Div([
        dcc.Graph(id="cost-trend-chart"),
        dcc.Graph(id="cost-category-pie"),
        dcc.Graph(id="project-comparison-bar")
    ]),

    # Data Table
    html.Div([
        html.H3("Detailed Cost Data"),
        dcc.Graph(id="transaction-table")
    ])
])

# Callbacks
@app.callback(
    [Output("summary-cards", "children"),
     Output("cost-trend-chart", "figure"),
     Output("cost-category-pie", "figure"),
     Output("project-comparison-bar", "figure"),
     Output("transaction-table", "figure")],
    [Input("project-dropdown", "value"),
     Input("date-picker", "start_date"),
     Input("date-picker", "end_date")]
)
def update_dashboard(project_id, start_date, end_date):
    filtered_data = data[
        (data['project_id'] == project_id) &
        (data['date'] >= start_date) &
        (data['date'] <= end_date)
    ]

    # Summary Metrics
    total_cost = filtered_data['cost'].sum()
    materials_cost = filtered_data[filtered_data['category'] == 'Materials']['cost'].sum()
    labor_cost = filtered_data[filtered_data['category'] == 'Labor']['cost'].sum()
    overhead_cost = filtered_data[filtered_data['category'] == 'Overhead']['cost'].sum()

    summary_cards = [
        html.Div([
            html.H4("Total Cost"),
            html.P(f"${total_cost:,.2f}")
        ], style={"border": "1px solid #ccc", "padding": "10px", "width": "20%"}),
        html.Div([
            html.H4("Materials Cost"),
            html.P(f"${materials_cost:,.2f}")
        ], style={"border": "1px solid #ccc", "padding": "10px", "width": "20%"}),
        html.Div([
            html.H4("Labor Cost"),
            html.P(f"${labor_cost:,.2f}")
        ], style={"border": "1px solid #ccc", "padding": "10px", "width": "20%"}),
        html.Div([
            html.H4("Overhead Cost"),
            html.P(f"${overhead_cost:,.2f}")
        ], style={"border": "1px solid #ccc", "padding": "10px", "width": "20%"})
    ]

    # Cost Trend Chart
    cost_trend_fig = px.line(
        filtered_data.groupby(['date', 'category'])['cost'].sum().reset_index(),
        x="date", y="cost", color="category",
        title="Cost Trends Over Time"
    )

    # Cost Category Pie Chart
    category_pie_fig = px.pie(
        filtered_data.groupby('category')['cost'].sum().reset_index(),
        names="category", values="cost",
        title="Cost Distribution by Category"
    )

    # Project Comparison Bar Chart
    project_comparison_fig = px.bar(
        data.groupby(['project_id', 'category'])['cost'].sum().reset_index(),
        x="project_id", y="cost", color="category",
        title="Cost Comparison Across Projects"
    )

    # Transaction Table
    transaction_table_fig = px.bar(
        filtered_data, x="date", y="cost", color="category",
        hover_data={"cost": ":$.2f"},
        title="Detailed Transactions"
    )

    return summary_cards, cost_trend_fig, category_pie_fig, project_comparison_fig, transaction_table_fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
