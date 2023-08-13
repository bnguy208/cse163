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
import matplotlib.pyplot as plt


def extract_xlsx(xlsx_name, ws_name):
    """
    This function takes the path of a multi-sheet Excel workbook file and the
    name of the workshee of interest and returns a Pandas dataframe.
    """
    xlsx = pd.ExcelFile(xlsx_name)
    return pd.read_excel(xlsx, ws_name)


def merge_geo(shp_file_name, xlsx_file=None, csv_file_name=None):
    """
    This function takes the name of the shapes file and Excel workbook file OR a CSV file
    and returns a geospatial dataframe that joins these two datasets by state.
    """
    shp_file = gpd.read_file(shp_file_name)
    if xlsx_file is None:
        csv_file = pd.read_csv(csv_file_name)
        csv_file = csv_file[
            (csv_file["State Name"] != "Alaska") &
            (csv_file["State Name"] != "Hawaii")
        ]
        merged_data = shp_file.merge(csv_file, left_on='STUSPS',
                                     right_on='State', how='outer')
    else:
        merged_data = shp_file.merge(xlsx_file, left_on="NAMELSAD",
                                     right_on="Location")
    return merged_data


# (1) How has the number of drug overdose cases changed between 2015 and 2023
# in Washington State?
def drug_overdose_change(data, start=2015.0, end=2023.0) -> None:
    """
    This function takes in the geospatial dataframe and returns the number
    of drug overdose cases from 2015-2023.
    """

    # This chunk below is replaced by the overdose_geo() call but I'm too
    # scared to delete it yet
    '''
    data = data[data["STATE_NAME"] == "Washington"]
    drug = data["Drug Category"] == "Any Drug"
    county = data["Geography"] == "County"
    year = (data["Year"] >= start) & (data["Year"] <= end)
    time = data["Time Aggregation"] == "1 year rolling counts"
    remove_star = data["Death Count"] != "*"
    county_data = data[drug & county & time & year & remove_star]
    county_data["Death Count"] = county_data["Death Count"].astype("int")
    county_data = county_data.dissolve(by="Year", aggfunc="sum").reset_index()
    '''


#  (2) Which counties in Washington state have the highest number/rate
#  of drug overdose cases?
def overdose_deaths_counties(data: gpd.GeoDataFrame, drug_name='Any Drug',
                             year_start=2016.0, year_end=2022.0) -> None:
    """
    This function takes in the geospatial dataframe and returns the counties
    in Washington that have the highest number of drug overdose cases.
    """
    data = data[data['STATE_NAME'] == 'Washington'].copy()
    drug = data['Drug Category'] == drug_name
    county = data['Geography'] == 'County'
    time = (data['Time Aggregation'] == '1 year rolling counts')
    remove_star = data['Death Count'] != '*'
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


def overdose_geo(data, start=2016.0, end=2022.0) -> pd.DataFrame:
    wa_data = data[data["STATE_NAME"] == "Washington"].copy()
    drug = wa_data["Drug Category"] == "Any Drug"
    county = wa_data["Geography"] == "County"
    wa_data["Year"] = pd.to_numeric(data["Year"], errors="coerce")
    year = (wa_data["Year"] >= start) & (wa_data["Year"] <= end)
    time = wa_data["Time Aggregation"] == "1 year rolling counts"
    remove_star = wa_data["Death Count"] != "*"
    county_data = wa_data[drug & county & time & year & remove_star].copy()
    county_data["Death Count"] = county_data["Death Count"].astype("int")
    county_data = \
        county_data.groupby("Year").agg({"Death Count": "sum"}).reset_index()

    fig = px.line(
        county_data,
        x="Year",
        y="Death Count",
        title=f"Drug Overdose Deaths in WA between "
        f"{int(start)} and {int(end)}",
        markers=True
    )
    fig.update_layout(title_x=0.5, title_y=0.95, font=dict(size=15))
    fig.update_traces(line=dict(width=4), marker=dict(size=10))

    # fig.show()
    fig.write_image('wa_overdose.png')


def overdose_df(geo_data: gpd.GeoDataFrame) -> pd.DataFrame:
    county_data_pd = pd.DataFrame(geo_data.drop(columns='geometry'))
    county_data_pd = county_data_pd.drop(columns='ALAND')
    county_data_pd = county_data_pd.drop(columns='AWATER')

    return county_data_pd


# (3) How does the number of overdoses in WA compare to number of overdoses in
# other states in the USA? - Brandon
def wa_versus_us(usa_data):
    usa_data = usa_data[['State', 'Year', 'Month', 'Period', 'Indicator', 'Data Value']].copy()
    usa_data['Year'] = usa_data['Year'].astype(str)
    any_drug = (usa_data['Indicator'] == 'Number of Drug Overdose Deaths')

    # Create masks
    year = (usa_data['Year'] == '2019') | (usa_data['Year'] == '2020')
    month = (usa_data['Month'] == 'March')
    states = (usa_data['State'] == 'WA') | (usa_data['State'] == 'US') # State US?

    # Filter data
    usa_data = usa_data[any_drug & year & month & states]
    usa_data

    fig = px.bar(usa_data, x='Year', y='Data Value', color='State',
                 title='Drug Overdose Deaths in Washington vs. U.S.')
    fig.update_layout(barmode='stack')
    fig.update_yaxes(type='log')
    fig.update_yaxes(title="Death Count")  # Stacked bar chart needs fixing
    # fig.write_image('wa_versus_us.png')


# (4) How does race impact overdose deaths in Washington? - Karin


def main():
    xlsx_file = extract_xlsx("Data/OverdoseDeathWA.xlsx",
                             "By Location and Date")
    wa_geo_data = merge_geo("Data/geodata/cb_2022_us_county_500k.shp",
                            xlsx_file)
    national_geo_data = merge_geo(
        "Data/geodata/cb_2022_us_county_500k.shp",
        csv_file_name="Data/NationalOverdose.csv",
    )
    # drug_overdose_change(wa_geo_data)
    overdose_geo(wa_geo_data)
    overdose_deaths_counties(wa_geo_data)
    wa_versus_us(national_geo_data)
    # most_prevalent_drug(national_geo_data)


if __name__ == "__main__":
    main()
