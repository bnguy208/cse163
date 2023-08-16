"""
Daria Gileva, Brandon Nguyen, Karin Stoddart
CSE 163 AA

This file tests the methods in the script. Each test function prints a
dataframe in the terminal used to do a sanity check of each of the four
visualizations.
"""

from extract_and_merge import extract_xlsx, merge_geo
import pandas as pd
import geopandas as gpd


def test_wa_overdose_change(wa_data: pd.ExcelFile,
                            start: float = 2016.0,
                            end: float = 2022.0) -> pd.DataFrame:
    """
    This function tests the wa_overdose_change() method from question_1.py
    """
    geography = wa_data["Geography"] == 'County'
    drug = wa_data["Drug Category"] == "Any Drug"
    year = (wa_data["Year"] >= start) & (wa_data["Year"] <= end)
    time = wa_data["Time Aggregation"] == "1 year rolling counts"
    remove_star = wa_data["Death Count"] != "*"
    county_data = wa_data[geography & drug & time & year & remove_star].copy()
    county_data["Death Count"] = county_data["Death Count"].astype("int")
    county_data = \
        county_data.groupby("Year").agg({"Death Count": "sum"}).reset_index()

    print()
    print('QUESTION 1')
    print('Printing table of death counts in Washington 2016-2022:')
    print()
    print(county_data)


def test_overdose_deaths_counties(wa_geo_data: gpd.GeoDataFrame,
                                  drug_name: str = 'Any Drug',
                                  year_start: float = 2016.0,
                                  year_end: float = 2022.0) -> pd.DataFrame:
    """
    This function tests the overdose_deaths_counties() method
    from question_2.py
    """
    data = wa_geo_data[wa_geo_data['STATE_NAME'] == 'Washington'].copy()

    # Create masks
    drug = data['Drug Category'] == drug_name
    county = data['Geography'] == 'County'
    time = (data['Time Aggregation'] == '1 year rolling counts')
    remove_star = data['Death Count'] != '*'
    counties = (data['NAMELSAD'] == 'Skagit County') | \
               (data['NAMELSAD'] == 'Snohomish County') | \
               (data['NAMELSAD'] == 'King County') | \
               (data['NAMELSAD'] == 'Pierce County')

    # Filter dataframe
    county_data = data[drug & county & time & remove_star & counties].copy()
    county_data['Death Count'] = county_data['Death Count'].astype('int')

    # Slice dataframe
    county_data = county_data[['NAMELSAD', 'Year', 'Death Count']]

    # Print statements
    print()
    print('QUESTION 2')
    print('Printing table of death counts in Washington counties 2016-2022:')
    print()
    for i in range(int(year_start), int(year_end)+1):
        year = (county_data['Year'] == i)
        year_data = county_data[year]
        print('Overdose Deaths in ' + str(i) + ':')
        print()
        print(year_data)
        print()


def test_wa_versus_us(national_geo_data: gpd.GeoDataFrame) -> pd.DataFrame:
    """
    This function tests the wa_versus_us method from question_3.py
    """
    usa_data = national_geo_data[['State', 'Year', 'Month', 'Period',
                                  'Indicator', 'Data Value',
                                  'COUNTYNS']].copy()
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
    usa_data = usa_data[['State', 'Data Value']]

    # Group by state and sum up death counts
    usa_data = usa_data.groupby('State')['Data Value'].first().reset_index()

    # Print datatable
    print()
    print('QUESTION 3')
    print('Printing table of national death counts in 2022:')
    print()
    print(usa_data)


def test_race_death_wa(wa_race_data: pd.ExcelFile) -> pd.DataFrame:
    """
    This function tests the race_death_wa method from question_4.py
    """
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

    # Slice dataframe
    king_county = king_county[['Race', 'Death Count', 'Population',
                               'Death per Capita']]

    # Print datatable
    print()
    print('QUESTION 4')
    print('Printing table of death counts per capita in King County (2022):')
    print()
    print(king_county.loc[:, ['Race', 'Death per Capita']])
    print()
    print('Sanity Check: Deaths Counts & Population')
    print(king_county.loc[:, ['Race', 'Death Count', 'Population']])


def main():
    # Load in data
    xlsx_file = extract_xlsx("Data/OverdoseDeathWA.xlsx",
                             "By Location and Date")
    wa_geo_data = merge_geo("Data/geodata/cb_2022_us_county_500k.shp",
                            xlsx_file)
    national_geo_data = merge_geo("Data/geodata/cb_2022_us_county_500k.shp",
                                  csv_file_name="Data/NationalOverdose.csv")
    wa_race_data = extract_xlsx("Data/OverdoseDeathWA.xlsx",
                                "By Demo-RE")

    # Test methods
    test_wa_overdose_change(xlsx_file)
    test_overdose_deaths_counties(wa_geo_data)
    test_wa_versus_us(national_geo_data)
    test_race_death_wa(wa_race_data)


if __name__ == "__main__":
    main()
