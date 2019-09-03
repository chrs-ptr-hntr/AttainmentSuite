import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv('https://raw.githubusercontent.com/chrs-ptr-hntr/AttainmentSuite/master/data/attendance.csv')

df["ACORN"] = df["ACORN"].astype('str')
df["SIMD"] = df["SIMD"].astype('str')

app.layout = html.Div([
        
    dbc.Row(dbc.Col(dbc.Navbar(
                
            dbc.Col(html.Img(src="https://raw.githubusercontent.com/chrs-ptr-hntr/AttainmentSuite/master/assets/logo.jpg", height="50px")),
                
               color="dark",
               dark=True,
            
            )
    )),
        
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
                id='simd_filter',
                options=[{'label': i, 'value': i} for i in sorted(df["SIMD"].unique())],
                placeholder="Select SIMD Quintile",
                multi = True),
                        
                dcc.Dropdown(
                id='gender_filter',
                options=[{'label': i, 'value': i} for i in sorted(df["Gender"].unique())],
                placeholder="Select Gender",
                multi = True)], width = 3),
            
            dbc.Col(dcc.Graph(id='timeseriesgraph'))

             ]),

                    ])

@app.callback(
    [Output('timeseriesgraph', 'figure'),
     Output('acorn_filter', 'options'),
     Output('school_filter', 'options'),
     Output('gender_filter', 'options'),
     Output('simd_filter', 'options')],
    [Input('acorn_filter', 'value'),
     Input('school_filter', 'value'),
     Input('gender_filter', 'value'),
     Input('simd_filter', 'value')])
    
def update_figure(selected_acorn, selected_school, selected_gender, selected_simd):
    
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
        
    if not selected_simd:
        dfa = dfa
    else:
        dfa = dfa[dfa['SIMD'].isin(selected_simd)]
    
    dff = dfa.groupby("Year", as_index = False, sort = "ascending").sum()
    
    return [{
            'data': [
                {'x': dff.Year, 'y':dff.Actual/dff.Possible, 'mode': 'lines'}
            ], 
            'layout': {
                'title': 'Attendance over time',
                'yaxis': dict(range=[0,1],tickformat="%"),
                'xaxis': {'type': 'category', 'categoryorder': 'category ascending'},
                'margin':{'pad':20}
            }
        
        },
            
        [{'label': i, 'value': i} for i in sorted(dfa["ACORN"].unique(), reverse=True)],
        [{'label': i, 'value': i} for i in sorted(dfa["School"].unique())],
        [{'label': i, 'value': i} for i in sorted(dfa["Gender"].unique())],
        [{'label': i, 'value': i} for i in sorted(dfa["SIMD"].unique())]
        
]


if __name__ == '__main__':
    app.run_server(debug=True)