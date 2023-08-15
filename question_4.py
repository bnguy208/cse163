"""
Daria Gileva, Brandon Nguyen, Karin Stoddart
CSE 163 AA

This program explores opioid overdose cases in the United States. It uses
national drug overdose data and Washington drug overdose data. The methods
in this program read in these datasets and combine them with geospatial
data to produce visualizations that allow us to answer questions about
opioid overdose across the U.S. and within Washington.
"""

import pandas as pd
import matplotlib.pyplot as plt

from extract_and_merge import extract_xlsx


# (4) How does race impact overdose deaths in Washington?
def race_death_wa(wa_race_data: pd.DataFrame) -> None:
    king_county = wa_race_data[['Year', 'Location', 'Drug Category', 'Race',
                                'Time Aggregation', 'Death Count',
                                'Population']].copy()

    # Filter data
    year = (king_county['Year'] == 2022)
    is_king = (king_county['Location'] == 'King County')
    drug = (king_county['Drug Category'] == 'Any Drug')
    time = (king_county['Time Aggregation'] == '1 year rolling counts')
    not_star = (king_county['Death Count']) != '*'

    king_county = king_county[year & is_king & drug & time & not_star]
    king_county['Death Count'] = king_county['Death Count'].astype(float)

    # Normalize to total population
    tot_pop = king_county['Population'].sum()
    king_county['Death per Capita'] = king_county['Death Count']/tot_pop

    # Plot
    plt.figure(figsize=(15, 7))
    colors = ['lightsalmon', 'sandybrown', 'khaki', 'lightgreen', 'lightcyan', 'lavender']
    plt.bar(king_county['Race'], king_county['Death per Capita'], color=colors)
    plt.xlabel('Race', fontsize=14)
    plt.ylabel('Death per Total Population', fontsize=14)
    plt.title('Drug Overdose Deaths for All Drugs in King County (2022)', fontsize=18)
    plt.savefig('wa_race_overdose.png')


# def overdose_df(geo_data: gpd.GeoDataFrame) -> pd.DataFrame:
#     county_data_pd = pd.DataFrame(geo_data.drop(columns='geometry'))
#     county_data_pd = county_data_pd.drop(columns='ALAND')
#     county_data_pd = county_data_pd.drop(columns='AWATER')

#     return county_data_pd


# def race_death_wa(data) -> None:
#     wa_data = data[data["STATE_NAME"] == "Washington"].copy()
#     drug = wa_data["Drug Category"] == "Any Drug"
#     wa_data["Year"] = pd.to_numeric(data["Year"], errors="coerce")
#     time = wa_data["Time Aggregation"] == "1 year rolling counts"
#     remove_star = wa_data["Death Count"] != "*"
#     county_data = wa_data[drug & time & remove_star].copy()
#     county_data["Death Count"] = county_data["Death Count"].astype("int")

#     # Some race names had * at the end so I took them out
#     county_data['Race'] = county_data['Race'].apply(remove_race_asterisk)

#     # Not sure how these categories are defined in the dataset
#     # county_data = county_data[county_data['Race'] != 'Hispanic']
#     # county_data = county_data[county_data['Race'] != 'Unknown']
#     # county_data = county_data[county_data['Race'] != 'Multiple Races*']

#     # absolute, bar height shows change in total overdose deaths
#     # fig = px.histogram(county_data, x='Year', y='Death Count', color='Race', title="Change in Racial Makeup of Overdose Deaths in WA over 2016-2022")

    
#     # trying to have each bar be 100% but this doesn't make sense yet
#     percent_data = county_data
#     print(percent_data)
#     grouped_year = percent_data.groupby('Year')['Death Count'].sum()
#     print(grouped_year)
#     # I know I'm doing the indexing wrong on this line but idk how to do it right:
#     percent_data['Race Percent'] = (percent_data['Death Count'])/(grouped_year[percent_data['Year']])
#     fig = px.histogram(percent_data, x='Year', y='Race Percent', color='Race Percent')
    

#     fig.update_layout(barmode='stack')
#     fig.update_yaxes(type='log')
#     fig.write_image('race_death_wa.png')


# def remove_race_asterisk(s: str) -> str:
#     if s[(len(s)-1):] == '*':
#         s = s[:(len(s)-1)]
#     return s


def main():
    # Accessing the right excel tab for race_death_wa()
    wa_race_data = extract_xlsx("Data/OverdoseDeathWA.xlsx",
                                "By Demo-RE")

    # Methods to answer research question
    race_death_wa(wa_race_data)


if __name__ == "__main__":
    main()
