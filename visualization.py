import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import calculation_methods
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

markdown_text = '''
### DE Assignment

Made by Polina Turishcheva  
Group BS-18-03  
Variant 22
'''

app.layout = html.Div([

    dbc.Row(html.Div(dcc.Markdown(children=markdown_text)), justify='center'),

    dbc.Row([
        html.Div('Choose Methods'),
        html.Div('Initial x', style={'width': "auto", 'marginLeft': 50}),
        html.Div('Initial y', style={'width': "auto", 'marginLeft': 200}),
        html.Div('Max x', style={'width': "auto", 'marginLeft': 200}),
        html.Div('Define Step', style={'width': "auto", 'marginLeft': 200}),
        html.Div('Number of Steps', style={'width': "auto", 'marginLeft': 200}),
    ], style={'marginLeft': 50}),

    dbc.Row([
        dbc.Checklist(id='check',
                      options=[
                          {'label': 'Classic Euler', 'value': 'CE'},
                          {'label': 'Enhanced Euler', 'value': 'EE'},
                          {'label': 'Runge-Kutta', 'value': 'RK'},
                          {'label': 'Exact Solution', 'value': 'EX'}
                      ],
                      value=['CE', 'EE', 'RK', 'EX']),
        # dbc.Col(html.Div('Initial x')),
        dbc.Input(id='x_0', value='1.0', type='number', style={'width': "auto", 'marginLeft': 15}),
        # dbc.Col(html.Div('Initial y')),
        dbc.Input(id='y_0', value='1.0', type='number', style={'width': "auto", 'marginLeft': 15}),
        # dbc.Col(html.Div('Max x')),
        dbc.Input(id='max_x', value='6.0', type='number', style={'width': "auto", 'marginLeft': 15}),
        # dbc.Col(html.Div('Define Step')),
        dbc.Input(id='h_0', value='0.1', type='number', style={'width': "auto", 'marginLeft': 15}),
        dbc.Input(id='n', value='30', type='number', style={'width': "auto", 'marginLeft': 15})
    ], style={'marginLeft': 50}),

    dcc.Graph(id='graph'),
    dcc.Graph(id='errors')
])


def is_ce(arr, x, y, h, max_x=None, n=None):
    if 'CE' in arr:
        return calculation_methods.ordinary_euler(x, y, h, max_x, n)
    else:
        return None


def is_ee(arr, x, y, h, max_x=None, n=None):
    if 'EE' in arr:
        return calculation_methods.enhanced_euler(x, y, h, max_x, n)
    else:
        return None


def is_rk(arr, x, y, h, max_x=None, n=None):
    if 'RK' in arr:
        return calculation_methods.runge_kutta(x, y, h, max_x, n)
    else:
        return None


def is_exact(arr, x, y, h, max_x=None, n=None):
    if 'EX' in arr:
        return calculation_methods.my_func(x, y, h, max_x, n)
    else:
        return None


def final_arr(arr, x, y, h, max_x):
    df = pd.DataFrame()
    ex = is_exact(arr, x, y, h, max_x)
    ee = is_ee(arr, x, y, h, max_x)
    ce = is_ce(arr, x, y, h, max_x)
    rk = is_rk(arr, x, y, h, max_x)
    if ex is not None:
        df = df.append(ex)
    if ee is not None:
        df = df.append(ee)
    if ce is not None:
        df = df.append(ce)
    if rk is not None:
        df = df.append(rk)
    return df


@app.callback(
    Output('graph', 'figure'),
    [Input('check', 'value'),
     Input('x_0', 'value'),
     Input('y_0', 'value'),
     Input('h_0', 'value'),
     Input('max_x', 'value')])
def update_figure(selected_methods, x, y, h, max_x):
    x = float(x)
    y = float(y)
    h = float(h)
    max_x = float(max_x)
    df = final_arr(selected_methods, x, y, h, max_x)

    traces = []
    for i in df.method.unique():
        df_by_method = df[df['method'] == i]
        traces.append(go.Scatter(
            x=df_by_method['x'],
            y=df_by_method['y'],
            text=df_by_method['method'],
            # mode='markers',
            opacity=0.7,
            marker={
                'size': 10,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'x'},
            yaxis={'title': 'y'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


@app.callback(
    Output('errors', 'figure'),
    [Input('check', 'value'),
     Input('x_0', 'value'),
     Input('y_0', 'value'),
     Input('h_0', 'value'),
     Input('n', 'value')])
def errors(selected, x, y, h, n):
    x = float(x)
    y = float(y)
    h = float(h)
    n = int(n)
    df = pd.DataFrame()
    exact = calculation_methods.my_func(x, y, h, n=n)
    # print(exact)
    exact.drop('x', axis=1, inplace=True)
    exact.drop('method', axis=1, inplace=True)
    if is_ee(selected, x, y, h, n=n) is not None:
        help = calculation_methods.enhanced_euler(x, y, h, n=n)
        help.drop('x', axis=1, inplace=True)
        help.drop('method', axis=1, inplace=True)
        df1 = calculation_methods.errors(exact, help, 'enhanced_euler')
        df1.drop('global', axis=1, inplace=True)
        df = df.append(df1)
    if is_ce(selected, x, y, h, n=n) is not None:
        help = calculation_methods.ordinary_euler(x, y, h, n=n)
        help.drop('x', axis=1, inplace=True)
        help.drop('method', axis=1, inplace=True)
        df1 = calculation_methods.errors(exact, help, 'ordinary_euler')
        df1.drop('global', axis=1, inplace=True)
        df = df.append(df1)
    if is_rk(selected, x, y, h, n=n) is not None:
        help = calculation_methods.runge_kutta(x, y, h, n=n)
        help.drop('x', axis=1, inplace=True)
        help.drop('method', axis=1, inplace=True)
        df1 = calculation_methods.errors(exact, help, 'runge_kutta')
        df1.drop('global', axis=1, inplace=True)
        df = df.append(df1)

    traces = []
    for i in df.method.unique():
        df_by_method = df[df['method'] == i]
        traces.append(go.Scatter(
            x=df_by_method['n'],
            y=df_by_method['local'],
            text=df_by_method['method'],
            # mode='markers',
            opacity=0.7,
            marker={
                'size': 10,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'n'},
            yaxis={'title': 'local error'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


def run():
    app.run_server(debug=True)


# if __name__ == '__main__':
#     app.run_server(debug=True)
