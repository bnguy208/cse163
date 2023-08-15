"""
Daria Gileva, Brandon Nguyen, Karin Stoddart
CSE 163 AA

This function is a part of the program that explores opioid overdose cases
in the United States. It uses national drug overdose data and Washington drug
overdose data. This method combines the WA drug overdose data with geospatial
data and produces multiple geoplots that allow us to answer questions about
opioid overdose numbers in WA state counties over a specified time period.
"""

import geopandas as gpd
import matplotlib.pyplot as plt
from extract_and_merge import extract_xlsx, merge_geo


def overdose_deaths_counties(wa_geo_data: gpd.GeoDataFrame,
                             drug_name='Any Drug',
                             year_start=2016.0, year_end=2022.0) -> None:
    """
    This function takes in the geospatial dataframe and plots the drug
    overdose cases in different counties in Washington over a specified
    timeframe. The timeframe can be changed using default parameters as well
    as a category of drug name. Default drug is Any Drug but it can changed
    to other catergories in the dataset.
    """
    data = wa_geo_data[wa_geo_data['STATE_NAME'] == 'Washington'].copy()

    # Create masks
    drug = data['Drug Category'] == drug_name
    county = data['Geography'] == 'County'
    time = (data['Time Aggregation'] == '1 year rolling counts')
    remove_star = data['Death Count'] != '*'

    # Filter dataframe
    county_data = data[drug & county & time & remove_star].copy()
    county_data['Death Count'] = county_data['Death Count'].astype('int')

    plt.figure(figsize=(15, 12))
    plt.subplots_adjust(hspace=0.2)
    plt.suptitle("Washington County Overdose Deaths", fontsize=18, y=0.95)
    n = int(year_end - year_start)
    height, width = n // 2 + 1, 2
    for i in range(int(year_start), int(year_end)+1):
        year = (county_data['Year'] == i)
        year_data = county_data[year]

        ax = plt.subplot(height, width, i - int(year_start)+1)

        data.plot(ax=ax, color='#d3d3d3')
        year_data.plot(ax=ax, column='Death Count', legend=True)
        ax.set_title(i)
        ax.set_aspect('equal')
    plt.savefig('counties_overdose.png')


def main():
    # Loading in the overdose data
    xlsx_file = extract_xlsx("Data/OverdoseDeathWA.xlsx",
                             "By Location and Date")
    wa_geo_data = merge_geo("Data/geodata/cb_2022_us_county_500k.shp",
                            xlsx_file)

    # Methods to answer research question
    overdose_deaths_counties(wa_geo_data)


if __name__ == "__main__":
    main()
