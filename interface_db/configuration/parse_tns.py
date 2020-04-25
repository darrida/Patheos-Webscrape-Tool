# coding: utf-8
#########################################################
# SETUP (since I don't have a setup.py file):
# (1) Place parse_tns.py into %python%\Lib\site-packages\
# (2) Load with "import parse_tns" or "import parse_tns as pt"
#
# EXAMPLE USAGE: 
# (1) Declare variables for the SID of the server and the directory that contains tnsnames.ora
# (2) Pass variables into the parse_tnsnames() function. See the following three lines.
#
# SID = "PPRD"
# tnsnames_path = ""
# Call parse_tnsnames(tnsnames_path, SID)
#########################################################

import re

def parse_tnsnames(tnsnames_path, server):
    lines_tested = 0
    connection = ""
    try:
        tns_read = tnsnames_path + "tnsnames.ora"
        with open(tns_read, 'r') as f:
            for line in f:
                if line.startswith(server + " =") or line.startswith(server + "="):
                    counter = 0
                    search_line = line
                    while counter < 7:
                #SEARCH FOR HOSTNAME
                        #print(str(counter) + ":" + search_line)
                        if re.match(".*HOST = ", search_line):
                            host = search_line.split('HOST = ')[1]
                            host = host.split(')')[0]
                        elif re.match(".*HOST=", search_line):
                            host = search_line.split('HOST=')[1]
                            host = host.split(')')[0]
                #SEARCH FOR PORT
                        if re.match(".*PORT = ", search_line):
                            port = search_line.split('PORT = ')[1]
                            port = port.split(')')[0]
                        elif re.match(".*PORT=", search_line):
                            port = search_line.split('PORT=')[1]
                            port = port.split(')')[0]
                #SEARCH FOR SERVICENAME
                        if re.match(".*SERVICE_NAME = ", search_line):
                            service_name = search_line.split('SERVICE_NAME = ')[1]
                            service_name = service_name.split(')')[0]
                        elif re.match(".*SERVICE_NAME=", search_line):
                            service_name = search_line.split('SERVICE_NAME=')[1]
                            service_name = service_name.split(')')[0]

                        search_line = next(f)
                        counter += 1
                    connection = "@" + host + ":" + port + "/" + service_name
                    #return connection
                    
                else:
                    lines_tested += 1
            try:
                if connection != "":
                    return connection
                else:
                    raise NoServerError
            except NoServerError:
                print("EXCEPTION: " + str(lines_tested) + " lines were read, but specified SID "
                          + "not found in tnsnames.ora. Please check server name and tnsnames.ora path.")
                
    except FileNotFoundError:
        print("ERROR: Unable to find or open tnsnames.ora. Double check submitted path.")
    return connection

# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions."""
    pass

class NoServerError(Error):
    """Raised when SID is not found in tnsnames.ora file."""
    pass

class DuplicateEntriesError(Error):
    """Raised when SID is not unique."""
    pass

# USED FOR IN SCRIPT TESTING
#def main():
#    SID = "SERV1"
#    tnsnames_path = ""
#    print(parse_tnsnames(tnsnames_path, SID))
#main()

