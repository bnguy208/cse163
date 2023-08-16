"""
Daria Gileva, Brandon Nguyen, Karin Stoddart
CSE 163 AA

This program loads in and transforms Washington and U.S. overdose data, which
are to be used in the runnable Python modules (question_1.py, question_2.py,
question_3.py, question_4.py) for the analysis of drug overdose deaths in
Washington state.
"""

import pandas as pd
import geopandas as gpd
from typing import Optional


def extract_xlsx(xlsx_name: str, ws_name: str) -> pd.ExcelFile:
    """
    This function takes the path of a multi-sheet Excel workbook file and the
    name of the worksheet of interest and returns a Pandas dataframe.
    """
    xlsx = pd.ExcelFile(xlsx_name)
    return pd.read_excel(xlsx, ws_name)


def merge_geo(shp_file_name: str, xlsx_file: Optional[pd.ExcelFile] = None,
              csv_file_name: Optional[str] = None) -> gpd.GeoDataFrame:
    """
    This function takes the name of the shapes file and Excel workbook file OR
    a CSV file and returns a geospatial dataframe that joins these two datasets
    by state.
    """
    shp_file = gpd.read_file(shp_file_name)
    is_mainland = (shp_file['STUSPS'] != 'AK') & \
                  (shp_file['STUSPS'] != 'HI') & \
                  (shp_file['STUSPS'] != 'GU') & \
                  (shp_file['STUSPS'] != 'PR') & \
                  (shp_file['STUSPS'] != 'MP') & \
                  (shp_file['STUSPS'] != 'AS') & \
                  (shp_file['STUSPS'] != 'VI')
    shp_file = shp_file[is_mainland]

    if xlsx_file is None:
        csv_file = pd.read_csv(csv_file_name)
        merged_data = shp_file.merge(csv_file, left_on='STUSPS',
                                     right_on='State')
    else:
        merged_data = shp_file.merge(xlsx_file, left_on="NAMELSAD",
                                     right_on="Location")
    return merged_data
