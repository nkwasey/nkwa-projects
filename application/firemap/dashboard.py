__author__ = "Nana Ekow Nkwa Sey"

"""Instantiate a Fire Dashboard app."""
from datetime import datetime as dt
import dash_bootstrap_components as dbc
import dash
import dash_daq as daq
from dash import html
from dash import dcc
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go

from application.firemap.create_df import create_viirs_arc_df, create_modis_arc_df, create_graph_df

df = create_graph_df()

year_options = []
for year in df['Year'].unique():
    year_options.append({'label': str(year), 'value': year})

source_options = []
for source in df['Source'].unique():
    source_options.append({'label': str(source), 'value': source})

country_options = []
for country in df['Country'].unique():
    country_options.append({'label': str(country), 'value': country})

# Plotly mapbox public token
mapbox_access_token = 'pk.eyJ1Ijoibmt3YXNleSIsImEiOiJja2E2dThpeHAwM2l2MnBtemVja25hZHphIn0.HhZtkswYL5b3O7cJbrhyUw'


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""

    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashboard/',
        external_stylesheets=[dbc.themes.BOOTSTRAP])

    navbar = dbc.NavbarSimple(
        brand="Nkwa's Projects",
        brand_href="#",
        color="primary",
        dark=True,
    )

    date_dropdown = [
        dcc.DatePickerSingle(
            id="date-picker",
            min_date_allowed=dt(2020, 1, 1),
            max_date_allowed=dt(2020, 10, 29),
            initial_visible_month=dt(2020, 1, 1),
            date=dt(2020, 1, 1).date(),
            display_format="MMMM D, YYYY",
            style={"border": "0px solid black", "font-size": "4px"},

        )]

    arc_modis = [
        daq.BooleanSwitch(
            className='',
            id='arc_modis',
            label='MODIS',
            color="#ffaa00",
            labelPosition='top',
            on=True
        )]

    arc_viirs = [
        daq.BooleanSwitch(
            id='arc_viirs',
            label='VIIRS',
            labelPosition='top',
            color='#ff0000',
            on=False
        )]

    markdown = [dcc.Markdown(
        className="mt-3",
        children=[
            "Data Source: [EORIC  ](https://eoric.uenr.edu.gh/)"
        ],
    ), ]

    tab_content = dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        dbc.Row([dbc.Col(html.Div(children=date_dropdown))], justify="center"),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(children=arc_modis), className="mt-6"),
                                dbc.Col(html.Div(children=arc_viirs), className="mt-6"),
                            ]
                        ),
                        dbc.Row([dbc.Col(html.Div(children=markdown))], justify="center"),
                    ]
                )
            ]
        ),
        className="m-1",

    )

    year_dropdown = [
        dcc.Dropdown(
            id="year-picker",
            options=year_options,
            value=df['Year'].max(),
            placeholder="Select a year",
        )]

    instr_dropdown = [
        dcc.Dropdown(
            id="source-picker",
            options=source_options,
            value=df['Source'].min(),
            placeholder="Select source",
        )]

    graph = [dbc.Col(dcc.Graph(id="graph"))]

    graphMenu = html.Div(
        [
            dbc.Row([dbc.Col(html.Div(html.H2("Monthly Fire Charts")))], align='center'),
            dbc.Row([dbc.Col(html.Hr())], align='center'),
            dbc.Row([dbc.Col(html.Div(html.P("""Select different year and source using the dropdown menu to view 
            different bar charts""")))], align='center'),
            dbc.Row([dbc.Col(html.Div(children=year_dropdown))], align='center'),
            dbc.Row([dbc.Col(html.Hr())], align='center'),
            dbc.Row([dbc.Col(html.Div(children=instr_dropdown))], align='center'),
        ]
    )

    def serve_layout():
        return html.Div(style={'backgroundColor': '#FFFFFF'}, children=[
            dbc.Row([dbc.Col(navbar)], align='center'),
            dbc.Row(
                style={'backgroundColor': '#FFFFFF'}, className='m-2', children=[
                    dbc.Col(html.Div(children=[
                        dbc.Button(
                            "Click for Fire Options", id="popover-target", color="primary"
                        ),
                        dbc.Popover(
                            [
                                dbc.PopoverHeader("Available Fire Hotspots in Ghana (Jan, 2020 to October, 2020)"),
                                dbc.PopoverBody(children=tab_content),
                            ],
                            id="popover",
                            is_open=False,
                            placement='bottom-end',
                            target="popover-target",
                        ),
                    ], ))
                ],
                justify="end",
            ),
            dbc.Row(
                style={'backgroundColor': '#FFFFFF'}, className='m-2', children=[
                    dbc.Col(dcc.Graph(id="map"))]),
            dbc.Row([dbc.Col(html.Hr())], align='center'),
            dbc.Row(style={'backgroundColor': '#FFFFFF'},
                    className='m-1',
                    children=[
                        dbc.Col(html.Div(children=graphMenu), md=3),
                        dbc.Col(html.Div(children=graph), md=9)
                    ]
                    )
        ])

    @dash_app.callback(
        Output("popover", "is_open"),
        [Input("popover-target", "n_clicks")],
        [State("popover", "is_open")],
    )
    def toggle_popover(n, is_open):
        if n:
            return not is_open
        return is_open

    # callbacks
    @dash_app.callback(Output('map', 'figure'),
                       [Input('date-picker', 'date'), Input('arc_modis', 'on'), Input('arc_viirs', 'on')])
    def update_map(select_date, source_modis_arc, source_viirs_arc):
        if source_modis_arc:
            df1 = create_modis_arc_df(select_date)
        else:
            df1 = pd.DataFrame(np.nan, index=[0], columns=['latitude', 'longitude'])
        if source_viirs_arc:
            df2 = create_viirs_arc_df(select_date)
        else:
            df2 = pd.DataFrame(np.nan, index=[0], columns=['latitude', 'longitude'])

        return go.Figure(
            data=[
                go.Scattermapbox(
                    lat=df1['latitude'],
                    lon=df1['longitude'],
                    mode="markers",
                    name="MODIS",
                    marker=go.scattermapbox.Marker(
                        size=8,
                        color='rgb(255, 170, 0)',
                        opacity=0.7
                    ),

                    # hoverinfo='none',

                ),
                go.Scattermapbox(
                    lat=df2['latitude'],
                    lon=df2['longitude'],
                    mode="markers",
                    name="VIIRS",
                    marker=go.scattermapbox.Marker(
                        size=8,
                        color='rgb(255,0,0)',
                        opacity=0.7
                    ),

                    # hoverinfo='none',

                ),
            ],
            layout=go.Layout(
                autosize=True,
                height=540,
                hovermode='closest',
                margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                showlegend=False,
                mapbox=dict(
                    accesstoken='pk.eyJ1Ijoibmt3YXNleSIsImEiOiJja2E2dThpeHAwM2l2MnBtemVja25hZHphIn0.HhZtkswYL5b3O7cJbrhyUw',
                    center=dict(lat=7.6381663, lon=-2.1138797),
                    style="satellite-streets",
                    bearing=0,
                    zoom=5,

                ),
                updatemenus=[
                    dict(
                        buttons=(
                            [
                                dict(
                                    args=[
                                        {

                                            "mapbox.style": "streets",
                                        }
                                    ],
                                    label=" Streets ",
                                    method="relayout",
                                ),

                                dict(
                                    args=[
                                        {
                                            "mapbox.zoom": 5,
                                            "mapbox.center.lon": "-2.1138797",
                                            "mapbox.center.lat": "7.6381663",
                                            "mapbox.bearing": 0,
                                            "mapbox.style": "satellite-streets",
                                        }
                                    ],
                                    label=" Reset ",
                                    method="relayout",
                                ),

                                dict(
                                    args=[
                                        {

                                            "mapbox.style": "dark",
                                        }
                                    ],
                                    label=" Dark ",
                                    method="relayout",
                                ),

                            ]
                        ),

                        direction="left",
                        pad={"r": 0, "t": 0, "b": 0, "l": 0},
                        showactive=False,
                        type="buttons",
                        x=0.45,
                        y=0.02,
                        xanchor="left",
                        yanchor="bottom",
                        bgcolor="#323130",
                        borderwidth=1,
                        bordercolor="#6d6d6d",
                        font=dict(color="#FFFFFF"),
                    )
                ],
            ),
        )

    @dash_app.callback(Output('graph', 'figure'),
                       [Input('year-picker', 'value'), Input('source-picker', 'value')])
    def update_bar(selected_year, selected_source):
        if selected_year is None and selected_source is None:
            selected_year = 2019
            selected_source = 'MODIS'

        if selected_source is None:
            selected_source = 'MODIS'

        if selected_year is None:
            selected_year = 2019

        filtered_df = df[(df['Year'] == selected_year) & (df['Source'] == selected_source)]
        traces = []
        for country_name in filtered_df['Country'].unique():
            df_by_country = filtered_df[filtered_df['Country'] == country_name]
            # print(df_by_country)
            traces.append(go.Bar(
                x=df_by_country['Month'],
                y=df_by_country['Fire Count'],
                text=df_by_country['Country'],
                name=country_name
            ))
        return {
            'data': traces,
            'layout': go.Layout(
                title='Monthly Fire Counts in ' + str(selected_year) + ' (' + selected_source + ')',
                xaxis={'title': 'Months'},
                yaxis={'title': 'Fire Counts'},
                hovermode='closest',
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                dragmode="select",
                font=dict(color="black"),
            )
        }

    # Create Layout
    dash_app.layout = serve_layout
    return dash_app.server
