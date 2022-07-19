import os
from datetime import timedelta, date

filenames = []
filesInDir = os.listdir()

for i in filesInDir:
    if ".txt" in i:
        filenames.append(i)


print(filenames)


ping27 = "********* iCon Advanced Alarm Response *********"
ping40 = "********* Load Limit Status Threshold Response *********"

#not needed as of rn
valid_meter_ids = [1231234]

#Data Headings
data_headings_ping27 = "Date,TOI,Flexnet ID,PHS A Voltage,PHS A Current,Meterology Temp, Current E1 Reading,Meter Warnings"
data_headings_ping40 = "Date,TOI,Flexnet ID,TAO Threshold,Temp Delta Hot Socket Detect,Reduced Threshold Value,Temp Slope,Flexnet Temp,Metro Temp PHA"

#functions
def main(name):

    filedata = import_file(name)
    data_group_ping27 = group_data(filedata,ping27)
    data_group_ping40 = group_data(filedata,ping40)
    ping27_filtered = ping27_filter(data_group_ping27,name)
    ping40_filtered = ping40_filter(data_group_ping40,name)

    write_to_csv(ping27_filtered,ping40_filtered,name)

def import_file(name_of_file):
    """
    Reads datafiles to lines and strips all whitespace
    filename: string contaning the name of the datafile for filtering
    Returns: List of Lines of a File stripped of all whitespace
    """

    f = open(name_of_file,"r")
    filelist = []
    for line in f:
        line = line.strip()
        filelist.append(line)
    f.close()
    return filelist

def group_data(file_as_list,ping_type):
    """
    file_as_list: file as a list of lines
    ping_type: string containing the line only a valid ping would carry  ex: ********* iCon Advanced Alarm Response *********
    return: list of relevant meter queries which are made up of lines in the list
    """
    acceptable_requests = []
    tmplist = []
    flag = False
    for i in range(len(file_as_list)):
        if ("TOI" in file_as_list[i]) and (file_as_list[i+3] == ping_type):
            flag = True

        if file_as_list[i] == "" and (flag == True):
            flag = False
            acceptable_requests.append(tmplist)
            tmplist = []
            
        if flag == True:
            tmplist.append(file_as_list[i])
            
    return acceptable_requests

def ping27_filter(data,name):
    """ 
    filters data from a ********* iCon Advanced Alarm Response ********* (ping 27) request
    data: List of the lines in a valid request (output from group_data)
    return: only the relevant numbers in the request
    """
    date_object = Pull_date(name)
    previous_time = "AM" 

    export_list = []
    for i in data:
        #updates date when time switchs to am
        TOI = i[1][3:14].strip()
        if TOI[-2:] == "AM" and previous_time == "PM":
            date_object = date_object+timedelta(days=1)
        previous_time = TOI[-2:]

        #pulls data from the file
        tmp = []
        tmp.append(date_object.strftime("%m/%d/%Y")+",")#Date
        tmp.append(i[1][3:14]+",".strip())              #TOI
        tmp.append(i[1][17:25]+",")                     #Flexnet ID
        tmp.append(i[8][0:6].strip()+",")               #PHS A Voltage
        tmp.append(i[9][0:7].strip()+",")               #PHS A current
        tmp.append(pull_nums(i[11])+",")                #Meterology Temperature
        tmp.append(pull_nums(i[12])+",")                #Current E1 Reading
        tmp.append(i[16][-6:]+",")                      #Meter Warnings
        export_list.append(tmp)
    return export_list

def ping40_filter(data,name):
    date_object_40 = Pull_date(name)
    previous_time = "AM" 
    export_list = []

    for i in data:
        #updates date when time switchs to am
        TOI = i[1][3:14].strip()
        if TOI[-2:] == "AM" and previous_time == "PM":
            date_object_40 = date_object_40+timedelta(days=1)
        previous_time = TOI[-2:]

        tmp = []
        tmp.append(date_object_40.strftime("%m/%d/%Y")+",") #Date
        tmp.append(TOI + ",")                  #TOI
        tmp.append(i[1][17:25]+",")                         #Flexnet ID
        tmp.append(pull_nums(i[11])+",")                    #TAO threshhold
        tmp.append(pull_nums(i[12])+",")                    #Temp Delta Hot Socket Detect
        tmp.append(pull_nums(i[13])+" "+i[13][-10:]+",")    #Reduced Threshold Value
        tmp.append(pull_nums(i[14])+",")                    #Temperature Slope
        tmp.append(pull_nums(i[19])+",")                    #Flexnet Temp
        tmp.append(pull_nums(i[20])+",")                    #MetroTemp PHA
        export_list.append(tmp)
    return export_list

def write_to_csv(pingX,pingY,theName):
    """
    Writes data to a csv file
    list_of_lists: list conaining lists each with a single line of data
    Post-conditions: CSV with data from the lists is created
    """
    f = open(theName[0:-4]+"_output.csv","w")

    if pingX is not None:
        f.write(data_headings_ping27)
        f.write("\n")
        for i in pingX:
            for j in i:
                f.write(j)
            f.write("\n")
    
    if pingY is not None:
        f.write(data_headings_ping40)
        f.write("\n")
        for i in pingY:
            for j in i:
                f.write(j)
            f.write("\n")
    f.close()

def pull_nums(string):
    """
    Pulls numbers from a string (has been updated to also grab any decimals or negaive signs)
    String: a string possibly complaning numbers
    Return: int comprised of numbers in the string
    """
    returnvalue = ""
    for i in string:
        if i.isdigit() or i == "." or i == "-":
            returnvalue = returnvalue+i
    return returnvalue
    
def Pull_date(name_of_file):
    """
    inputs: name of file to be filtered 
    ex: Batch_ResponseStream_05-04-2022_103124
    return: Starting date of data collection
    """
    date_string = name_of_file[21:31]
    month = int(date_string[0:2])
    day = int(date_string[3:5])
    year = int(date_string[-4:])
    date_obj_to_return = date(year,month,day)
    return date_obj_to_return

for i in filenames:
    main(i)