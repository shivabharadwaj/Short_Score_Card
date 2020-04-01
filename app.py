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


    html.Div(id='Fundamental_Score'),
    html.Div(id='fundamentals-table'),

    html.Div([
        html.Div([
            html.H6('How strong is the brand?'),
            dcc.Slider(
                id='Brand_Strength',
                min=0,
                max=3,
                step=1,
                value = 0,
                updatemode='drag'
            ),
            html.Div(id='slider_1', style={'margin-top': 10})
        ], style={'padding': 10}, className="six columns"),

        html.Div([
            html.H6('How strong is the product?'),
            dcc.Slider(
                id='Product_Strength',
                min=0,
                max=3,
                value=0,
                updatemode='drag'
            ),
            html.Div(id='slider_2', style={'margin-top': 10})
        ], style={'padding': 10}, className="six columns"),
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
                updatemode='drag'
            ),
            html.Div(id='slider_3', style={'margin-top': 10})
        ], style={'padding': 10}, className="six columns"),

        html.Div([
            html.H6('Turnaround plan?'),
            dcc.Slider(
                id='Turnaround_Plan',
                min=0,
                max=3,
                value=0,
                updatemode='drag'
            ),
            html.Div(id='slider_4', style={'margin-top': 10})
        ], style={'padding': 10}, className="six columns"),
    ], className="row"),

    html.Div(id='Sentiment_Score'),

    html.Div([
        html.Div([
            html.H6('52-week range'),
            dcc.Slider(
                id='Range',
                min=0,
                max=3,
                value=0,
                updatemode='drag'
            ),
            html.Div(id='slider_5', style={'margin-top': 10})
        ], style={'padding': 10}, className="six columns"),

        html.Div([
            html.H6('How strong is the product?'),
            dcc.Slider(
                id='News',
                min=0,
                max=3,
                value=0,
                updatemode='drag'
            ),
            html.Div(id='slider_6', style={'margin-top': 10})
        ], style={'padding': 10}, className="six columns"),
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
                updatemode='drag'
            ),
            html.Div(id='slider_7', style={'margin-top': 10})
        ], style={'padding': 10}, className="six columns"),

        html.Div(id='score'),
    ], className="row"),


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



#Update Slider

@app.callback(Output('slider_1', 'children'),
              [Input('Brand_Strength', 'value')])
def display_value(value):
    output = ""
    if(value==0):
        output = "nobody knows this brand"
    if(value==1):
        output = "Lesser-known"
    if(value==2):
        output = "Even during times of change, there will be an impact, but there will also be demand"
    if(value==3):
        output = "There will always be some people who want this product"
    return output


@app.callback(Output('slider_2', 'children'),
              [Input('Product_Strength', 'value')])
def display_value(value):
    output = ""
    if(value==0):
        output = "This is going away completely eventually"
    if(value==1):
        output = "Some people will still buy this product"
    if(value==2):
        output = "Even during times of change, there will be an impact, but there will also be demand"
    if(value==3):
        output = "There will always be some people who want this product"
    return output

@app.callback(Output('slider_3', 'children'),
              [Input('Industry_Disruption', 'value')])
def display_value(value):
    output = ""
    if(value==0):
        output = "This whole industry is about to go away"
    if(value==1):
        output = "Industry is in serious trouble"
    if(value==2):
        output = "Industry is starting to wane"
    if(value==3):
        output = "Industry is strong, just this one company isn't doing well"
    return output

@app.callback(Output('slider_4', 'children'),
              [Input('Turnaround_Plan', 'value')])
def display_value(value):
    output = ""
    if(value==0):
        output = "Bad and Will Get Worse"
    if(value==1):
        output = "Unlikely"
    if(value==2):
        output = "OK Shot"
    if(value==3):
        output = "Good shot"
    return output

@app.callback(Output('slider_5', 'children'),
              [Input('Range', 'value')])
def display_value(value):
    output = ""
    if(value==0):
        output = "Price is at all time lows and dropping fast"
    if(value==1):
        output = "Price has been stable or declining "
    if(value==2):
        output = "Price gradually went up and has plateaued OR Price is close to lows but there has been a recent recovery and plateau"
    if(value==3):
        output = "Big step up in the price in the last year "
    return output


@app.callback(Output('slider_6', 'children'),
              [Input('News', 'value')])
def display_value(value):
    output = ""
    if(value==0):
        output = "Horrible"
    if(value==1):
        output = "Bad"
    if(value==2):
        output = "OK"
    if(value==3):
        output = "Good"
    return output

@app.callback(Output('slider_7', 'children'),
              [Input('Analyst', 'value')])
def display_value(value):
    output = ""
    if(value==0):
        output = "Very Bearish"
    if(value==1):
        output = "Mixed with bad bias"
    if(value==2):
        output = "Mixed with good bias"
    if(value==3):
        output = "Good ratings"
    return output
if __name__ == '__main__':
    app.run_server(debug=True)



