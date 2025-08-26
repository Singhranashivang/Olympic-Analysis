import numpy as np
import pandas as pd

def medal_tally(df):
    medal_tally = (
        df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
          .groupby('region')
          .agg({'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'})
          .reset_index()
    )
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally = medal_tally.sort_values('Gold', ascending=False).reset_index(drop=True)
    return medal_tally


def country_year_list(df):
    years = df['Year'].dropna().unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = (
            temp_df.groupby('Year')
                   .agg({'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'})
                   .reset_index()
        )
    else:
        x = (
            temp_df.groupby('region')
                   .agg({'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'})
                   .reset_index()
        )

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x.sort_values('Gold', ascending=False).reset_index(drop=True)


def data_over_time(df, col):
    data = (
        df.drop_duplicates(['Year', col])
          .groupby('Year')
          .size()
          .reset_index(name=col)
          .sort_values('Year')
    )
    return data


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = (
        temp_df['Name'].value_counts()
                       .reset_index()
                       .merge(df, left_on='index', right_on='Name', how='left')
                       .drop_duplicates('index')
                       [['index', 'Name_x', 'Sport', 'region']]
                       .rename(columns={'index': 'Athlete', 'Name_x': 'Medals'})
    )

    return x.head(15)


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    final_df = (
        temp_df.drop_duplicates(['Year', 'Sport', 'Event', 'Medal'])
               .groupby('Year')
               .count()['Medal']
               .reset_index()
    )
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    pt = (
        temp_df.drop_duplicates(['Year', 'Sport', 'Event', 'Medal'])
               .pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count')
               .fillna(0)
               .astype(int)
    )
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = (
        temp_df['Name'].value_counts()
                       .reset_index()
                       .merge(df, left_on='index', right_on='Name', how='left')
                       .drop_duplicates('index')
                       [['index', 'Name_x', 'Sport']]
                       .rename(columns={'index': 'Athlete', 'Name_x': 'Medals'})
    )

    return x.head(10)


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='outer').fillna(0).rename(columns={'Name_x': 'Male', 'Name_y': 'Female'})
    return final
