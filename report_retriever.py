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
from datetime import date, timedelta
import requests
import numpy as np
import pandas as pd
import pprint
from tqdm import tqdm
# from ast import literal_eval


def get_filter_options():
    '''Returns a dictionary with the options and acceptable values to filter
    WAHIS diseases.'''

    # wahis filter names taked from the filter columns
    # on https://wahis.woah.org/#/events
    wahis_filter_names = ["country", "region", "epiEventId", "diseases", "diseaseType",
                          "reason", "eventDate", "eventStatus", "reportHistoryType", "reportDate"]
    report_filter_options = {}

    try:
        for item in wahis_filter_names:
            url = f"https://wahis.woah.org/pi/reports/filters?columnName={item}"
            # if keeping "payload" and "headers" blank doesn't work you may need to
            # cURL, PostMan can generate this code automatically...
            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            report_filter_options[item] = response.json()['dropDownValue']
    except:
        print("Something went wrong when trying to access filter lists.")

    return report_filter_options


def save_filter_options(save_path):
    '''Save a file with contents of get_filter_options() in file path of your
    choosing.'''

    file_name = "WAHIS_filter_options"
    full_path = os.path.join(save_path, file_name+".json")
    filter_options = get_filter_options()
    print("Creating file with filter options for you to check...")
    file = open(full_path, "w")
    json.dump(filter_options, file)
    file.close()
    print(f"File saved as {file_name}.json in 'OUTPUTS' folder.")


def get_report_list(country=[], region=[], disease=[], start_date=str("1901-01-01"), end_date=str(date.today())):
    '''Returns a dictionary of reports corresponding to the filter results
    parsed in the funtion. Be carefull, the default is to return all results
    from 01/01/1901 to present date. It is your responsibilty to limit results
    using filters specified in the documentation (link at top of file).'''  # setup

    URL = "https://wahis.woah.org/pi/getReportList"
    headers = {}

    # don't think that i need the header below. keeping temporarily until sure it isn't necessary.
    #   'authority': 'wahis.woah.org',
    #   'accept': 'application/json',
    #   'accept-language': 'en',
    #   'access-control-allow-headers': 'X-Requested-With, Content-Type, Origin, Authorization, Accept,Client-Security-Token, Accept-Encoding, accept-language, type, authorizationToken, methodArn',
    #   'access-control-allow-methods': 'POST, GET, OPTIONS, DELETE, PUT',
    #   'access-control-allow-origin': '*',
    #   'cache-control': 'no-cache',
    #   'clientid': 'OIEwebsite',
    #   'content-type': 'application/json',
    #   'cookie': '_ga=GA1.2.1528097890.1659352073; _gid=GA1.2.493419287.1659682725',
    #   'env': 'PRD',
    #   'expires': 'Sat, 01 Jan 2000 00:00:00 GMT',
    #   'origin': 'https://wahis.woah.org',
    #   'pragma': 'no-cache',
    #   'referer': 'https://wahis.woah.org/',
    #   'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    #   'sec-ch-ua-mobile': '?0',
    #   'sec-ch-ua-platform': '"macOS"',
    #   'sec-fetch-dest': 'empty',
    #   'sec-fetch-mode': 'cors',
    #   'sec-fetch-site': 'same-origin',
    #   'temporal_reference_date': '2022-07-07 13:34:59',
    #   'token': '#PIPRD202006#',
    #   'type': 'REQUEST',
    #   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    #   'x-content-type-options': 'nosniff',
    #   'x-frame-options': 'sameorigin'
    # }

    payload = json.dumps({
        "pageNumber": 1,
        "pageSize": 1000000000,  # 1000000000 is the MAX allowable to be given in payload without "BAD REQUEST ERROR"
        "searchText": "",  # Not yet added to the possible arguments for get_report_list()
        "sortColName": "",  # Not yet added to the possible arguments for get_report_list()
        # "ASC" = Ascending oldest to newest, "DESC" = Descending oldest to newest.
        "sortColOrder": "DESC",
        "reportFilters": {
            "country": country,  # See list wahis_filter_names['country'] for possible options/
            "region": region,  # See list wahis_filter_names['region'] for possible options/
            "epiEventId": [],
            "diseases": disease,  # See list wahis_filter_names['disease'] for possible options/
            "diseaseType": [],  # Not yet added to the possible arguments for get_report_list()
            "reason": [],  # Not yet added to the possible arguments for get_report_list()
            "eventDate": {},  # Not yet added to the possible arguments for get_report_list()
            "eventStatus": [],  # Not yet added to the possible arguments for get_report_list()
            "reportHistoryType": [],  # Not yet added to the possible arguments for get_report_list()
            "reportDate": {
                "startDate": start_date,  # Must be in a string in YYYY-MM-DD format. Must Precede endDate
                "endDate": end_date  # Must be in a string in YYYY-MM-DD format. Must come after startDate
            }
        },
        "languageChanged": False  # Not yet added to the possible arguments for get_report_list()
    })

    response_report_list = requests.request("POST", URL, headers=headers, data=payload)

    # JSON RESULTS from POST /pi/getReportList
    return response_report_list.json()


