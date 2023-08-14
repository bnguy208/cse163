"""
Daria Gileva, Brandon Nguyen, Karin Stoddart
CSE 163 AA

This file tests the methods in the script.
"""

import final_project as fp


def main():
    # Loading in the overdose data
    test_xlsx_file = fp.extract_xlsx("test/OverdoseDeathWA_test.xlsx",
                                     "By Location and Date")
    test_wa_geo_data = fp.merge_geo("test/geodata/cb_2022_us_county_500k.shp",
                                    test_xlsx_file)
    test_national_geo_data = fp.merge_geo(
        "Data/geodata/cb_2022_us_county_500k.shp",
        csv_file_name="Data/NationalOverdose.csv")

    # Methods to answer research questions
    fp.wa_overdose_change(test_wa_geo_data)
    fp.overdose_deaths_counties(test_wa_geo_data)
    fp.wa_versus_us(test_national_geo_data)


if __name__ == "__main__":
    main()
