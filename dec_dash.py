#Project_Name : DEC Interactive dashboard using 
# 1.Python-3
# 2. dash (a plotly frameworkused for dashboards)


# Name of the Programmer : K Sunil Joshi

# app reuirements : install python-3 , install dash using command 'pip install -- dash'

#run this .py file and copy paste the IP address generated into ypur browser to visualize the dashboard

'''APP Development '''


# imporing required librarie for dash , pandas data frame

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd


# dash app layout which decides the main UI of the app


app = dash.Dash()

#read test.csv data from local path/location

df1 = pd.read_csv('test.csv',low_memory = False)


#seelcting data only from year 1995

new_df = df1.loc[(df1['SAMPLE_YEAR'] > 1995)]




#save to new file

new_df.to_csv('new_data.csv')


# use new data set which contains data from year 1995

df = pd.read_csv('new_data.csv',low_memory = False)


#selecting different columns from the datafarem and making them unique() so that there are no duplicates

df1 = df['WATER'].unique()

df2 = df['SAMPLE_YEAR']

df3 = df['Characteristic_Name'].unique()
df4 =df['County'].unique()
df5 = df['BASIN'].unique()
df6 = df['Result Value']






# dash UI layout for dropdowns to select , radioitems
# dropdowns include chemical_type or Basin 
# and radio itesm for scale on graph like linear or log scale 
# the graph div is for data represinting the graph
# te slider is used to slide between years and visualize the data , given min , max range




app.layout = html.Div([
    html.Div([

        # the dropdown and radiobutton here is for main graph on the left of the dashboard
        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in df3],
                value = 'chemical_type'
            
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value':   i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        # this dropdown and radiobutton is for time series graph on righthand side 
        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in df3],
                value='chemical_type'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Albany'}]},
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    # the slider here is used to select year b/w 1995-2017 and visualize data accordingly
    html.Div(dcc.Slider(
        id='crossfilter-year--slider',
        min=df['SAMPLE_YEAR'].min(),
        max=df['SAMPLE_YEAR'].max(),
        value=df['SAMPLE_YEAR'].max(),
        step=None,
        marks={str(year): str(year) for year in df['SAMPLE_YEAR'].unique()}
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'}) 
])


'''basically a calllback is a decorator in python which is used to call data from other functions defined in the program,
 here the dash app callback uses args like what column ,type and slider uses what value'''



# the input ouput in call backs are the propertis of a particular components ,
# for this callback the input component is value and o/p component is figure with their respective id like scatter, xaxis , yaxis col.


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])


# In this update_graph fucntion  we are updating graph data by passing 4 args(xasix data, y axis data , types and year value) whcih returns graph data 
#values and regions and the html componens of the graph like size, width and color.

def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['SAMPLE_YEAR'] == year_value]

    return {
        'data': [go.Scatter(
            x=dff[dff['Characteristic_Name'] == xaxis_column_name]['Result Value'],
            y=dff[dff['Characteristic_Name'] == yaxis_column_name]['Result Value'],
            text=dff[dff['Characteristic_Name'] == yaxis_column_name]['County'],
            customdata=dff[dff['Characteristic_Name'] == yaxis_column_name]['County'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


# ths time_series_function takes 3 args and try to update the valus which display on right hand side of the dashboard visulization ,
# which basically returns valus to be plotted on time series graph from the dataset coulns like year,
# result value and also html componens of the graph.





def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['SAMPLE_YEAR'],
            y=dff['Result Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }

@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])


# here we are upating timesseries graph of Y axis on right hand side in the dashboard
# this fucntion takes 3 params like county name , char_name and updates the graph with its labels

# hoverdata is when we move our cursor on the graph it will automatically display the corresponding time_series data on right hand side

def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    county_name = hoverData['points'][0]['customdata']
    dff = df[df['County'] == county_name]
    dff = dff[dff['Characteristic_Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(county_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)

@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])


# here we are upating timesseries graph of X axis on right hand side in the dashboard
# this fucntion takes 3 params like county name , char_name and returns time_sreis function data which is called ref to above create_time_series_fucn
#and updates  the graph with its labels

def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['County'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Characteristic_Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)


# this is the css styling applied to the app from the url 
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


# main fucntion used to run directy the .py file
if __name__ == '__main__':
    app.run_server()
 