def get_report_contents(report_info_id):
    '''Returns report data as dictionary for a given reportID.'''

    url_report = f'https://wahis.woah.org/pi/getReport/{str(report_info_id)}'
    # Don't think payload or headers are needed in this case...
    # tk May beed to add solution if code doesn't work on other systems.
    payload_report = {}
    headers_report = {}

    try:
        # sleep to reduce server load
        time.sleep(0.5)
        response_single_report = requests.request(
            "GET", url_report, headers=headers_report, data=payload_report)

        # save report contents as temporary dict & log progress
        contents_single_report = response_single_report.json()

    except error as e:
        print(e)

    return contents_single_report


def make_list_of_outbreaks_in_report(contents_single_report):
    '''When given the JSON contents of a WAHIS report this function will parse
    and clean outbreaks in the report. That is it extracts outbreaks from
    reports. Returning only a list of dictionaries containing parsed outbreak
    information.'''

    list_of_outbreak_dicts = []

    if contents_single_report['eventOutbreakDto']['outbreakMap']:
        try:

            for key, value in contents_single_report['eventOutbreakDto']['outbreakMap'].items():

                # 1. GATHERING OUTBREAK DATA
                # merge dicts in list of "speciesDetails"
                try:
                    contents_single_report['eventOutbreakDto']['outbreakMap'][key]['speciesDetails'] = {
                        k: v for list_item in contents_single_report['eventOutbreakDto']['outbreakMap'][key]['speciesDetails'] for (k, v) in list_item.items()}
                except:
                    print(f'Mistake with outbreak:',
                          contents_single_report['eventOutbreakDto']['outbreakMap'][key]['oieReference'])
                    # tk need a better way of dealing with reports that don't have outbreaks within them...
                    pprint.pprint(contents_single_report['eventOutbreakDto']['outbreakMap'][key])
                    continue

                # 2. CLEANING OUTBREAK DATA
                # within'outbreakMap' create key "isWild" from contents of exhisting 'animalCategory'
                contents_single_report['eventOutbreakDto']['outbreakMap'][key]['isWild'] = contents_single_report[
                    'eventOutbreakDto']['outbreakMap'][key]['animalCategory'][0]['isWild']
                # remove now uneeded 'animalCategory' with .pop()
                contents_single_report['eventOutbreakDto']['outbreakMap'][key].pop(
                    'animalCategory', None)

                # 3. APPEND CLEANED DATA TO OUTBREAK DICTIONARY (list_of_outbreak_info)
                list_of_outbreak_dicts.append(
                    contents_single_report['eventOutbreakDto']['outbreakMap'][key])
        except:
            print(f"Unable to add {contents_single_report['reportDto']['reportId']}")

        return list_of_outbreak_dicts

    else:
        pass


def append_report_data_to_outbreak(list_of_outbreak_dicts, contents_single_report, hide_contact_info=True):
    '''This function appends report data to each outbreak in a list of outbreaks
    (from same report). It also has the option of removing identifying
    information of people involved with data entry/manipulation in the
    government bodies involved in maintaining accurate WAHIS data.'''

    # Give the option to hide_contact_info of the people involved with submitting and processing WAHIS data
    if hide_contact_info == True:
        # make lists of fields to remove from 'enterInfoDto' in report data
        enterInfoDto_fields_to_remove = ['enterContactNum',
                                         'enterEmail',
                                         'enterFirstName',
                                         'enterImagePath',
                                         'enterLastName',
                                         'enterTitle',
                                         'recieverFullName']

        # make lists of fields to remove from 'senderDto' in report data
        senderDto_fields_to_remove = ['role',
                                      'sendPath',
                                      'senderAddress',
                                      'senderEmail',
                                      'senderFax',
                                      'senderFirstName',
                                      'senderFullName',
                                      'senderLastName',
                                      'senderNationalReference',
                                      'senderTelephone',
                                      'senderTitle']
        for field in enterInfoDto_fields_to_remove:
            contents_single_report['enterInfoDto'].pop(field, None)
        for field in senderDto_fields_to_remove:
            contents_single_report['senderDto'].pop(field, None)

    # because outbreak data has been aquired from make_list_of_outbreaks_in_report()
    # remove 'eventOutbreakDto' to avoid duplicate data
    contents_single_report.pop('eventOutbreakDto', None)

    # for each outbreak in the list of outbreaks add information for report it
    # was taken from
    for outbreak_dict in list_of_outbreak_dicts:
        outbreak_dict.update(contents_single_report)

    return list_of_outbreak_dicts


