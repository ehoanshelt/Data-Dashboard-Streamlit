import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
class BigQuery:
    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        self.client = bigquery.Client(credentials=self.credentials)


# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
    @st.cache_data(ttl=600)
    def run_query(_self, query: str) -> pd.DataFrame:
        results = _self.client.query(query).to_dataframe()
        return results