COVID-19-GLOBAL-TRACKER

# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Filter data for Kenya
df_kenya = df[df['location'] == 'Kenya']

# Define specific default dates
start_date_default = datetime.date(2020, 1, 1)
end_date_default = datetime.date(2021, 12, 31)

# Define the minimum and maximum selectable dates
min_date = datetime.date(2020, 1, 1)
max_date = datetime.date(2021, 12, 31)

# Sidebar for user input
st.sidebar.title("COVID-19 Data Tracker - Kenya")
start_date = st.sidebar.date_input(
    "Start Date",
    value=start_date_default,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "End Date",
    value=end_date_default,
    min_value=min_date,
    max_value=max_date
)

# Filter data based on user input
filtered_data = df_kenya[(df_kenya['date'] >= pd.to_datetime(start_date)) &
                         (df_kenya['date'] <= pd.to_datetime(end_date))]

# Display filtered data
st.write(f"Displaying data for Kenya from {start_date} to {end_date}")
st.dataframe(filtered_data)

# Plot total cases over time
fig = px.line(filtered_data, x='date', y='total_cases', title="Total COVID-19 Cases in Kenya")
st.plotly_chart(fig)

# Plot total deaths over time
fig = px.line(filtered_data, x='date', y='total_deaths', title="Total Deaths in Kenya")
st.plotly_chart(fig)

# Plot total vaccinations over time
fig = px.line(filtered_data, x='date', y='total_vaccinations', title="Total Vaccinations in Kenya")
st.plotly_chart(fig)

# Calculate death rate
filtered_data['death_rate'] = filtered_data['total_deaths'] / filtered_data['total_cases']
fig = px.line(filtered_data, x='date', y='death_rate', title="Death Rate in Kenya")
st.plotly_chart(fig)

# Optional: Plot ICU patients over time if available
if 'icu_patients' in df.columns:
    icu_data = df_kenya[(df_kenya['date'] >= pd.to_datetime(start_date)) &
                        (df_kenya['date'] <= pd.to_datetime(end_date))]
    fig = px.line(icu_data, x='date', y='icu_patients', title="ICU Patients in Kenya")
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
