# Copyright 2022, Loic Leray
# Please acknowledge Loic Leray for making this data available in your
# research.
# ---
# See https://github.com/loicleray/OIE_WAHIS.ReportRetriever for documentation
# and explanations.

import argparse
import json
import os
import time
import requests
import numpy as np
import pandas as pd
import pprint
# from tqdm.auto import tqdm
# from ast import literal_eval


def get_filter_options():
    '''Returns a dictionary with the options and acceptable values to filter
    WAHIS diseases.'''

    # wahis filter names taked from the filter columns
    # on https://wahis.woah.org/#/events
    wahis_filter_names = ["country", "region", "epiEventId", "diseases", "diseaseType", "reason", "eventDate", "eventStatus", "reportHistoryType", "reportDate"]
    report_filter_options = {}

    try:
        for item in wahis_filter_names:
            url = f"https://wahis.woah.org/pi/reports/filters?columnName={item}"
            # if keeping "payload" and "headers" blank doesn't work you may need to
            # cURL, PostMan can generate this code automatically...
            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            report_filter_options[item]= response.json()['dropDownValue']
    except:
        print("Something went wrong when trying to access filter lists.")

    return report_filter_options

def save_filter_options():
    '''Save a file with contents of get_filter_options() in present directory.'''

    filter_options = get_filter_options()
    file_name = "WAHIS_filter_options.json"
    print("Creating file with filter options for you to check...")
    file = open(file_name, "w")
    json.dump(filter_options, file)
    file.close()
    print(f"File saved as {file_name}")

def parser_country(a):
    pass

    # tk tk tk
def main():
    print("This is running from the main().")
    parser = argparse.ArgumentParser(description="Gather WAHIS reports based on inputs.")
    parser.add_argument("-op",
                        "--options",
                        action="store_true",
                        help=" Creates a file with the posible filter options for limiting your report results.",
                        )
    parser.add_argument("-c",
                        "--country",
                        action="store",
                        type=str,
                        help="Countries for which you want report results. E.G. '' ",
                        )
    # parser.add_argument("-r",
    #                     "--region",
    #                     type=str,
    #                     choices
    #                     )
    # parser.add_argument("epiEventId", type=str, choices
    # )
    # parser.add_argument("diseases", type=str, choices
    # )
    # parser.add_argument("diseaseType", type=str, choices
    # )
    # parser.add_argument("reason", type=str, choices
    # )
    # parser.add_argument("eventDate", type=str, choices
    # )
    # parser.add_argument("eventStatus", type=str, choices
    # )
    # parser.add_argument("reportHistoryType", type=str, choices
    # )
    # parser.add_argument("reportDate", type=str, choices
    # )

    parsed_args = parser.parse_args()

    #run save_filter_options() based on CLI input
    if parsed_args.options == True and not os.path.exists("WAHIS_filter_options.json"):
        save_filter_options()


if __name__ == "__main__":
    main()
