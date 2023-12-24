import plotly.express as px
import pandas as pd

def generate_data_selection(data:pd.DataFrame, settings:dict) -> pd.DataFrame:
    if len(settings["year"]) == 0:
        return data[data["install_name"] == settings["install_name"]]
    
    return data[(data["install_name"] == settings["install_name"]) & (data["year"].isin(settings["year"]))]

def generate_boxplots(data:pd.DataFrame, xValue, yValue):
    fig = px.box(data, x=xValue, y=yValue)
    return fig

def generate_histplots(data:pd.DataFrame, xValue, category="year"):
    fig = px.histogram(data, x=xValue, color=category)
    return fig