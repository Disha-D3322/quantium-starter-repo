import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the CSV file (replace 'formatted_sales_data.csv' with the actual file path)
df = pd.read_csv('formatted_sales_data.csv')

# Convert 'date' column to datetime for proper sorting
df['date'] = pd.to_datetime(df['date'])

# Set the date of the price increase
price_increase_date = pd.Timestamp('2021-01-15')

# Calculate total sales before and after the price increase
sales_before = df[df['date'] < price_increase_date]['sales'].sum()
sales_after = df[df['date'] >= price_increase_date]['sales'].sum()

# Initialize the Dash app
app = dash.Dash(__name__)

# Create a figure using Plotly's go.Figure for advanced customization
fig = px.line(df, x='date', y='sales', color='region',
              title='Sales of Pink Morsels Over Time',
              labels={'sales': 'Sales ($)', 'date': 'Date'})

# Add a vertical line for the price increase date
fig.add_vline(x=price_increase_date, line_width=3, line_dash="dash", line_color="red")

# Add shaded areas to represent the periods before and after the price increase
fig.add_vrect(x0=min(df['date']), x1=price_increase_date, fillcolor="green", opacity=0.2,
              annotation_text="Before Price Increase", annotation_position="top left")
fig.add_vrect(x0=price_increase_date, x1=max(df['date']), fillcolor="blue", opacity=0.2,
              annotation_text="After Price Increase", annotation_position="top right")

# Create the layout
app.layout = html.Div([
    html.H1("Pink Morsel Sales Data Visualizer"),  # Header
    
    # Add a summary of total sales before and after the price increase
    html.Div([
        html.H2(f"Total Sales Before Price Increase: ${sales_before:.2f}"),
        html.H2(f"Total Sales After Price Increase: ${sales_after:.2f}"),
    ]),

    # Line chart visualization
    dcc.Graph(id='sales-line-chart', figure=fig),
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
