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
				death count (deaths on date, as known on report date)<br>

That is, the dictionary contains all the NYC case/hosp/death tables, one per day of report.

# Excel sheets
probables.xlsx = accounting of NYC "probable" deaths; digitized from graphs in pdfs folder.<br>
influenza.xlsx = 1918 influenza numbers, digitized; source: https://www.archives.nyc/blog/2018/3/1/the-flu-epidemic-of-1918 <br>
clinicaltrials18Apr.xls = a (somewhat unrelated) excel sheet of covid clinical trials, with analysis of their methodology<br>


# KNOWN ISSUES
Data for 3/28 and 3/29 are not presently available. <br>
4/13 update, which came mid-day rather than at COB, updated cases, but not hospitalizations or deaths.<br>
4/14 update also came at mid-day; this time, both cases and deaths were updated up to 4/13 (prior updates had day-of numbers rather than day-before updates); this makes the update roughly equivalent to what one would have expected for the old-style 4/13 update. As a consequence, there is functionally a 1-day discontinuity in the data. Also, hospitalizations appear not to have been updated, even though deaths have been.<br>
4/15 DATE_OF_INTEREST header is mislabeled. Error is rectified when combiner.py is run. Hospitalized count is still one day behind.<br>
4/27 DATE_OF_INTEREST header, PROBABLE_DEATHS header are mislabeled in probable/confirmed file. Error is rectified when combiner.py is run. (NYCDOHMH, why you change field names?)

# DATA SOURCES
NYCDOHMH: <br>
	a) https://www1.nyc.gov/site/doh/covid/covid-19-data.page<br>
	b) https://github.com/nychealth/coronavirus-data<br>