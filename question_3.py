"""
Daria Gileva, Brandon Nguyen, Karin Stoddart
CSE 163 AA

This module contains a function that is a part of the program that explores
drug overdose deaths. It uses U.S. national drug overdose data merged with
geospatial data and allows us to answer questions about how drug overdose
deaths compare across states in mainland U.S. in addition to the District
of Columbia.
"""

import geopandas as gpd
import matplotlib.pyplot as plt
from extract_and_merge import merge_geo


# (3) How does the number of overdoses in WA compare to number of overdoses in
# other states in the USA? - Brandon
def wa_versus_us(national_geo_data: gpd.GeoDataFrame) -> None:
    """
    This function takes in the merged national drug overdose geodata, plots
    the number of drug overdose deaths across the mainland U.S. in 2022,
    and saves the file as wa_versus_us.png.
    """
    usa_data = national_geo_data[['State', 'Year', 'Month', 'Period',
                                  'Indicator', 'Data Value',
                                  'geometry']].copy()
    usa_data['Year'] = usa_data['Year'].astype(str)
    usa_data['Data Value'] = usa_data['Data Value'].str.replace(',', '')
    usa_data['Data Value'] = usa_data['Data Value'].fillna('0').astype(float)

    # Create masks
    any_drug = (usa_data['Indicator'] == 'Number of Drug Overdose Deaths')
    year = (usa_data['Year'] == '2022')
    month = (usa_data['Month'] == 'December')
    states = (usa_data['State'] != 'AK') & (usa_data['State'] != 'HI') & \
             (usa_data['State'] != 'YC') & (usa_data['State'] != 'US')

    # Filter data
    usa_data = usa_data[any_drug & year & month & states]

    # Further slicing
    usa_data = usa_data[['State', 'Data Value', 'geometry']]

    # Group by state
    usa_data = usa_data.dissolve(by='State')

    # Plot data
    fig, ax = plt.subplots(1, figsize=(15, 7))
    usa_data.plot(ax=ax, color='#EEEEEE')
    usa_data.plot(ax=ax, column='Data Value', legend=True)
    plt.title('National Drug Overdose Deaths in 2022', fontsize=16)
    fig.savefig('wa_versus_us.png')


def main():
    # Load in data
    national_geo_data = merge_geo("Data/geodata/cb_2022_us_county_500k.shp",
                                  csv_file_name="Data/NationalOverdose.csv")

    # Methods to answer research question
    wa_versus_us(national_geo_data)


if __name__ == "__main__":
    main()