# def report_amalgamator(reports_for_disease, directory, save_rate=250, export_name="WAHIS_ReportOutbreaks"):
#     ###### Amalgamate reports and output .xlsx file(s) ######
#     file_save_counter = 1
#     amalgam_all_report_outbreaks = []
#
#     for count, report_object in enumerate(tqdm(reports_for_disease['homePageDto'], desc='Building report sheets: '), 1):
#         print(count)
#         # build list of outbreak dicts from each report; add report data and metadata to outbreak listing
#         # get single report contents
#         contents_single_report = get_report_contents(report_object['reportInfoId'])
#         # make list of outbreaks in report
#         list_of_outbreak_dicts = make_list_of_outbreaks_in_report(contents_single_report)
#         # add report metadata to each report_info in outbreak list
#         for outbreak in list_of_outbreak_dicts:
#             outbreak.update(report_object)
#         report_outbreaks = append_report_data_to_outbreak(list_of_outbreak_dicts,
#                                                           contents_single_report,
#                                                           hide_contact_info=True)
#
#         # add report metadata to each item in outbreak list
#         amalgam_all_report_outbreaks.extend(report_outbreaks)
#         # once added to "definitive" list, delete temp variables
#         del contents_single_report, list_of_outbreak_dicts, report_outbreaks
#
#         # Save a csv every parsed_args.save_rate^th report time
#         if count % save_rate == 0 or count == len(reports_for_disease['homePageDto']):
#             # Make pandas dataframe ( aka "table") with data we've built up to this point
#             df_amalgam_all_report_outbreaks = pd.json_normalize(
#                 amalgam_all_report_outbreaks, record_path=None, meta=None, meta_prefix=None, record_prefix=None, errors='raise', sep='.', max_level=None)
#             # df_amalgam_all_report_outbreaks = pd.DataFrame.from_records(amalgam_all_report_outbreaks, index=None, exclude=None, columns=None, coerce_float=False, nrows=None)
#             try:
#                 df_amalgam_all_report_outbreaks.to_excel(
#                     f'{OUTPUT_DIRECTORY}/{export_name}_{file_save_counter}.xlsx', index=False)
#             except:
#                 df_amalgam_all_report_outbreaks.to_csv(
#                     f'{OUTPUT_DIRECTORY}/{export_name}_{file_save_counter}.csv', index=False)
#             # once the outbreak dataframe has been exported as a csv we no longer need it. Delete to save RAM.
#             del df_amalgam_all_report_outbreaks
#             # clear all contents of the list of outbreaks
#             amalgam_all_report_outbreaks.clear()
#             file_save_counter += 1
#
#     return f'{directory}/{export_name} is done.'


