try:
    from common_libs import logger
    from common_libs import coroutines_threads
except:
    import logger
    import coroutines_threads

from pathlib import Path

logManager = logger.logManager
logManager()
threadManager = coroutines_threads.threadManager()

def read(path, file_name, file_extension):
    file_name = path+"/"+file_name+"."+file_extension
    Path("/"+path).mkdir(parents=True, exist_ok=True)
    try:
        file = open(file_name,"r")
        string=""
        for i in file:
            string=string+i.strip(" \t\n")
        file.close()
    except:
        string = ""
    if len(string) <= 1:
        return {}
    dictionary = decodeJson(string)
    logManager.Current.logInfo("file '"+file_name+"' read correctly")
    return dictionary

def decodeJson(json):
    return turnIntoDictionary(json)

def removeOuterChar(string,char):
    if char == "{":
        char_reversed = "}"
    elif char == "[":
        char_reversed = "]"
    else:
        char_reversed = char
    string = string.strip()
    last_char = len(string)-1
    changed = False
    if string[0]== char and string[last_char]== char_reversed:
        string = string.strip().removeprefix(char).removesuffix(char_reversed)
        changed = True
    return string, changed
        
def seperateString(string, seperateing_char):
    no_parenthesise = 0
    isString = False
    strings = []
    char_no=-1
    changed=False
    while len(string)>0:
        char_no+=1
        if char_no > len(string)-1:
            strings.append(string)
            string=""
            break
        if string[char_no] in ["{","[","("]:
            no_parenthesise+=1
        elif string[char_no] in ["}","]",")"]:
            no_parenthesise-=1
        elif string[char_no] == '"':
            if isString:
                isString = False
            else:
                isString = True
        elif string[char_no] == seperateing_char and no_parenthesise<=0 and not isString:
            strings.append(string[:char_no])
            string = string.removeprefix(string[:char_no]+seperateing_char)
            char_no=-1
            changed=True
    return strings, changed

def turnIntoDictionary(string):
    dictionary={}
    string, changed = removeOuterChar(string,"{")
    if not changed:
        string ,changed01 = removeOuterChar(string,"[")
    strings, changed2 = seperateString(string, ",")
    if changed == True:
        if changed2:
            for string2 in strings:
                dictionary.update(turnIntoDictionary(string2))
        else:
            strings2, changed3 = seperateString(strings[0], ":")
            dictionary[turnIntoDictionary(strings2[0])] = turnIntoDictionary(strings2[1])
    elif changed01 == True:
        array = []
        num = 250
        if len(strings) < num:
            for string in strings:
                array.append(turnIntoDictionary(string))
        else:
            results = []
            for index in range(0,1+(len(strings)//num)):
                results.append([])
                array.append([threadingTIDWrapper,results,index,strings[num*index:num*(index+1)]])
            threadManager.Current.holdForTasks(*array)
            array = []
            for result in results:
                array.extend(result)
        return tuple(array)
    elif changed == False and changed01 == False:
        strings2, changed3 = seperateString(strings[0], ":")
        if changed3:
            dictionary[turnIntoDictionary(strings2[0])] = turnIntoDictionary(strings2[1])
        else:
            string21, changed33 = removeOuterChar(strings2[0],'"')
            if changed33:
                return string21.strip()
            elif not changed33:
                if string21.isdecimal():
                    return int(string21.strip())
                else:
                    return string21
            return "Error"
    return dictionary

def threadingTIDWrapper(results,index,strings):
    for string in strings:
        results[index].append(turnIntoDictionary(string))
        

def write(path, file_name, file_extension, content, append = False):
    if append:
        dictionary = read(path,file_name,file_extension)
        if isinstance(content, (dict,list)):
            content.extend(dictionary)
    string = encodeJson(content)
    file = open(path+"/"+file_name+"."+file_extension,"w")
    file.write(string)
    file.close()
    logManager.Current.logInfo("file '"+file_name+"' writen correctly")

def encodeJson(dictionary):
    return turnIntoString(dictionary)
    
def turnIntoString(content):
    string = ""
    if isinstance(content, dict):
        string="{"
        for key in content.keys():
            string = string+turnIntoString(key)+':'+turnIntoString(content[key])+","
        string=string.strip().removesuffix(",")
        string=string+"}"
    elif isinstance(content, (list,tuple)):
        string="["
        for item in content:
            string=string+turnIntoString(item)+","
        string=string.strip().removesuffix(",")
        string=string+"]"
    elif isinstance(content, str):
        string='"'+content+'"'
    elif isinstance(content, (int,float)):
        string = str(content)
    else:
        string = repr(content)
    return string
