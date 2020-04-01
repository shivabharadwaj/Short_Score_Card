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
    html.Div(id = 'Title', style={'margin':25, 'textAlign': 'center'}),

    dcc.Input(id = 'input', value = 'aapl', type = 'text', debounce= True),

    html.Div(id = 'output-graph'),

    html.Div(id='intermediate-value', style={'display': 'none'}),


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
                marks={0: 'Nobody knows this brand', 1: 'Lesser-known', 2: 'Well-known ', 3: 'Household name'}
            )
        ], style={'padding': 25}, className="six columns"),

        html.Div([
            html.H6('How strong is the product?'),
            dcc.Slider(
                id='Product_Strength',
                min=0,
                max=3,
                value=0,
                marks={0: 'Going away eventually', 1: 'Some people will still buy this product', 2: 'Even during times of change, there will be an impact, but there will also be demand', 3: 'There will always be some people who want this product'}
            )
        ], style={'padding': 25}, className="six columns"),
    ],className="row"),
    html.Div(children='''
        
    '''),

    html.Div([
        html.Div([
            html.H6('Industry being disrupted?'),
            dcc.Slider(
                id='Industry_Disruption',
                min=0,
                max=3,
                value=0,
                marks={0: 'This whole industry is about to go away', 1: 'Industry is in serious trouble', 2: 'Industry is starting to wane', 3: 'Industry is strong, just this one company is not doing well'}
            )
        ], style={'padding': 25}, className="six columns"),

        html.Div([
            html.H6('Turnaround plan?'),
            dcc.Slider(
                id='Turnaround_Plan',
                min=0,
                max=3,
                value=0,
                marks={0: 'Bad and Will Get Worse', 1: 'Unlikely', 2: 'OK Shot', 3: 'Good shot'}
            )
        ], style={'padding': 25}, className="six columns"),
    ], className="row"),

    html.Div(id = 'Fundamental_Score'),

    html.H3('Sentiment', style={'padding': 10}),

    html.Div([
        html.Div([
            html.H6('52-week range'),
            dcc.Slider(
                id='Range',
                min=0,
                max=3,
                value=0,
                marks={0: 'Price is at all time lows and dropping fast', 1: 'Price has been stable or declining ', 2: 'Price gradually went up and has plateaued OR Price is close to lows but there has been a recent recovery and plateau', 3: 'Big step up in the price in the last year '}
            )
        ], style={'padding': 25}, className="six columns"),

        html.Div([
            html.H6('How strong is the product?'),
            dcc.Slider(
                id='News',
                min=0,
                max=3,
                value=0,
                marks={0: 'Horrible', 1: 'Bad', 2: 'OK', 3: 'Good'}
            )
        ], style={'padding': 25}, className="six columns"),
    ], className="row"),
    html.Div(children='''

    '''),

    html.Div([
        html.Div([
            html.H6('Analyst'),
            dcc.Slider(
                id='Analyst',
                min=0,
                max=3,
                value=0,
                marks={0: 'Very Bearish', 1: 'Mixed with bad bias', 2: 'Mixed with good bias', 3: 'Good ratings'}
            )
        ], style={'padding': 25}, className="six columns"),

        html.Div(id='score'),
    ], className="row"),

    html.Div(id = 'Sentiment_Score'),

    html.Div(id='Advantage_Score')


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

@app.callback(Output('intermediate-value', 'children'), [Input('input', 'value')])
def clean_data(input_data):
    scores = []
    debt = get_debt(input_data)[0]
    scores.append(debt)
    revenue, profit = get_revenue_profit(input_data)
    scores.append(revenue)
    scores.append(profit)
    z_score = get_altman(input_data)
    scores.append(z_score)
    return scores


@app.callback(
    Output(component_id = 'fundamentals-table', component_property='children'), [Input('intermediate-value', 'children')])
def update_graph(input_data):
    debt = str(input_data[0])
    revenue = str(input_data[1])
    profit = str(input_data[2])
    z_score = str(input_data[3])

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

@app.callback(
    Output(component_id = 'Fundamental_Score', component_property='children'),
    [Input('Brand_Strength','value'), Input('Product_Strength','value'), Input('Industry_Disruption','value'), Input('Turnaround_Plan','value'),Input('intermediate-value', 'children')]
)
def update_fundamental_score(a,b,c,d,e):
    l = [a,b,c,d]
    score = str(round(100*((sum(l)+sum(e))/24)))
    return html.H1('Fundamental Score: '+ score+ "%")

@app.callback(
    Output(component_id = 'Sentiment_Score', component_property='children'),
    [Input('Range','value'), Input('News','value'), Input('Analyst','value')]
)
def update_fundamental_score(a,b,c):
    l = [a,b,c]
    score = str(round(100*((sum(l))/9)))
    return html.H1('Sentiment Score: '+ score+ "%")


@app.callback(
    Output(component_id = 'Advantage_Score', component_property='children'),
    [Input('Brand_Strength','value'), Input('Product_Strength','value'), Input('Industry_Disruption','value'), Input('Turnaround_Plan','value'),Input('intermediate-value', 'children'),Input('Range','value'), Input('News','value'), Input('Analyst','value')]
)
def update_fundamental_score(a,b,c,d,e,f,g,h):
    l = [a,b,c,d]
    fundamental_score = round(100*((sum(l)+sum(e))/24))
    h = [f,g,h]
    sentimental_score = round(100 * ((sum(h)) / 9))
    advantage = str(sentimental_score-fundamental_score)
    return html.H1('Advantage: '+ advantage+ "%")



if __name__ == '__main__':
    app.run_server(debug=True)



