# OIE_WAHIS.ReportRetriever
Automatically download publicly available animal disease reports from the World Organisation for Animal Health WAHIS database. Researchers can filter and download disease outbreak information to Excel Spreadsheets, without having to do it manually.

**Made with ♥ by [Loic Leray](https://loicleray.com). I hope that the se tools will help epidemiologists and researchers with their projects.**

## Intro
This document describes a new method for "web scraping" data from the World Organisation for Animal Health's (WOAH, previously OIE) World Animal Health Information System (WAHIS). It replaces [previous efforts to automate WAHIS data download](https://onlinelibrary.wiley.com/doi/abs/10.1111/tbed.14133?casa_token=V85WAk0RTFMAAAAA:lPcjIz-Os652-5RChFVqjZcWOhrb-8IdP6IKr5CsoS9NfCoP5CwVUiNPY78-GYhEO1cSM1m4CUeKvg).


### The problem.
Since changing their website in 2020 the World Organisation for Animal Health ([WAOH](https://www.woah.org), previously OIE) has made access to their data a lot faster. It is a vast improvement on a the previous platform. However, there are some still bugs that limit data selection and subsequent download. Long story short, it is impractical to use. This is especially true for research projects that require access to large volumes of WAHIS data.

### The Solution.
I have managed to reverse engineer WOAH's private application programming interface (API) and offer a couple of custom scripts that help download large amounts of disease outbreak information. It actually allows more detailed information to be downloaded than is available natively through the WAHIS portal.

This code merely automates the retrieval of publicly available information at a large scale. We are not stealing data. I have also attempted to limit the rate of requests to WOAH servers so as to not overload them. Please be considerate and don't overuse WOAH's server resources.

## What data can I access?

By default this script creates an excel spreadsheet for each outbreak in the disease and filters you specify. For each outbreak it shows outbreak information (ID#s, location, animal population affected, disease and strain, testing ect...) as well as report information the outbreak was taken from (organisations involved, control methods, report IDs ect...).

![image](https://user-images.githubusercontent.com/47128655/190842786-afdd502e-628f-4d90-815e-63dd41ab26db.jpeg)

You can run the `get_filter_options()` function to return a summary of the
filters you can use to narrow your search.The dictionary it outputs shows you filters (KEYS) and their possible options (VALUES). These include:
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

For example get reports for "*African Swine Fever* reports in *Albania* between a *certain date range*" **OR** *Equine arteritis virus (Inf. with)* in *Asia* that are a *recurrence of an eradicated disease*. Reports can be filtered by any date range `start_date` and `end_date` in *YYYY-MM-DD* format.


# How to use this tool?
You will need a decent computer and basic understanding of Python programming to run this script. I have created fairly extensive documentation for the script so that you can either run it OR adapt it to suit your needs, see "USAGE". If you are having trouble, please **contact me**.

In your preffered command line tool*tk Continue documentation from here*


## Usage
