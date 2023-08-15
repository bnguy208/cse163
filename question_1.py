"""
Daria Gileva, Brandon Nguyen, Karin Stoddart
CSE 163 AA

This function is a part of the program that explores opioid overdose cases
in the United States. It uses national drug overdose data and Washington drug
overdose data. This method reads the WA drug overdose data and produces a line
graph that allows us to answer questions about opioid overdose in WA state over
a specified time period.
"""

import plotly.express as px
import pandas as pd
from extract_and_merge import extract_xlsx


def wa_overdose_change(wa_data:  pd.ExcelFile,
                       start: float = 2016.0,
                       end: float = 2022.0) -> None:
    """
    This function takes in an excel dataframe and produces a line graph
    that shows the number  of drug overdose cases in Washington
    from 2016-2022.

    The timeframe can be chagned by using default parameters. 
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
    fig.write_image('wa_overdose.png')


def main():
    # Loading in the overdose data
    xlsx_file = extract_xlsx("Data/OverdoseDeathWA.xlsx",
                             "By Location and Date")

    # Call method to answer research question
    wa_overdose_change(xlsx_file)


if __name__ == "__main__":
    main()
