import pandas as pd
import streamlit as st

@st.cache_data(ttl=600)
def feature_engineer(data: pd.DataFrame) -> pd.DataFrame:
    data["date_created"] = pd.to_datetime(data["date_created"]) # Convert to Datetime object

    #Create new features
    data["month"] = data["date_created"].dt.month
    data["day_of_week"] = data["date_created"].dt.day_of_week
    data["week_of_year"] = data["date_created"].dt.isocalendar().week
    data["year"] = data["date_created"].dt.year

    #Convert date to display date only
    data["date_created"] = data["date_created"].dt.date
    return data
