import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv('https://raw.githubusercontent.com/chrs-ptr-hntr/AttainmentSuite/master/data/attendance.csv')

df["ACORN"] = df["ACORN"].astype('str')

app.layout = html.Div([
        
    dbc.Row(dbc.Col(html.H1("The Attainment Suite"))),
        
    dbc.Row([dbc.Col([dcc.Dropdown(
                id='school_filter',
                options=[{'label': i, 'value': i} for i in sorted(df["School"].unique())],
                placeholder="Select School",
                multi = True),
                  
                dcc.Dropdown(
                id='acorn_filter',
                options=[{'label': i, 'value': i} for i in sorted(df["ACORN"].unique(), reverse=True)],
                placeholder="Select ACORN Category",
                multi = True),
                        
                dcc.Dropdown(
                id='gender_filter',
                options=[{'label': i, 'value': i} for i in sorted(df["Gender"].unique())],
                placeholder="Select Gender",
                multi = True)]),
            
            dbc.Col(dcc.Graph(id='timeseriesgraph'))

             ]),

                    ])

@app.callback(
    Output('timeseriesgraph', 'figure'),
    [Input('acorn_filter', 'value'),
     Input('school_filter', 'value'),
     Input('gender_filter', 'value')])
    
def update_figure(selected_acorn, selected_school, selected_gender):
    
    if not selected_acorn:
        dfa = df
    else:
        dfa = df[df['ACORN'].isin(selected_acorn)]
        
    if not selected_school:
        dfa = dfa
    else:
        dfa = dfa[dfa['School'].isin(selected_school)]
        
    if not selected_gender:
        dfa = dfa
    else:
        dfa = dfa[dfa['Gender'].isin(selected_gender)]
    
    dff = dfa.groupby("Year", as_index = False, sort = "ascending").sum()
    
    return {
            'data': [
                {'x': dff.Year, 'y':dff.Actual/dff.Possible, 'mode': 'lines'}
            ], 
            'layout': {
                'title': 'Attendance over time',
                'yaxis': dict(range=[0,1],tickformat="%"),
                'xaxis': {'type': 'category', 'categoryorder': 'category ascending'},
                'margin':{'pad':20},
            }
        
    }



if __name__ == '__main__':
    app.run_server(debug=True)