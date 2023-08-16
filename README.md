# Investigating Drug Overdose in Washington
### CSE 163: Final Project
### Daria Gileva, Brandon Nguyen, Karin Stoddart

## Introduction
This assessent explores drug overdose patterns in Washington State using data from the Washington State Department of Health and United States Center for Disease Control and Prevention (CDC). These datasets can be downloaded via the following websites provided:
- [Washington Overdose Data](https://doh.wa.gov/data-and-statistical-reports/washington-tracking-network-wtn/opioids)
    - This database has data on drug overdose deaths, hospitalizations, and opioid prescriptions given in Washington State.
    - Download Excel or CSV by viewing one of the three datasets and then choosing tables that are not summary. The opioid and drug overdoses database has a download button under the graph and the other two with prescriptions have an export button in the lower right side of the window where we need to choose crosstab and then a preferred download format. 
- [U.S. Overdose Data](https://www.cdc.gov/nchs/nvss/vsrr/drug-overdose-data.htm)
    - This dataset presents a number of overdose deaths across the US, with states and drug types specified
    - Download Excel or CSV by going to the Options section, then Download Datasets, and selecting state overdose deaths to download data on the total overdose deaths in each state. 

Overdose deaths are visualized geospatially using geospatial data from the United States Census Bureau. This dataset can be downloaded via the following link:
- [U.S. Census Geodata](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html)
    - Download shapefile by going to Cartographic Boundary by Geography, then Counties, and selecting the download option for 500,000 (national) to download the 11 MB file.

## Installations
All visualizations were developed through VS Code using the Anaconda cse163 environment that supports Python version 3.9.17. Necessary packages include pandas, geopandas, matplotlib, and plotly. Instructions on how to set up the Anaconda cse163 environent and VS Code are provided [here](https://courses.cs.washington.edu/courses/cse163/software/).

Additionally, to support union operators in type annotations, the Optional class had to be imported from the typing module. However, note that this would not have been necessary if Python version 3.10 were used.

## Python Files
`extract_and_merge.py` has functions defined to load in the xlsx Washington Overdose data and merge the Washington and U.S. datasets with geospatial data.

`question_1.py` produces a line plot that shows how overdose deaths have changed from 2016-2022 in Washington. The plot is saved as wa_overdose.png.

`question_2.py` produces subplots that show how drug overdose deaths compare across Washington counties from 2016-2022. The plot is saved as counties_overdose.png.

`question_3.py` produces a map of the U.S. and uses a color scale to color each state according to death count. The plot is saved as wa_versus_us.png.

`question_4.py` produces a bar graph to show how death counts in King County 2022 compare across races. The plot is saved as wa_race_overdose.png.

`test.py` tests all the methods from the question_x.py modules (x = 1 through 4).

## Run the Project 
1. Go to any of the question_x.py modules.
2. Type "_python question_x.py_" in the VS Code terminal, replacing x with the appropriate question number (1-4), and then run.
3. Wait for the module to run. Note that this can take awhile since we are working with large datasets.
4. Access a png image of your visualization in the cse163 environment folder on your local computer.
5. If you would like to do a sanity check of your visualization, go to the test.py module, type "_python test.py_" in the terminal, then run.
