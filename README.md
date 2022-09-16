# OIE_WAHIS.ReportRetriever
Automatically download publicly available animal disease reports from the World Organisation for Animal Health WAHIS database. Researchers can filter and download disease outbreak information as Excel Spreadsheets, without having to do it manually.

---

Made with ♥ by [Loic Leray](https://loicleray.com)

I hope that these tools will help epidemiologists and researchers with their projects.

---

## Intro
This document describes a new method for "web scraping" data from the World Organisation for Animal Health's (WOAH, previously OIE) World Animal Health Information System (WAHIS). It replaces [previous efforts to automate WAHIS data download](https://onlinelibrary.wiley.com/doi/abs/10.1111/tbed.14133?casa_token=V85WAk0RTFMAAAAA:lPcjIz-Os652-5RChFVqjZcWOhrb-8IdP6IKr5CsoS9NfCoP5CwVUiNPY78-GYhEO1cSM1m4CUeKvg).

tk LINK TO VIDEO??



### The problem.
Since changing their website in 2020 the World Organisation for Animal Health ([WAOH](https://www.woah.org), previously OIE) has made access to their data a lot faster. It is a vast improvement on a the previous platform. However, there are some still bugs that limit data selection and subsequent download. Long story short, it is impractical to use. This is especially true for research projects that require access to large volumes of WAHIS data.

### The Solution.
I have managed to reverse engineer WOAH's private application programming interface (API) and offer a couple of custom scripts that help download large amounts of disease outbreak information. It actually allows more detailed information to be downloaded than is available natively through the WAHIS portal.

This code merely automates the retrieval of publicly available information at a large scale. We are not stealing data. I have also attempted to limit the rate of requests to WOAH servers so as to not overload them.

# How to use this tool?
You will need a decent computer and basic understanding of Python programming to run this script. I have created fairly extensive documentation for the script so that you can either run it OR adapt it to suit your needs. If you are having trouble, please **contact me**.

*tk Continue documentation from here*

---