def main():
    ##############################
    ### Parsing User Arguments ###
    ##############################
    parser = argparse.ArgumentParser(description="Gather WAHIS reports based on user's filters.")
    parser.add_argument("-op",
                        "--options",
                        action="store_true",
                        help=" Creates a file with the posible filter options for limiting your report results. See OUTPUTS folder in you current working directory.",
                        )
    parser.add_argument("-c",
                        "--country",
                        type=str,
                        nargs="*",
                        default=[],
                        help="After flag ('-c' or '--country') add countries for which you want report results seperated by a single space. E.G. '-c France Germany Ethiopia'",
                        )
    parser.add_argument("-r",
                        "--region",
                        type=str,
                        nargs="*",
                        default=[],
                        help="After flag ('-r' or '--region') add regions for which you want report results seperated by a single space. E.G. '-r Oceana Asia Europe'",
                        )
    parser.add_argument("-d",
                        "--disease",
                        type=str,
                        nargs="*",
                        default=[],
                        help="Disease(s) of interst, entered in bewteem apostrophes seperated by spaces. Be carefull to add full official name. EG: -d 'Anthrax ' 'Morbillivirus (Inf. with)(marine mammals)(2008-)'",
                        )

    parser.add_argument("-sd",
                        "--start_date",
                        required=False,
                        default=str(date.today() - timedelta(days=7)),
                        type=str,
                        help="[REQUIRED] Must be in 'YYYY-MM-DD' format and precede given 'end_date'.")
    parser.add_argument("-ed",
                        "--end_date",
                        required=False,
                        default=str(date.today()),
                        type=str,
                        help="[REQUIRED] Must be in 'YYYY-MM-DD' format and be after given 'start_date'."
                        )
    parser.add_argument("-s",
                        "--save_rate",
                        default=250,
                        type=int,
                        help="How many reports you want accessed before saving to output to computer. More = more demanding for your computer."
                        )
    parsed_args = parser.parse_args()

    # run save_filter_options() based on CLI input
    if parsed_args.options == True and not os.path.exists(OUTPUT_DIRECTORY + "WAHIS_filter_options.json"):
        save_filter_options(OUTPUT_DIRECTORY)

    # get current directory and create new folder "ouputs" if it doesn't exhist
    CURRENT_DIRECTORY = os.getcwd()
    OUTPUT_DIRECTORY = os.path.join(CURRENT_DIRECTORY, r'OUTPUTS')
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    EXPORT_NAME = "WAHIS_ReportOutbreaks"

    ########################
    ### Main tool logic. ###
    ########################
    if not parsed_args.options:
        if (parsed_args.country
            or parsed_args.region
            or parsed_args.disease
            or parsed_args.start_date
                or parsed_args.end_date):
            ###### Get list of reports ######
            reports_for_disease = get_report_list(
                country=parsed_args.country,
                region=parsed_args.region,
                disease=parsed_args.disease,
                start_date=parsed_args.start_date,
                end_date=parsed_args.end_date,)

            amalgam_reports_final = []
            file_save_counter = 1
            print(OUTPUT_DIRECTORY)

            for count, report_object in enumerate(tqdm(reports_for_disease['homePageDto'], desc='Gathering Reports...'), 1):
                # build list of outbreak dicts from each report; add report data and metadata to outbreak listing
                # get single report contents
                contents_single_report = get_report_contents(report_object['reportInfoId'])

                try:
                    if contents_single_report['eventOutbreakDto']['outbreakMap']:
                        list_of_outbreak_dicts = make_list_of_outbreaks_in_report(
                            contents_single_report)
                        # add report metadata to each report_info in outbreak list
                        for outbreak in list_of_outbreak_dicts:
                            outbreak.update(report_object)
                        report_outbreaks = append_report_data_to_outbreak(list_of_outbreak_dicts,
                                                                          contents_single_report,
                                                                          hide_contact_info=True)

                        # add report metadata to each item in outbreak list
                        amalgam_reports_final.extend(report_outbreaks)
                        # once added to "definitive" list, delete temp variables
                        del contents_single_report, list_of_outbreak_dicts, report_outbreaks

                    else:
                        amalgam_reports_final.extend(report_outbreaks)
                except:
                    print(
                        f"Report ID: {report_object['reportId']}. Error creating final report amalgam (amalgam_reports_final).")

                finally:
                    # Save a csv every SAVE_RATE^th report time
                    if count % parsed_args.save_rate == 0 or count == len(reports_for_disease['homePageDto']):
                        # Make pandas dataframe ( aka "table") with data we've built up to this point
                        df_amalgam_reports_final = pd.json_normalize(amalgam_reports_final)
                        # df_amalgam_reports_final = pd.DataFrame.from_records(amalgam_reports_final, index=None, exclude=None, columns=None, coerce_float=False, nrows=None)
                        try:
                            df_amalgam_reports_final.to_excel(f'{OUTPUT_DIRECTORY}/{EXPORT_NAME}_{file_save_counter}.xlsx', index=False)
                        except:
                            df_amalgam_reports_final.to_csv(f'{OUTPUT_DIRECTORY}/{EXPORT_NAME}_{file_save_counter}.csv', index=False)
                            # once the outbreak dataframe has been exported as a csv we no longer need it. Delete to save RAM.
                        del df_amalgam_reports_final
                        # clear all contents of the list of outbreaks
                        amalgam_reports_final.clear()
                        parsed_args.save_rate += 1


if __name__ == "__main__":
    main()
