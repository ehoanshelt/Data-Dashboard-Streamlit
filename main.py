import pandas as pd
import streamlit as st
import utilities.prepare_data as prepare
from utilities.graphs import GraphHelper
from utilities.bigquery import BigQuery

page_title = "Sales Dashboard"
page_icon = ":zap:"
st.set_page_config(page_title= page_title, page_icon= page_icon)

# Pull in data from Big Query
bq = BigQuery()
df = bq.run_query("""
                    SELECT 
                        EXTRACT(DATE FROM date_created) as date_created,
                        install_name, 
                        count(order_id) as total_orders, 
                        ROUND(sum(sub_total_usd), 2) as total_revenue
                    FROM `streamlit-data-409015.gmv_orders.raw_data`
                    GROUP BY EXTRACT(DATE FROM date_created), install_name
                  """)

# Add features to the data set
df = prepare.feature_engineer(df)

# Render the page
with st.sidebar: # Sidebar
    st.image("assets/Screenshot 2023-12-23 at 2.25.21 PM.png", width=150)

    install_name = st.selectbox("Install Name", df["install_name"].sort_values().unique())

    year = st.multiselect("Choose Year", df[df["install_name"] == install_name]["year"].sort_values().unique())
    
    #import data into GraphHelper
    gh = GraphHelper(df)
    
    # Filters the dataframes for visuals based on the conditions above
    filtered_df = gh.filter_data({"install_name": install_name, "year": year})

with st.container(): # Main Content Area

    st.title(f'Sales Dashboard for {install_name}')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Average revenue per order")
        st.write(round(filtered_df["total_revenue"].sum() / filtered_df["total_orders"].sum(), 2))
    with col2:
        st.subheader("Average revenue per day")
        st.write(round(filtered_df["total_revenue"].mean(), 2))
    with col3:
        st.subheader("Average orders per day")
        st.write(round(filtered_df["total_orders"].mean(), 0))

    st.divider()

    st.subheader('Revenue over time ')
    st.plotly_chart(gh.generate_lineplot("date_created", "total_revenue"), use_container_width=True)


    st.subheader('How many orders per day?')
    st.plotly_chart(gh.generate_histplot( "total_orders"), use_container_width=True)

    st.subheader('How much revenue per day?')
    st.plotly_chart(gh.generate_histplot("total_revenue"), use_container_width=True)

    st.subheader("Distribution of Sales")

    by_month, day_of_week, by_week = st.tabs(["By Month", "By Day of Week", "By Week"])
    y = "total_revenue"

    with by_month:
        st.plotly_chart(gh.generate_boxplot("month", y), use_container_width=True)
    with day_of_week:
        st.plotly_chart(gh.generate_boxplot("day_of_week", y),use_container_width=True)
    with by_week:
        st.plotly_chart(gh.generate_boxplot("week_of_year", y), use_container_width=True)

    st.subheader(f"Raw Data for {install_name}")
    st.dataframe(df[df["install_name"] == install_name][["date_created", "install_name", "total_orders", "total_revenue"]].sort_values('date_created'), hide_index=True, use_container_width=True)






