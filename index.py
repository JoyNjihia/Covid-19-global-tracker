import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
df = pd.read_csv(url)

# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Sidebar for user input
st.sidebar.title("COVID-19 Data Tracker")
selected_country = st.sidebar.selectbox("Select Country", df['location'].unique())
start_date = st.sidebar.date_input("Start Date", df['date'].min())
end_date = st.sidebar.date_input("End Date", df['date'].max())

# Filter data based on user input
filtered_data = df[(df['location'] == selected_country) &
                   (df['date'] >= pd.to_datetime(start_date)) &
                   (df['date'] <= pd.to_datetime(end_date))]

# Display filtered data
st.write(f"Displaying data for {selected_country} from {start_date} to {end_date}")
st.dataframe(filtered_data)

# Plot total cases over time
fig = px.line(filtered_data, x='date', y='total_cases', title=f"Total COVID-19 Cases in {selected_country}")
st.plotly_chart(fig)

# Plot total deaths over time
fig = px.line(filtered_data, x='date', y='total_deaths', title=f"Total Deaths in {selected_country}")
st.plotly_chart(fig)

# Plot total vaccinations over time
fig = px.line(filtered_data, x='date', y='total_vaccinations', title=f"Total Vaccinations in {selected_country}")
st.plotly_chart(fig)

# Calculate death rate
filtered_data['death_rate'] = filtered_data['total_deaths'] / filtered_data['total_cases']
fig = px.line(filtered_data, x='date', y='death_rate', title=f"Death Rate in {selected_country}")
st.plotly_chart(fig)

# Optional: Plot ICU patients over time if available
if 'icu_patients' in df.columns:
    icu_data = df[(df['location'] == selected_country) &
                  (df['date'] >= pd.to_datetime(start_date)) &
                  (df['date'] <= pd.to_datetime(end_date))]
    fig = px.line(icu_data, x='date', y='icu_patients', title=f"ICU Patients in {selected_country}")
    st.plotly_chart(fig)
else:
    st.write("ICU patient data is not available in the dataset.")

# Optional: Choropleth map of total cases by country
latest_data = df[df['date'] == df['date'].max()]
latest_data = latest_data[['iso_code', 'location', 'total_cases']].dropna()

fig = px.choropleth(latest_data,
                    locations="iso_code",
                    color="total_cases",
                    hover_name="location",
                    title="Global COVID-19 Cases (Latest)",
                    color_continuous_scale="Reds")
st.plotly_chart(fig)
