import os
import matplotlib as mpl

####################################################
#User Options 
####################################################

# 1 to output a single csv or 0 an individual csv for eatch batch files
output = 1

#Output png Graphs 1 = yes 0 = no
graphs = 0

###################################################
#Main Code Below
###################################################

# Variables
valid_request = "********* Load Limit Status Threshold Response *********"

valid_meter_ids = [1231234]

data_headings = "TOI,Flexnet ID, TAO Threshold,Temp Delta Hot Socket Detect,Reduced Threshold Value,Temp Slope,Flexnet Temp,Metro Temp PHA,Metro Temp PHC"


#functions
def gather_txt_filenames():
    """Gathers the names of all the text files in the current directory
        Return: List of filenames"""
    filenames = []
    filesInDir = os.listdir()
    for i in filesInDir:
        if ".txt" in i:
            filenames.append(i)

def main(names):
    """Calls all functions to output parsed data as a CSV"""
    for name in names:
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
        if ("TOI" in file_as_list[i]) and (file_as_list[i+3] == valid_request):
            flag = True

        if file_as_list[i] == "" and (flag == True):
            flag = False
            acceptable_requests.append(tmplist)
            tmplist = []
            
        if flag == True:
            tmplist.append(file_as_list[i])
            
    return acceptable_requests

def sfilter(data):
    export_list = []
    for i in data:
        tmp = []
        tmp.append(i[1][3:14]+",".strip())
        tmp.append(i[1][17:25]+",")
        tmp.append(pull_nums(i[11])+",")
        tmp.append(pull_nums(i[12])+",")
        tmp.append(pull_nums(i[13])+" "+i[13][-10:]+",")
        tmp.append(pull_nums(i[14])+",")
        tmp.append(pull_nums(i[19])+",")
        tmp.append(pull_nums(i[20])+",")
        tmp.append(pull_nums(i[21])+",")
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
        if i.isdigit():
            returnvalue = returnvalue+i
    return returnvalue

def prep_data_for_graph(filted_data):
    meter_numbers = []
    export = []
    for i in filtered_data:
        if i[1] not in meter_numbers:
            meter_numbers.append(i)

    for i in meter_numbers:
        l = []
        for j in filted_data:
            single_point = []
            if j[1] == i:
                single_point.append([i[0],i[1],i[-2],i[-1]])
                l.append(single_point)
        export.append(l)
    return export
def graph_data(graphable_data):
    
main(gather_txt_filenames())