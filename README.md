# nyccovid
Data regarding and analysis of COVID in NYC.

# JSON FORMAT
Dictionary:  	keys = Dates of report (MMDD)<br>
		values = lists of lists:<br>
			[0] = list of headers; <br>
			[n] = nth list of data, one datum per header, currently:<br>
				date of interest,<br>
				new covid cases (presumably positive tests as of date)<br>
				hospitalized case count <br>
				death count (cumulative deaths as of date, as known on report date)<br>

That is, the dictionary contains all the NYC case/hosp/death tables, one per day of report.

# KNOWN ISSUES
Data for 3/28 and 3/29 are not presently available. <br>
The 4/13 update, which came mid-day rather than at COB, updated cases, but not hospitalizations or deaths.

# DATA SOURCES
NYCDOHMH: <br>
	a) https://www1.nyc.gov/site/doh/covid/covid-19-data.page<br>
	b) https://github.com/nychealth/coronavirus-data<br>