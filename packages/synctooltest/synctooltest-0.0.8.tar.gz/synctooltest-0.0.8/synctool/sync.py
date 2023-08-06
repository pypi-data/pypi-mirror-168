# Script to download images and text files to local machine and generate path file
import requests
import os
import sys
from multiprocessing.pool import ThreadPool
import base64


# IP+port or url of the server # (eg: https://qa.deepzea.com)
serverUrl = 'http://localhost:8080' # default

failedDownloadsPresent = False

# get variables from cmd
cmd_args = sys.argv

if(len(cmd_args)!=6):
    print(f"Required 5 arguments but recived {len(cmd_args)-1}")
    print("arguments: <url> <version ID> <format type> <api key> <secret>")
    quit()

# get server url
serverUrl = cmd_args[1]

# get dataset url data from server
baseUrl = f'{serverUrl}/api/datasetVersion/getVersionData/' 

versionId = cmd_args[2]
callUrl = baseUrl + versionId + '/'

exportType = cmd_args[3]
callUrl = callUrl + exportType

api_key = cmd_args[4]
secret = cmd_args[5]   

# method to get item URL list from layerX (per page)
# # @params - callUrl=(Url to get itemlist of given group and version from layerx), payload=(pageNo,pageSize)
# @returns - response=(response from layerX containing URL list) 
def getDataFromServer(callUrl, payload):
    # Get the url list of dataset items from node backend
    string_key_secret = f'{api_key}:{secret}'
    key_secret_bytes = string_key_secret.encode("ascii")
    encoded_key_secret_bytes = base64.b64encode(key_secret_bytes)
    encoded_key_secret = encoded_key_secret_bytes.decode("ascii")

    hed = {'Authorization': 'Basic ' + encoded_key_secret}

    print(hed)
    try:
        callResponse = requests.get(callUrl, params=payload, headers=hed, timeout=10)
    except:
        print(f'Error connecting to layerx')
        print("We are facing a problem with the network, please retry to download missing items")
        quit()
    response = callResponse.json()
    return response

# method to get item URL list from layerX (per page)
# # @params - callUrl=(Url to get itemlist of given group and version from layerx), payload=(pageNo,pageSize)
# @returns - response=(response from layerX containing URL list) 
def getDataFromServerTemp(callUrl, payload):
    # Get the url list of dataset items from node backend
    string_key_secret = f'{api_key}:{secret}'
    key_secret_bytes = string_key_secret.encode("ascii")
    encoded_key_secret_bytes = base64.b64encode(key_secret_bytes)
    encoded_key_secret = encoded_key_secret_bytes.decode("ascii")

    hed = {'Authorization': 'Basic ' + encoded_key_secret}

    print(hed)
    try:
        callResponse = requests.get(callUrl, params=payload, headers=hed, timeout=10)
    except:
        print(f'Error connecting to layerx')
        print("We are facing a problem with the network, please retry to download missing items")
        quit()
    response = callResponse.json()
    return response

# Method to download files
# @params: fileData=(data including url of file), downloadLocation=(file path to save downloaded file)
def downloadFile(fileData, downloadLocation):
    # download files from newly added paths
    # print('Downloading file '+fileData["fileName"])
    r = requests.get(fileData["fileUrl"], timeout=25)
    downloadPath = downloadLocation
    # print(downloadLocation)
    with open(downloadPath, 'wb') as f:
        f.write(r.content)

