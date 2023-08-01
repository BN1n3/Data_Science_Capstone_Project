# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

path=r'C:\Users\juanc\OneDrive\Escritorio\Python\IBM\Data Science Capstone Project\spacex_launch_dash.csv'
with open(path, 'rb') as csvfile:
    spacex_df = pd.read_csv(csvfile, 
                encoding = "ISO-8859-1")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),

                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                                 {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                                 {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                                 {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'}
                                             ],
                                             value='ALL',
                                             placeholder='Select a launch site here',
                                             searchable=True
                                             ),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class'] == 1]
        total_val = filtered_df['Launch Site'].value_counts().sum()
        values = filtered_df['Launch Site'].value_counts()/total_val
        names = values.index.values
        values_df=pd.DataFrame(values)
        fig = px.pie(values_df, values='count', 
        names = names, 
        title = 'Total succes launches by launch site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df = filtered_df[['class']]
        val_count = filtered_df.value_counts().sum()
        rate = filtered_df.value_counts()/val_count
        names = rate.index.values
        rate_df = pd.DataFrame(rate)
        fig = px.pie(rate_df, values='count', 
        names = names, 
        title = 'Total launches for site: {}'.format(entered_site))
        return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site, payload_slider):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        min = payload_slider[0]
        max = payload_slider[1]
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min) & (spacex_df['Payload Mass (kg)'] <= max)]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=entered_site)
        return fig
    else:
        min = payload_slider[0]
        max = payload_slider[1]
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min) & (spacex_df['Payload Mass (kg)'] <= max)]
        filtered_df = filtered_df[filtered_df['Launch Site']==entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=entered_site)
        return fig

if __name__ == '__main__':
    app.run_server(port=8051)