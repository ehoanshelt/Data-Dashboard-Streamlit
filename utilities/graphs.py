import plotly.express as px
import pandas as pd

class GraphHelper:
    def __init__(self, data: pd.DataFrame):
        """A class that helps eliminate redundant code. 
        When ready, use the import_data method to capture the data"""
        self.data: pd.DataFrame = data

    def filter_data(self, settings:dict) -> pd.DataFrame:
        """Pass the settings for the Year and Install Name as a dictionary to return a filtered DataFrame"""
        if len(settings["year"]) == 0:
            self.data = self.data[self.data["install_name"] == settings["install_name"]]
            return self.data
        
        self.data = self.data[(self.data["install_name"] == settings["install_name"]) & (self.data["year"].isin(settings["year"]))]
        return self.data

    def generate_boxplot(self, xValue: str, yValue: str):
        fig = px.box(self.data, x=xValue, y=yValue)
        return fig

    def generate_histplot(self, xValue: str, category: str ="year", sortby: str="year") -> px.histogram:
        fig = px.histogram(self.data.sort_values(sortby), x=xValue, color=category, barmode="overlay", color_discrete_sequence=px.colors.sequential.Inferno)
        return fig

    def generate_lineplot(self, xValue: str, yValue: str, sortby: str="date_created") -> px.line:
        fig = px.line(self.data.sort_values(sortby), x=xValue, y=yValue)
        return fig