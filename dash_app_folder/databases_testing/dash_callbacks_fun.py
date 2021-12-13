import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd



data_frame = pd.read_sql_query('select * from "supply"',con=engine)