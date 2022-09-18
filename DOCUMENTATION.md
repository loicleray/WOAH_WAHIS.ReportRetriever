Please note that the documentation is not yet finalised. I am still actively working on it.
For general use instructions see the "README.md" file.
*See https://github.com/loicleray/OIE_WAHIS.ReportRetriever for documentation and explanations.*

# How I think the WAHIS API works.

You can run the `get_filter_options()` function to return a more complete summary of the filters you can apply to your search. The dictionary it outputs shows you filters (`keys`) and their possible options (`values`). WAHIS Disease naming is a bit inconsistent with extra spaces and weird parenthesis *(see image below)*. I strongly recommend using this function to see how the disease you are interested in is being saved on the WAHIS database.

![Screen Shot 2022-09-17 at 16 47 39](https://user-images.githubusercontent.com/47128655/190844671-a5d8ca55-e14d-425d-b75f-d0b875f07b68.jpg)


# WAHIS Disease Event Report and Outbreak Mass Download


Made by [Loic Leray](https://loicleray.com) - [CONTACT](mailto:hi@loicleray.com)

---
This document describes a new method for "web scraping" data from the World Animal Health Information System (WAHIS), it replaces [previous efforts to automate WAHIS data download](https://onlinelibrary.wiley.com/doi/abs/10.1111/tbed.14133?casa_token=V85WAk0RTFMAAAAA:lPcjIz-Os652-5RChFVqjZcWOhrb-8IdP6IKr5CsoS9NfCoP5CwVUiNPY78-GYhEO1cSM1m4CUeKvg).

### The problem.

Since changing their website in 2020 the World Organisation for Animal Health ([WAOH](https://www.woah.org), previously OIE) has made access to their data a lot faster. It is a vast improvement on a the previous platform. However, there are some still bugs that limit data selection and subsequent download. Long story short, it is impractical for research projects that require access to large volumes of WAHIS data.

### The Solution.
I have managed to reverse engineer WOAH's private application programming interface (API) and offer a couple of custom scripts that help download large amounts of disease outbreak information. It actually allows more detailed information to be downloaded than is available natively through the WAHIS portal.

This code merely automates the retreival of publically available information at a large scale. We are not stealing this data. I have also attempted to limit the rate of requests to WOAH servers so as to not overload them.

### About the Solution

I have been teaching myself to code for the last couple of years, this is the first (actually) usefull project I've built.

You will need a decent computer and basic understanding of Python programming to run this script. I have created fairly extenssive documentation for the script so that you can adapt it to suit your needs (with minimal effort). Depending on the amount of data you need to collect it should run aboutI hoped that this helps researchers and epidemiologists more further research. If you are having trouble, I can likely help you get the data (so long as you pay for my time).

## Parsing Report Filter Options
The next few lines of code are used to find and extract the available filters you can use to limit report results.

These filters enable customised calls to be made to the **POST ...pi/getReportList API** to limit search results based on needs of end used. EG:
- Get results for African Swine Fever reports in Albania.
- Get results for Equine arteritis virus (Inf. with) reports in Asia that are a recurrence of an eradicated disease.

The dictionary it outputs shows you filters (KEYS) and their show you possible options (VALUES).
Filters include:
1. country
2. region
3. epiEventId
4. diseases
5. diseaseType
6. reason
7. eventDate
8. eventStatus
9. reportHistoryType
10. reportDate

> NOTE: reports can be filtered by any date range start_date and end_date in YYYY-MM-DD format, but this is added to the **POST pi/getReportList API** request payload. See cells "Get Report Lists" below.


## Get reports list, based on filters you specify.
The API calls the WAHIS server for information via the **URL**. More detail about the information it wants to retreived is passed through the **payload**. The payload allows you to filter for specific reports, see cells above. The default behaviour (ie when no filter is specified) is to include all results.

Meta information such as machine/browser making the request is modified in **headers**.



# Known API Access points.
Below is a list of access points for the WAHIS database, if you find more please let me know about them.

## pi/getReportList
* https://wahis.woah.org/pi/getReportList
  * Gets a list of reports based on payload entered into it.
```
javascript
{"pageNumber": 1,
  "pageSize": 1000000000, # 1000000000 is the MAX allowable to be given in payload without "BAD REQUEST ERROR"
  "searchText": "", # Not yet added to the possible arguments for get_report_list()
  "sortColName": "", # Not yet added to the possible arguments for get_report_list()
  "sortColOrder": "DESC", # "ASC" = Ascending oldest to newest, "DESC" = Descending oldest to newest.
  "reportFilters": {
    "country": country, # See list wahis_filter_names['country'] for possible options/
    "region": region, # See list wahis_filter_names['region'] for possible options/
    "epiEventId": [],
    "diseases": disease, # See list wahis_filter_names['disease'] for possible options/
      "diseaseType": [], # Not yet added to the possible arguments for get_report_list()
      "reason": [], # Not yet added to the possible arguments for get_report_list()
      "eventDate": {}, # Not yet added to the possible arguments for get_report_list()
      "eventStatus": [], # Not yet added to the possible arguments for get_report_list()
      "reportHistoryType": [], # Not yet added to the possible arguments for get_report_list()
      "reportDate": {
        "startDate": start_date, # Must be in a string in YYYY-MM-DD format. Must Precede endDate
        "endDate": end_date # Must be in a string in YYYY-MM-DD format. Must come after startDate
      }
    },
    "languageChanged": False # Not yet added to the possible arguments for get_report_list()
  })
```

## pi/getAllOutbreaks
* https://wahis.woah.org/pi/getAllOutbreaks
  * JSON list of disease outbreak. Only shows outbreak meta informatiom (outbreak id, location, date, reportid it bleongs to etc), no details of the actual outbreak contents (disease, number of animals affected, contron measures etc...). It seems like the only payload it accepts is the standard one below. This means that it can only return ALL OUTBREAKS? Please let me know if you figure out how to fine tune and filter results.

**Payload to include:**
```
javascript
{"pageNumber":1,"pageSize":25,"searchText":"","sortColName":"","sortColOrder":"ASC","reportFilters":{"reportDate":{"startDate":"1950-01-01","endDate":"2022-09-06"}},"languageChanged":false}
```
**Example json response:**
```
javascript
{...},
{
    "outbreakId": 42635,
    "locationName": "TROULLOI",
    "startDate": "2016-10-05",
    "endDate": "2016-12-13",
    "latitude": 35.005867,
    "longitude": 33.628462,
    "reportId": 10203,
    "totalOutbreaks": 1,
    "isCluster": false,
    "animalCategory": [
        {
            "isWild": false
        }
    ],
    "outbreakInfosId": 42635,
    "reportInfoId": 21902
},
{...}
```
## pi/getReport/<report_id>
* https://wahis.woah.org/pi/getReport/22103
  * JSON response contains all data specific to given report ID

### Understanding the contents of an individual report.
- Reports are identified using a unique report ID.
- Each report contains information including:
    - Sender information (*SenderDto*)
        - Information about the informing agency/government and details on their representitive.
        - Institution/Agency, Address, Contact Name, Telephone number, Contact's Email, Contact Job Position
    - enterInfoDto
        - Information about the person receiving information
        - Address, Contact Name, Telephone number, Contact's Email, Contact Job Position
    - generalInfoDto
        - General overview information about the report
        -  Country or Zone, Disease Name, start and end date, aquatic or land, disease variant, confirmation date, reson, causal agent, disease categorie (OIE listed or not), report date, date of last occurence, translation of reason, country or territory
    - epidemiologyDto
        - soil information, Comment about disease
    - eventCmDto
        - Information about the control measures (CM) applied to contents of this report.
        - CM category, description of applied CMs, CMs to be applied
    - diagSumDto
        - Information about the diagnostics of this report (and its outbreaks)
        -  isClinical, isOutbreakLevel
        - diagDetailsDtoList"
        - testName, category, laboratory name, laboratory ID, species sampled, species sample required, total outbreak, testing start date, testing end date, test type, etc
    - eventQtySumDto
        - Quantitative information about the outbreaks in the report. I think it's only given if there is one outbreak in the report, but not 100% sure yet.
        - specieName, lastLevelSpecieName, totalSusceptible, totalNcase, totalDead, totalUnit, specieId, measuringUnit, susceptible, number of case case, number dead
    - eventOutbreakDto
        - Gives details of every outbreak contained withing the report.
        - Outbreak ID ("ob_XXXXX"), geographic coordinates (longitude and latitude),nationalObReference, oieReference, outbreakStartDate, firstAdmDivision, strain, secondAdmDivision, epiUnitType (farm, village, stable, pond etc), geographicCoordinates, thirdAdmDivision, locationApprox (true or false), affectedDesc (describes the epidemiological unit type, updates to controne measures for specific outbreaks
        - species details --> spicieName, lastLevelSpecieName, unit, specieId, totalDead, totalSusceptible, totalKilledDisposed, totalSlaughtered, totalNcase, totalVaccinated, control measues, diagnostic test summary, locations (text)
    - reportDto
        - reportId, reportStatus, eventStatus, selfDeclaration, reportTitle, reportDate, eventDescriptionStatus
    - totalCases
    
 ---
**REST OF DOCUMENT IN NOT FINALISED!**
 ---

  1. **country**
      * **EG:** Afghanistan, Albania, Algeria, American Samoa, etc...
  2. **region**
      * **EG:** Africa, Americas, Asia, Europe, Middle East, ect...
  3. **epiEventId**
      * **EG:** EBLV1, EBLV2, H1, H10, H10N1, H10N2, H10N33, ect...
  4. **diseases**
      * **EG:** African swine fever virus (Inf. with), Algal toxicosis (2008-), Anthrax, Toxoplasma gondii (Inf. with)(2008-), Toxoplasmosis, ect...
  5. **diseaseType**
      * **EG:** EBLV1, EBLV2, H1, H10, H10N1, H10N2, H10N33, ect...
  6. **reason**
      * **EG:** Emerging disease, First occurrence in a zone or a compartment, First occurrence in the country, New host, etc...
  7. **eventDate**
      * Any date range that you input.
  8. **eventStatus**
      * **EG:** On-going, Resolved, Stable
  9. **reportHistoryType**
      * **EG:** Follow-up report, Immediate notification, etc...
  10. **reportDate**
      * Any date range that you input.
