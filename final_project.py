"""
Daria Gileva, Brandon Nguyen, Karin Stoddart
CSE 163 AA

Write about final project bluh bluh bluh bluh
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
    This function takes the name of the shapes file and Excel workbook file
    and returns a geospatial dataframe that joins these two datasets by state.
    """
    shp_file = gpd.read_file(shp_file_name)
    if xlsx_file is None:
        csv_file = pd.read_csv(csv_file_name)
        csv_file = csv_file[
            (csv_file["State Name"] != "Alaska") &
            (csv_file["State Name"] != "Hawaii")
        ]
        merged_data = shp_file.merge(
            csv_file, left_on="NAMELSAD", right_on="State Name", how="outer"
        )
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
    data = data[data["STATE_NAME"] == "Washington"]
    drug = data["Drug Category"] == "Any Drug"
    county = data["Geography"] == "County"
    year = (data["Year"] >= start) & (data["Year"] <= end)
    time = data["Time Aggregation"] == "1 year rolling counts"
    remove_star = data["Death Count"] != "*"
    county_data = data[drug & county & time & year & remove_star]
    county_data["Death Count"] = county_data["Death Count"].astype("int")
    county_data = county_data.dissolve(by="Year", aggfunc="sum").reset_index()
    fig = px.line(
        county_data,
        x="Year",
        y="Death Count",
        title=f"Drug Overdose Deaths in WA between \
            {int(start)} and {int(end)}",
        markers=True,
    )
    fig.update_layout(title_x=0.5, title_y=0.95, font=dict(size=20))
    fig.update_traces(line=dict(width=4), marker=dict(size=10))

    fig.show()


#  (2) Which counties in Washington state have the highest number/rate
#  of drug overdose cases?
def overdose_deaths_counties(data, drug_name="Any Drug", year_date=2022.0):
    """
    This function takes in the geospatial dataframe and returns the counties
    in Washington that have the highest number of drug overdose cases.
    """
    data = data[data["STATE_NAME"] == "Washington"]
    drug = data["Drug Category"] == drug_name
    county = data["Geography"] == "County"
    year = data["Year"] == year_date
    time = data["Time Aggregation"] == "1 year rolling counts"
    remove_star = data["Death Count"] != "*"
    county_data = data[drug & county & time & year & remove_star]
    # county_data = county_data[['Location', 'geometry',
    # 'Death Count', 'Time Aggregation', 'Year']]
    county_data["Death Count"] = county_data["Death Count"].astype("int")

    fig, ax = plt.subplots(1)
    data.plot(ax=ax, color="#d3d3d3")
    county_data.plot(ax=ax, column="Death Count", legend=True)
    plt.title(f"Washington County Overdose Deaths in {int(year_date)}")
    plt.savefig("county_population_map.png")


# (3) How does the number of overdoses in WA compare to number of overdoses in
# other states in the USA?

# Create bar graph

# Normalize cases in Washington by dividing by total WA pop

# Normalize national case count by dividing by total national pop


# (4) What is the most prevalent drug that has been associated with drug
# overdose, and how has it changed over time?


def main():
    xlsx_file = extract_xlsx("Data/OverdoseDeathWA.xlsx",
                             "By Location and Date")
    wa_geo_data = merge_geo("Data/geodata/cb_2022_us_county_500k.shp",
                            xlsx_file)
  
    # Commented bc flake 8 didn't like that it wasn't used yet
    '''
    national_geo_data = merge_geo(
        "Data/geodata/cb_2022_us_county_500k.shp",
        csv_file_name="Data/NationalOverdose.csv",
    )
    '''
    drug_overdose_change(wa_geo_data)
    overdose_deaths_counties(wa_geo_data)


if __name__ == "__main__":
    main()
