import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

df = pd.read_csv('https://raw.githubusercontent.com/chrs-ptr-hntr/AttainmentSuite/master/data/attendance.csv')

df["ACORN"] = df["ACORN"].astype('str')
df["SIMD"] = df["SIMD"].astype('str')
df["Year"] = df["Year"].astype('str')


app.layout = html.Div([
        
        dbc.Navbar(dbc.Row(
                [
                    dbc.Col(html.Img(src="https://raw.githubusercontent.com/chrs-ptr-hntr/AttainmentSuite/master/assets/mainlogo.jpg", height="50px"),width=2),
                    dbc.Col(dbc.NavbarBrand("The Attainment Suite"), width = 6, align="center"),
                    dbc.Col(
                    dbc.DropdownMenu(
                            children=[
                            dbc.DropdownMenuItem("More tools", header=True),
                            dbc.DropdownMenuItem("Attendance", href="#"),
                            dbc.DropdownMenuItem("CfE Levels", href="#"),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="More tools",
                        toggle_style={'color':'white'}
        ), width=4, align='center'),

                ]),
    color="dark",
    dark=True,
    sticky=True
),
        
       dbc.Row([dbc.Col([
                
                html.H5("Filters",style={'color': 'steelblue', 'text-align':'center'}),
                
                dcc.Dropdown(
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
                multi = True),
                        
                dcc.Dropdown(
                id='year_filter',
                options=[{'label': i, 'value': i} for i in sorted(df["Year"].unique())],
                placeholder="Select Year",
                multi = True)], width = 3),
            
            dbc.Col(dcc.Graph(id='timeseriesgraph'),width = 4),

            dbc.Col(dcc.Graph(id='bubblegraph'),width = 5)

             ])

                    ],style={'background-color':'WhiteSmoke'})

@app.callback(
    [Output('timeseriesgraph', 'figure'),
     Output('bubblegraph', 'figure'),
     Output('acorn_filter', 'options'),
     Output('school_filter', 'options'),
     Output('gender_filter', 'options'),
     Output('simd_filter', 'options'),
     Output('year_filter', 'options')],
    [Input('acorn_filter', 'value'),
     Input('school_filter', 'value'),
     Input('gender_filter', 'value'),
     Input('simd_filter', 'value'),
     Input('year_filter', 'value')])
    
def update_figure(selected_acorn, selected_school, selected_gender, selected_simd, selected_year):
    
    if not selected_acorn:
        dfa = df
        dfp = df
        afa = df
        afp = df
    else:
        dfa = df[df['ACORN'].isin(selected_acorn)]
        dfp = df[df['ACORN'].isin(selected_acorn)]
        afa = df
        afp = df
                
    if not selected_school:
        dfa = dfa
        afa = afa
    else:
        dfa = dfa[dfa['School'].isin(selected_school)]
        afa = afa[afa['School'].isin(selected_school)]   
    
    if not selected_gender:
        dfa = dfa
        dfp = dfp  
        afa = afa
        afp = afp
        
    else:
        dfa = dfa[dfa['Gender'].isin(selected_gender)]
        dfp = dfp[dfp['Gender'].isin(selected_gender)]
        afa = afa[afa['Gender'].isin(selected_gender)]
        afp = afp[afp['Gender'].isin(selected_gender)]       
        
              
    if not selected_simd:
        dfa = dfa
        dfp = dfp
        afa = afa
        afp = afp
    else:
        dfa = dfa[dfa['SIMD'].isin(selected_simd)]
        dfp = dfp[dfp['SIMD'].isin(selected_simd)]
        afa = afa[afa['SIMD'].isin(selected_simd)]
        afp = afp[afp['SIMD'].isin(selected_simd)]
        
    if not selected_year:
        afa = afa
        afp = afp
    else:
        afa = afa[afa['Year'].isin(selected_year)]
        afp = afp[afp['Year'].isin(selected_year)] 
    
    dff = dfa.groupby("Year", as_index = False, sort = "ascending").sum()
    dfpkc = dfp.groupby("Year", as_index = False, sort = "ascending").sum()
    
    aff = afa.groupby("ACORN", as_index = False, sort = "ascending").sum()
    afpkc = afp.groupby("ACORN", as_index = False, sort = "ascending").sum()
    
    bubblesize = [len(afa[afa['ACORN'] == '5'])/len(afa),len(afa[afa['ACORN'] == '4'])/len(afa),len(afa[afa['ACORN'] == '3'])/len(afa),len(afa[afa['ACORN'] == '2'])/len(afa),len(afa[afa['ACORN'] == '1'])/len(afa)]
    pkcbubblesize = [len(afp[afp['ACORN'] == '5'])/len(afp),len(afp[afp['ACORN'] == '4'])/len(afp),len(afp[afp['ACORN'] == '3'])/len(afp),len(afp[afp['ACORN'] == '2'])/len(afp),len(afp[afp['ACORN'] == '1'])/len(afp)]
    
    bubblesize = [round(x*100) for x in bubblesize]
    pkcbubblesize = [round(x*100) for x in pkcbubblesize]
    return [{
            'data': [
                
                {'x': dfpkc.Year, 'y':dfpkc.Actual/dfpkc.Possible, 'mode': 'lines', 'name': "PKC", 'marker':{'color':'darkgrey'}},
                {'x': dff.Year, 'y':dff.Actual/dff.Possible, 'mode': 'lines', 'name': "Selection",'marker':{'color':'blue'}},
                
            ], 
            'layout': {
                'title': 'Attendance over time',
                'yaxis': dict(range=[0,1],tickformat="%"),
                'xaxis': {'type': 'category', 'categoryorder': 'category ascending'},
                'margin':{'pad':20}
            }
        
        },
           
        {
            'data': [
                
                {'x': afpkc.ACORN, 'y':afpkc.Actual/afpkc.Possible, 'mode': 'markers','name': "PKC", 'marker':{'color':'darkgrey','size':pkcbubblesize, 'sizemode':'area','sizeref':2.*max(pkcbubblesize)/(40**2), 'sizemin':4}},
                {'x': aff.ACORN, 'y':aff.Actual/aff.Possible, 'mode': 'markers', 'name': "Selection",'marker':{'color':'blue','size':bubblesize, 'sizemode':'area','sizeref':2.*max(bubblesize)/(40**2), 'sizemin':4}},
                
            ], 
            'layout': {
                'title': 'Attendance by ACORN Category',
                'yaxis': dict(range=[0,1],tickformat="%"),
                'xaxis': {'type': 'category', 'categoryorder': 'category descending'}
            }
        
        },    
            
            
        [{'label': i, 'value': i} for i in sorted(dfa["ACORN"].unique(), reverse=True)],
        [{'label': i, 'value': i} for i in sorted(dfa["School"].unique())],
        [{'label': i, 'value': i} for i in sorted(dfa["Gender"].unique())],
        [{'label': i, 'value': i} for i in sorted(dfa["SIMD"].unique())],
        [{'label': i, 'value': i} for i in sorted(afa["Year"].unique())]
]


if __name__ == '__main__':
    app.run_server(debug=True)