import os
from datetime import timedelta, date
from meter_filter_types import *

#Grabs Batch files in Directory
filenames = []
filesInDir = os.listdir()

for i in filesInDir:
    if ("Response" in i) and (".txt" in i):
        filenames.append(i)




ping27 = "********* iCon Advanced Alarm Response *********"
ping40 = "********* Load Limit Status Threshold Response *********"

ping_types = [ping27,ping40]
ping_filter_functions = [ping27_filter,ping40_filter_PHS_A]

#functions
def main(name):
    filedata = import_file(name)

    data = []
    for i, value in enumerate(ping_types):
        data_group_ping = group_data(filedata,value)
        new_list = ping_filter_functions[i](data_group_ping,name)
        data.append(new_list)

    write_to_csv(data,name)

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

def write_to_csv(pings,theName):
    """
    Writes data to a csv file
    pings: list containing lists conaining lists each with a single line of data
    Post-conditions: CSV with data from the lists is created
    """
    f = open(theName[0:-4]+"_output.csv","w")
    for i in pings:
        #Triple nested loop whoops
        if i is not None:
            for j in i:
                for k in j:
                    f.write(k)
                f.write("\n")

    f.close()

for i in filenames:
    main(i)