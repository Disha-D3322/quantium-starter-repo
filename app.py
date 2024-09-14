import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Load the CSV file (replace 'formatted_sales_data.csv' with the actual file path)
df = pd.read_csv('formatted_sales_data.csv')

# Convert 'date' column to datetime for proper sorting
df['date'] = pd.to_datetime(df['date'])

# Set the date of the price increase
price_increase_date = pd.Timestamp('2021-01-15')

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the layout
app.layout = html.Div([
    html.H1("SOULFOODS - PINK MORSEL SALES DATA VISUALIZER", className='header'),  # Header
    
    # Region radio button filter
    html.Label('Select Region:', className='label'),
    dcc.RadioItems(
        id='region-filter',
        options=[
            {'label': 'All', 'value': 'all'},
            {'label': 'NORTH', 'value': 'north'},
            {'label': 'EAST', 'value': 'east'},
            {'label': 'SOUTH', 'value': 'south'},
            {'label': 'WEST', 'value': 'west'}
        ],
        value='all',  # Default value is 'all'
        className='radio-items'
    ),

    # Line chart visualization
    dcc.Graph(id='sales-line-chart'),

    # Add a summary of total sales before and after the price increase
    html.Div(id='sales-summary', className='sales-summary'),
])

# Callback to update the graph based on selected region
@app.callback(
    Output('sales-line-chart', 'figure'),
    Output('sales-summary', 'children'),
    Input('region-filter', 'value')
)
def update_chart(selected_region):
    # Filter the dataframe by the selected region
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]

    # Create the line chart
    fig = px.line(filtered_df, x='date', y='sales', color='region',
                  title=f'Sales of Pink Morsels ({selected_region.title()}) Over Time',
                  labels={'sales': 'Sales ($)', 'date': 'Date'})

    # Add a vertical line for the price increase date
    fig.add_vline(x=price_increase_date, line_width=3, line_dash="dash", line_color="red")

    # Add shaded areas to represent the periods before and after the price increase
    fig.add_vrect(x0=min(df['date']), x1=price_increase_date, fillcolor="green", opacity=0.2,
                  annotation_text="Before Price Increase", annotation_position="top left")
    fig.add_vrect(x0=price_increase_date, x1=max(df['date']), fillcolor="blue", opacity=0.2,
                  annotation_text="After Price Increase", annotation_position="top right")

    # Calculate total sales before and after the price increase
    sales_before = filtered_df[filtered_df['date'] < price_increase_date]['sales'].sum()
    sales_after = filtered_df[filtered_df['date'] >= price_increase_date]['sales'].sum()

    # Return the updated figure and sales summary
    summary = [
        html.H2(f"Total Sales Before Price Increase: ${sales_before:.2f}"),
        html.H2(f"Total Sales After Price Increase: ${sales_after:.2f}")
    ]

    return fig, summary

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
