# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output


spacex_df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')

min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

app = dash.Dash()

# Create Layout
app.layout = html.Div(children=[
    html.H1(
        children='Dashboard',
        style={
            'textAlign': 'center'
        }
    ),

                # Create dropdown
                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                ],
                                value='ALL',
                                placeholder="Select a Launch Site here",
                                searchable=True
                                ),

                    html.Br(),

                    html.Div([
                            html.Div(dcc.Graph(id='success-pie-chart'))], style={'display': 'flex'}),

                    html.P('Payload range (Kg)'),

                # Create rangeslider
                dcc.RangeSlider(min=0, 
                                max=10000, 
                                step=1000,
                                marks={0: '0', 100: '100'},
                                value=[min_payload, max_payload],
                                id='payload-slider'),

                    html.Div([
                            html.Div(dcc.Graph(id='success-payload-scatter-chart'))], style={'display': 'flex'}),

])


# Function decorator to specify function input and output for pie chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
            
def get_pie_chart(entered_site):
    pie_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(pie_df, 
            values='class', 
            names='Launch Site', 
            title='Total Success Launches by Sites')
        return fig
    
    else:
        pie_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        pie_df = filtered_df.groupby(['Launch Site','class']).size().reset_index(name = 'Total class')
        fig1 = px.pie(filtered_df,
            values = 'Total class',
            names='class', 
            title='Total Success Launches for site {}'.format(entered_site))
        return fig1


# Function decorator to specify function input and output for scatter chart
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site, payload):
    scatter_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]
    if entered_site == 'ALL':
        fig2 = px.scatter(scatter_df,
            x = 'Payload Mass (kg)', 
            y ='class', 
            color="Booster Version Category")
        return fig2
    
    else:
        scatter_df = spacex_df[spacex_df['Launch Site'] == entered_site, payload]
        fig3 = px.scatter(scatter_df,
            x = 'Payload Mass (kg)',
            y = 'Total class',
            color="Booster Version Category")
        return fig3



# Run the app
if __name__ == '__main__':
    app.run_server()