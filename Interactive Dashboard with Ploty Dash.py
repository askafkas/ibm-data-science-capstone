#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
#wget wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"
# pip3 install pandas dash

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[{'label': 'All Sites', 'value': 'ALL'},
                                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                                                value='ALL',
                                                                placeholder='Select a Launch Site here',
                                                                searchable=True),                            
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={ 0: {'label': '0 Kg', 'style': {'color': '#77b0b1'}},
                                                        1000: {'label': '1000 Kg'},
                                                        2000: {'label': '2000 Kg'},
                                                        3000: {'label': '3000 Kg'},
                                                        4000: {'label': '4000 Kg'},
                                                        5000: {'label': '5000 Kg'},
                                                        6000: {'label': '6000 Kg'},
                                                        7000: {'label': '7000 Kg'},
                                                        8000: {'label': '8000 Kg'},
                                                        9000: {'label': '9000 Kg'},
                                                        10000: {'label': '10000 Kg'}},
                                                value=[min_payload , max_payload]),                               
 
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df.groupby('Launch Site')['class'].sum().to_frame().reset_index().rename(columns={"class": "nb_success"})
        fig = px.pie(filtered_df, values='nb_success', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]['class'].value_counts().to_frame().reset_index()
        filtered_df = filtered_df.rename(columns={"index": "class", "class": "count"})
        fig = px.pie(filtered_df, values="count", 
        names="class", 
        title='Total Success Launches for '+ entered_site)
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, slider_value):
    if entered_site == 'ALL':
        filtered_df = spacex_df[['Payload Mass (kg)', 'class', 'Booster Version Category']]
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)'].between(slider_value[0], slider_value[1], inclusive=True)]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
        title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]['Payload Mass (kg)', 'class', 'Booster Version Category']
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)'].between(slider_value[0], slider_value[1], inclusive=True)]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
        title='Correlation between Payload and Success for ' + entered_site)
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
