"""
Daria Gileva, Brandon Nguyen, Karin Stoddart
CSE 163 AA

This file tests the methods in the script.
"""

from extract_and_merge import extract_xlsx, merge_geo
import pandas as pd
import geopandas as gpd


def test_wa_overdose_change(wa_data, start=2016.0, end=2022.0) -> pd.DataFrame:
    """
    This function tests the wa_overdose_change() method from question_1.py
    """
    drug = wa_data["Drug Category"] == "Any Drug"
    year = (wa_data["Year"] >= start) & (wa_data["Year"] <= end)
    time = wa_data["Time Aggregation"] == "1 year rolling counts"
    remove_star = wa_data["Death Count"] != "*"
    county_data = wa_data[drug & time & year & remove_star].copy()
    county_data["Death Count"] = county_data["Death Count"].astype("int")
    county_data = \
        county_data.groupby("Year").agg({"Death Count": "sum"}).reset_index()

    print()
    print('QUESTION 1')
    print('Printing table of death counts in Washington 2016-2022:')
    print()
    print(county_data)


def test_overdose_deaths_counties(wa_geo_data: gpd.GeoDataFrame,
                                  drug_name='Any Drug',
                                  year_start=2016.0, year_end=2022.0) -> None:
    """
    This function tests the overdose_deaths_counties() method
    from question_2.py
    """
    pass
    # data = wa_geo_data[wa_geo_data['STATE_NAME'] == 'Washington'].copy()

    # # Create masks
    # drug = data['Drug Category'] == drug_name
    # county = data['Geography'] == 'County'
    # time = (data['Time Aggregation'] == '1 year rolling counts')
    # remove_star = data['Death Count'] != '*'

    # # Filter dataframe
    # county_data = data[drug & county & time & remove_star].copy()
    # county_data['Death Count'] = county_data['Death Count'].astype('int')

    # print()
    # print('QUESTION 2')
    # print('Printing table of death counts in each county:')

    # for i in range(int(year_start), int(year_end)+1):
    #     year = (county_data['Year'] == i)
    #     year_data = county_data[year]

    #     print()
    #     data.plot(ax=ax, color='#d3d3d3')
    #     year_data.plot(ax=ax, column='Death Count', legend=True)


# def test_wa_versus_us():
#     pass


# def race_death_wa():
#     pass


def main():
    # Load in data
    xlsx_file = extract_xlsx("Data/OverdoseDeathWA.xlsx",
                             "By Location and Date")
    wa_geo_data = merge_geo("Data/geodata/cb_2022_us_county_500k.shp",
                            xlsx_file)

    # Test methods
    test_wa_overdose_change(xlsx_file)
    test_overdose_deaths_counties(wa_geo_data)


if __name__ == "__main__":
    main()
