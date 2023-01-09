import os
import tarfile
import shutil
import re
import copy
import sys
import argparse

sys.path.append(os.path.join(sys.path[0],'log_messenger'))
from pyScriptLogger import logMessage

"""
print(len(sys.argv))

print(sys.argv)


# Create a parser object
parser = argparse.ArgumentParser()

# Add a required argument
parser.add_argument("input_file", help="The input file to process")

# Add an optional argument with a default value
parser.add_argument("--output_file", default="output.txt", help="The output file (default: output.txt)")

# Parse the command line arguments
args = parser.parse_args()

# Access the values of the arguments
input_file = args.input_file
output_file = args.output_file

# Print the values of the arguments
print(f"Input file: {input_file}")
print(f"Output file: {output_file}")
"""

scaapp_keywords = ['START_INDICATOR']
date_pattern = "^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$"

def extract_target_file(filename):
    print(f"extracting file {filename}!")

    if not os.path.exists('temp//'):
        os.makedirs('temp//')

    tempFileName = "./temp/" + filename.split('\\')[-1]
    shutil.copyfile(filename, tempFileName)
    print(f"file {filename} copied to temp location!")

    tgz_in_fhandle = tarfile.open(tempFileName, "r:gz")
    tgz_in_fhandle.list(verbose=True)
    tgz_in_fhandle.extractall('temp//')
    tgz_in_fhandle.close()
    print(f"extraction done for {filename}!")

def get_scaapplog_details():
    tempdict = {}
    for root, dirs, files in os.walk(".\\temp" +'\\'):
        for file in files:
            # print(f"{file}")
            # print(f"{root} + {file}")
            if file.strip().startswith('scaapp') and file.strip().endswith('.log'):
                with open(os.path.join(root, file)) as logfile:
                    """
                    logfilestring = logfile.read()
                    if re.search('|'.join(['\\b'+item+'\\b' for item in scaapp_keywords]),logfilestring):
                        print("",re.finditer('|'.join(['\\b'+item+'\\b' for item in scaapp_keywords]),logfilestring))
                        for m in re.finditer('|'.join(['\\b'+item+'\\b' for item in scaapp_keywords]),logfilestring):
                            print("occurances found at ", m.start(), m.end())
                    """

                    for line in logfile:
                        for item in scaapp_keywords:
                            if item in line:
                                if line.split()[0] in tempdict.keys():
                                    tempdict[line.split()[0]].append(line.split()[1])
                                else:
                                    print(line.index("/"))
                                    if re.match(date_pattern, line.split()[0]):
                                        tempdict[line.split()[0]] = [line.split()[1]]
                                    else:
                                        if (line.split()[0])[line.split()[0].index("/")-2:] in tempdict.keys():
                                            tempdict[(line.split()[0])[line.split()[0].index("/")-2:]].append(line.split()[1])
                                        else:
                                            tempdict[(line.split()[0])[line.split()[0].index("/")-2:], line.split()[1]]
                                
                                print(line.split()[0], line.split()[1])
                    print(tempdict)


def get_debuglog_details():
    pass


def main():

    # Create custome logger object.
    loggerObject = logMessage(__name__)

    # Create a parser object
    parser = argparse.ArgumentParser()

    # Add a required argument
    parser.add_argument("input_file", help="The input file to process")

    # Add an optional argument
    parser.add_argument("--optional", help="Selective Debug funtion to process", required=False, action='store_true')

    # Parse the command line arguments
    args = parser.parse_args()

    # Access the values of the arguments
    input_file = args.input_file
    optional_flag = args.optional

    # print(f"optional flag value is {optional_flag}")

    loggerObject.logger.info(f"optional flag value is {optional_flag}")

    print(f"the input file name is: {input_file}")

    if not optional_flag:
        if os.path.exists(input_file) and input_file.strip().endswith(('.tgz','.tar','.tgx')):
            extract_target_file(input_file)
            get_scaapplog_details()
            get_debuglog_details()
        else:
            print("extraction is not done!")
    else:
        get_scaapplog_details()

if __name__ == '__main__':
    main()