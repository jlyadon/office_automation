# office_automation
Scripts for automating tasks at JRBT

Note: Because these scripts work on confidential information, I am unable to include sample inputs and outputs.

## CRTSignUpProject

This script manages employees' sign-up status for a required civil rights training. The Jupyter notebook functions as an interface to update the statuses of those who sign up and send them an automated confimation email. The notebook also contains code for sending emails to specific groups, i.e., reminding those who have not yet signed up.

## DeadlineReports

The input for this script is prepared by exporing search results in an Excel spreadsheet from XCM. The user places this spreadsheet in the RawSearchResults directory and loads it into DeadlineReport.py. The script then exports a pivot table as an Excel spreadsheet that informs staff of the status of tax returns for which each accountant is responsible. It also exports a matplotlib stacked bar graph with the same information as a png file. Returns that still require the accountants attention are counted in a black bar; returns in the status 'eFile Awaiting 8879' are indicated in gray, since the next step is the responsibility of the client.

Publishing this information supports business decisions by allowing accountants to plan well and pace themselves and by enabling them to 'share the load.' When one accountant falls behind in the count, others can step into to help, turning a collection of individuals into a team.

## OldAP_Project

This script takes as input the 'awaiting pickup' list available for download via XCM. It removes unnecessary columns and creates two csv files: one of files that have been on the list longer than two weeks and one of files that have been on the list for one week to two weeks. The result is a 'call list' for contacting clients who are delayed in picking up their doucments.

## TrackingApp

This app takes as input a csv list of packages to be tracked. It makes calls to USPS's Tracking API, reads the XML response, generates a report of delivered packages, and removes delivered packages from the input csv.