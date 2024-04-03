import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the formatted output data
df = pd.read_csv('formatted_output.csv')

# Sort the dataframe by date
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

# Get unique regions
regions = df['region'].unique()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define CSS styling
styles = {
    'container': {
        'padding': '10px'
    },
    'radioItems': {
        'display': 'inline-block',
        'margin-right': '10px'
    }
}

# Define the layout of the app
app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualizer", style={'text-align': 'center'}),
    html.Div([
        dcc.RadioItems(
            id='region-selector',
            options=[{'label': region.capitalize(), 'value': region} for region in ['all'] + list(regions)],
            value='all',
            style=styles['radioItems']
        )
    ], style=styles['container']),
    dcc.Graph(id='sales-chart'),
])

# Define callback to update the chart based on region selection
@app.callback(
    Output('sales-chart', 'figure'),
    [Input('region-selector', 'value')]
)
def update_chart(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]
    
    # Create a line chart
    fig = px.line(filtered_df, x='date', y='sales', title="Pink Morsel Sales (" + str(selected_region.capitalize()) + ")")
    
    # Highlight the date of price increase
    fig.add_vline(x='2021-01-15', line_dash='dash', line_color='red', annotation_text="Price Increase")
    
    # Update axes labels
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Sales")
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
