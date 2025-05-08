import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the data
df = pd.read_csv("owid-covid-data.csv")

# Ensure 'date' is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Filter out continents (iso_code length not equal to 3 indicates non-country entries)
countries = df[df['iso_code'].str.len() == 3]['location'].unique()

# Dropdown to select countries (no default values)
selected_countries = st.multiselect(
    'Select Countries',
    options=sorted(countries)
)

# Check if no countries are selected
if not selected_countries:
    st.warning("Please select at least one country.")
else:
    # Filter data based on selected countries
    filtered_df = df[df['location'].isin(selected_countries)].copy()
    filtered_df.dropna(subset=['date', 'total_cases', 'total_deaths'], inplace=True)

    # Set plotting style
    sns.set(style="whitegrid")

    st.title("COVID-19 Data Analysis")

    # Date range selector
    start_date, end_date = st.slider(
        'Select Date Range',
        min_value=filtered_df['date'].min().date(),
        max_value=filtered_df['date'].max().date(),
        value=(filtered_df['date'].min().date(), filtered_df['date'].max().date())
    )

    # Filter based on date
    filtered_data = filtered_df[
        (filtered_df['date'] >= pd.to_datetime(start_date)) &
        (filtered_df['date'] <= pd.to_datetime(end_date))
    ]

    # Show filtered data
    st.write(filtered_data)

    # Plotting functions
    def plot_total_cases():
        fig, ax = plt.subplots(figsize=(12, 6))
        for country in filtered_data['location'].unique():
            country_data = filtered_data[filtered_data['location'] == country]
            ax.plot(country_data['date'], country_data['total_cases'], label=country)
        ax.set_title('Total COVID-19 Cases Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Total Cases')
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)

    def plot_total_deaths():
        fig, ax = plt.subplots(figsize=(12, 6))
        for country in filtered_data['location'].unique():
            country_data = filtered_data[filtered_data['location'] == country]
            ax.plot(country_data['date'], country_data['total_deaths'], label=country)
        ax.set_title('Total COVID-19 Deaths Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Total Deaths')
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)

    def plot_new_cases():
        fig, ax = plt.subplots(figsize=(12, 6))
        for country in filtered_data['location'].unique():
            country_data = filtered_data[filtered_data['location'] == country]
            ax.plot(country_data['date'], country_data['new_cases'], label=country)
        ax.set_title('Daily New COVID-19 Cases')
        ax.set_xlabel('Date')
        ax.set_ylabel('New Cases')
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)

    def plot_new_deaths():
        fig, ax = plt.subplots(figsize=(12, 6))
        for country in filtered_data['location'].unique():
            country_data = filtered_data[filtered_data['location'] == country]
            ax.plot(country_data['date'], country_data['new_deaths'], label=country)
        ax.set_title('Daily New COVID-19 Deaths')
        ax.set_xlabel('Date')
        ax.set_ylabel('New Deaths')
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)

    # Show plots
    plot_total_cases()
    plot_total_deaths()
    plot_new_cases()
    plot_new_deaths()

    # Choropleth Section
    st.subheader("🌍 Choropleth Map - Latest Global Data")

    # Prepare latest data by iso_code
    latest = df[df['iso_code'].str.len() == 3].sort_values('date').groupby('iso_code').tail(1)

    # Dropdown for metric selection
    metric = st.selectbox(
        "Select a metric to display on the map",
        options=["total_cases", "total_deaths", "people_fully_vaccinated_per_hundred"],
        format_func=lambda x: x.replace('_', ' ').title()
    )

    fig_map = px.choropleth(
        latest,
        locations='iso_code',
        color=metric,
        hover_name='location',
        color_continuous_scale='Viridis',
        title=f"{metric.replace('_', ' ').title()} by Country",
        projection='natural earth'
    )

    st.plotly_chart(fig_map, use_container_width=True)

# Footer
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.0);
        color: #6c757d;
        text-align: center;
        padding: 10px 0;
        font-size: 14px;
    }
    .footer a {
        margin: 0 10px;
        text-decoration: none;
        color: #6c757d;
    }
    .footer a:hover {
        color: #1f77b4;
    }
    </style>

    <div class="footer">
        © 2025 Daniel Kabuna. All rights reserved.
        <br>
        <a href="https://github.com/Kabuna254" target="_blank">GitHub</a> |
        <a href="https://www.linkedin.com/in/daniel-kabuna-0824a1217/" target="_blank">LinkedIn</a> |
        <a href="mailto:danielkabuna@email.com">Email</a>
    </div>
""", unsafe_allow_html=True)
