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
    colors = ['lightsalmon', 'sandybrown', 'khaki', 'lightgreen', 'lightcyan',
              'lavender']
    plt.bar(king_county['Race'], king_county['Death per Capita'], color=colors)
    plt.xlabel('Race', fontsize=14)
    plt.ylabel('Death per Total Population', fontsize=14)
    plt.title('Drug Overdose Deaths for All Drugs in King County (2022)',
              fontsize=18)
    plt.savefig('wa_race_overdose.png')


def main():
    # Accessing the right excel tab for race_death_wa()
    wa_race_data = extract_xlsx("Data/OverdoseDeathWA.xlsx",
                                "By Demo-RE")

    # Methods to answer research question
    race_death_wa(wa_race_data)


if __name__ == "__main__":
    main()
