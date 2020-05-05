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
    if inheader == "DIAGNOSIS_DATE": # Early datasets
        outheader = "DATE_OF_INTEREST"
    elif "retrieving" in inheader.lower(): #"Retrieving data..." 4/15 dataset
        outheader = "DATE_OF_INTEREST"
    elif inheader.upper()=="DATE_OF_DEATH":
        outheader = "DATE_OF_INTEREST"
    elif inheader.upper() == "PROBABLE_COUNT":
        outheader = "PROBABLE_DEATHS"
    elif inheader.upper() == "HOSPITALIZED_COUNT":
        outheader = "HOSPITALIZED_CASE_COUNT"
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
def parse_deathsfile(infileptr):
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

def kill_badchars(instring):
    badcharlist = ['*',':',' ']
    outstring = instring
    for badchar in badcharlist:
        outstring = outstring.replace(badchar,"")
    return outstring;

##
# PROCEDURE parse_summaryfile
# IN: file pointer to DOHMH "summary.csv" file, (delimiter)
# OUT: dictionary containing the header (key) and datum (value)
#
def parse_summaryfile(infileptr):
    outlist = []
    datadict = {}
    tableheadstring = "<thead>"
    headsplit = "<th>"
    tablebodyindicator = "<tbody>"
    tablebodyendindicator = "<\tbody>"
    datasplit = "<td>"
    wholepage = infilepointer.read().decode('utf-8',errors='ignore')
    headstartindex = wholepage.find(tableheadstring)
    if len(tableheadstring) > -1:
        trimmedpage = wholepage[headstartindex:]
    else:
        trimmedpage = ""
        print("Trim error...")
    headsplitlist = trimmedpage.split(headsplit)
    newrawheader = headsplitlist[1]
    endindex =newrawheader.find("<")
    newheader = "summary_"+kill_badchars(newrawheader[:endindex]).lower()
    newrawdatum = headsplitlist[2]
    endindex =newrawdatum.find("<")    
    newdatum = kill_badchars(newrawdatum[:endindex]).lower()
    datadict[newheader] = newdatum
    bodystart = trimmedpage.find(tablebodyindicator)
    bodyend = trimmedpage.find(tablebodyendindicator)
    trimmedpage = trimmedpage[bodystart:bodyend]
    datasplitlist = trimmedpage.split(datasplit)
    numfields = int((len(datasplitlist) - 1)/2)
    for i in range (0,numfields):
        headerindex = i*2 + 1
        datumindex = i*2 + 2
        newrawheader = datasplitlist[headerindex]
        newrawdatum = datasplitlist[datumindex]
        endindex =newrawheader.find("<")
        newheader = "summary_"+kill_badchars(newrawheader[:endindex]).lower()
        endindex =newrawdatum.find("<")
        newdatum = kill_badchars(newrawdatum[:endindex]).lower()
        datadict[newheader]=newdatum
        
    
#    rawheaderlist = trimmedpage.split(headsplit)
#    for i in range(1,len(rawheaderlist)):
#        rawheader = rawheaderlist[i]
#        endbracketindex = rawheader.find("<")
#        header = rawheader[:endbracketindex]
#        headerlist.append(rectify_header(header))
#    outlist.append(headerlist)
#
#    tablebodyindex = trimmedpage.find(tablebodyindicator)
#    trimmedpage = trimmedpage[tablebodyindex:]
#    rawentrylist = trimmedpage.split(entrysplit)
#    for i in range(1,len(rawentrylist)):
#        rawentry = rawentrylist[i]
#        rawdatalist = rawentry.split(datasplit)
#        datalist = []
#        for j in range (1, len(rawdatalist)):
#            rawdatum = rawdatalist[j]
#            endbracketindex = rawdatum.find("<")
#            datum = rawdatum[:endbracketindex]
#            datalist.append(datum)
#        outlist.append(rectify_datalist(datalist))        
    return datadict;


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
            if targetfieldname in currentfile[0]:
                targetindex = currentfile[0].index(targetfieldname)
            else:
                targetindex = -1
            i = 1
            while i > 0:
                testdatum = currentfile[i]
                testdate = testdatum[dateindex]
                if testdate == date:
                    if (targetindex > -1) and (targetindex < len(testdatum)):
                        target = str(testdatum[targetindex])
                    else:
                        target = "0"
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


