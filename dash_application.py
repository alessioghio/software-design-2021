import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import os


df = pd.read_csv('databases_testing/database_supply.csv')
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })


assets_path = os.getcwd() + '/static'

# Create dash app
def create_dash_application(flask_app):
    # Crear la conexión entre las dos libreríás 
    # Indicar las configuraciones: 
    # - Necesita correr en un server de flask
    dash_app = dash.Dash(__name__, server = flask_app, url_base_pathname="/dash/",update_title=None, assets_folder=assets_path)

    dash_app.layout = html.Div(
        children=[
        #build_preloader(),
        build_search_overlay(),
        build_wrapper(),
        build_dashboardtitle(),
        build_clearfix(),
        build_graphics()
    ])

    return dash_app

def build_preloader():
    return html.Section(
        id = "preloader",
        children=[
            html.Div(
                className="loader",
                id="loader",
                children=[
                    html.Div(
                        className="loader-img"
                            )
                        ]
                    )
                ]
            )

def build_search_overlay():
    return html.Div(
                className="search-overlay-menu",
                children=[
                    html.Span(
                        className="search-overlay-close",
                        children=[
                            html.I(
                                className="ion ion-ios-close-empty"
                            )
                        ]   
                    )
                ])

def build_wrapper():
    return html.Div(
                className="wrapper",
                children=[
                    html.Header(
                        id="header",
                        className="header shadow",
                        children=[
                            html.Div(
                                className="header-inner",
                                children=[
                                    # Primer Div de Logo
                                    html.Div(
                                        className="logo",
                                        children=[
                                            html.A(
                                                href="../",
                                                children=[
                                                    html.Img(
                                                        className="logo-light",
                                                        src="../static/img/gth-logo-white.png",
                                                        alt="Global Talent House"),
                                                    html.Img(
                                                        className="logo-dark",
                                                        src="../static/img/gth-logo-dark.png",
                                                        alt="Global Talent House")
                                                ])
                                        ]),
                                    # Fin del div de Logo
                                    html.Div(
                                        className="nav-mobile nav-bar-icon",
                                        children=[html.Span()]),
                                    # Inicio de Nav Menu
                                    html.Div(
                                        className="nav-menu",
                                        children=[
                                            html.Ul(
                                                className="nav-menu-inner",
                                                children=[
                                                    html.Li(children=[html.A("Profile",className="btn btn-md btn-black join-btn", href="../profile-stocker")]),
                                                    # html.Li(
                                                    #     children=[
                                                    #         html.A(
                                                    #             className="menu-has-sub",
                                                    #             children=["Emprendimientos Powered by Stocker",html.I(className="fa fa-angle-down")]),
                                                    #         html.Ul(
                                                    #             className="sub-dropdown dropdown",
                                                    #             children=[  html.Li(children=[html.A("Pizza Raúl",href="../home-pizza")]),
                                                    #                         html.Li(children=[html.A("Cevicheria Raúl",href="#")]),
                                                    #                         html.Li(children=[html.A("Postres Raúl",href="#")]),
                                                    #                         html.Li(children=[html.A("Profile ",href="../profile-stocker")])
                                                    #                     ]),
                                                    #             ]),
                                                    html.Li(children=[html.A("Log Out",className="btn btn-md btn-black join-btn", href="#")])
                                                        ]
                                                    )

                                                ]

                                            )

                                        ]
                                    )
                                    # Fin de Nav Menu
                                ]
                            )
                        ]
                    )

def build_dashboardtitle(): 
    return html.Section(className="inner-intro dark-bg overlay-dark",
                        children=[
                            html.Div(className="container",
                                     children=[
                                         html.Div(className="row title",
                                                  children=[
                                                      html.H2("Dashboard Stocker",className="h2")
                                                  ])
                                     ])
                        ])

def build_clearfix():
    return html.Div(className="clearfix")

def build_graphics(): 
    return html.Div(id="fullpage",
        children=[
            dcc.Graph(
                id='tabla_supply',
                figure=px.bar(df, x="name", y="quantity", color="category ", barmode="group")
            )
        ])