# nyccovid
Data regarding and analysis of COVID in NYC.

# JSON FORMAT
Dictionary:  	keys = Dates of report (MMDD)
		values = lists of lists:
			[0] = list of headers; 
			[n] = nth list of data, one datum per header, currently:
				date of interest,
				new covid cases (presumably positive tests as of date)
				hospitalized case count 
				death count (cumulative deaths as of date, as known on report date)

That is, the dictionary contains all the NYC case/hosp/death tables, one per day of report.

# KNOWN ISSUES
Please note that the data for 3/28 and 3/29 are not presently available. 

# DATA SOURCES
NYCDOHMH: 
	a) https://www1.nyc.gov/site/doh/covid/covid-19-data.page
	b) https://github.com/nychealth/coronavirus-data