import streamlit as st
import pandas as pd
import plotly.express as px
import preprocessor, helper

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

# Medal Tally
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year))
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    else:
        st.title(selected_country + " performance in " + str(selected_year))

    st.table(medal_tally)

# Overall Analysis
if user_menu == 'Overall Analysis':

    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Year", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Year", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Year", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

# Country-wise Analysis
if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

# Athlete wise Analysis
if user_menu == 'Athlete wise Analysis':
    athlete_df = df.dropna(subset=['Age'])

    x1 = athlete_df[athlete_df['Medal'] == 'Gold']['Age']
    x2 = athlete_df[athlete_df['Medal'] == 'Silver']['Age']
    x3 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age']

    fig = px.histogram(athlete_df, x="Age", nbins=50, title="Distribution of Age of Athletes")
    st.plotly_chart(fig)

    st.title("Age distribution by Medal Type")
    st.write("Gold Medalists")
    st.plotly_chart(px.histogram(x1, nbins=30))
    st.write("Silver Medalists")
    st.plotly_chart(px.histogram(x2, nbins=30))
    st.write("Bronze Medalists")
    st.plotly_chart(px.histogram(x3, nbins=30))
