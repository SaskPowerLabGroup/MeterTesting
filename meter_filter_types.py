from datetime import timedelta, date
#Ping27
def ping27_filter(data,name):
    """ 
    filters data from a ********* iCon Advanced Alarm Response ********* (ping 27) request
    data: List of the lines in a valid request (output from group_data)
    return: only the relevant numbers in the request
    """
    date_object = Pull_date(name)
    previous_time = "AM" 

    export_list = [["Date,","TOI,","Flexnet ID,","PHS A Voltage,","PHS A Current,","Meterology Temp,", "Current E1 Reading,","Meter Warnings,"]]
    for i in data:
        #updates date when time switchs to am
        TOI = i[1][3:14].strip()
        if TOI[-2:] == "AM" and previous_time == "PM":
            date_object = date_object+timedelta(days=1)
        previous_time = TOI[-2:]

        #pulls data from the file
        tmp = []
        tmp.append(date_object.strftime("%m/%d/%Y")+",")#Date
        tmp.append(TOI+",")              #TOI
        tmp.append(i[1][17:25]+",")                     #Flexnet ID
        tmp.append(i[8][0:6].strip()+",")               #PHS A Voltage
        tmp.append(i[9][0:7].strip()+",")               #PHS A current
        tmp.append(pull_nums(i[11])+",")                #Meterology Temperature
        tmp.append(pull_nums(i[12])+",")                #Current E1 Reading
        tmp.append(i[16][-6:]+",")                      #Meter Warnings
        export_list.append(tmp)
    return export_list

#Ping40
def ping40_filter_PHS_A(data,name):
    """ 
    filters data from a ********* Load Limit Status Threshold Response ********* (ping 40) request
    data: List of the lines in a valid request (output from group_data)
    return: only the relevant numbers in the request
    """
    date_object = Pull_date(name)
    previous_time = "AM" 
    export_list = [["Date,","TOI,","Flexnet ID,","TAO Threshold,","Temp Delta Hot Socket Detect,","Reduced Threshold Value,","Temp Slope,","Flexnet Temp,","Metro Temp PHA,"]]

    for i in data:
        #updates date when time switchs to am
        TOI = i[1][3:14].strip()
        if TOI[-2:] == "AM" and previous_time == "PM":
            date_object = date_object + timedelta(days=1)
        previous_time = TOI[-2:]

        tmp = []
        tmp.append(date_object.strftime("%m/%d/%Y")+",") #Date
        tmp.append(i[1][3:14]+",".strip())                  #TOI
        tmp.append(i[1][17:25]+",")                         #Flexnet ID
        tmp.append(pull_nums(i[11])+",")                    #TAO threshhold
        tmp.append(pull_nums(i[12])+",")                    #Temp Delta Hot Socket Detect
        tmp.append(pull_nums(i[13])+" "+i[13][-10:]+",")    #Reduced Threshold Value
        tmp.append(pull_nums(i[14])+",")                    #Temperature Slope
        tmp.append(pull_nums(i[19])+",")                    #Flexnet Temp
        tmp.append(pull_nums(i[20])+",")                    #MetroTemp PHA
        export_list.append(tmp)
    return export_list

#Ping 5
def ping5_filter(data,name):
    date_object = Pull_date(name)
    export_list = [["Date","TOI","Flexnet ID","Alarm","Temp (C)","Reading","High Temp","Over Current"]]
    previous_time = "AM"

    for i in data:
        tmp = []
        TOI = i[1][3:14].strip()
        if TOI[-2:] == "AM" and previous_time == "PM":
            date_object = date_object+timedelta(days=1)

        previous_time = TOI[-2:]    

        tmp.append(date_object.strftime("%m/%d/%Y")+",")    #Date                    
        tmp.append(TOI+",")                                 #Time
        tmp.append(i[1][17:25].strip()+",")                 #Flexnet ID
        tmp.append(i[4][42:50].strip()+",")                 #Alarm

        #Getting error interpreting -1 as 255 this more or less fixes it
        given_temp = int(pull_nums(i[5][42:47]))            
        if given_temp > 127:
            given_temp = given_temp - 256

        tmp.append(str(given_temp)+",")                     #Temp
        tmp.append(pull_nums(i[7][-17:])+",")               #Reading
        tmp.append(i[8][12]+",")                            #High Temp
        tmp.append(i[10][-1]+",")                           #Overcurrent
        
        export_list.append(tmp)



#git test
















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
