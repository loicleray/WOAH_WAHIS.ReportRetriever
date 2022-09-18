Please note that the documentation is not yet finalised. I am still actively working on it.
For general use instructions see the "README.md" file.
*See https://github.com/loicleray/OIE_WAHIS.ReportRetriever for documentation and explanations.*

---

# Get reports list, based on filters you specify.
The API calls the WAHIS server for information via the **https://wahis.woah.org/pi/<API_entry_point>**. More detail about the information it wants to retrieve is passed through the **payload**. The payload allows you to filter for specific parameters. The default behaviour (ie when no filter is specified) is to include all results.

Meta information such as machine/browser making the request is modified in **headers**, but it doesn't seem this information is necessary to get a successful reponse.

# Known API Access points.
Below is a list of access points for the WAHIS database, if you find more please let me know about them.

## pi/getReportList
* https://wahis.woah.org/pi/getReportList
  * Gets a list of reports based on payload entered into it.

```javascript
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
```javascript
{"pageNumber":1,"pageSize":25,"searchText":"","sortColName":"","sortColOrder":"ASC","reportFilters":{"reportDate":{"startDate":"1950-01-01","endDate":"2022-09-06"}},"languageChanged":false}
```
**Example json response:**
```javascript
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
    - `SenderDto`
        - Sender information; information about the informing agency/government and details on their representitive.
        - Institution/Agency, Address, Contact Name, Telephone number, Contact's Email, Contact Job Position
    - `enterInfoDto`
        - Information about the person receiving information
        - Address, Contact Name, Telephone number, Contact's Email, Contact Job Position
    - `generalInfoDto`
        - General overview information about the report
        -  Country or Zone, Disease Name, start and end date, aquatic or land, disease variant, confirmation date, reson, causal agent, disease categorie (OIE listed or not), report date, date of last occurence, translation of reason, country or territory
    - `epidemiologyDto`
        - soil information, Comment about disease
    - `eventCmDto`
        - Information about the control measures (CM) applied to contents of this report.
        - CM category, description of applied CMs, CMs to be applied
    - `diagSumDto`
        - Information about the diagnostics of this report (and its outbreaks)
        -  isClinical, isOutbreakLevel
        - diagDetailsDtoList"
        - testName, category, laboratory name, laboratory ID, species sampled, species sample required, total outbreak, testing start date, testing end date, test type, etc
    - `eventQtySumDto`
        - Quantitative information about the outbreaks in the report. I think it's only given if there is one outbreak in the report, but not 100% sure yet.
        - specieName, lastLevelSpecieName, totalSusceptible, totalNcase, totalDead, totalUnit, specieId, measuringUnit, susceptible, number of case case, number dead
    - `eventOutbreakDto`
        - Gives details of every outbreak contained withing the report.
        - Outbreak ID ("ob_XXXXX"), geographic coordinates (longitude and latitude),nationalObReference, oieReference, outbreakStartDate, firstAdmDivision, strain, secondAdmDivision, epiUnitType (farm, village, stable, pond etc), geographicCoordinates, thirdAdmDivision, locationApprox (true or false), affectedDesc (describes the epidemiological unit type, updates to controne measures for specific outbreaks
        - species details --> spicieName, lastLevelSpecieName, unit, specieId, totalDead, totalSusceptible, totalKilledDisposed, totalSlaughtered, totalNcase, totalVaccinated, control measues, diagnostic test summary, locations (text)
    - `reportDto`
        - reportId, reportStatus, eventStatus, selfDeclaration, reportTitle, reportDate, eventDescriptionStatus
    - `totalCases`

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
