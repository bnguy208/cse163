"""
Daria Gileva, Brandon Nguyen, Karin Stoddart
CSE 163 AA

This module contains a function that is a part of the program that explores
drug overdose deaths. It uses Washington drug overdose data. This module
allows us to answer questions about the disproportionate impact of overdose
deaths across different races.
"""

import pandas as pd
import matplotlib.pyplot as plt

from extract_and_merge import extract_xlsx


def race_death_wa(wa_race_data: pd.DataFrame) -> None:
    """
    This function takes in the Washington overdose dataset and produces
    a bar graph of overdose death counts in King County 2022 for each race.
    The death counts for each race are normalized to the total population of
    that particular race in King County.

    The graph is saved as a file named wa_race_overdose.png.
    """
    king_county = wa_race_data[['Year', 'Location', 'Drug Category', 'Race',
                                'Time Aggregation', 'Death Count',
                                'Population']].copy()

    # Filter data
    year = king_county["Year"] == 2022
    is_king = king_county["Location"] == "King County"
    drug = king_county["Drug Category"] == "Any Drug"
    time = king_county["Time Aggregation"] == "1 year rolling counts"
    not_star = (king_county["Death Count"]) != "*"

    king_county = king_county[year & is_king & drug & time & not_star]
    king_county["Death Count"] = king_county["Death Count"].astype(float)

    # Normalize to total population
    king_county['Death per Capita'] = \
        king_county['Death Count']/king_county['Population']

    # Plot
    plt.figure(figsize=(15, 7))
    colors = [
        "lightsalmon",
        "sandybrown",
        "khaki",
        "lightgreen",
        "lightcyan",
        "lavender",
    ]
    plt.bar(king_county["Race"], king_county["Death per Capita"], color=colors)
    plt.xlabel("Race", fontsize=14)
    plt.ylabel("Death per Total Population", fontsize=14)
    plt.title("Drug Overdose Deaths for All Drugs in King County (2022)",
              fontsize=18)
    plt.savefig("wa_race_overdose.png")


def main():
    # Accessing the right excel tab for race_death_wa()
    wa_race_data = extract_xlsx("Data/OverdoseDeathWA.xlsx", "By Demo-RE")

    # Methods to answer research question
    race_death_wa(wa_race_data)


if __name__ == "__main__":
    main()
