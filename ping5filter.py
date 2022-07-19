import os
import time
from datetime import timedelta, date

filenames = []
filesInDir = os.listdir()

for i in filesInDir:
    if ("Response" in i) and (".txt" in i):
        filenames.append(i)

valid_request = "********* C&I Meter Alarm *********"
#not needed as of rn
valid_meter_ids = [1231234]

#Data Headings
data_headings = "Date,TOI,Flexnet ID,Alarm,Temp (C),Reading,High Temp,Over Current"
#functions
def main(name):
    global date_object

    date_object = Pull_date(name)
    filedata = import_file(name)
    data_group = group_data(filedata)
    filtered = sfilter(data_group)
    write_to_csv(filtered,name)

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

def group_data(file_as_list):
    """
    file_as_list: file as a list of lines
    return: list of relevant queries which are made up of lines in the list
    """
    acceptable_requests = []
    tmplist = []
    flag = False
    for i in range(len(file_as_list)):
        try:
            if ("TOI" in file_as_list[i]) and (file_as_list[i+3] == valid_request):
                flag = True

            if file_as_list[i] == "" and (flag == True):
                flag = False
                acceptable_requests.append(tmplist)
                tmplist = []
                
            if flag == True:
                tmplist.append(file_as_list[i])
        except:
            print("Error: Partial Ping Detected ")    
    return acceptable_requests

def sfilter(data):
    global date_object
    export_list = []
    previous_time = "AM"

    for i in data:
        tmp = []
        TOI = i[1][3:14].strip()
        if TOI[-2:] == "AM" and previous_time == "PM":
            date_object = date_object+timedelta(days=1)

        previous_time = TOI[-2:]    
        date_to_export = date_object.strftime("%m/%d/%Y")
        #Date
        tmp.append(date_to_export+",")
        #Time
        tmp.append(TOI+",")
        #Flexnet ID
        tmp.append(i[1][17:25].strip()+",")
        #Alarm
        tmp.append(i[4][42:50].strip()+",")
        #Temp
        given_temp = int(pull_nums(i[5][42:47]))
        
        if given_temp > 127:
            given_temp = given_temp - 256

        tmp.append(str(given_temp)+",")
        #Reading
        tmp.append(pull_nums(i[7][-17:])+",")
        #High Temp
        tmp.append(i[8][12]+",")
        #Overcurrent
        tmp.append(i[10][-1]+",")
        
        export_list.append(tmp)

    return export_list
def write_file_text(list_of_lists):
    f = open(filename[0:-4]+"_output.txt","w")
    f.write("\n")
    for i in list_of_lists:
        f.write("\n")
        for j in i:
            f.write(j)
            f.write("\n")
    f.close()

def write_to_csv(list_of_lists,theName):
    f = open(theName[0:-4]+"_output.csv","w")
    f.write(data_headings)
    f.write("\n")
    for i in list_of_lists:
        for j in i:
            f.write(j)
        f.write("\n")
    f.close()

def pull_nums(string):
    """
    Pulls numbers from a string
    Return: int comprised of numbers in the string
    """
    returnvalue = ""
    for i in string:
        if i.isdigit() or i == ".":
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
    
time.sleep(5)