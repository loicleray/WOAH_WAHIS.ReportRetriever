# OIE_WAHIS.ReportRetriever
Automatically download publicly available animal disease reports from the World Organisation for Animal Health WAHIS database. Researchers can filter and download disease outbreak information to CSV/Excel Spreadsheets, without having to do it manually.

> By [Loic Leray](https://loicleray.com). If this was of use to you, please consider [buying me a "coffee"](https://www.buymeacoffee.com/loicleray) and share your projects with me! I hope that these tools will help epidemiologists and researchers with their projects.
Happy researching! 🤓

---

### NOTE
WAHIS has updated it's system since this was released. I have had emails from researchers stating some script functionality was no longer working as expected. I haven't had sufficient time to test and rework it. If there is sufficient demand from researchers I may start working on this again. That said, a lot of the contents in the scripts should be a big headstart those that can code.

---

![RR-Thumbnail@8x](https://user-images.githubusercontent.com/47128655/190937217-a42465cc-b2d6-4ca6-bbf2-2aac3ea3f31d.png)

## Introduction
This document describes a new method for "web scraping" data from the World Organisation for Animal Health's (WOAH, previously OIE) World Animal Health Information System (WAHIS). It replaces [previous efforts to automate WAHIS data download](https://onlinelibrary.wiley.com/doi/abs/10.1111/tbed.14133?casa_token=V85WAk0RTFMAAAAA:lPcjIz-Os652-5RChFVqjZcWOhrb-8IdP6IKr5CsoS9NfCoP5CwVUiNPY78-GYhEO1cSM1m4CUeKvg).


### The problem.
Since changing their website in 2020 the World Organisation for Animal Health ([WAOH](https://www.woah.org), previously OIE) has made access to their data a lot faster. It is a vast improvement on a the previous platform. However, there are some still bugs that limit data selection and subsequent download. Long story short, it is impractical to use. This is especially true for research projects that require access to large volumes of WAHIS data.

### The Solution.
I have managed to reverse engineer WOAH's private application programming interface (API) and offer a couple of custom scripts that help download large amounts of disease outbreak information. It actually allows more detailed information to be downloaded than is available natively through the [WAHIS portal](https://wahis.woah.org/#/home).

This code merely automates the retrieval of publicly available information at a larger scale. I have also attempted to limit the rate of requests to WOAH servers so as to not overload them. Please be considerate and don't overuse WOAH's server resources.

## What data can I access?

By default this script creates an excel spreadsheet for each outbreak in the disease and filters you specify. For each outbreak it shows outbreak information (ID#s, location, animal population affected, disease and strain, testing ect...) as well as report information the outbreak was taken from (organisations involved, control methods, report IDs ect...).

![image](https://user-images.githubusercontent.com/47128655/190842786-afdd502e-628f-4d90-815e-63dd41ab26db.jpeg)

---
# I am still working on this tool. It is not yet finalised, but should work for most diseases. [If you need specific data contact me through my website.](https://www.loicleray.com/contact/).
---

## How to use this tool?
There are two ways you can interact with this tool. Either via the command-line interface (CLI) or in your own scripts. The CLI is the recommended (and most approachable way) for non-coders to get WAHIS report data.

 That said, there is fairly extensive documentation (*see DOCUMENTATION.md file*) for those wanting to build their own scripts. This requires will need a decent computer and basic understanding of Python programming language.

# USAGE: ReportRetriever in the Command-line (RECOMMENDED)
WAHIS has a lot of data. You're going to want to limit your search results to access only the data you need. This will reduce how long it takes for the program to run and also helps minimise the load on WAHIS servers. As you'll see below, reports must also be filtered by date range `start_date` and `end_date` in *YYYY-MM-DD* format. You can currently filter reports parameters listed below.

1. **country**
    * **EG:** Afghanistan, Albania, Algeria, American Samoa, etc...
    * flag: `-c` or `--country`
2. **region**
    * **EG:** Africa, Americas, Asia, Europe, Middle East, ect...
    * flag: `-r` or `--region`
4. **diseases**
    * **EG:** African swine fever virus (Inf. with), Algal toxicosis (2008-), Anthrax, Toxoplasma gondii (Inf. with)(2008-), Toxoplasmosis, ect...
    * flag: `-d` or `--disease`
4. **start_date**
    * date in YYYY-MM-DD format
    * **EG:** 2022-02-19
    * flag: `-sd` or `--start_date`
5. **end_date**
    * date in YYYY-MM-DD format
    * **EG:** 2022-02-19
    * flag: `-ed` or `--end_date`


## 1. Getting filter options
I reccomend you get a complete summary of the filters you can apply to your search by running:
```bash
python3 report_retriever.py -op
```
This will output a file named *"WAHIS_filter_options.json"* in the *"OUTPUTS"* folder. This file shows you filters (`keys`) and their possible options (`values`). Use it to figure out how you want to filter results.  I strongly recommend using this function to see how the disease you are interested in is being saved on the WAHIS database.

**NOTE:** WAHIS Disease naming is a bit inconsistent with extra spaces and weird parenthesis *(see image below)*.

![Screen Shot 2022-09-17 at 16 47 39](https://user-images.githubusercontent.com/47128655/190844671-a5d8ca55-e14d-425d-b75f-d0b875f07b68.jpg)



## 2. Gathering reports
Now that you've thought about the data that is of interest it's time to start telling the program to access the data. Copy and paste filter values of interest into the command-line as per the instructions below. The program accepts multiple inputs for each filter flags. Filter flags can be combined.

> Please note that depending on the amount of data you're accessing this may take a LONG time. Processing 4000 reports may take up to 5hrs. The code automatically saves progress as it runs, by default an excel spreadsheet is saved every 250 reports.


### i) Selecting date range
You **MUST** limit report results based on a date range using the `-sd` (`start_date`) and `-ed` (`end_date`) flags. Date arguments must be added in *YYYY-MM-DD* format. The `start_date` must precede `end_date`.

**Example:**
```bash
python3 report_retriever.py -sd 1990-01-01 -ed 2020-08-13
```

### ii) Selecting specific disease(s)
Limit results based on disease(s) of interest using `--disease` or `-d` flags.
For single disease run:
```bash
python3 report_retriever.py -d 'Official_Disease_Name'
```
For multiple diseases run:
```bash
python3 report_retriever.py -d 'Official_Disease_Name_1' 'Official_Disease_Name_2' '...' 'Official_Disease_Name_x'
```

### iii) Limit data to specific region (or regions)
Limit results based on disease(s) of interest using *--region* or *-r* flags.
For single region run:
```bash
python3 report_retriever.py -r Region
```
For multiple regions run:
```bash
python3 report_retriever.py -r Region_1 Region_2 ... Region_X
```

### iv) Limit data to specific country (or countries)
Limit results based on disease(s) of interest using *--country* or *-c* flags.
For single country run:
```bash
python3 report_retriever.py -c Country
```
For multiple countries run:
```bash
python3 report_retriever.py -c Country_1 Country_2 ... Country_X
```

### Combining filter flags
You can combine filter flags. The program will return reports that fit all of the filters you applied.

Assume you want to get reports for the following query:
> Reports for *African Swine Fever* and *Foot & Mouth Disease* in *Europe* between a *January 1st 1990* and *August 13th 2020*

You would need to run:
```bash
python3 report_retriever.py -d 'African swine fever virus (Inf. with) ' 'Foot and mouth disease virus (Inf. with) ' -r Europe -sd 1990-01-01 -ed 2020-08-13
```
Admittedly this code isn't very pretty, but it gets the job done!

### Running without filter flags
I strongly recommend you **DO NOT** run the script without adding filter/flags. That said, the default behaviour for the program is to return all reports for all diseases submitted in the previous 7 days.

The code I don't reccoment you run:
```bash
python3 report_retriever.py
```
## What happens after I run the program?
The program will make a list of reports that fit your criteria. For each report in the list it will access the report data, extract the outbreak from the data and append them to a excel spreadsheet. A new spreadsheet is saved after every 250 reports it processes. There is a loading bar that shows the programs progress. However, the progress bar shows rough estimates only, time estimates are not very accurate.

To understand the outputted spreadsheets, you need to understand the information contained in each report. The "DOCUMENTATION.md" file has a section called "Understanding the contents of an individual report" which explains this in detail.

# USAGE: Understanding the outputted data.
I am going to leave this blank for the time being. If people use this I will elaborate on report contents.