# handle download for a single dataset item (image and textfile)
# @params: arg_list=[fileData=(data of file), identifier=(unique identifier name for the dataset version)]
# @returns: {False<when download failed>, arg_list<from params>}
#       or  {
#               True<when download success>, 
#               {textFileImagePathData={imagePath=(file path of downloaded item), pathFileName=("training path file" name - stores paths of downloaded images used for training)}}
#           }
def handleOneDownload(arg_list):
    fileData = arg_list[0]
    # print(fileData)
    identifier = arg_list[1]
    # ---------------------

    formattedWriteKey = fileData['fileName']
    # imagePath = os.path.abspath(f'./{dataDirectoryName}/'+ fileData['imageIdentifier'])
    filePath = f'{fileData["fileDownloadFolderLocation"]}/' + fileData['fileName']
    filePathAbsoulute = os.path.abspath(f'./{dataDirectoryName}/'+ filePath)

    if "writingPathFileName" in fileData:
        # write to a annotation file path list
        pathFileName = fileData["writingPathFileName"]
        textFileImagePathData = (filePathAbsoulute, pathFileName)
    else:
        textFileImagePathData = None
    
    if(not os.path.exists(filePathAbsoulute)):
        # download files
        try:
            if "fileUrl" in fileData:
                downloadFile(fileData, filePathAbsoulute) # download image
        except Exception as e:
            print(f'Failed downloading - {formattedWriteKey}') 
            return (False, arg_list)

        # If item is not available in the syncdatafile (file hasn't downloaded before)
        print('Downloded item - '+ formattedWriteKey)

        # return fileName and textFileName to update the textfile
        return (True,  textFileImagePathData)

    else:
        print('Item already exists, OK ', fileData['fileName'] ) 
        return (True, textFileImagePathData)


# main method to download items and update datafiles
# @params: dataList=(response from layerX containing URL list)
def downloadPage(dataList):
    
    global failedDownloadsPresent

    arg_list = []
    for val in dataList['resourceArray']:
        arg_list.append([val, dataList['identifier']])

    # Download items in parallel
    print("starting page download")
    with ThreadPool(10) as p:
        for res in p.imap(handleOneDownload, arg_list):
            isDownloded = res[0]
            downloadData = res[1]
            if not isDownloded:
                # try again to download the failed download
                print(f"Retrying Download - {downloadData[0]['fileName']}")
                res = handleOneDownload(downloadData)
                isDownloded = res[0]
                downloadData = res[1]

            if isDownloded:
                #if file is downloaded, write it to master csv
                textFileImagePathData = downloadData

                if textFileImagePathData is not None:
                    # write image file path to train text file
                    imagePath = textFileImagePathData[0]
                    pathFileName = textFileImagePathData[1]
                    textPathFileLocation = os.path.join(dataDirectoryName, pathFileName)
                    with open(textPathFileLocation, 'a+', newline='') as train_txt_file:
                        train_txt_file.write(imagePath + "\n")
                    p.close()
            else:
                print(f"Retrying Failed! - {downloadData[0]['fileName']}")
                failedDownloadsPresent = True
                p.close()

    print("page download done")
       
# Method to create required directories for file download
def initiateDownload(response, pageNo):
    print("data format: ",response['format'])

    global dataDirectoryName # folder to download image and text files
    dataDirectoryName = response['groupUniqueName'] # create a folder with dataset groupname
    dataDirectoryPath = f'./{dataDirectoryName}'

    if pageNo == 1:
        print('1st page')
        # create required files and directories
        if not os.path.exists(dataDirectoryPath):
            os.makedirs(dataDirectoryPath)
            print(f"Created {dataDirectoryName} folder")
        
    # create required directories
    for directory in response["creatableDirectories"]:
        dirPath = os.path.join(dataDirectoryPath, directory)
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
            print(f"Created folder - {dirPath}")

    # updateVersionData(response)
    downloadPage(response)

# method to get url list from server and execute the main script for all pages
# @params - callUrl (Url to get itemlist of given group and version from layerx), pageNo
def getAllPages(callUrl, pageNo):
    payload = {'pageNo': pageNo, 'pageSize': 250}
    response = getDataFromServer(callUrl, payload)
    print('Downloading page no: '+ str(pageNo))
    if "identifier" in response:
        
        # Direct the response to download files
        initiateDownload(response, pageNo)

        # recursively call this again to get next page
        if(response['nextPage']==True):
            nextPageNo = int(pageNo)+1
            getAllPages(callUrl, nextPageNo)
        print("Download Complete")
        if failedDownloadsPresent:
            print("Unfortunately we failed to download everything, please retry to download missing items")
        quit()
    else:
        print("No data recieved from remote for given group and/or version")
        
# main script below
def main():
    # start operation
    getAllPages(callUrl, 1)

# run main method
main()
# ---------------


# sample run command:
# python3 sync.py <url> <version ID> <format type> <access token>