# OIE_WAHIS.ReportRetriever
Automatically download publicly available animal disease reports from the World Organisation for Animal Health WAHIS database. Researchers can filter and download disease outbreak information to Excel Spreadsheets, without having to do it manually.

**Made with ♥ by [Loic Leray](https://loicleray.com). I hope that these tools will help epidemiologists and researchers with their projects. If you use this tool I'd really appreciate if you showed me the projects you're working on.**

## Intro
This document describes a new method for "web scraping" data from the World Organisation for Animal Health's (WOAH, previously OIE) World Animal Health Information System (WAHIS). It replaces [previous efforts to automate WAHIS data download](https://onlinelibrary.wiley.com/doi/abs/10.1111/tbed.14133?casa_token=V85WAk0RTFMAAAAA:lPcjIz-Os652-5RChFVqjZcWOhrb-8IdP6IKr5CsoS9NfCoP5CwVUiNPY78-GYhEO1cSM1m4CUeKvg).


### The problem.
Since changing their website in 2020 the World Organisation for Animal Health ([WAOH](https://www.woah.org), previously OIE) has made access to their data a lot faster. It is a vast improvement on a the previous platform. However, there are some still bugs that limit data selection and subsequent download. Long story short, it is impractical to use. This is especially true for research projects that require access to large volumes of WAHIS data.

### The Solution.
I have managed to reverse engineer WOAH's private application programming interface (API) and offer a couple of custom scripts that help download large amounts of disease outbreak information. It actually allows more detailed information to be downloaded than is available natively through the [WAHIS portal](https://wahis.woah.org/#/home).

This code merely automates the retrieval of publicly available information at a larger scale. I have also attempted to limit the rate of requests to WOAH servers so as to not overload them. Please be considerate and don't overuse WOAH's server resources.

## What data can I access?

By default this script creates an excel spreadsheet for each outbreak in the disease and filters you specify. For each outbreak it shows outbreak information (ID#s, location, animal population affected, disease and strain, testing ect...) as well as report information the outbreak was taken from (organisations involved, control methods, report IDs ect...).

![image](https://user-images.githubusercontent.com/47128655/190842786-afdd502e-628f-4d90-815e-63dd41ab26db.jpeg)

### Filtering to the data I need?

WAHIS has a lot of data. You're going to want to limit your search results to access only the data you need.

> *African Swine Fever* reports in *Albania* between a *certain date range*"

**OR**

>*Equine arteritis virus (Inf. with)* in *Asia* that are a *recurrence of an eradicated disease*.

This will reduce how long it takes for the program to run and also helps minimise the load on WAHIS servers. Reports should also be filtered by date range `start_date` and `end_date` in *YYYY-MM-DD* format. Reports can be filtered via 10 filters, including:

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

You can run the `get_filter_options()` function to return a more complete summary of the filters you can apply to your search. The dictionary it outputs shows you filters (`keys`) and their possible options (`values`). WAHIS Disease naming is a bit inconsistent with extra spaces and weird parenthesis *(see image below)*. I strongly recommend using this function to see how the disease you are interested in is being saved on the WAHIS database.

![Screen Shot 2022-09-17 at 16 47 39](https://user-images.githubusercontent.com/47128655/190844671-a5d8ca55-e14d-425d-b75f-d0b875f07b68.jpg)

# How to use this tool?
You will need a decent computer and basic understanding of Python programming to run this script. I have created fairly extensive documentation (*see documentation.md file*)for the script. You can either run it as is or adapt the script it to suit your needs.

## Using the Command-line Tool

### 1. Getting filter options
To view filter options in your commandline run:

`python
python3 -c 'import report_retriever; print(report_retriever.get_filter_options())'`

To save filter options as a ".json" file in run:

`python
python3 -c 'import report_retriever; report_retriever.save_filter_options()'`

### 2. Gathering reports
Now that you've thought about the data that is of interest to you, you're going to need to make a list of all the reports that fit the criteria of your filter options.

Please note that depending on the amount of data you're accessing this may take a LONG time. Processing 4000 reports may take up to 5hrs. The code automatically saves progress as it runs. Depending on how many people use this tool I will work on
