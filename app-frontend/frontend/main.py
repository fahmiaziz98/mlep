import requests
import streamlit as st

from settings import API_URL, TITLE
from components import build_data_plot


st.set_page_config(page_title=TITLE)
st.title(TITLE)

area = None
consumer_type = None
# Buat dropdown untuk area cari di router area_values view.py
area_response = requests.get(API_URL / "area_values")
area = st.selectbox(
    label="Industry Code DE36",
    options=area_response.json().get("values", [])
)

# Buat dropdown untuk consumer type cari dirouter consumer_type_values
consumer_type_response = requests.get(API_URL / "consumer_type_values")
consumer_type = st.selectbox(
    label="Industry Code DE19",
    options=consumer_type_response.json().get("values", [])
)

if area is not None and consumer_type is not None:
    st.plotly_chart(build_data_plot(area, consumer_type))
