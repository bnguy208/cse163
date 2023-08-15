"""
Daria Gileva, Brandon Nguyen, Karin Stoddart
CSE 163 AA

This program explores opioid overdose cases in the United States. It uses
national drug overdose data and Washington drug overdose data. The methods
in this program read in these datasets and combine them with geospatial
data to produce visualizations that allow us to answer questions about
opioid overdose across the U.S. and within Washington.
"""

import plotly.express as px
import geopandas as gpd
import pandas as pd
from extract_and_merge import extract_xlsx, merge_geo


def overdose_df(geo_data: gpd.GeoDataFrame) -> pd.DataFrame:
    county_data_pd = pd.DataFrame(geo_data.drop(columns='geometry'))
    county_data_pd = county_data_pd.drop(columns='ALAND')
    county_data_pd = county_data_pd.drop(columns='AWATER')

    return county_data_pd


# (4) How does race impact overdose deaths in Washington? - Karin
def race_death_wa(data) -> None:
    wa_data = data[data["STATE_NAME"] == "Washington"].copy()
    drug = wa_data["Drug Category"] == "Any Drug"
    wa_data["Year"] = pd.to_numeric(data["Year"], errors="coerce")
    time = wa_data["Time Aggregation"] == "1 year rolling counts"
    remove_star = wa_data["Death Count"] != "*"
    county_data = wa_data[drug & time & remove_star].copy()
    county_data["Death Count"] = county_data["Death Count"].astype("int")

    # Some race names had * at the end so I took them out
    county_data['Race'] = county_data['Race'].apply(remove_race_asterisk)

    # Not sure how these categories are defined in the dataset
    # county_data = county_data[county_data['Race'] != 'Hispanic']
    # county_data = county_data[county_data['Race'] != 'Unknown']
    # county_data = county_data[county_data['Race'] != 'Multiple Races*']

    # absolute, bar height shows change in total overdose deaths
    fig = px.histogram(county_data, x='Year', y='Death Count', color='Race')

    '''
    # trying to have each bar be 100% but this doesn't make sense yet
    percent_data = county_data
    grouped_year = percent_data.groupby('Year')['Death Count'].sum()
    percent_data['Race Percent'] = (percent_data['Death Count'])
    /(grouped_year[str(percent_data['Year'])])
    fig = px.histogram(percent_data, x='Year', y='Race Percent',
    color='Race Percent')
    '''

    fig.update_layout(barmode='stack')
    fig.update_yaxes(type='log')
    fig.write_image('race_death_wa.png')


def remove_race_asterisk(s: str) -> str:
    if s[(len(s)-1):] == '*':
        s = s[:(len(s)-1)]
    return s


def main():
    # Accessing the right excel tab for race_death_wa()
    xlsx_file_race = extract_xlsx("Data/OverdoseDeathWA.xlsx",
                                  "By Demo-RE")
    wa_geo_data_race = merge_geo("Data/geodata/cb_2022_us_county_500k.shp",
                                 xlsx_file_race)

    # Methods to answer research question
    race_death_wa(wa_geo_data_race)


if __name__ == "__main__":
    main()
