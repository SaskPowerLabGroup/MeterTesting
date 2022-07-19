import os

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



filenames = []
filesInDir = os.listdir()

for i in filesInDir:
    if ".txt" in i:
        filenames.append(i)


print(filenames)


valid_request = "********* Load Limit Status Threshold Response *********"
#not needed as of rn
valid_meter_ids = [1231234]

#Data Headings
data_headings = "TOI,Flexnet ID, TAO Threshold,Temp Delta Hot Socket Detect,Reduced Threshold Value,Temp Slope,Flexnet Temp,Metro Temp PHA,Metro Temp PHC"
#functions
def main(name):
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

for i in filenames:
    main(i)