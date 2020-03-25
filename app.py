# -*- coding: utf-8 -*-
import datetime
from Scraping_Logic import *
import dash_table
import pandas_datareader as web
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app.layout = html.Div(children=[
    html.Div(id = 'Title'),


    html.Div(children='''
        Symbol to graph
    '''),

    dcc.Input(id = 'input', value = 'aapl', type = 'text', debounce= True),

    html.Div(id = 'output-graph'),





    html.H3('Fundamentals', style={'padding': 10}),
    html.Div(id='fundamentals-table'),

    html.Div([
        html.Div([
            html.H6('How strong is the brand?'),
            dcc.Slider(
                id='Brand_Strength',
                min=0,
                max=3,
                value=0,
                marks={0: '0', 1: '1', 2: '2', 3: '3'}
            )
        ], style={'padding': 10}, className="six columns"),

        html.Div([
            html.H6('How strong is the product?'),
            dcc.Slider(
                id='Product_Strength',
                min=0,
                max=3,
                value=0,
                marks={0: '0', 1: '1', 2: '2', 3: '3'}
            )
        ], style={'padding': 10}, className="six columns"),
    ],className="row"),
    html.Div(children='''
        
    '''),

    html.Div([
        html.Div([
            html.H6('Industry being disrupted?'),
            dcc.Slider(
                id='Industry Disruption',
                min=0,
                max=3,
                value=0,
                marks={0: '0', 1: '1', 2: '2', 3: '3'}
            )
        ], style={'padding': 10}, className="six columns"),

        html.Div([
            html.H6('Turnaround plan?'),
            dcc.Slider(
                id='Turnaround Plan',
                min=0,
                max=3,
                value=0,
                marks={0: '0', 1: '1', 2: '2', 3: '3'}
            )
        ], style={'padding': 10}, className="six columns"),
    ], className="row"),

    html.H3('Sentiment', style={'padding': 10})



])


@app.callback(
    Output(component_id = 'Title', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_graph(input_data):
    line = input_data.upper() + " Short Score Card"
    return html.H1(children= line)


@app.callback(
    Output(component_id = 'output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_graph(input_data):
    start = datetime.datetime(2015, 1, 1)
    end = datetime.datetime.now()
    df = web.DataReader(input_data, 'yahoo', start, end)

    return dcc.Graph(
        id = 'example-graph',
        figure = {
            'data' : [
                {'x': df.index, 'y': df.Close, 'type': 'line', 'name': input_data}
            ],
            'layout' : {
                'title' : input_data
            }
        }
    )

@app.callback(
    Output(component_id = 'fundamentals-table', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_graph(input_data):
    line = input_data.upper() + " Short Score Card"
    debt = str(get_debt(input_data)[0])
    revenue, profit = get_revenue_profit(input_data)
    revenue = str(revenue)
    profit = str(profit)
    z_score = str(get_altman(input_data))

    thisdict = {
        "": ("Debt", "Revenue",'Profit', 'Altman Z-Score'),
        "3": ("No debt", "Revenue growth flat or increasing ", 'Profitable', 'Safe'),
        "2":('Little Debt', 'Revene just started declining', 'Just started losing money', 'Gray'),
        "1": ('Large debt', 'Decline has been going on for a sustained period', 'Losing money for a couple quarters', 'Gray/Distressed'),
        "0": ('Massive debt', 'decline has been going on for years', 'Losing money consistently', 'Distressed'),
        "Ratings": (debt, revenue,profit, z_score )
    }
    df = pd.DataFrame(thisdict)
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('rows'),
        style_data_conditional=[
            {
                'if': {
                    'column_id': debt,
                    'filter_query': '{1} contains "Large debt"'
                },
                'backgroundColor': '#3D9970',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': revenue,
                    'filter_query': '{1} contains "Decline"'
                },
                'backgroundColor': '#3D9970',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': profit,
                    'filter_query': '{1} contains "Losing"'
                },
                'backgroundColor': '#3D9970',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': z_score,
                    'filter_query': '{1} contains "Gray"'
                },
                'backgroundColor': '#3D9970',
                'color': 'white',
            }
        ]
)

if __name__ == '__main__':
    app.run_server(debug=True)



