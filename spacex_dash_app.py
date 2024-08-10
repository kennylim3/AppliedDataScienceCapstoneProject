import pandas as pd
from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = int(spacex_df['Payload Mass (kg)'].max())
min_payload = int(spacex_df['Payload Mass (kg)'].min())

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
        ],
        value='ALL',
        placeholder='Select a Launch Site',
        style={'width': '80%'}
    ),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={i: str(i) for i in range(0, max_payload+1, 10000)},
        value=[min_payload, max_payload]
    ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        df = spacex_df
    else:
        df = spacex_df[spacex_df['Launch Site'] == selected_site]

    success_counts = df['class'].value_counts()
    fig = px.pie(
        names=success_counts.index,
        values=success_counts.values,
        title=f"Launch Success Count for {selected_site}" if selected_site != 'ALL' else "Launch Success Count for All Sites"
    )
    return fig

# TASK 4: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    min_payload, max_payload = payload_range
    if selected_site == 'ALL':
        df = spacex_df
    else:
        df = spacex_df[spacex_df['Launch Site'] == selected_site]

    df = df[(df['Payload Mass (kg)'] >= min_payload) & (df['Payload Mass (kg)'] <= max_payload)]

    fig = px.scatter(
        df,
        x='Payload Mass (kg)',
        y='class',
        color='class',
        title=f"Payload vs. Success for {selected_site}" if selected_site != 'ALL' else "Payload vs. Success for All Sites",
        labels={'class': 'Launch Success'}
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)