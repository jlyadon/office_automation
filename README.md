# office_automation
Scripts for automating tasks at JRBT

## OldAPsScript.py

This script takes as input the 'awaiting pickup' list available for download via XCM. It removes unnecessary columns and creates two csv files: one of files that have been on the list longer than two weeks and one of files that have been on the list for one week to two weeks.

## TBDListNotebook.ipynb

This is the Jupyter notebook for testing parts of the script, diagnosing problems, and experimenting with changes.

## TrackingScript4.py

This app takes as input a csv list of packages to be tracked. It makes calls to USPS's Tracking API, generates a report of delivered packages, and removes delivered packages from the list.

## TrackingProjectNotebook.ipynb

A 'workbench' notebook for experiementing with new methods, diagnosing problems, and testing parts of the script

## Output

This directory stores file outputs from both scripts.
