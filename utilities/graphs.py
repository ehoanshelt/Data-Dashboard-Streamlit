import plotly.express as px
import pandas as pd

def generate_data_selection(data:pd.DataFrame, settings:dict) -> pd.DataFrame:
    if len(settings["year"]) == 0:
        return data[data["install_name"] == settings["install_name"]]
    
    return data[(data["install_name"] == settings["install_name"]) & (data["year"].isin(settings["year"]))]

def generate_boxplot(data:pd.DataFrame, xValue: str, yValue: str):
    fig = px.box(data, x=xValue, y=yValue)
    return fig

def generate_histplot(data:pd.DataFrame, xValue: str, category: str ="year", sortby: str="year") -> px.histogram:
    fig = px.histogram(data.sort_values(sortby), x=xValue, color=category, barmode="overlay", color_discrete_sequence=px.colors.sequential.Inferno)
    return fig

def generate_lineplot(data: pd.DataFrame, xValue: str, yValue: str, sortby: str="date_created") -> px.line:
    fig = px.line(data.sort_values(sortby), x=xValue, y=yValue)
    return fig