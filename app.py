import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv('formatted_output.csv')

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualizer"),
    dcc.Graph(id='sales-chart'),
])

@app.callback(
    Output('sales-chart', 'figure'),
    [Input('sales-chart', 'hoverData')]
)
def update_chart(hoverData):
    if hoverData:
        date = hoverData['points'][0]['x']
        sales_before = df[df['date'] < date]['sales'].sum()
        sales_after = df[df['date'] >= date]['sales'].sum()
    else:
        sales_before = df['sales'].sum()
        sales_after = 0
    
    fig = px.line(df, x='date', y='sales', title='Pink Morsel Sales Over Time')

    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Sales")
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
