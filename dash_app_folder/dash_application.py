import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import os



# Create dash app
def create_dash_application(flask_app,engine):
    # Crear la conexión entre las dos libreríás 
    # Indicar las configuraciones: 
    # - Necesita correr en un server de flask
    dash_app = dash.Dash(__name__, server = flask_app, url_base_pathname="/dash/",update_title=None)#, assets_folder= assets_path)

    data_frame = pd.read_sql_query('select * from "supply"',con=engine)

    dash_app.layout = html.Div(
        children=[
        build_page(data_frame)
    ],style={'marginBottom': 0, 'marginTop': 0})

    return dash_app,data_frame

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

def build_graphics(data_frame): 
    fig_pie = build_pie(data_frame)
    return html.Div(id="fullpage",
        children=[
            dcc.Graph(
                id='tabla-supply'),
            dcc.Graph(id='pie-supply',figure=fig_pie)
                
        ])

def build_footer(): 
    return html.Footer(
        className="footer pt-60", 
        children=[
            html.Div(className="container",
            children=[
                html.Div(className="row footer-info mb-30",
                    children=[
                    # col-md-6
                    html.Div(className="col-md-6 col-sm-12 col-xs-12 mb-sm-30 text-sm-left",
                             children=[html.P("Powered by STOCKER",className="mb-xs-0"),
                                       html.Ul(className="link-small",
                                               children=[
                                                   html.Li([html.A(href="mailto:yourname@domain.com",children=["stocker@infostocker.com",html.I(className="fa fa-envelope-o left")])]),
                                                   html.Li([html.A([html.I(["948 577 658"],className="fa fa-phone left",)])])
                                               ])

                             ]),
                    # col-md-6 col-sm-12
                    html.Div(className="col-md-6 col-sm-12 col-xs-12 text-right text-sm-left",
                             children=[
                                 html.Ul(className="link",
                                         children=[
                                                html.Li([html.A(["Políticas de Privacidad"],href="privacy-policy.html")]),
                                                html.Li([html.A(["T&C"],className="terms-and-conditions.html")]),
                                                html.Li([html.A(["FAQ"],className="faq.html")]),
                                                html.Li([html.A(["Contacto"],className="contact-us.html")])                                                
                                                  ]),
                                 html.Div(className="spacer-30"),
                                 html.Ul(className="social",
                                         children=[
                                                html.Li([html.A([html.I(className="fa fa-twitter")],target="_blank",href="https://www.twitter.com/")]),
                                                html.Li([html.A([html.I(className="fa fa-instagram")],target="_blank",href="https://instagram.com/")]),
                                                html.Li([html.A([html.I(className="fa fa-facebook")],target="_blank",href="https://www.facebook.com/")]),
                                                html.Li([html.A([html.I(className="fa fa-youtube")],target="_blank",href="https://youtube.com/")]),
                                                html.Li([html.A([html.I(className="fa fa-linkedin")],target="_blank",href="https://www.linkedin.com/")])                                                 
                                                  ])
                             ])
                    
                    
                    ])

                ])
            ]
    )

def build_scroll():
    return html.A([html.I(className="fa fa-angle-double-up")],className="scroll-top")

def build_page(data_frame):
    return html.Div(children=[
        #build_search_overlay(),
        build_wrapper(),
        build_dashboardtitle(),
        build_clearfix(),
        build_dash_graphics(data_frame),
        build_footer(),
        build_scroll()],style={'overflowY': 'scroll', 'height': '100vh'})#style={'overflowY': 'scroll', 'height': 720})

def build_table(dataframe,max_rows = 4):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], className="table")

def build_dropdown_supply():
    return html.Div([
        dcc.Dropdown(
            id = 'category-supply',
            options = [{'label':'Precio','value':'price'},{'label':'Cantidad','value':'quantity'}],
            value = "price"
        )
    ],style={'padding-top':'50px'})

def build_dash_graphics(data_frame): 
    return html.Div([
        build_dropdown_supply(),
        build_graphics(data_frame),
        build_table(data_frame)
    ],style={'padding-left':'8%','padding-right':'8%','padding-top':'50px '})

def build_pie(data_frame):
    data_frame_edit = data_frame.groupby('category')['quantity'].count()
    # print(data_frame_edit)
    fig_pie = px.pie(data_frame_edit,values='quantity')    
    #dcc.Graph(id="pie-chart", fig=fig_pie)
    return fig_pie