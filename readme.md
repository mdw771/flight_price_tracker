# Flight Price Tracker

## Introduction

Scrapes air ticket prices using Selenium, fetch the price value, save it in a CSV log file, and plot price history. 

This program is currently designed for retrieving the US-China flight prices from [flychina.com](flychina.com).

## Usage

This program requires the proper ChromeDriver that works with Selenium and is compatible with your Google Chrome or
Chromium. A Windows version ChromeDriver that works with Chrome version 118 is included with the source code.
For other versions, see [here](https://sites.google.com/chromium.org/driver/downloads?authuser=0). After downloading
the right ChromeDriver, place it under `source_path/bin`. 

- Go to [https://www.flychina.com/](https://www.flychina.com/) and search the flight with the from/to locations,
dates, and other options you want. After hitting Search, copy the URL of the returned webpage. 
- Open the driver script `main.py`. Set the URL for the `Retriver` object. 
- Run `main.py`. The first time you run it, the program creates a log file as `source_path/log/log.csv`. Future
queries on different dates are automatically appended to this log file, and a plot showing the ticket price
history is generated at the end. 