delimiter = "\t"
deathsfileprefix = "case-hosp-death."
probsfileprefix = "probable-confirmed-dod."
summaryfileprefix = "summary."
filesuffix = ".csv"
earliestmonth = 3
earliestday = 25
zerodate = "0301"
datefield = "DATE_OF_INTEREST"

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
summarydict = {}
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
        deathsfilename = deathsfileprefix + infix + filesuffix
        try:
            infilepointer = open(deathsfilename,"rb")
            newdatalist = parse_deathsfile(infilepointer)
            datadict[infix] = newdatalist
            infilepointer.close()
        except:
            print("Deaths file problem on date",infix)
        summaryfilename = summaryfileprefix + infix + filesuffix
        if (month > 4) or ((month == 4) and (day >= 15)): #when summary files became available
            try:
                infilepointer = open(summaryfilename,"rb")
                newdatadict = parse_summaryfile(infilepointer)
                summarydict[infix] = newdatadict
                infilepointer.close()
            except:
                print("Summary file problem on date",infix)
        probsfilename = probsfileprefix + infix + filesuffix
        if (month > 4) or ((month == 4) and (day >= 19)): #when probs files became available
            try:
                infilepointer = open(probsfilename,"rb")
                newdatalist = parse_deathsfile(infilepointer)
                newheaderlist = newdatalist[0]
                newdateindex = newheaderlist.index(datefield)
                olddatalist = datadict[infix]
                oldheaderlist = olddatalist[0]
                olddateindex = oldheaderlist.index(datefield)
                numnewheaders = 0
                for rawheader in newheaderlist:
                    header = rectify_header(rawheader)
                    if header not in oldheaderlist:
                        numnewheaders+=1
                for i in range(1,len(newdatalist)):
                    datum = newdatalist[i]
                    counter = 1
                    while olddatalist[counter][olddateindex] != datum[newdateindex]:
                        counter+=1
                    for j in range (0,len(datum)):
                        if rectify_header(newheaderlist[j]) not in oldheaderlist:
                            olddatalist[counter].append(datum[j])
                for rawheader in newheaderlist:
                    header = rectify_header(rawheader)
                    if header not in oldheaderlist:
                        olddatalist[0].append(header)
                datadict[infix] = olddatalist
                infilepointer.close()
            except:
                print("Probables file problem on date",infix)

for date in datadict.keys(): #pad short lists appropriately
    datalist = datadict[date]
    headerlist = datalist[0]
    headerlength = len(headerlist)
    for i in range(1,len(datalist)):
        datum = datalist[i]
        if len(datum) != len(headerlist):
            delta = len(headerlist) - len(datum)
            for k in range(0,delta):
                datum.append(0)
#            datalist[k]=datum
#    datadict[date] = datalist
    
    

jsonfile = open(jsonfilename,"w")
dictjson = json.dumps(datadict)
print (dictjson, file=jsonfile)
jsonfile.close()

datelist = generate_datelist(zerodate,180)
fieldnamelist = ["DEATH_COUNT","HOSPITALIZED_CASE_COUNT","NEW_COVID_CASE_COUNT","PROBABLE_DEATHS"]
for fieldname in fieldnamelist:
    print_tsv_to_file(datadict,fieldname)

summaryvaluefilename = "summaryvalues.tsv"
summaryvaluefile = open(summaryvaluefilename,"w")
headerlist = []
for date in summarydict.keys(): #get all headers
    datadict = summarydict[date]
    for rawheader in datadict.keys():
        header = rectify_header(rawheader)
        if header not in headerlist:
            headerlist.append(header)
print ('summary_date'+delimiter+delimiter.join(headerlist),file=summaryvaluefile) #print headers to file
for date in summarydict.keys():
    outstring = date
    datadict = summarydict[date]
    for header in headerlist:
        outstring += delimiter
        if header in datadict.keys():
            outstring += datadict[header]
    print (outstring,file=summaryvaluefile)

