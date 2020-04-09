import json

## JSON FORMAT
## Dictionary:  keys = Dates of report (MMDD)
##              values = lists of lists:
##                      [0] = list of headers; [n] = nth list of data

def two_digitify(num):
    if (num <= 0) or (num > 31):
        answer = "ERROR"
    elif num >= 10:
        answer = str(num)
    else:
        answer = "0" + str(num)
    return answer;

def days_in_month(num):
    daysarray = [31,29,31,30,31,30,31,31,30,31,30,31]
    if (num > 12) or (num < 1):
        answer = -1
    else:
        answer = daysarray[num-1]
    return answer;

def rectify_header(inheader):
    if inheader == "DIAGNOSIS_DATE":
        outheader = "DATE_OF_INTEREST"
    else:
        outheader = inheader
    return outheader;

def generate_datelist(zerodate,length):
    counter = 0
    outlist = []
    month = int(zerodate[0:2])
    day = int (zerodate[2:4])
    
    while counter < length:
        todaydate = two_digitify(month) + two_digitify(day)
        outlist.append(todaydate)
        day += 1
        if day > days_in_month(month):
            day = 1
            month +=1
        if month > 12:
            month = 1
        counter += 1
    return outlist;
            

def rectify_datalist(inlist):
    outlist = []
    for item in inlist:
        if item.find("/")>-1: #it's a date
            datelist = item.split("/")
            month = two_digitify(int(datelist[0]))
            day = two_digitify(int(datelist[1]))
            newitem = month+day
        else:
            if item == "":
                newitem = 0
            else:
                newitem = int(item)
        outlist.append(newitem)
    return outlist;
            
            
##
# PROCEDURE parse_dohmh_file
# IN: file pointer to DOHMH "csv" file, (delimiter)
# OUT: list containing the header (list) and data (list)
#
def parse_file(infileptr):
    outlist = []
    tableheadstring = "<thead>"
    headsplit = "<th>"
    tablebodyindicator = "<tbody>"
    entrysplit = "<tr id"
    datasplit = "<td>"
    wholepage = infilepointer.read().decode('utf-8',errors='ignore')
    headstartindex = wholepage.find(tableheadstring)
    if len(tableheadstring) > -1:
        trimmedpage = wholepage[headstartindex:]
    else:
        trimmedpage = ""
        print("Trim error...")
    headerlist = []
    rawheaderlist = trimmedpage.split(headsplit)
    for i in range(1,len(rawheaderlist)):
        rawheader = rawheaderlist[i]
        endbracketindex = rawheader.find("<")
        header = rawheader[:endbracketindex]
        headerlist.append(rectify_header(header))
    outlist.append(headerlist)

    tablebodyindex = trimmedpage.find(tablebodyindicator)
    trimmedpage = trimmedpage[tablebodyindex:]
    rawentrylist = trimmedpage.split(entrysplit)
    for i in range(1,len(rawentrylist)):
        rawentry = rawentrylist[i]
        rawdatalist = rawentry.split(datasplit)
        datalist = []
        for j in range (1, len(rawdatalist)):
            rawdatum = rawdatalist[j]
            endbracketindex = rawdatum.find("<")
            datum = rawdatum[:endbracketindex]
            datalist.append(datum)
        outlist.append(rectify_datalist(datalist))
            
    return outlist;


##
# PROCEDURE print_tsv_to_file
# IN: data dictionary,fieldname (delimiter)
# OUT: (to file) 2-dimensional delimited file of the field indicated 
#
def print_tsv_to_file(indict,targetfieldname,delimiter="\t"):
    datefieldname = "DATE_OF_INTEREST"
    outfilename = fieldname.lower()+".tsv"
    outfile = open(outfilename,"w")
    keyiterable = indict.keys()
    outstring = "\t"
    count = 0
    for item in keyiterable:
        if count == 0:
            outstring += item
        else:
            outstring += delimiter + item
        count += 1
    print (outstring,file=outfile)
    lastdatumdate = item
    lastdatumlist = indict[lastdatumdate]
    dateindex = lastdatumlist[0].index(datefieldname)
    datelist = []
    for datum in lastdatumlist[1:]:
        date = datum[dateindex]
        datelist.append(date)

    for date in datelist:
        outstring = date
        for filedate in keyiterable:
            currentfile = indict[filedate]
            dateindex = currentfile[0].index(datefieldname)
            targetindex = currentfile[0].index(targetfieldname)
            i = 1
            while i > 0:
                testdatum = currentfile[i]
                testdate = testdatum[dateindex]
                if testdate == date:
                    target = str(testdatum[targetindex])
                    i = -1
                else:
                    i+=1
                    if i >= len(currentfile):
                        i = -1
                        target = ""
            outstring += delimiter + target
        print(outstring,file=outfile)
            
    return;



### MAIN BODY ###


outdelimiter = "\t"
fileprefix = "case-hosp-death."
filesuffix = ".csv"
earliestmonth = 3
earliestday = 25
zerodate = "0301"

jsonfilename = "nyc-case-hosp-death.json"

validanswer = False
while not validanswer:
    lastdate = input ("What is the MMDD of the final file? ")
    if len(lastdate.strip())==4:
        try:
            lastmonth = int(lastdate[0:2])
            lastday = int(lastdate[2:4])
            if (lastday > 0) and (lastday <= days_in_month(lastmonth)):
                validanswer = True
        except:
            print("Invalid date...")


datadict = {}
for month in range(earliestmonth,lastmonth+1):
    if month == earliestmonth:
        startday = earliestday
    else:
        startday = 1
    if month == lastmonth:
        endday = lastday
    else:
        endday = days_in_month(month)
    for day in range (startday,endday+1):
        infix = two_digitify(month) + two_digitify(day)
        filename = fileprefix + infix + filesuffix
        try:
            infilepointer = open(filename,"rb")
            newdatalist = parse_file(infilepointer)
            datadict[infix] = newdatalist
            infilepointer.close()
        except:
            print("File problem on date",infix)

jsonfile = open(jsonfilename,"w")
dictjson = json.dumps(datadict)
print (dictjson, file=jsonfile)
jsonfile.close()

datelist = generate_datelist(zerodate,180)
fieldnamelist = ["DEATH_COUNT","HOSPITALIZED_CASE_COUNT","NEW_COVID_CASE_COUNT"]
for fieldname in fieldnamelist:
    print_tsv_to_file(datadict,fieldname)
