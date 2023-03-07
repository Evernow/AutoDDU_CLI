Version_of_AutoDDU_CLI = "0.2.0"
LICENSE = """
MIT License

Copyright (c) 2022-present Daniel Suarez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import traceback
import urllib.request
# import wexpect
import zipfile
from datetime import datetime, timezone, date
from subprocess import CREATE_NEW_CONSOLE

#import ntplib
import wmi
from win32com.shell import shell, shellcon
import winreg
import ctypes

from win32event import CreateMutex
from win32api import CloseHandle, GetLastError
from winerror import ERROR_ALREADY_EXISTS
import webbrowser
import psutil
import urllib.error
import posixpath
import codecs
from tqdm import tqdm
import packaging.version 
import multiprocessing
import win32com.client
import importlib.metadata
import dns.resolver
import tempfile 
import ssl
import xmltodict
import difflib    
import zlib
import socket
import struct


advanced_options_dict_global = {"disablewindowsupdatecheck": 0, "bypassgpureq": 0, "provideowngpuurl": [],
                                "disabletimecheck": 0, # Kept here even though it does nothing. This is for backwards compatibility reason
                                # For example lets say someone runs latest version but it has a problem, then they're told to try an old version,
                                # if it's old enough it will expect this to be in config, and it will fail if it isn't, even though there was
                                # never a public AutoDDU release that actually did something with this variable.
                                "RemovePhysX": 0, "disableinternetturnoff": 0, "donotdisableoverclocks": 0,
                                "disabledadapters": [], "avoidspacecheck": 0, "amdenterprise" : 0,
                                "nvidiastudio" : 0, "startedinsafemode" : 0, "inteldriverassistant" : 0,
                                "dnsoverwrite" : 0, "pciidsfallback" : 0, 'changegpumode':0} # ONLY USE FOR INITIALIZATION IF PERSISTENTFILE IS TO 0. NEVER FOR CHECKING IF IT HAS CHANGED.

clear = lambda: os.system('cls')

Appdata = shell.SHGetFolderPath(0, shellcon.CSIDL_COMMON_APPDATA, 0, 0)
Appdata_AutoDDU_CLI = os.path.join(Appdata, "AutoDDU_CLI")
Persistent_File_location = os.path.join(Appdata, "AutoDDU_CLI", "PersistentDDU_Log.txt")
root_for_ddu_assembly = os.path.join(Appdata, "AutoDDU_CLI", "DDU_Parser")
ddu_AssemblyInfo = os.path.join(Appdata, "AutoDDU_CLI", "DDU_Parser\\", "AssemblyInfo.vb")
ddu_zip_path = os.path.join(Appdata, "AutoDDU_CLI", "DDU_Parser\\", "DDU.exe")
ddu_extracted_path = os.path.join(Appdata, "AutoDDU_CLI", "DDU_Extracted")
Users_directory = os.path.dirname(shell.SHGetFolderPath(0, shellcon.CSIDL_PROFILE, 0, 0))

exe_location = os.path.join(Appdata_AutoDDU_CLI, "AutoDDU_CLI.exe")

Script_Location_For_startup = os.path.join(Appdata_AutoDDU_CLI ,"AutoDDU_CLI.lnk")

log_file_location = os.path.join(Appdata_AutoDDU_CLI, "AutoDDU_LOG.txt")
PROGRAM_FILESX86 = shell.SHGetFolderPath(0, shellcon.CSIDL_PROGRAM_FILESX86, 0, 0)

Jsoninfofileslocation = os.path.join(Appdata_AutoDDU_CLI, "JsonInfoFiles")

EOL_NVIDIA = ['NV1', 'NV3', 'NV4', 'NV5', 'MCP04', 'NV40', 'NV40GL', 'CK804', 'nForce2', 'nForce', 'MCP2A', 'MCP2S', 'G70', 'G70M', 'G70GL', 'NV0A', 
    'NV41', 'NV41M', 'NV41GLM', 'NV42GL', 'NV41GL', 'nForce3', 'CK8S', 'NV43', 'G70/G71', 'NV45GL', 'NV39', 'NV35', 'NV37GL', 'NV38GL', 'NV19', 
    'NV10', 'NV10GL', 'NV11', 'NV11M', 'NV11GL', 'NV43M', 'NV43GL', 'NV15', 'NV15GL', 'NV44', 'NV44M', 'NV17', 'NV17M', 'NV17GL', 'NV18', 'NV18M', 
    'NV18GL', 'G80', 'G80GL', 'G72', 'G7', 'G72M', 'G72GLM', 'G72GL', 'NV1F', 'NV20', 'NV20GL', 'NV48', 'NV44A', 'C51PV', 'C51', 'C51G', 'NV25', 
    'NV25GL', 'MCP51', 'NV28', 'NV28M', 'NV28GL', 'NV28GLM', 'G71', 'G71M', 'G71GLM', 'G71GL', 'NV2A', 'MCPX', 'G73', 'NV30', 'NV30GL', 'NV31', 
    'NV31G', 'NV31M', 'NV31GLM', 'NV34', 'NV34M', 'NV34GL', 'NV38', 'NV35GL', 'NV36', 'NV36M', 'NV36GL', 'MCP55', 'G73M', 'G73GLM', 'G73GL', 'C55', 
    'C61', 'MCP61', 'G84', 'G84M', 'G84GL', 'G84GLM', 'G92', 'G86', 'G86M', 'G86GLM', 'MCP65', 'C67', 'C68', 'MCP67', 'MCP78S', 'MCP73', 'NF200', 
    'GT200b', 'GT200', 'GT200GL', 'G92M', 'G92GL', 'G92GLM', 'G94', 'G94M', 'G94GL', 'G94GLM', 'G96C', 'G96', 'G96CM', 'G96M', 'G96GL', 'G96CGL', 
    'G96GLM', 'G98', 'G98M', 'G98GL', 'G98GLM', 'MCP77', 'MCP72XE/MCP72P/MCP78U/MCP78S', 'C73', 'C77', 'C78', 'C79', 'MCP7A', 'MCP79', 
    'MCP89', 'GT216', 'GT216M', 'GT216GL', 'GT216GLM', 'GT218', 'GT218M', 'GT218GL', 'GT218GLM', 'GT215', 'GT215M', 'GT215GLM', 
    'Xavier', 'MCP78U', 'MCP72P' , 'MCP72XE','GK104', 'GK106', 'GK208', 'GK110', 'GK107', 'GK107M', 'GK107GL', 'GK107GLM', 'GK110B',
                 'GK110GL', 'GK110BGL', 'GK180GL', 'GK210GL', 'GK104GL', 'GK104M', 'GK104GLM', 'GK106M', 
                 'GK106GL', 'GK106GLM', 'GK208B', 'GK208M', 'GK208BM', 'GK20', 'GK208GLM','GF100', 'GF100M', 'GF100G', 'GF100GL', 'GF100GLM', 'GF106', 
                 'GF108', 'GF104', 'GF116', 'GF106M', 'GF106GL', 'GF106GLM', 'GF108M', 'GF108GL', 'GF108GLM', 'GF119', 'GF110', 'GF114', 'GF104M', 
                 'GF104GLM', 'GF11', 'GF119M', 'GF110GL', 'GF117M', 'GF114M', 'GF116M']

unrecoverable_error_print = (r"""
   An unrecoverable error has occured in this totally bug free 
   software.
   
   Chika is disappointed, but at least this error shows what went wrong.
   Please share the stacktrace below to Evernow so he can fix it.
   In addition, above the stacktrace is the directory of where
   DDU and your drivers are downloaded if they were downloaded.
   
   {ddu_extracted_path}
   {Appdata}
   """.format(ddu_extracted_path=ddu_extracted_path, Appdata=Appdata_AutoDDU_CLI))

login_or_not = """
You should be logged in automatically to a
user profile we created, if it doesn't then login
yourself manually (password is Evident@Omega@Winnings4@Matted@Swear@Handled
).
"""

AutoDDU_CLI_Settings = os.path.join(Appdata_AutoDDU_CLI, "AutoDDU_CLI_Settings.json")

# Suggestion by Arron to bypass fucked PATH environment variable
powershelldirectory = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"

def TestForStupidityPart43():
    # This protects against people willy nilly going to the github repo
    # and just grabbing the python file and running it, which won't bloody
    # work due to numerious assumptions specific to PyInstaller.

    # This has happened twice now.
    if not (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')):
        print("""
You did not run AutoDDU_CLI correctly. You likely
grabbed the python file from the GitHub instead
of downloading the executable. Do not run
the python file raw, as numerious code paths are
made with the expectation of it running as a 
frozen executable.

Opening browser to download executable now.
        """)
        webbrowser.open('https://github.com/Evernow/AutoDDU_CLI/raw/main/signedexecutable/AutoDDU_CLI.exe')
        time.sleep(1)
        os._exit(1)


def HandleChangingGPUProcess():
    for vendor in ['amd','intel','nvidia']:
        download_helper(f'https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/{vendor}_gpu.json',os.path.join(Jsoninfofileslocation,f'{vendor}_gpu.json'),False)
    with open(os.path.join(Jsoninfofileslocation,'nvidia_gpu.json')) as json_file:
        nvidia_gpu = json.load(json_file)
    with open(os.path.join(Jsoninfofileslocation,'amd_gpu.json')) as json_file:
        amd_gpu = json.load(json_file)
    with open(os.path.join(Jsoninfofileslocation,'intel_gpu.json')) as json_file:
        intel_gpu = json.load(json_file)
    GPUDrivers = {1: amd_gpu, 2: intel_gpu, 3:nvidia_gpu}
    UserResponseToContinue = -1
    while UserResponseToContinue == -1:
        print("""
You are placing AutoDDU into change GPU mode.
This is made for when you have a current GPU
and are changing it to a different GPU.
It will involve performing DDU in safe mode,
and then when DDU is finished AutoDDU will
shutdown your PC instead of restarting it,
then when shutdown you will then change
the GPU to your new one and boot up.

Is this what you want to do or do you 
instead wish to perform DDU without changing GPUs?

1 - I wish to change my GPU after doing DDU.
2 - I am not going to change my GPU.""")
        try:
            UserResponseToContinue = int(input('Type the number for your response and press enter: '))
            if UserResponseToContinue != 1 and UserResponseToContinue != 2:
                UserResponseToContinue = -1
                raise ValueError
        except ValueError:
            print("Invalid option selected. Refreshing in 5 seconds.")
            time.sleep(5)

        clear()
    if UserResponseToContinue == 2:
        return 0
    else:
        print()
        VendorChoice = -1
        while VendorChoice == -1:
            print("""
Which GPU vendor are you switching to?
In other word, which vendor made your future
GPU?
Your CURRENT GPU vendor is NOT IMPORTANT unless
it just happens to be the same vendor. All these
questions relate to your FUTURE GPU, not your 
current one. 
1 - AMD.
2 - Intel.
3 - NVIDIA.
4 - I'll install drivers myself.""")
            try:
                VendorChoice = int(input('Type the number for your response and press enter: '))
                if VendorChoice != 1 and VendorChoice != 2 and VendorChoice != 3 and VendorChoice != 4:
                    VendorChoice = -1
                    raise ValueError
            except ValueError:
                print("Invalid option selected. Refreshing in 5 seconds.")
                time.sleep(5)
            clear()
    if VendorChoice == 4:
        return None
    time.sleep(0.1)
    stringforuser = 'Please select which GPU driver is for your future GPU: \n'
    drivers = []
    for branch in GPUDrivers[VendorChoice]:
        stringforuser += f"""{len(drivers)+1} / {GPUDrivers[VendorChoice][branch]['description']} \n  \ {(GPUDrivers[VendorChoice][branch]['link'])[GPUDrivers[VendorChoice][branch]['link'].rfind('/')+1:]} - {GPUDrivers[VendorChoice][branch]['version']}\n\n"""
        drivers.append(GPUDrivers[VendorChoice][branch]['link'])
    stringforuser += f'{len(drivers)+1} / I have no idea (starts search GPU process).'
    print(stringforuser)
    user_choice_for_driver = None
    while user_choice_for_driver == None:
        try:
            user_choice_for_driver = int(input('Your choice: '))
            if user_choice_for_driver not in list(range(1,len(drivers)+2)):
                raise ValueError
        except ValueError:
            print("Invalid option selected. Refreshing in 5 seconds.")
            time.sleep(5)
    VendorChoice_dict = {1: 'amd', 2: 'intel', 3:'nvidia'}
    if user_choice_for_driver == len(drivers)+1:
        return [UserInput(VendorChoice_dict[VendorChoice])]
    else:
        return [drivers[user_choice_for_driver-1]]
def SearchGPU(gpu_vendor,provided_name):
    download_helper(f'https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/{gpu_vendor}_gpu.json',os.path.join(Jsoninfofileslocation,f'{gpu_vendor}_gpu.json'),False)
    with open(os.path.join(Jsoninfofileslocation,f'{gpu_vendor}_gpu.json')) as json_file:
        gpu_json = json.load(json_file)
    download_helper("https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/PCI-IDS.json", os.path.join(Jsoninfofileslocation,'PCI-IDS.json'),False)
    with open(os.path.join(Jsoninfofileslocation,'PCI-IDS.json')) as json_file:
        PCIIDS_DATA = json.load(json_file)
    vendor_id_dict = {'nvidia':'10de', 'amd':'1002', 'intel':'8086'}
    gpu_names = {}
    for branch in gpu_json:
        gpu_names_wip = []
        for gpu in gpu_json[branch]['SupportedGPUs']:
            try:
                gpunamefromdatabse = PCIIDS_DATA[vendor_id_dict[gpu_vendor]]['devices'][gpu.lower()]['name']
                # Get Rid of Radeon name before the below split 
                gpunamefromdatabse = gpunamefromdatabse.replace('Radeon','')
                gpunamefromdatabse = gpunamefromdatabse[gpunamefromdatabse.find('[')+1:gpunamefromdatabse.find(']')]
                if gpu_vendor == 'amd': #
                    # AMD shares PCI IDS between GPUs almost 100% of the time
                    # For example: Radeon RX 6700S / 6800S / 6650 XT is extremely common.
                    # This really screws up our search results, so lets just split by / and include all of them seperately.
                    for amd_gpu in gpunamefromdatabse.split('/'):
                        gpu_names_wip.append(amd_gpu.strip())
                        break # Too much madness can happen if we do the usual we do for Intel and NVIDIA, so lets leave it here.
                # Get rid of stuff from the name that will just confuse users and doesn't affect anything here to begin with.
                gpunamefromdatabse = gpunamefromdatabse.replace('Mobile','').replace('Max-Q','').replace('Laptop','').replace('Lite Hash Rate','').replace('Refresh','').replace('/','')
                # Get rid of extra spaces from here: https://stackoverflow.com/a/1546883/17484902
                gpunamefromdatabse = ' '.join(gpunamefromdatabse.split())
                gpu_names_wip.append(gpunamefromdatabse.strip())
                # Lets get rid of brand names since someone may type for example "RTX 3060" and not "Geforce RTX 3060", but leave quadro name as those are
                # fairly rare and taint our results otherwise.
                gpunamefromdatabse = gpunamefromdatabse.replace('GeForce','')
                gpu_names_wip.append(gpunamefromdatabse.strip())
            except KeyError:
                pass
                # This protects against PCI IDS not having a GPU that's in the SupportedGPUs list, which happens pretty frequently with AMD and Intel.
        # Get rid of duplicates that can easily occur
        gpu_names_wip = list(set(gpu_names_wip))

        # We do this by priority so we can then later sort by priority so we're checker the ones that should be used for a specific
        # GPU first. This avoids giving all NVIDIA users studio drivers or all AMD users PRO drivers.
        gpu_names[gpu_json[branch]['priority']] = gpu_names_wip
        gpu_names = dict(sorted(gpu_names.items())) 

        # Get a list of similar strings to the one the user provided, max of 3 results per branch
        matching_names = {}
        for branch in gpu_names:
            results = difflib.get_close_matches(provided_name, gpu_names[branch],3,cutoff=.5)
            for result in results:
                if (result not in matching_names.keys()):
                    matching_names[result] = branch

            
    return(matching_names)
        
def UserInput(gpu_vendor):
    driver = None
    attempts = 0
    while driver == None:
        attempts += 1
        if attempts %5 == 0:
            userchoicewhetherhehasalife = None
            while userchoicewhetherhehasalife == None:
                print("""
You attempted this 5 more times,
you sure you want to continue?

1 - Yes I want to continue
2 - No I want to just install drivers myself""")
                try:
                    userchoicewhetherhehasalife = int(input('Your Choice:'))
                    if userchoicewhetherhehasalife !=  1 and userchoicewhetherhehasalife !=  2:
                        userchoicewhetherhehasalife = None
                        raise ValueError
                except ValueError:
                    userchoicewhetherhehasalife = None
                    print("Invalid option selected. Refreshing in 5 seconds.")
                    time.sleep(5)
                if userchoicewhetherhehasalife ==  1:
                    continue
                else:
                    return None
        print("""
You initiated the search option.
You can put in the name of your GPU
as accurate as possible and we will
list you potential matches in our
database, from which you pick the closest
approximation to your FUTURE gpu.""")
        provided_name = input('Enter the name of your FUTURE GPU: ')
        if len(provided_name) < 3 or (not provided_name.isascii()):
            print('Please put a valid potential name that is at least 3')
            print('characters long and contains only english characters.')
            print('Showing prompt to enter a name again in 10 seconds.')
            time.sleep(10)
            clear()
            continue
        results_of_user_search = SearchGPU(gpu_vendor,provided_name)
        if len(results_of_user_search) > 1:
            user_show_results = '\nThese are the potential GPUs we know of given the name you provided.\n'
            processed_results = []
            for result in results_of_user_search.keys():
                user_show_results += f'{len(processed_results)+1} / {result} \n'
                processed_results.append(result)
            
            user_show_results +=(f'{len(processed_results)+1} / None of these match, I wish to enter another name.\n')
            user_show_results +=(f'{len(processed_results)+2} / None of these match, I wish to install drivers myself.\n')
            print(user_show_results)
            
            choice_from_search = None
            while choice_from_search == None:
                print('Enter the number of the result which most closely matches your FUTURE GPU.')
                try:                   
                    choice_from_search = int(input('Enter the number corresponding to the closest GPU: '))
                    if choice_from_search not in list(range(1,len(processed_results)+3)):
                        choice_from_search = None
                        raise ValueError
                except ValueError:
                    print("Invalid option selected. Refreshing in 5 seconds.")
                    time.sleep(5)
            if choice_from_search == len(processed_results)+1:
                continue
            if choice_from_search == len(processed_results)+2:
                return None 
            download_helper(f'https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/{gpu_vendor}_gpu.json',os.path.join(Jsoninfofileslocation,f'{gpu_vendor}_gpu.json'),False)
            with open(os.path.join(Jsoninfofileslocation,f'{gpu_vendor}_gpu.json')) as json_file:
                gpu_json = json.load(json_file)
            for branch in gpu_json:
                if gpu_json[branch]['priority'] == results_of_user_search[processed_results[(choice_from_search-1)]]:
                    return gpu_json[branch]['link']
        else: # No results
            print("No results came from your search, try again.")
            print("Try to be as clear as possible, if you fail 5 times")
            print("We will offer an option to provide your own drivers.")
            print("Gonna ask again for the name of the FUTURE GPU in 15 seconds")
            time.sleep(15)


def LogBasicSysInfo():
    # Info useful sometimes in tracking down problems, for example norwegian and german have caused issues..
    knownCPUArchitectures = {0: 'x86', 1: 'MIPS', 2: 'Alpha', 'PowerPC': 3,
                            5:'ARM', 6:'ia64', 9:'x64', 12:'ARM64'}
    for profile in wmi.WMI().Win32_Processor() : # Technically someone can have more than one CPU, so worth being in a loop...
            if profile.Architecture in knownCPUArchitectures.keys():
                logger('CPU architecture: ' + knownCPUArchitectures[profile.Architecture])
            else:
                logger('CPU architecture unknown, Windows identified it as: ' + str(profile.Architecture))
                logger('Windows identifiers for CPU architecture can be found here: https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-processor')
            logger('CPU name is: ' + str(profile.Name))
            logger('CPU enabled cores is: ' + str(profile.NumberOfEnabledCore))
    locale = wmi.WMI().Win32_OperatingSystem  ()[0].Locale
    logger('Locale: ' + str(locale))
    language = wmi.WMI().Win32_OperatingSystem  ()[0].OSLanguage
    logger('language: ' + str(language))
    installdate = wmi.WMI().Win32_OperatingSystem  ()[0].InstallDate
    logger('installdate: ' + str(installdate))
    NameOfWindows = wmi.WMI().Win32_OperatingSystem  ()[0].Name
    logger('NameOfWindows: ' + str(NameOfWindows))
    # This allows us to see the full build number which is VERY useful for determining
    # which channel of insider someone is on.
    VersionOfWindows = os.system('ver')
    logger('VersionOfWindows: ' + str(VersionOfWindows))

    AreWeBootedOnaUSB = wmi.WMI().Win32_OperatingSystem  ()[0].PortableOperatingSystem
    logger('AreWeBootedOnaUSB: ' + str(AreWeBootedOnaUSB))
    MotherboardModel = wmi.WMI().Win32_BaseBoard   ()[0].Product
    logger('MotherboardModel: ' + str(MotherboardModel))
    MotherboardManuf = wmi.WMI().Win32_BaseBoard   ()[0].Manufacturer
    logger('MotherboardManuf: ' + str(MotherboardManuf))
    # Invaluable to know which release was built with so we if we get a
    # python specific error we know which line number to go to in the cpython repo.
    logger('Python version: ' + sys.version)
    # Tells us whether Windows is currently in debug mode, useful as behavior is slightly different and can explain performance issues
    DebugMode = wmi.WMI().Win32_OperatingSystem()[0].Debug
    logger('DebugMode: ' + str(DebugMode))
    # Logs all open processes
    processes = list()
    for process in wmi.WMI().Win32_Process((["Name"])): # This guy is a genius: https://stackoverflow.com/questions/61762991/counting-number-of-running-processes-with-wmi-python-is-slow
        processes.append(process.Name)
    processes = str(processes)
    # Sucks, I know, but like, holy shit I am going insane debugging some of these issues 
    # which I am convinced are caused by some wacky app
    zlibz = str(zlib.compress(str(processes).encode()))
    logger("Below is the a list of all open processes put as a string and then compressed with zlib")
    logger(zlibz)


def GPUZINFO():
    try:
        try:
            os.remove(os.path.join(Appdata_AutoDDU_CLI,'GPUOutput.xml'))
        except:
            pass
        download_helper("https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/GPU-Z.exe", os.path.join(Appdata_AutoDDU_CLI,'GPU-Z.exe'),False)
        subprocess.call([os.path.join(Appdata_AutoDDU_CLI,'GPU-Z.exe'),'-minimized','-dump','GPUOutput.xml'],
                            cwd=Appdata_AutoDDU_CLI  , stderr=subprocess.DEVNULL)

        with open(os.path.join(Appdata_AutoDDU_CLI,'GPUOutput.xml'), 'r', encoding='utf-8') as file:
            my_xml = file.read()
        my_dict = xmltodict.parse(my_xml)
        logger("In GPU-Z, expect a lot of verbose crap while this method is new.")
        cardlist = []
        logger(str(my_dict['gpuz_dump']['card']))
        if type(my_dict['gpuz_dump']['card']) == dict: #Workaround issues relating to how multi gpu setups appear. 
            cardlist.append(my_dict['gpuz_dump']['card'])
            my_dict['gpuz_dump']['card'] = cardlist
        logger(str(my_dict['gpuz_dump']['card']))
        logger(str(my_dict))
        GPUsFound = {}
        for gpu in (my_dict['gpuz_dump']['card']):
            logger(str(gpu))
            # 1002 = AMD ; 8086 = Intel ; 10de = NVIDIA ; 121a = Voodoo (unlikely but I mean.. doesn't hurt?)

            if gpu['vendorid'].lower() == '1002' or gpu['vendorid'].lower() == '8086' or gpu['vendorid'].lower() == '10de' or gpu['vendorid'].lower() == '121a':     
                GPUsFound[str(gpu['cardname'])] = [str(gpu['gpuname']), str(gpu['vendorid']).lower(), str(gpu['deviceid']).lower()]
        logger("Gonna return from the GPU-Z method")
        logger(str(GPUsFound))
        return (GPUsFound)
    except:
        logger("GPU-Z method failed with the following error, gonna fallback to PCIIDS method")
        logger(str(traceback.format_exc()))
        return {} # This triggers the fallback to the PCI-IDS method

def TestMultiprocessingTarget(enable):
        wrxAdapter = wmi.WMI( namespace="StandardCimv2").query("SELECT * FROM MSFT_NetAdapter") 
        list_of_names = list()
        list_test = list()
        for adapter in wrxAdapter:
            list_of_names.append(adapter.Name)
            if adapter.Virtual == False and adapter.LinkTechnology != 10:
                    pass
def TestMultiprocessing():
    # Check because some system configurations are incompatible with multiprocessing. 
    proc = multiprocessing.Process(target=TestMultiprocessingTarget, args=(True,)) 
    proc.start()
    time.sleep(1)
    if proc.is_alive():
        time.sleep(10)
    proc.terminate()


def VerifyDDUAccountCreated():
    listofusers = []
    for profile in wmi.WMI().Win32_UserAccount() :
        if len(profile.Name) > 0:
            listofusers.append(profile.Name)
    logger("List of users in Windows install is:")
    logger(str(listofusers))
    if obtainsetting("ProfileUsed") not in listofusers:
        return False
    return True


def RestartPending():
    # Checks to see if a restart is pending for updates, this is to prevent issues with us restarting and not landing in safe mode.
    key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'
    reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    try:
        k = winreg.OpenKey(reg, key) # if the key exists then we have an update pending that needs a restart to finish.
        logger("Got a pending Windows update restart.")
        return True
    except:
        logger("I believe there is not a Windows update restart pending.")
        logger(str(traceback.format_exc()))
        return False

def CheckPublisherOfDriver(driver):
    logger("Dealing with driver {} in CheckPublisherOfDriver".format(driver))
    p = str(subprocess.Popen(
            "{powershell} (Get-AuthenticodeSignature '{driver}').SignerCertificate.subject".format(powershell=powershelldirectory, driver=driver),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=CREATE_NEW_CONSOLE).communicate())
    logger("Got output {} which I'm going to assume is:".format(p))
    if 'NVIDIA' in p.upper():
        logger('NVIDIA')
        return 'NVIDIA'
    if 'AMD' in p.upper() or 'advanced micro devices' in p.lower():
        logger('AMD')
        return 'AMD'
    if 'intel' in p.lower():
        logger('intel')
        return 'Intel'
    logger('Do not know who publisher is.')
    return None


def IsKasperskyInstalled():
    software = []
    for p in wmi.WMI().Win32_Product():
        if p.Caption is not None:
            software.append (str(p.Caption))
    for softwarepossibility in software:
        if 'kaspersky' in softwarepossibility.lower():
            return True
    return False


def CheckIfBackupAccountExists():
    userprofiles = list()
    for group in wmi.WMI().Win32_UserAccount():
        userprofiles.append(group.Caption.replace((group.Domain + '\\'), ''))
    if 'BackupDDUProfile' in userprofiles:
        return True
    else:
        return False

def BackupLocalAccount():
    # Prevents a situation where the user has an MS Account on W11 Home
    # And they cannot log back in after DDU (where DDU profile no longer exists)
    # Due to MS requiring an internet connection.
    if CheckIfBackupAccountExists() == False:
        firstcommand = "net user /add BackupDDUProfile"
        secondcommand = "net localgroup {administrators} BackupDDUProfile /add".format(administrators=AdminGroupName())
        subprocess.run(firstcommand, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(secondcommand, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        


def AdminGroupName():
    # This exists because german localizes group names, so administrator is not the name of the admin group
    # in german. https://youtu.be/APbJcnH1brg
    for group in wmi.WMI().Win32_Group(): # https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/win32-group
        if group.SID == 'S-1-5-32-544': # https://docs.microsoft.com/en-US/windows/security/identity-protection/access-control/security-identifiers
            adminname = group.Caption.replace((group.Domain + '\\'), '') 
    return(adminname)


def serialize_req(obj):
    return json.dumps(obj, separators=(',', ':'))


def getDispDrvrByDevid(query_obj, timeout=10):
    ENDPOINT = 'https://gfwsl.geforce.com/nvidia_web_services/' \
        'controller.gfeclientcontent.NG.php/' \
        'com.nvidia.services.GFEClientContent_NG.getDispDrvrByDevid'
    url = posixpath.join(ENDPOINT, serialize_req(query_obj))
    http_req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'NvBackend/36.0.0.0'
        }
    )
    with urllib.request.urlopen(http_req, None, timeout) as resp:
        coding = resp.headers.get_content_charset()
        coding = coding if coding is not None else 'utf-8-sig'
        decoder = codecs.getreader(coding)(resp)
        res = json.load(decoder)
    return res


def get_latest_geforce_driver(dev_id):

    notebook=False
    x86_64=True
    os_version="10.0"
    os_build="19044"
    language=1033
    beta=False
    dch=True
    crd=False
    timeout=10
    query_obj = {
        "dIDa": dev_id,                   # Device PCI IDs:
                                          # ["DEVID_VENID_DEVID_VENID"]
        "osC": os_version,                # OS version (Windows 10)
        "osB": os_build,                  # OS build
        "is6": "1" if x86_64 else "0",    # 0 - 32bit, 1 - 64bit
        "lg": str(language),              # Language code
        "iLp": "1" if notebook else "0",  # System Is Laptop
        "prvMd": "0",                     # Private Model?
        "gcV": "3.25.1.27",               # GeForce Experience client version
        "gIsB": "1" if beta else "0",     # Beta?
        "dch": "1" if dch else "0",       # 0 - Standard Driver, 1 - DCH Driver
        "upCRD": "1" if crd else "0",     # Searched driver: 0 - GameReady Driver, 1 - CreatorReady Driver
        "isCRD": "1" if crd else "0",     # Installed driver: 0 - GameReady Driver, 1 - CreatorReady Driver
    }
    try:
        res = getDispDrvrByDevid(query_obj, timeout)
    except urllib.error.HTTPError as e:
        logger(e)
        if e.code == 404:
            res = None
        else:
            raise e
    return res




def FindOutOfBranchDriver(vendorid_deviceid):
    # '1BE0_10DE'
    drv = get_latest_geforce_driver([vendorid_deviceid])
    if drv is None:
        return None

    else:
        return drv['DriverAttributes']['DownloadURLAdmin']



def checkifvaliddownload(url):
   logger("Checking if custom URL {} is valid".format(str(url)))
   try:
        my_referer = "https://www.amd.com/en/support/graphics/amd-radeon-6000-series/amd-radeon-6700-series/amd-radeon-rx-6700-xt"
        file = urllib.request.Request(url)
        file.add_header('Referer', my_referer)
        file.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0')
        file = urllib.request.urlopen(file, timeout=5)
        logger("Got size of custom URL to be {}".format(str(file.length)))
        if file.length < 6000000: # 6MB, which is size of intel driver assistant
            return False
        else:
            return True
   except:
        logger("Failed valid check with error " +str(traceback.format_exc())  )
        return False




def checkBatteryLevel():
    try:
        if psutil.sensors_battery() != None and int(psutil.sensors_battery().percent) < 40 and psutil.sensors_battery().power_plugged == False:
            print("Your battery is less than 40%")
            print("Please connect your laptop to power, then continue with instructions below.")
            HandleOtherLanguages()
    except:
        logger("Failed to check battery level with")
        logger(str(traceback.format_exc()))

def cleanupAutoLogin():
    try:
        Winlogon_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon')
        if winreg.QueryValueEx(Winlogon_key, 'DefaultUserName')[0] == obtainsetting("ProfileUsed"):
            failed = 0
            try:
                winreg.DeleteValue(Winlogon_key, 'AutoAdminLogon')
            except:
                failed = 1 
                logger("Failed in cleanupAutoLogin 1")
                logger(str(traceback.format_exc()))
            try:
                winreg.DeleteValue(Winlogon_key, 'DefaultUserName')
            except:
                failed = 1  
                logger("Failed in cleanupAutoLogin 2")
                logger(str(traceback.format_exc()))

            try:
                winreg.DeleteValue(Winlogon_key, 'DefaultPassword') 
            except:
                failed = 1 
                logger("Failed in cleanupAutoLogin 3")
                logger(str(traceback.format_exc()))
            try:
                winreg.DeleteValue(Winlogon_key, 'AutoLogonCount') 
            except:
                # I think this is normal to occur so...
                logger("EXPECTED failure in cleanupAutoLogin 4")
                logger(str(traceback.format_exc()))
        else:
            failed = 1
            logger("Did not log because DefaultUserName did not match ProfileUsed, used is {used} and defaultusername is {default}".format(default=winreg.QueryValueEx(Winlogon_key, 'DefaultUserName')[0], user=obtainsetting("ProfileUsed")))
        winreg.CloseKey(Winlogon_key)
        print("Finished AutoLogin cleanup")
        logger("Finished cleanupAutoLogin successfully")
    except:
        failed = 1
        logger("Failed in cleanupAutoLogin 5")
        logger(str(traceback.format_exc()))
    if failed == 1:
        print("WARNING: Something MAY have gone wrong in some cleanup")
        print("DDU finished just fine, just that when we log you out,")
        print("you MAY be logged back into this DDU profile, if you are")
        print("please log out then then restart, you may have to do this FIVE times for it to stop.")
        print("We'll continue in 30 seconds.")
        time.sleep(30)


def PendingUpdatesCount():
    # https://stackoverflow.com/questions/70792656/how-do-i-get-pending-windows-updates-in-python
    # https://github.com/Evernow/AutoDDU_CLI/issues/14

    try:
        wua = win32com.client.Dispatch("Microsoft.Update.Session")    
        avilable_update_seeker = wua.CreateUpdateSearcher()
        search_available = avilable_update_seeker.Search("IsInstalled=0 and Type='Software'")
        pendingupdates = int(search_available.Updates.Count )
        logger("Got pending updates to be " + str(pendingupdates))
        return pendingupdates
    except:
        logger("Failed to check Pending updates with following error")
        logger(str(traceback.format_exc()))
        logger("Gonna be trying to log every element of Microsoft Update Session")
        try:
            # I don't have a lot of data on how this fails, but know for a fact that it does in some situations,
            # and in those situations the person usually leaves and logs don't provide useful info, so this is why
            # I added all these logs.
            logger("Going to try to dispatch Microsoft.Update.Session")
            wua = win32com.client.Dispatch("Microsoft.Update.Session")
            logger(str(wua))
            logger("Going to try to create update searcher")
            avilable_update_seeker = wua.CreateUpdateSearcher()
            logger(str(avilable_update_seeker))
            logger("Going to try search with the specific variables to know which updates ain't installed")
            search_available = avilable_update_seeker.Search("IsInstalled=0 and Type='Software'")
            logger(str(search_available))
            logger("Going to try to get result from previous search")
            logger(search_available.Updates.Count)
            if type(search_available.Updates.Count) ==int:
                logger("No idea how but this check didn't fail??")
            else:
                logger("Type of Updates.Count is not the expected one, it is")
                logger(str(type(search_available.Updates.Count)))
        except:
            logger("Failed in logging extra info with")
            logger(str(traceback.format_exc()))

        print("Something is crucially wrong with")
        print("your Windows Updates service.")
        print("This is a major issue and can cause a great pain later on.")
        print("We recommend running SFC and DISM, then restarting.")
        print("If you don't know what this is then show this message")
        print("to the person who sent you this, they likely know.")
        print("If this keeps happening and you're sure there's no problems")
        print("then here we offer the option to also continue like")
        print("if nothing is wrong, but we only recommend doing this")
        print("once you've corrected the problem,if to correct this")
        print("you need to restart it's fine, AutoDDU will continue on")
        print("when you launch it later. We'll show option to continue in 60 seconds.")
        time.sleep(60)
        HandleOtherLanguages()

def HandlePendingUpdates():
    print("We're checking to see if there's pending updates, this can take a few minutes.")
    if PendingUpdatesCount() > 0:
        print(r"""
There's pending Windows Updates. Having pending
Windows Updates can cause issues when rebooting into
safe mode. For this reason we're going to pause
and you will have to go to Windows Updates in Settings app
and check for updates (may have to check manually multiple times)
and apply these updates. If these updates require a restart then
restart when asked, and then when you're back up you can
launch AutoDDU yourself afterwards. If no restart is needed then just
apply the updates and once applied come back here, we'll show
an option to continue in 10 minutes. You usually do not
need to install optional updates. If you're still getting
this message and see no pending updates, check manually for updates
by clicking the 'Check for Updates' button. If you believe you
applied all Windows updates and don't want to wait 10 mins then close 
and reopen AutoDDU.""")
        print("")
        time.sleep(600)
        if PendingUpdatesCount() > 0:
            print("""
We are still seeing pending updates. Are you sure you
want us to continue? This can cause great annoyances later on.
Do the below prompt if you want to continue, if you don't then do whatever
you need to do to not have updates pending, it is fine to close AutoDDU
and restart if needed, we'll go from where we ended once you open 
AutoDDU again. Or if you're in the process of installing them and
they do not need a restart just do the below prompt to continue once
they're installed.""") 

            HandleOtherLanguages()
    

def suspendbitlocker():
    try:
        p = str(subprocess.Popen(
            "{powershell} Suspend-BitLocker -MountPoint 'C:' -RebootCount 3".format(powershell=powershelldirectory),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=CREATE_NEW_CONSOLE).communicate())
        logger("Suspended bitlocker with output " + str(p))
    except:
        logger("Did not suspend bitlocker with output " + p)
    
def handleoutofdate():


    download_helper("https://raw.githubusercontent.com/Evernow/AutoDDU_CLI/main/Version.json", os.path.join(Jsoninfofileslocation,'Version.json'),False)
    with open(os.path.join(Jsoninfofileslocation,'Version.json')) as json_file:
        data = json.load(json_file)

    if (packaging.version.parse(Version_of_AutoDDU_CLI)) < packaging.version.parse(data['version']):
        logger("Version did not match, version in local variable is {local} while version on GitHub is {git}".format(git=data['version'], local=Version_of_AutoDDU_CLI))
        print("You are running a version that is not the latest.")
        print("Do you want to continue?")
        print("Type in 'Yes' and we'll continue along")
        print("using this outdated version.")
        print("")
        print("Type 'No' and we'll exit linking you to the latest release so you can launch it.")
        answer = ""
        while "yes" not in answer.lower() and "no" not in answer.lower():
            answer = input("Type in Yes or No then enter key: ")
        if "no" in answer.lower():
            webbrowser.open('https://github.com/Evernow/AutoDDU_CLI/raw/main/signedexecutable/AutoDDU_CLI.exe')
            time.sleep(1)
            os._exit(1)
        print("")


def insafemode():
    bootstate = wmi.WMI().Win32_ComputerSystem()[0].BootupState.encode("ascii", "ignore").decode(
            "utf-8")
    if "safe" in bootstate.lower():
        return True
    else:
        return False


# https://stackoverflow.com/a/65501621/17484902
class singleinstance:
    """ Limits application to single instance """

    def __init__(self):
        self.mutexname = "AutoDDUCLI_{91473d5a-5f6e-4266-ab87-22115e93b84b}"
        self.mutex = CreateMutex(None, False, self.mutexname)
        self.lasterror = GetLastError()
    
    def alreadyrunning(self):
        return (self.lasterror == ERROR_ALREADY_EXISTS)
        
    def __del__(self):
        if self.mutex:
            CloseHandle(self.mutex)

def accountforoldcontinues(num):
    if os.path.exists(Persistent_File_location):
        if abs(int(time.time()) - os.path.getmtime(Persistent_File_location)) > 86400:
            try:
                os.remove(Persistent_File_location)
                os.remove(AutoDDU_CLI_Settings)
                logger("Deleted persistent file in 24hrs check")
            except:
                if num == 1:
                    raise Exception("Failure in accountforoldcontinues")
                print("""
Warning: Saw this session is continuing after over
24 hours. This is possibily a bug.

I tried to restart but it failed. This could cuase issues.""")
                logger("Failed to delete persistent file in 24hrs check")
                logger(str(traceback.format_exc()))


def internet_on():
    remaining_tries = 5
    while remaining_tries > 0:
        try:
            download_helper('https://www.google.com/', 'Internet_Check_Directory_Unneeded',False,0,True,True)
            return True
        except:
            remaining_tries = remaining_tries - 1
            logger(f"Failed to verify if we're online, gonna give it {remaining_tries} more tries.")
            logger(str(traceback.format_exc()))
    return False


def time_checker():
    # Returns true when time Windows is following is within 48 hours
    # of what the actual time is. This catches issues where 
    # someone's PC has not been turned on for a long time and cannot
    # sync with Microsoft's time servers (like idiot blocks Microsoft domains)
    try:
        server = 'us.pool.ntp.org'
        client = ntplib.NTPClient()
        response = client.request(server, version=3)
        # Time from U.S. NTP timeserver
        internet_time = int(time.mktime((datetime.fromtimestamp(response.tx_time, timezone.utc)).timetuple()))

        # Time computer is following
        local_time = time.time()
        if (internet_time - 172800) <= local_time <= (internet_time + 172800):  # Check if within 48 hours
            return True
        return False
    except:
        logger("Checking the time failed")
        logger(str(traceback.format_exc()))
        print("INFO: TIME CHECK FAILED (NON FATAL)", flush=True)
        print("WARNING: THIS CAN CAUSE ISSUES.", flush=True)
        print("WILL CONTINUE IN 10 SECONDS", flush=True)
        time.sleep(10)


def get_free_space():
    twenty_gigabytes = 20474836480
    return shutil.disk_usage(Appdata).free > twenty_gigabytes


def findnottaken():
    # TODO: this is dumb, but I don't like the risk of deleting user profile folders... Windows deletes these after a
    #  while anyways if they aren't associated with a user.
    ddu_next = "DDU"
    subfolders = list()
    for entry_name in os.listdir(Users_directory):
        entry_path = os.path.join(Users_directory, entry_name)
        if os.path.isdir(entry_path):
            subfolders.append(entry_name.upper())
    while ddu_next in subfolders:
        ddu_next = ddu_next + "U"
    logger("Used users are: " + str(subfolders))
    logger("Ended up using user: " + str(ddu_next))
    return ddu_next


def obtainsetting(index):
    with open(AutoDDU_CLI_Settings, 'r+') as f:
        advanced_options_dict = json.load(f)
        return advanced_options_dict[index]


def default_config():
    advanced_options_dict_global["ProfileUsed"] = findnottaken()
    if not os.path.exists(Appdata_AutoDDU_CLI):
        os.makedirs(Appdata_AutoDDU_CLI)
    with open(AutoDDU_CLI_Settings, "w+") as outfile:
        json.dump(advanced_options_dict_global, outfile)


def AdvancedMenu():
    logger("User entered AdvancedMenu")
    option = -1
    while option != "12":
        clear()
        time.sleep(0.5)
        print("WARNING: THIS MAY BEHAVE UNEXPECTADLY!", flush=True)
        print('1 --' + AdvancedMenu_Options(1), flush=True)  # Disable Windows Updates check
        print('2 --' + AdvancedMenu_Options(2), flush=True)  # Bypass supported GPU requirement
        print('3 --' + AdvancedMenu_Options(3), flush=True)  # Provide my own driver URLs
        print('4 --' + AdvancedMenu_Options(4), flush=True)  # RemovePhyX
        print('5 --' + AdvancedMenu_Options(5), flush=True)  # Do not turn internet off when needed
        print('6 --' + AdvancedMenu_Options(6), flush=True)  # Do not disable overclocking/undervolts/fan curves
        print('7 --' + AdvancedMenu_Options(7), flush=True)  # Disable 20GB free storage requirement
        print('8 --' + AdvancedMenu_Options(8), flush=True)  # Use AMD Enterprise driver
        print('9 --' + AdvancedMenu_Options(9), flush=True)  # Use NVIDIA Studio driver (Pascal and up)
        print('10 --' + AdvancedMenu_Options(10), flush=True)  # Manual DNS Resolving
        print('11 --' + AdvancedMenu_Options(11), flush=True)  # Fallback to PCI-IDS GPU Detection
        print('12 -- Start', flush=True)
        option = str(input('Enter your choice: '))
        change_AdvancedMenu(option)


def AdvancedMenu_Options(num):
    with open(AutoDDU_CLI_Settings, 'r+') as f:
        advanced_options_dict = json.load(f)
        if num == 1:
            if advanced_options_dict["disablewindowsupdatecheck"] == 0:
                return " Disable Windows Updates check"
            else:
                return " Enable Windows Updates check"

        if num == 2:
            if advanced_options_dict["bypassgpureq"] == 0:
                return " Bypass supported GPU requirement"
            else:
                return " Enable supported GPU requirement"

        if num == 3:
            if len(advanced_options_dict["provideowngpuurl"]) == 0:
                return " Provide my own driver URLs"
            else:
                return " Let AutoDDU look for drivers"

        if num == 4:
            if advanced_options_dict["RemovePhysX"] == 0:
                return " Remove PhysX when running DDU"
            else:
                return " Don't remove PhysX when running DDU"

        if num == 5:
            if advanced_options_dict["disableinternetturnoff"] == 0:
                return " Do not turn internet off when needed"
            else:
                return " Turn internet off when needed"

        if num == 6:
            if advanced_options_dict["donotdisableoverclocks"] == 0:
                return " Do not disable overclocking/undervolts/fan curves"
            else:
                return " Disable overclocking/undervolts/fan curves"
        if num == 7:
            if advanced_options_dict["avoidspacecheck"] == 0:
                return " Disable 20GB free storage requirement"
            else:
                return " Enable 20GB free storage requirement"
        if num == 8:
            if advanced_options_dict["amdenterprise"] == 0:
                return " Use AMD Enterprise Driver"
            else:
                return " Use AMD Consumer Driver"
        if num == 9:
            if advanced_options_dict["nvidiastudio"] == 0:
                return " Use NVIDIA Studio driver (Pascal and up)"
            else:
                return " Use NVIDIA Game Ready driver"
        if num == 10:
            if advanced_options_dict["dnsoverwrite"] == 0:
                return " Do Manual DNS Resolving"
            else:
                return " Let OS Perform DNS Resolving"
        if num == 11:
            if advanced_options_dict["dnsoverwrite"] == 0:
                return " Fallback to PCI-IDS GPU Detection"
            else:
                return " Use GPU-Z for GPU Detection"
        f.seek(0)
        json.dump(advanced_options_dict, f, indent=4)
        f.truncate()
        logger("Advanced options are now: " + str(advanced_options_dict))


def change_AdvancedMenu(num, ExtraArgument=[]):
    logger("User is changing option " + str(num))
    with open(AutoDDU_CLI_Settings, 'r+') as f:
        advanced_options_dict = json.load(f)
        if num == "1":
            if advanced_options_dict["disablewindowsupdatecheck"] == 0:
                advanced_options_dict["disablewindowsupdatecheck"] = 1
            else:
                advanced_options_dict["disablewindowsupdatecheck"] = 0

        if num == "2":
            if advanced_options_dict["bypassgpureq"] == 0:
                advanced_options_dict["bypassgpureq"] = 1
            else:
                advanced_options_dict["bypassgpureq"] = 0

        if num == "3":
            if len(advanced_options_dict["provideowngpuurl"]) == 0:
                isitinvalid = True
                while isitinvalid:
                    option = str(input('Type in the driver download URL: '))
                    if checkifvaliddownload(option):
                        advanced_options_dict["provideowngpuurl"].append(option)
                        isitinvalid = False
                    else:
                        print("The URL download you provided is invalid.")
                        print("Please make sure it is a direct download link")
                        print("If you are still having issues please contact Evernow")
                        print("You can try inputing URL again.")

            else:
                advanced_options_dict["provideowngpuurl"] = []

        if num == "4":
            if advanced_options_dict["RemovePhysX"] == 0:
                advanced_options_dict["RemovePhysX"] = 1
            else:
                advanced_options_dict["RemovePhysX"] = 0

        if num == "5":
            if advanced_options_dict["disableinternetturnoff"] == 0:
                advanced_options_dict["disableinternetturnoff"] = 1
            else:
                advanced_options_dict["disableinternetturnoff"] = 0

        if num == "6":
            if advanced_options_dict["donotdisableoverclocks"] == 0:
                advanced_options_dict["donotdisableoverclocks"] = 1
            else:
                advanced_options_dict["donotdisableoverclocks"] = 0
        if num == "7":
            if advanced_options_dict["avoidspacecheck"] == 0:
                advanced_options_dict["avoidspacecheck"] = 1
            else:
                advanced_options_dict["avoidspacecheck"] = 0
        if num == "8":
            if advanced_options_dict["amdenterprise"] == 0:
                advanced_options_dict["amdenterprise"] = 1
            else:
                advanced_options_dict["amdenterprise"] = 0
        if num == "9":
            if advanced_options_dict["nvidiastudio"] == 0:
                advanced_options_dict["nvidiastudio"] = 1
            else:
                advanced_options_dict["nvidiastudio"] = 0
        if num == "10":
            if advanced_options_dict["dnsoverwrite"] == 0:
                advanced_options_dict["dnsoverwrite"] = 1
            else:
                advanced_options_dict["dnsoverwrite"] = 0
        if num == "11":
            if advanced_options_dict["pciidsfallback"] == 0:
                advanced_options_dict["pciidsfallback"] = 1
            else:
                advanced_options_dict["pciidsfallback"] = 0
        if num == "97":
            advanced_options_dict["changegpumode"] = ExtraArgument
        if num == "98":
            if advanced_options_dict["inteldriverassistant"] == 0:
                advanced_options_dict["inteldriverassistant"] = 1
            else:
                advanced_options_dict["inteldriverassistant"] = 0

        if num == "99":
            if advanced_options_dict["startedinsafemode"] == 0:
                advanced_options_dict["startedinsafemode"] = 1
            else:
                advanced_options_dict["startedinsafemode"] = 0
        f.seek(0)
        json.dump(advanced_options_dict, f, indent=4)
        f.truncate()
        logger("Advanced options is now " + str(advanced_options_dict))


def print_menu1():
    print('Press Enter Key -- Start normally', flush=True)
    print('2 -- I am changing my GPU', flush=True)
    print('3 -- Advanced Options', flush=True)
    print('4 -- Show LICENSE', flush=True)
    option = str(input('Enter your choice: '))
    if option == "2":
        change_AdvancedMenu('97', HandleChangingGPUProcess())
    if option == "3":
        AdvancedMenu()
    if option == "4":
      print(LICENSE)
      print_menu1()
      


def returnifduplicate():
    # TODO: If someone downloads this twice the process name will be "AutoDDU_CLI.exe (1) , which won't be caught by this
    processes = list()
    for process in wmi.WMI().Win32_Process():
        processes.append(process.Name)
    return processes.count("AutoDDU_CLI.exe") > 2


def BadLanguage():
    lang = wmi.WMI().Win32_OperatingSystem()[0].OSLanguage
    # https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/win32-operatingsystem
    ok_languages = [9, 1033, 2057, 3081, 4105, 5129, 6153, 7177, 8201, 10249, 11273]  # Basically all english versions
    logger("Language is " + str(lang))
    if lang in ok_languages:
        return False
    else:
        return True


def HandleOtherLanguages():
    # Due to some languages not having correct letters on their keyboards
    # Instead of doing the "I do" shit, we just have them press enter on their keyboards
    # twice. Much safer, since I assume every keyboard has this.. right?
    logger("Did other language workaround")
    howmany = 0
    while howmany < 2:
        input("Press your enter key {n} more time(s)".format(n=2 - howmany))
        howmany += 1
    print("Starting!")


def logger(log):
    # The goal is to log everything that is practical to log. 
    # I'm at the end of my rope! 
    # Why do I have to coach someone incompetent like you every single time?
    # I'm done with it! If you ever need help with anything else, please don't ask me!
    if not os.path.exists(Appdata_AutoDDU_CLI):
        os.makedirs(Appdata_AutoDDU_CLI)
    file_object = open(log_file_location, 'a+')
    file_object.write(datetime.now(timezone.utc).strftime("UTC %d/%m/%Y %H:%M:%S ") + str(log))
    file_object.write("\n")
    file_object.close()


def cleanup():
    try:
        shutil.rmtree(os.path.join(Appdata, "AutoDDU_CLI", "Drivers"))
        logger("Finished cleanup in cleanup()")
    except:
        logger("Failed to delete Drivers folder with error")
        logger(str(traceback.format_exc()))

    logger("Starting process of attempting to cleanup user folder")
    if os.path.exists(os.path.join(Users_directory, obtainsetting("ProfileUsed"))):
        if abs(int(time.time()) - os.path.getctime(os.path.join(Users_directory, obtainsetting("ProfileUsed")))) < 14400:
            if os.getlogin() != obtainsetting("ProfileUsed"):
                try:
                    subprocess.call('takeown /R /A /F "{}" /D N'.format(os.path.join(Users_directory, obtainsetting("ProfileUsed"))), shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                    time.sleep(1)
                    subprocess.call('icacls "{Profile}" /grant {Administrators}:F /T /C'.format(Profile=os.path.join(Users_directory, obtainsetting("ProfileUsed")), Administrators=AdminGroupName()), shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                    time.sleep(1)
                    subprocess.call('rmdir /S /Q "{}"'.format(os.path.join(Users_directory, obtainsetting("ProfileUsed"))), shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                    logger("Deleted {} folder".format(obtainsetting("ProfileUsed")))
                    
                except:
                    logger("Failed to delete {} folder in cleanup".format(obtainsetting("ProfileUsed")))
                    logger(str(traceback.format_exc()))
            else:
                logger("Was going to delete used {} profile but was logged in as user somehow".format(obtainsetting("ProfileUsed")))
        else:
            logger("Was going to delete used {} profile but was older than 4 hours".format(obtainsetting("ProfileUsed")))
    possible_error = ""
    try:
        possible_error = subprocess.Popen(
                    '{powershell} Remove-LocalUser -Name "{profile}"'.format(profile='BackupDDUProfile',powershell=powershelldirectory),
                    shell=True, check=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    creationflags=CREATE_NEW_CONSOLE).communicate()
    except:
        logger(str(possible_error))

    logger("Exited cleanup()")


def makepersist(CopyExecutablle):
    time.sleep(0.5)
    if CopyExecutablle == True:
        try:
            if os.path.exists(exe_location):
                os.remove(exe_location) 
                    
            shutil.copyfile(sys.executable, exe_location)    
            logger("Successfully copied executable to Appdata directory")
        except:
            logger("Falled back to downloading from github method for going to Appdata directory due to error: " + str(traceback.format_exc()))
            try:

                logger("Directory name of where executable is located is: " + str(os.path.dirname(sys.executable)))
                logger("Contents of directory are: " + str(os.listdir(os.path.dirname(sys.executable))))
            except:
                logger("Failed to log info about directory where sys.executable is located with error: " +  str(traceback.format_exc()))
            download_helper("https://raw.githubusercontent.com/Evernow/AutoDDU_CLI/main/signedexecutable/AutoDDU_CLI.exe", exe_location)
    try:
        # # make shortcut to the auto startup location, reason for this is we don't want to
        # # have an actual copy of the executable here since we have to delete this file to stop
        # # auto starts up from happening, and we can't delete ourselves. 
        # # Inspired by https://www.codespeedy.com/create-the-shortcut-of-any-file-in-windows-using-python/

        # # Update, this technically isn't needed anymore as of 0.1.1 because we instead use registry keys to
        # # automate startup. But I leave it in so we can fallback to deleting the shortcut instead of the registry key in case of error.
        # if os.path.exists(Script_Location_For_startup):
        #     os.remove(Script_Location_For_startup) 
        # shell = win32com.client.Dispatch("WScript.Shell")
        # shortcut = shell.CreateShortCut(Script_Location_For_startup)
        # shortcut.IconLocation = exe_location
        # shortcut.Targetpath = exe_location
        # shortcut.save()
        
        try:
            AutoStartupkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,"Software\Microsoft\Windows\CurrentVersion\RunOnce",0,winreg.KEY_ALL_ACCESS)
            winreg.DeleteValue(AutoStartupkey, '*AutoDDU_CLI')
        except:
            pass


        # Setup registry key to enable startup
        open = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,"Software\Microsoft\Windows\CurrentVersion\RunOnce",0,winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(open,"*AutoDDU_CLI",0,winreg.REG_SZ,exe_location)
        winreg.CloseKey(open)
    except:
        if insafemode() == True:
            print("Failed to enable the ability for AutoDDU to startup by itself")
            print("when out of safe mode.")
            print("When out of safe mode you will have to navigate to the following folder")
            print(str(Appdata_AutoDDU_CLI ))
            print("The executable will be located there. ProgramData is hidden by default,")
            print("if you have issues finding this ask about this.")
            print("We'll continue in 60 seconds.")
            logger("Failed to create shortcut for autostartup")
            logger(str(traceback.format_exc()))
            time.sleep(60)
        else:
            print("Failed to enable the ability for AutoDDU to startup by itself")
            print("when in safe mode. You'll have to start it manually in safe mode and")
            print("after safe mode outside of it in your normal profile.")
            print("The executable will be located on the desktop in safe mode, but")
            print("when out of safe mode you will have to navigate to the following folder")
            print(str(Appdata_AutoDDU_CLI ))
            print("The executable will be located there. ProgramData is hidden by default,")
            print("if you have issues finding this ask about this.")
            print("We'll continue in 60 seconds.")
            logger("Failed to create shortcut for autostartup")
            logger(str(traceback.format_exc()))
            time.sleep(60) 


    logger("Finished makepersist")


def autologin():
    #TODO this requires the hacky workaround of deleting the DDU user so it stops auto logging in.
    # https://superuser.com/questions/514265/set-user-for-auto-logon-on-windows-via-batch-script
    try:
        # https://docs.microsoft.com/en-us/troubleshoot/windows-server/user-profiles-and-logon/turn-on-automatic-logon
        Winlogon_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon')
        try: # This checks to see if someone has setup AutoLogin before, and warns them if it does
            checkthis = winreg.QueryValueEx(Winlogon_key, 'DefaultUserName')
            if checkthis[0] != None:
                print("If you have Windows setup so it auto logs")
                print("you into your user at boot up, you will have to ")
                print("set it up again yourself once everything is finished")
                print("We'll continue in 30 seconds.")
                print("")
                time.sleep(30)
        except: # Fails when key does not exist, aka when someone does not have AutoLogin setup on their own.
            pass
        
        winreg.SetValueEx(Winlogon_key, 'AutoAdminLogon', 0, winreg.REG_SZ, '1')

        winreg.SetValueEx(Winlogon_key, 'DefaultUserName', 0, winreg.REG_SZ, '{}'.format(obtainsetting("ProfileUsed")))

        winreg.SetValueEx(Winlogon_key, 'DefaultPassword', 0, winreg.REG_SZ, 'Evident@Omega@Winnings4@Matted@Swear@Handled')

        winreg.SetValueEx(Winlogon_key, 'AutoLogonCount', 0, winreg.REG_DWORD, '6')

        winreg.CloseKey(Winlogon_key)
        print("INFO: Successfully created autologin task")
        logger("Finished autologin successfully")
    except Exception as f:
        logger("Failed in autologin")
        logger(str(traceback.format_exc()))
        global login_or_not
        login_or_not = """
        You will need to login manually to the DDU
        profile account we created."""

def workaroundwindowsissues():
    subprocess.call('NET USER {profile} Evident@Omega@Winnings4@Matted@Swear@Handled'.format(profile=obtainsetting("ProfileUsed")), shell=True,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 
                        # Reason for password being complex is that gg5489 discovered that with gpo settings there are policies for what a password can be: https://activedirectorypro.com/how-to-configure-a-domain-password-policy/

    if insafemode():
        change_AdvancedMenu("99")
        logger("In Safemode while working around windows issues, falling back to Default folder copying method")
        try:
            time.sleep(0.5)
            if os.path.exists(os.path.join(Users_directory, "Default","Desktop", "AutoDDU_CLI.exe")):
                os.remove(os.path.join(Users_directory, "Default","Desktop", "AutoDDU_CLI.exe")) 
            shutil.copyfile(sys.executable, os.path.join(Users_directory, "Default","Desktop", "AutoDDU_CLI.exe"))
            logger("Successfully copied executable to new user")
        except:
            logger("Falled back to downloading from github method for going to new user folder due to error: " + str(traceback.format_exc()))
            try:
                logger("Directory of Users folder is: " + str(os.listdir(os.path.join(Users_directory))) )
                logger("Directory of Default User is: " + str(os.listdir(os.path.join(Users_directory,"Default"))) )
                logger("Directory name of where executable is located is: " + str(os.path.dirname(sys.executable)))
                logger("Contents of directory are: " + str(os.listdir(os.path.dirname(sys.executable))))

            except:
                logger("Trying to log directories in failure failed with error " + str(traceback.format_exc()))
            download_helper("https://raw.githubusercontent.com/Evernow/AutoDDU_CLI/main/signedexecutable/AutoDDU_CLI.exe",
                            os.path.join(Users_directory,"Default", "Desktop","AutoDDU_CLI.exe"))
    else:
        if os.path.exists(os.path.join(Users_directory,"Default","Desktop", "AutoDDU_CLI.exe")):
                os.remove(os.path.join(Users_directory,"Default","Desktop", "AutoDDU_CLI.exe"))
        try:
            time.sleep(0.5)
            if os.path.exists(os.path.join(Users_directory, "Default","Desktop", "AutoDDU_CLI.exe")):
                os.remove(os.path.join(Users_directory, "Default","Desktop", "AutoDDU_CLI.exe")) 
            shutil.copyfile(sys.executable, os.path.join(Users_directory, "Default","Desktop", "AutoDDU_CLI.exe"))
            logger("Successfully copied executable to new user")
        except:
            logger("Falled back to downloading from github method for going to new user folder due to error: " + str(traceback.format_exc()))
            try:
                logger("Directory of Users folder is: " + str(os.listdir(os.path.join(Users_directory))) )
                logger("Directory of Default User is: " + str(os.listdir(os.path.join(Users_directory,"Default"))) )
                logger("Directory name of where executable is located is: " + str(os.path.dirname(sys.executable)))
                logger("Contents of directory are: " + str(os.listdir(os.path.dirname(sys.executable))))

            except:
                logger("Trying to log directories in failure failed with error " + str(traceback.format_exc()))
            try:
                download_helper("https://raw.githubusercontent.com/Evernow/AutoDDU_CLI/main/signedexecutable/AutoDDU_CLI.exe",
                                os.path.join(Users_directory,"Default", "Desktop","AutoDDU_CLI.exe"))
            except:
                logger("Failed to also download to Default folder, going to back to old method.")
        if not os.path.exists(os.path.join(Users_directory,"Default","Desktop", "AutoDDU_CLI.exe")):
        ### Old Approach but unfortunately Kaspersky (and like others) did not like PSTools. Now only here as a backup because people always seem to do fucky things with crap like this.
            logger("Fell back to old (word that must not be spoken) logic because this idiot did something to his user folders, probably some 'But I don't use these folders so lemme delete them' mentality")
            # TODO: I think Kaspersky fucking searches for the presence of the word "PSTools" and blocks executable if it does.. so uhm.. maybe encrypt string then decrypt if we hit this code path?
            download_helper("https://download.sysinternals.com/files/PSTools.zip",
                            os.path.join(Appdata_AutoDDU_CLI, "PsTools.zip"))
            with zipfile.ZipFile(os.path.join(Appdata_AutoDDU_CLI, "PsTools.zip")) as zip_ref:
                zip_ref.extractall(os.path.join(Appdata_AutoDDU_CLI, "PsTools"))
            try:
                subprocess.call(
                    '{directory_to_exe} -accepteula -u {profile} -p Evident@Omega@Winnings4@Matted@Swear@Handled i- exit'.format(profile=obtainsetting("ProfileUsed"),
                                                                                        directory_to_exe=os.path.join(
                                                                                            Appdata_AutoDDU_CLI, "PsTools",
                                                                                            "PsExec.exe")), shell=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass  

            logger("Did prep work for working around Windows issue")
            try:
                time.sleep(0.5)
                if os.path.exists(os.path.join(Users_directory, "{}".format(obtainsetting("ProfileUsed")), "Desktop", "AutoDDU_CLI.exe")):
                    os.remove(os.path.join(Users_directory, "{}".format(obtainsetting("ProfileUsed")), "Desktop", "AutoDDU_CLI.exe")) 
                shutil.copyfile(sys.executable, os.path.join(Users_directory, "{}".format(obtainsetting("ProfileUsed")), "Desktop", "AutoDDU_CLI.exe"))
                logger("Successfully copied executable to new user")
            except:
                logger("Falled back to downloading from github method for going to new user folder due to error: " + str(traceback.format_exc()))
                try:
                    logger("Directory of Users folder is: " + str(os.listdir(os.path.join(Users_directory))) )
                    logger("Directory of Default User is: " + str(os.listdir(os.path.join(Users_directory,"{}".format(obtainsetting("ProfileUsed"))))) )
                    logger("Directory name of where executable is located is: " + str(os.path.dirname(sys.executable)))
                    logger("Contents of directory are: " + str(os.listdir(os.path.dirname(sys.executable))))

                except:
                    logger("Trying to log directories in failure failed with error " + str(traceback.format_exc()))

                download_helper("https://raw.githubusercontent.com/Evernow/AutoDDU_CLI/main/signedexecutable/AutoDDU_CLI.exe",
                                os.path.join(Users_directory, "{}".format(obtainsetting("ProfileUsed")), "Desktop", "AutoDDU_CLI.exe"))
    
    # This was old approach, leaving here for now incase we need a failback one day.

    #     from subprocess import CREATE_NEW_CONSOLE

    # # Windows does not create the folders of a user until you login: https://community.spiceworks.com/topic/247395-create-a-user-profile-without-logon
    # # This basically adds a 1234 password to the previously created DDU account, then logins in via command line so Windows is forced to create the directories.
    # # After this we can download the .exe to the desktop folder of the account.

    # # So here I am basically stuck between a rock and a hard place.

    # # I can either do the fairly risky workaround of this: https://superuser.com/questions/154686/autostart-program-in-safe-mode
    # # Which involves directly editing how Windows behaves at boot to make it launch AutoDDU even in safe mode automatically

    # # Or fiddle around with the above, but that introduces another serious problem, Windows designers are a bunch of retards and did this: 
    # # https://stackoverflow.com/questions/16107381/how-to-complete-the-runas-command-in-one-line

    # # So now what do I do? I think this is the least worst option. Seriously, fuck you Microsoft.
    # subprocess.call('NET USER DDU 1234 ', shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, creationflags=CREATE_NEW_CONSOLE)

    # child = wexpect.spawn('runas /env /profile /user:DDU cmd.exe', timeout=120)
    # time.sleep(5)
    # child.sendline("1234")
    # child.send('\r')

    # time.sleep(5) 
    # child.sendline('exit')
    # subprocess.call('NET USER "DDU" ""', shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

    # print("INFO: Successfully ran background task")
    # TODO: this is dumb

    # TODO: investigate this workaround later: https://community.spiceworks.com/topic/247395-create-a-user-profile-without-logon?page=1#entry-6915365




def PCIID(vendor, device):
    download_helper("https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/PCI-IDS.json", os.path.join(Jsoninfofileslocation,'PCI-IDS.json'),False)
    with open(os.path.join(Jsoninfofileslocation,'PCI-IDS.json')) as json_file:
        data = json.load(json_file)
    try:
        return data[vendor]['devices'][device]['name']
    except KeyError:
        return None

def getgpuinfos(testing=None):
    controllers = wmi.WMI().Win32_VideoController()
    gpu_dictionary = dict()  # GPU NAME = [VENDOR ID, DEVICE ID, ARCHITECTURE , RAW OUTPUT (for troubleshooting purposes), supportstatus (0=unchecked, 1=supported, 2=kepler, 3=fermiprof, 4=EOL), professional/consumer]
    logger("Working in getgpuinfos with this wmi output: ")
    for controller in controllers:
        name = controller.wmi_property('Name').value.encode("ascii", "ignore").decode("utf-8")
        gpu_list_to_parse = controller.wmi_property('PNPDeviceID').value.encode("ascii", "ignore").decode(
            "utf-8").lower().split("\\")  # .lower() is due to Windows not following PCI naming convention.
        logger(name)
        logger(''.join(gpu_list_to_parse))
        for gpu in gpu_list_to_parse:
            # We need to filter out by vendor or else we can parse in shit like Citrix or capture cards.
            if "dev_" in gpu and ("ven_10de" in gpu or "ven_121a" in gpu or "ven_8086" in gpu
                                  or "ven_1002" in gpu):  # 1002 = AMD ; 8086 = Intel ; 10de = NVIDIA ; 121a = Voodoo (unlikely but I mean.. doesn't hurt?)

                # Us assuming a ven and dev ID is 4 characters long is a safe one: https://docs.microsoft.com/en-us/windows-hardware/drivers/install/identifiers-for-pci-devices
                Arch = PCIID(gpu[gpu.find('ven_') + 4:gpu.find('ven_') + 8],
                             gpu[gpu.find('dev_') + 4:gpu.find('dev_') + 8])
                if Arch != None and '[' in Arch and ']' in Arch:
                    logger("Got more accurate name from PCI-IDS")
                    name = Arch[Arch.find('[')+1:Arch.find(']')]
                else:
                    logger("Depending on Windows giving us correct GPU name")
                if Arch != None:
                    Arch = Arch[:Arch.find(' ')]
                Vendor_ID = gpu[gpu.find('ven_') + 4:gpu.find('ven_') + 8]
                Device_ID = gpu[gpu.find('dev_') + 4:gpu.find('dev_') + 8]
                if Arch == None: # Can happen when we're dealing with a new GPU release that may not be in the database yet.
                    Arch = "Unknown"
                gpu_dictionary[name] = [Arch, Vendor_ID, Device_ID] # overwriting by name is fine, helps us filter out SLI setups early on
    if testing != None:
        gpu_dictionary = testing
    logger(str(gpu_dictionary))
    return gpu_dictionary

def GetGPUStatus(testing=None):
    # testing = {'GeForce RTX 3080': ['GA102', '10DE', '2206']}
    GPUZOutPut = GPUZINFO()
    if len(GPUZOutPut) < 1 or testing != None:
        DictOfGPUs = getgpuinfos(testing)
    else:
        DictOfGPUs = GPUZOutPut
    # NVIDIA Support status loading
    time.sleep(1)
    download_helper("https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/nvidia_gpu.json", os.path.join(Jsoninfofileslocation,'nvidia_gpu.json'),False)
    with open(os.path.join(Jsoninfofileslocation,'nvidia_gpu.json')) as json_file:
        nvidia_gpu = json.load(json_file)

    # AMD Support status loading
    time.sleep(1)
    download_helper("https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/amd_gpu.json", os.path.join(Jsoninfofileslocation,'amd_gpu.json'),False)
    with open(os.path.join(Jsoninfofileslocation,'amd_gpu.json')) as json_file:
        amd_gpu = json.load(json_file)

    # Intel Support status loading
    time.sleep(1)
    download_helper("https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/intel_gpu.json", os.path.join(Jsoninfofileslocation,'intel_gpu.json'),False)
    with open(os.path.join(Jsoninfofileslocation,'intel_gpu.json')) as json_file:
        intel_gpu = json.load(json_file)

    list_of_gpu_downloads = []
    for GPU in DictOfGPUs:
        logger("Handling GPU " + str(GPU))
        if DictOfGPUs[GPU][1].lower() == '10de': # NVIDIA 
            driver = None
            lastpriority = 99
            for possibledriver in nvidia_gpu:
                if DictOfGPUs[GPU][2].upper() in nvidia_gpu[possibledriver]['SupportedGPUs'] and int(nvidia_gpu[possibledriver]['priority']) < lastpriority:
                    
                    driver = nvidia_gpu[possibledriver]['link']
                    logger("Applicable GPU driver is " + driver )
                    lastpriority = int(nvidia_gpu[possibledriver]['priority'])
            if driver == None and DictOfGPUs[GPU][0] not in EOL_NVIDIA:
                logger("Not end of life and not in known drivers, trying GFE backend")
                # '1BE0_10DE'
                try:
                    driver = FindOutOfBranchDriver(DictOfGPUs[GPU][2].upper() + '_' + DictOfGPUs[GPU][1].upper())
                except:
                    logger("Issue with GFE backend, following error")
                    logger(str(traceback.format_exc()))
                if checkifvaliddownload(driver) == False:
                    logger("Driver provided by GFE is invalid, it is " + str(driver))
                    driver = None
            if obtainsetting('nvidiastudio') == 1 and DictOfGPUs[GPU][2].upper() in nvidia_gpu['consumer_studio']['SupportedGPUs']:
                driver = nvidia_gpu['consumer_studio']['link']
                logger("User asked for studio driver and it is supported, providing it.")
            if driver == None:
                logger("No known GPU driver found, assuming end of life")

                return "Unsupported"
            if driver not in list_of_gpu_downloads:
                list_of_gpu_downloads.append(driver)

        if DictOfGPUs[GPU][1].lower() == '1002': # AMD 
            driver = None
            lastpriority = 99
            for possibledriver in amd_gpu:
                if DictOfGPUs[GPU][2].upper() in amd_gpu[possibledriver]['SupportedGPUs'] and int(amd_gpu[possibledriver]['priority']) < lastpriority:
                    
                    driver = amd_gpu[possibledriver]['link']
                    logger("Applicable GPU driver is " + driver )
                    lastpriority = int(amd_gpu[possibledriver]['priority'])
            if obtainsetting('amdenterprise') == 1 and DictOfGPUs[GPU][2].upper() in amd_gpu['professional']['SupportedGPUs']:
                logger("User asked for professional driver and it is supported, providing it.")
                driver = amd_gpu['professional']['link']
            if driver == None:
                logger("No known GPU driver found, assuming end of life")
                return "Unsupported"
            if driver not in list_of_gpu_downloads:
                list_of_gpu_downloads.append(driver)
        if DictOfGPUs[GPU][1].lower() == '8086': # Intel 
            driver = None
            lastpriority = 99
            for possibledriver in intel_gpu:
                if DictOfGPUs[GPU][2].upper() in intel_gpu[possibledriver]['SupportedGPUs'] and int(intel_gpu[possibledriver]['priority']) < lastpriority:
                    
                    driver = intel_gpu[possibledriver]['link']
                    logger("Applicable GPU driver is " + driver )
                    lastpriority = int(intel_gpu[possibledriver]['priority'])
            if driver == None:
                logger("No known GPU driver found, assuming end of life")
                return "Unsupported"
            if driver not in list_of_gpu_downloads:
                list_of_gpu_downloads.append(driver)
    
    # Checks to make sure we aren't installing multiple different drivers from the same vendor. 
    # This prevents configs like Consumer and Quadros being together which is unsupported: https://nvidia.custhelp.com/app/answers/detail/a_id/2280/~/can-i-use-a-geforce-and-quadro-card-in-the-same-system%3F

    intel = 0
    amd = 0
    nvidia = 0
    for driverdownloadlink in list_of_gpu_downloads:
        if 'intel' in driverdownloadlink.lower():
            intel += 1
            if intel > 1:
                return "Unsupported"
        if 'amd' in driverdownloadlink.lower():
            amd += 1
            if amd > 1:
                return "Unsupported"
        if 'nvidia' in driverdownloadlink.lower():
            nvidia += 1
            if nvidia > 1:
                return "Unsupported"
    stringtouser = "Performing DDU on the following GPUs: "
    for gpuname in DictOfGPUs:
        stringtouser += gpuname + " (" + DictOfGPUs[gpuname][0] + ') \n'
    if len(list_of_gpu_downloads) == 0:
        stringtouser = """
WARNING: NO GPUS HAVE BEEN DETECTED BY WINDOWS.
THIS PROCESS WILL CONTINUE BUT YOU WILL NEED TO
INSTALL DRIVERS MANUALLY YOURSELF AFTER THIS PROCESS 
IS OVER. 
        
PLEASE REPORT THIS TO EVERNOW IF IT IS A BUG.
        
Chika is mad and confused at the same time."""
    return stringtouser ,list_of_gpu_downloads





# This keeps track of where we are in the process in a text file. 
def changepersistent(num):
    logger("Changing persistent file to: " + str(num))
    open(Persistent_File_location, 'w').close()
    with open(Persistent_File_location, 'r') as file:
        data = file.readlines()

    data.append(str(num))
    with open(Persistent_File_location, 'w') as file:
        file.writelines(data)


def getpersistent():
    try:
        with open(Persistent_File_location) as f:
            lines = f.read()
            first = lines.split('\n', 1)[0]
            logger("Got persistent file to be " + str(first))
            return int(first)
    except:
        logger("Tried to get persistent file but did not exist or failed")
        return -1


def BackupProfile():
    try:
        if len(obtainsetting("ProfileUsed")) > 19:
            # https://docs.microsoft.com/en-us/troubleshoot/windows-server/identity/net-add-not-support-names-exceeding-20-characters
            print("You have too many DDU profile folders in C:\\Users.")
            print("Please delete user profiles in settings and then also")
            print("their respective user folders tyvm")
            print("Once you did that close this and then reopen.")
            while True:
                time.sleep(1)
        firstcommand = "net user /add {profile}".format(profile=obtainsetting("ProfileUsed"))
        secondcommand = "net localgroup {administrators} {profile} /add".format(profile=obtainsetting("ProfileUsed"),administrators=AdminGroupName())
        subprocess.run(firstcommand, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger("Running command to add created to user to administrators")
        subprocess.run(secondcommand, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger("Successfully created DDU account")
        print("INFO: Created backup profile")
        logger("Created backup profile")
    except Exception as f:
        print("INFO: Did not create backup profile (not an error)")
        logger("Failed creating backup profile with error: " + str(f))
        logger("Failed to create DDU account, likely already existed")

def download_helper(url, fname,showbar=True,RecursionDepth=0,verify=True,skip_download=False):
    if RecursionDepth > 10:
        # A precaution against endless recursion which could potentially happen if the certificate workaround doesn't work correctly.
        logger('Hit max recursion depth, something has gone wrong. Terminating.')
        raise Exception("Hit max recursion depth when attempting to download something, here lies hell. ") 
    logger(f'Downloading file {url} to {fname} with arguments {str([showbar,RecursionDepth, verify])}')
    if skip_download == False:
        while not internet_on():
            logger("Saw no internet, asking user to connect")
            print("No internet connection")
            print("Please make sure internet is enabled")
            print("Retrying in 30 seconds")
            time.sleep(30)
    if showbar==True:
        print("Downloading file {}".format(fname.split("\\")[-1]))
    remaining_download_tries = 16
    SecurityVerification = verify
    while remaining_download_tries > 0:
        try:
            if os.path.exists(fname):
                os.remove(fname)
            with open(fname, "wb")  as download_file:
                if (remaining_download_tries % 3 == 0 or obtainsetting('dnsoverwrite') == 1) : 
                    # For bad DNS issues encountered on NVIDIA server, very rare but never hurts to have a fallback for this event.
                    # Credit to RandoNando for figuring this out, and the referenced GitHub issues for the issues I encountered while testing this.
                    logger("Landed in DNSFallback")
                    HOST = urllib.parse.urlsplit(url)[1]
                    PATH = urllib.parse.urlsplit(url)[2]
                    QUERY = urllib.parse.urlsplit(url)[3] # Used by Microsoft updater URLs
                    logger(f'Parsed from URL {HOST} and {PATH} and {QUERY}')
                    res = dns.resolver.Resolver()
                    res.nameservers = ['8.8.8.8'] # Google DNS
                    answers = res.resolve(HOST)
                    for rdata in answers:
                        address = (rdata.address)
                    logger("Got the folloing IP address from resolver " + str(address))
                    if QUERY == '':
                        url_dnsfallback = (f'http://{address}{PATH}')
                    else:
                        url_dnsfallback = (f'http://{address}{PATH}?{QUERY}') # Not entirely sure if this is universal persay, but it's used by Microsoft's update domain which is the only one that uses this.
                    logger(url_dnsfallback)
                    if 'amd.com' in url.lower():
                        headers = dict( [
                                    ("User-agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",),
                                    ("Referer", "https://www.amd.com/en/support/graphics/amd-radeon-6000-series/amd-radeon-6700-series/amd-radeon-rx-6700-xt",),
                                    ("Host", HOST), # https://github.com/python/cpython/issues/96287 I have not looked into the implications of this when using httpx now, but if it ain't broke don't fix it right?
                                    ("test", "test"),
                                ]
                            )
                    else:
                        headers = dict( [
                                    ("User-agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",),
                                    ("Host", HOST), # https://github.com/python/cpython/issues/96287 I have not looked into the implications of this when using httpx now, but if it ain't broke don't fix it right?
                                    ("test", "test"),
                                ]
                            )
                    httpx_arguments = httpx.stream("GET", url_dnsfallback,verify=False,headers=headers,follow_redirects=True)
                elif 'amd.com' in url.lower():
                    headers = dict( [
                                ("User-agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",),
                                ("Referer", "https://www.amd.com/en/support/graphics/amd-radeon-6000-series/amd-radeon-6700-series/amd-radeon-rx-6700-xt",),
                            ]
                        )
                    httpx_arguments = httpx.stream("GET", url,verify=SecurityVerification, headers=headers,follow_redirects=True)
                else:
                    headers = dict( [
                                ("User-agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",),
                            ]
                        )
                    httpx_arguments = httpx.stream("GET", url,verify=SecurityVerification, headers=headers,follow_redirects=True)
                with httpx_arguments as response:
                    total = int(response.headers["Content-Length"])
                    progress = tqdm(total=total, unit_scale=True, unit_divisor=1024, unit="B", disable=not showbar)
                    if skip_download == False:
                        num_bytes_downloaded = response.num_bytes_downloaded
                        for chunk in response.iter_bytes():
                            download_file.write(chunk)
                            progress.update(response.num_bytes_downloaded - num_bytes_downloaded)
                            num_bytes_downloaded = response.num_bytes_downloaded
            break
        except Exception as e:
            SecurityVerification = verify
            logger(f'Failed to download {url} with error {str(traceback.format_exc())} and have {str(remaining_download_tries)} remaining attempts')
            if 'certificate' in str(e).lower():
                download_helper('https://curl.se/ca/cacert.pem', os.path.join(Appdata_AutoDDU_CLI,'cacert.pem'),False,RecursionDepth+1,False)
                SecurityVerification = os.path.join(Appdata_AutoDDU_CLI,'cacert.pem')
            remaining_download_tries -= 1
            print("Download failed, retrying in 5 seconds")
            time.sleep(5)
    logger("Successfully finished download")


def download_drivers(list_to_download):
    if os.path.exists(os.path.join(Appdata, "AutoDDU_CLI", "Drivers\\")):
        shutil.rmtree(os.path.join(Appdata, "AutoDDU_CLI", "Drivers\\"))
    os.makedirs(os.path.join(Appdata, "AutoDDU_CLI", "Drivers\\"))
    for driver in list_to_download:
        url = driver.rstrip()  # Newline character is grabbed sometimes
        if "intel.com" in url.lower() and obtainsetting("inteldriverassistant") == 1:
            fileextension = "inteldriver.exe"
        else:
            fileextension = url.split("/")[-1]
        
        download_helper(url, os.path.join(Appdata, "AutoDDU_CLI", "Drivers\\", fileextension))



def ddu_download():
    if os.path.exists(ddu_extracted_path) and os.path.isdir(ddu_extracted_path):
        shutil.rmtree(ddu_extracted_path)
    if not os.path.exists(os.path.join(root_for_ddu_assembly)):
        os.makedirs(os.path.join(root_for_ddu_assembly))

    download_helper(
            'https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/DDU.exe',
            ddu_zip_path
        )


    download_helper("https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/DDUVersion.json", os.path.join(Jsoninfofileslocation,'DDUVersion.json'),False)
    with open(os.path.join(Jsoninfofileslocation,'DDUVersion.json')) as json_file:
        data = json.load(json_file)

    Latest_DDU_Version_Raw = data['version']

    if not os.path.exists(ddu_extracted_path):
        os.makedirs(ddu_extracted_path)
    ExtractDDUOutput = subprocess.run((ddu_zip_path + " -o{}".format(ddu_extracted_path) + " -y"), shell=True, check=True,
                 capture_output=True)
    logger("Output of extracting DDU " + str(ExtractDDUOutput))
    # Moves everything one directory up, mainly just to avoid crap with versioning, don't want to have to deal with
    # version numbers in the DDU method doing the command calling.
    where_it_is = os.path.join(ddu_extracted_path, "DDU v{}".format(Latest_DDU_Version_Raw))
    file_names = os.listdir(where_it_is)

    for file_name in file_names:
        shutil.move(os.path.join(where_it_is, file_name), ddu_extracted_path)


def latest_windows_version(majorversion):
    download_helper("https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/WindowsReleases.json", os.path.join(Jsoninfofileslocation,'WindowsReleases.json'),False)
    with open(os.path.join(Jsoninfofileslocation,'WindowsReleases.json')) as json_file:
        WindowsReleases = json.load(json_file)
    return max(WindowsReleases[majorversion])


def uptodate():
    # TODO: Switch to platform.release() once this is fixed: https://bugs.python.org/issue45382
    current_major_version = wmi.WMI().Win32_OperatingSystem()[0].Caption.encode("ascii", "ignore").decode(
            "utf-8")
    if "8" in current_major_version or "7" in current_major_version:  # AutoDDU only works on Windows 10 and above.
        logger("Got a Windows {} user".format(current_major_version))
        print("AutoDDU only works on Windows 10 and above. Updating you to Windows 10.")
        download_helper('https://go.microsoft.com/fwlink/?LinkId=691209',
                            os.path.join(Appdata, "MicrosoftUpdater.exe"))
        print("This window will now open the Microsoft Update Assistant to help you update to the latest version.",
                  flush=True)
        print("Once it is done you will have to restart, it should restart automatically when it is done.",
                  flush=True)
        print("If it doesn't, restart yourself. Once you are booted back up you open this utility again.",
                  flush=True)
        print("Update assistant will open in 15 seconds.")
        time.sleep(15)
        subprocess.run(Appdata + "\\MicrosoftUpdater.exe /auto upgrade /eula accept",
                           shell=True, check=True)
        print("You need to restart after Update Assistant is finished, then once logged back in open this again.",
                  flush=True)
        changepersistent(1)
        while True:
            time.sleep(1)
    elif "10" in current_major_version:  
        logger(
            "Going to be comparing {current} to {believedlatest}".format(current=str(platform.version().split('.')[2]),
                                                                         believedlatest=str(latest_windows_version("10"))))
        if int(platform.version().split('.')[2]) >= int(
                latest_windows_version("10")):  # We should consider insider builds. But that's outside the scope of v1 at least.
            print("System up to date already", flush=True)
            logger("I believe it is up to date")

        else:
            HandlePendingUpdates() # Unsure if we should even be doing this here but in main(), but I have to do more testing, and it is hard to reproduce the updating issues locally, so we'll need more guinea pigs.
            logger("I do not believe it is up to date")
            print("System is out of date, downloading Microsoft Update Assistant.", flush=True)
            download_helper('https://go.microsoft.com/fwlink/?LinkID=799445',
                            os.path.join(Appdata, "MicrosoftUpdater.exe"))
            print("This window will now open the Microsoft Update Assistant to help you update to the latest version.",
                  flush=True)
            print("Once it is done you will have to restart, it should restart automatically when it is done.",
                  flush=True)
            print("If it doesn't, restart yourself. Once you are booted back up you open this utility again.",
                  flush=True)
            print("Update assistant will open in 15 seconds.")
            time.sleep(15)
            subprocess.run(Appdata + "\\MicrosoftUpdater.exe /auto upgrade /passive /warnrestart:30 /skipeula",
                           shell=True, check=True)
            print("You need to restart after Update Assistant is finished, then once logged back in open this again.",
                  flush=True)
            makepersist(True) # So it auto starts up on restart so idiots don't think AutoDDU is done. Has happened twice, fucking dumbasses
            changepersistent(1)
            while True:
                time.sleep(1)
    elif "11" in current_major_version: # No update assistant for W11 yet afaik
        print("Windows already up to date")
        changepersistent(1)
    elif int(platform.version().split('.')[2]) > latest_windows_version("10"):
        logger("No idea what version of Windows it is but is later than latest Windows with " + str(platform.version().split('.')[2]))
    else:
        print("Something catastrophically went wrong. Cannot detect Windows version.")
        while True:
            time.sleep(1)

def disable_clocking():
    try:
        subprocess.call(
            '{powershell}  Unregister-ScheduledTask -TaskName "MSIAfterburner" -Confirm:$false'.format(powershell=powershelldirectory),
            shell=True, creationflags=CREATE_NEW_CONSOLE)
    except:
        pass
    try:
        subprocess.call(
            r'{powershell}  Remove-Item -Path HKLM:\SYSTEM\CurrentControlSet\Services\RTCore64'.format(powershell=powershelldirectory),
            shell=True, creationflags=CREATE_NEW_CONSOLE)
    except:
        pass
    try:
        subprocess.call(
            r'{powershell} Unregister-ScheduledTask -TaskName "EVGAPrecisionX" -Confirm:$false'.format(powershell=powershelldirectory),
            shell=True, creationflags=CREATE_NEW_CONSOLE)
    except:
        pass
    try:
        subprocess.call(
            r'{powershell} Unregister-ScheduledTask -TaskName "GPU Tweak II" -Confirm:$false'.format(powershell=powershelldirectory),
            shell=True, creationflags=CREATE_NEW_CONSOLE)
    except:
        pass
    try:
        subprocess.call(
            r'{powershell} Unregister-ScheduledTask -TaskName "Launcher GIGABYTE AORUS GRAPHICS ENGINE" -Confirm:$false'.format(powershell=powershelldirectory),
            shell=True, creationflags=CREATE_NEW_CONSOLE)
    except:
        pass


def safemode(ONorOFF):
    if ONorOFF == 1:
        subprocess.call('bcdedit /set {default} safeboot minimal', shell=True, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        logger("Ran command to enable safe mode")
    if ONorOFF == 0:
        subprocess.call('bcdedit /deletevalue {default} safeboot', shell=True, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        logger("Ran command to disable safe mode")

def DDUCommands():
    if insafemode() == True:
        if obtainsetting('RemovePhysX') == 0:
            subprocess.run([os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe'), '-silent', '-RemoveMonitors',
                            '-RemoveVulkan', '-RemoveGFE', '-Remove3DTVPlay', '-RemoveNVCP', '-RemoveNVBROADCAST',
                            '-RemoveNvidiaDirs', '-cleannvidia', '-logging'],check=True)
        else:
            subprocess.run([os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe'), '-silent', '-RemoveMonitors',
                            '-RemoveVulkan', '-RemoveGFE', '-Remove3DTVPlay', '-RemoveNVCP', '-RemoveNVBROADCAST',
                            '-RemoveNvidiaDirs', '-cleannvidia', '-RemovePhysx', '-logging'],check=True)
        print("1/3 finished with DDU", flush=True)
        sys.stdout.flush()
        subprocess.run([os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe'), '-silent', '-RemoveMonitors',
                        '-RemoveVulkan', '-RemoveAMDDirs', '-RemoveCrimsonCache', '-RemoveAMDCP', '-cleanamd', '-logging'],check=True)
        print("2/3 finished with DDU", flush=True)
        sys.stdout.flush()
        subprocess.run([os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe'), '-silent', '-RemoveMonitors',
                        '-RemoveVulkan', '-RemoveINTELCP', '-cleanintel', '-logging'],check=True)
        print("3/3 finished with DDU", flush=True)
        sys.stdout.flush()
        logger("Successfully finished DDU commands in safe mode.")
    else:
        logger("Somehow failed in DDUCOmmands due to not in safe mode?")
        logger(str(wmi.WMI().Win32_ComputerSystem()[0].BootupState.encode("ascii", "ignore").decode(
            "utf-8")))
        print("Something catastrophically went wrong.")
        print("Somehow tried to run DDU not in safe mode.")
        print("Resetting all settings to default, please run again.")
        print("If actually in safe mode, something is wrong with check, please sent this to Evernow:")
        print(str(wmi.WMI().Win32_ComputerSystem()[0].BootupState.encode("ascii", "ignore").decode(
            "utf-8")))
        cleanup()
        try:
            os.remove(Script_Location_For_startup)
        except:
            pass
        changepersistent(0)


def enable_internet(enable):
# https://stackoverflow.com/questions/59668995/how-do-i-discover-pci-information-from-an-msft-netadapter
# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/hh968170(v=vs.85)
    if obtainsetting("disableinternetturnoff") == 0:
        wrxAdapter = wmi.WMI( namespace="StandardCimv2").query("SELECT * FROM MSFT_NetAdapter") 
        logger("In enable_internet with argument to " + str(enable))
        list_of_names = list()
        list_test = list()
        for adapter in wrxAdapter:
            list_of_names.append(adapter.Name)
            if adapter.Virtual == False and adapter.LinkTechnology != 10:
                try:
                    if enable == False:
                        if adapter.State == 2:
                            adapter.Disable()
                            list_test.append(str(adapter.Name))
                            logger("Successfully disabled this : " + str(adapter.Name))
                    else:
                        if str(adapter.Name) in obtainsetting("disabledadapters"):
                                logger("Successfully enabled this : " + str(adapter.Name))
                                adapter.Enable()
                except:
                    logger("Got exception in enable_internet when trying something with " + adapter.Name)
                    logger(str(traceback.format_exc()))
                    pass
        if not enable:
            with open(AutoDDU_CLI_Settings, 'r+') as f:
                advanced_options_dict = json.load(f)
                advanced_options_dict["disabledadapters"] = list_test
                f.seek(0)
                json.dump(advanced_options_dict, f, indent=4)
                f.truncate()
        logger("Working with these adapters in enable_internet")
        logger(str(list_of_names))

# def RequestTimefromNtp(addr='pool.ntp.org'):
#     REF_TIME_1970 = 2208988800  # Reference time
#     client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     data = b'\x1b' + 47 * b'\0'
#     client.sendto(data, (addr, 123))
#     data, address = client.recvfrom(1024)
#     if data:
#         t = struct.unpack('!12I', data)[10]
#         t -= REF_TIME_1970
#     return t


# For testing you pass in a list with
# [{'NVIDIA GeForce RTX 3080': ['GA102', '10de', '2206']}, []]
#                   GPU infos                           , 
def mainpain(TestEnvironment):

    print(TestEnvironment)
    # Wine Easter Egg
    # try: # Tries to open key only present when running under Wine
    #     aKey = winreg.OpenKey(winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER), r"Software\Wine", 0, winreg.KEY_READ)

    #     subprocess.run("winebrowser https://funny.computer/linux/", shell=True) # Nobody actually installs IE in their prefixes right?
    #     print("Someone actually ran this on Linux lol")
    #     while True:
    #         time.sleep(1)
    # except:
    #     pass
    if len(TestEnvironment) == 0:
        os.system('mode con: cols=80 lines=40')
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x00|0x100))
        accountforoldcontinues(0)
    else:
        accountforoldcontinues(1)
    myapp = singleinstance()
    sys.stdout.flush()
    print("This software comes with no warranty as stated in the MIT License.")
    print("Copyright (c) 2022-present Daniel Suarez")
    print("\n", flush=True)
    if myapp.alreadyrunning():
            print(r"""
THERE IS A POSSIBILITY YOU OPENED THIS MORE THAN ONCE BY ACCIDENT. PLEASE 
CLOSE THIS WINDOW AS IT IS VERY RISKY TO HAVE MORE THAN ONE OPEN.                  
                  """)
            while True:
                time.sleep(1)

    try:
        if getpersistent() != 2 and os.getlogin() == obtainsetting("ProfileUsed"):
            logger("User logged into DDU profile early for some reason.")
            print("You logged into the DDU profile too early, you only log into it")
            print("When AutoDDU either auto logs you in or says it will.")
            print("Get out of this profile then login to your main one.")
            while True:
                time.sleep(1)
    except: # obtainsetting when unset will error out
        logger("Expected first failure to check if user is in incorrect profile, this means we're good.") 
    checkBatteryLevel()
    if not os.path.exists(Jsoninfofileslocation):
        os.mkdir(Jsoninfofileslocation)
    try:
        logger("Version " + Version_of_AutoDDU_CLI)
        logger("Running under user {}".format(os.getlogin()))
        try:
            LogBasicSysInfo()
        except:
            logger("Failed to capture all sysinfo with this error:")
            logger(str(traceback.format_exc()))    
        try:
            logger("Directory name of where executable is located is: " + str(os.path.dirname(sys.executable)))
            logger("Contents of directory contain executable: " + str("AutoDDU_CLI.exe" in os.listdir(os.path.dirname(sys.executable)))  )
        except:
            logger("Failed to log info about directory where sys.executable is located with error: " +  str(traceback.format_exc()))
                
        if not os.path.exists(Persistent_File_location) or getpersistent() == -1 or getpersistent() == 0:
            default_config()
            if not insafemode():
                if internet_on():
                    try:
                        handleoutofdate()
                    except:
                        logger("Failed to check if up to date with error " + str(traceback.format_exc()) )

            if len(TestEnvironment) == 0:
                TestForStupidityPart43() # Checks to make sure user isn't running this raw (ie outside of a pyinstaller exe)
                TestMultiprocessing() # Check to make sure multipricessing works correctly.
                if not internet_on() and insafemode(): 
                    # There is a code path for handling this in safe mode when we have an internet connection. It's when there's not an internet connection that we have a problem.
                    print("You DO NOT RUN AUTODDU IN SAFE MODE THE FIRST TIME. WE ALSO NEED AN INTERNET CONNECTION.")
                    print("AutoDDU should be first launched outside of safe mode in a normal user profile LIKE THE WIKI SAYS TO.")
                    print("AutoDDU will put itself in safe mode when it needs to, stop assuming and")
                    print("instead read the wiki you were sent.")
                    print("Get out of safe mode if you're in it, login to the user profile you always use THEN LAUNCH THIS.")
                    print("MAKE SURE TO HAVE AN INTERNET CONNECTION")
                    while True:
                        time.sleep(1)
                elif not internet_on():
                    print("We are unable to connect to the internet.")
                    print("Make sure your system time is setup correctly (including time zone)")
                    print("And also make sure that of course you have an internet connection.")
                    print("We need an internet connection up to a certain point (at which point we will disable the internet ourselves)")
                    print("We're going to stop, once you figure out why you don't have internet close this then reopen")
                    while True:
                        time.sleep(1)
                if IsKasperskyInstalled() == True:
                    logger("Kaspersky is installed, informing the user.")
                    print("Kaspersky is installed. This software is known to cause")
                    print(" issues with running AutoDDU at multiple steps, and has")
                    print(" caused many headaches. Highly recommended to either fully")
                    print(" uninstall Kaspersky or at the very least completely ")
                    print( " disabling it. I've tried to send AutoDDU for analysis")
                    print(" to Kaspersky multiple times but they keep saying all is good.")
                    print(" We'll continue in 5 minutes, between now and 5 minutes please disable it.")
                    time.sleep(300)
                    print("Continuing with normal setup now with the assumption you disabled it.")
                    print(" ")
                print_menu1()
                if RestartPending() == True and obtainsetting("disablewindowsupdatecheck") == 0:
                    print("There is pending Windows Updates that require a Restart")
                    print("Due to possible issues that can occur with AutoDDU running")
                    print("with a pending restart please check Windows Settings for updates")
                    print("and then restart. You may need to restart, check for updates, then restart again.")
                    while True:
                        time.sleep(1)
                if obtainsetting("disablewindowsupdatecheck") == 0:
                    HandlePendingUpdates()
            if not get_free_space() and len(TestEnvironment) == 0 and obtainsetting("avoidspacecheck") == 0:
                print(r"""
Too little free space to continue.
Please have at least 20GB of free space in C: drive.                 
                      """, flush=True)
                sys.stdout.flush()
                if len(TestEnvironment) == 0:
                    while True:
                        time.sleep(1)

            print("This process will attempt to perform DDU automatically.", flush=True)
            if obtainsetting("bypassgpureq") == 0 and obtainsetting("changegpumode") == 0 :
                try:
                    # for testing you pass something like this inside gpustatus
                    # {'NVIDIA GeForce RTX 3080': ['GA102', '10de', '2206']}
                    if len(TestEnvironment) == 0:
                        mainshit = GetGPUStatus()
                    else:
                        mainshit = GetGPUStatus(TestEnvironment[0])
                except Exception:
                    print("ERROR UNRECOVERABLE PLEASE REPORT THIS TO EVERNOW: \n", flush=True)
                    print(traceback.format_exc())
                    while True:
                        if len(TestEnvironment) == 0:
                            time.sleep(1)
                        else:
                            return("GPU REQ TEST  "  + str(traceback.format_exc())   )

                
                if mainshit == "Unsupported":
                    print(r"""
    INCOMPATIBLE GPU CONFIGURATION FOUND.
    
    CURRENTLY NO WAY TO RUN AUTODDU WITH THIS CONFIGURATION.
        """, flush=True)
                    while True:
                        if len(TestEnvironment) == 0:
                            time.sleep(1)
                        else:
                            return("Incompatible GPU")

                print(mainshit[0])
                time.sleep(3)
                
            print(r"""
This will update Windows if out of date, download needed drivers,
disable internet (needed to prevent Windows from fucking it up), 
and push you into safe mode. IT WILL DO THIS FOR YOU. 
YOU DO NOT NEED TO DO ANYTHING EXCEPT LAUNCH THIS APP ONCE RESTARTED
IN SAFE MODE IF IT DOESN'T BY ITSELF.
This will also disable all GPU overclocks/undervolts/custom fan curves.
Do not worry if you do not know what this is, it won't affect you.
When you are ready (this process can take up to 30 minutes 
and CANNOT be paused) please do what it says above. 
Save all documents and prepare for your computer to restart
without warning. 
 """, flush=True)
            sys.stdout.flush()
            if len(TestEnvironment) == 0:
                if BadLanguage() == False:
                    while True:
                        DewIt = str(input("Type in 'Do it' then press enter to begin: "))
                        if "do it" in DewIt.lower():
                            break
                else:
                    HandleOtherLanguages()
                time.sleep(5)
            if obtainsetting("changegpumode") == 0:
                if len(obtainsetting("provideowngpuurl")) != 0:
                    download_drivers(obtainsetting("provideowngpuurl"))
                elif len(obtainsetting("provideowngpuurl")) == 0 and obtainsetting("bypassgpureq") == 0:
                    download_drivers(mainshit[1])
            else: # For changing GPU crap
                if type(obtainsetting("changegpumode")) == list:
                    download_drivers(obtainsetting("changegpumode"))
            if obtainsetting("disablewindowsupdatecheck") == 0 and not insafemode():
                if len(TestEnvironment) == 0:
                    uptodate()
            changepersistent(1)
        if getpersistent() == 1:
            if RestartPending() == True and obtainsetting("disablewindowsupdatecheck") == 0:
                    print("There is pending Windows Updates that require a Restart")
                    print("Due to possible issues that can occur with AutoDDU running")
                    print("with a pending restart please check Windows Settings for updates")
                    print("and then restart. You may need to restart, check for updates, then restart again.")
                    while True:
                        time.sleep(1)

            if obtainsetting("disablewindowsupdatecheck") == 0 and not insafemode():
                if len(TestEnvironment) == 0:
                    uptodate()
            BackupProfile()
            ddu_download()
            print(
                "Now going to disable any oveclocks/undervolts/fan curves if any on the GPU. (If not changed to do otherwise)")
            print("If you had one you will have to reapply after this process is done.")
            print("If you do not know what any of this is, don't worry, you don't have to do anything.")
            print("We will resume in 5 seconds.", flush=True)
            if len(TestEnvironment) == 0:
                time.sleep(5)
            if obtainsetting("donotdisableoverclocks") == 0:
                disable_clocking()
            print(r"""          
----------------------------NOTICE----------------------------
This application will now enable safe mode, disable the internet
and then reboot you. IT WILL DO THIS FOR YOU. 
Safe mode is a state of Windows where no GPU Drivers are loaded,
this is needed so they we can do a proper clean install.
You wallpaper will be black, the resolution will look
messed up, this is normal.
In addition we're going to turn off the internet so
Windows cannot install drivers while we're installing them. Also
if you have BitLocker enabled we're going to temporarily
disable for three reboots.
            
{login_or_not}
We will automatically login to the user and run DDU. You may see
a blackscreen for up to 15 minutes, only force restart if this much
passes. Also note if you have multiple monitors and have issues with 
black screen you may want to disconnect all but one monitor.
We will auto login, run DDU, then restart, afterwards you will
be brought to your normal user login screen, at which you login
and AutoDDU will launch again to install drivers.
            
(Read what is above, window to continue will appear in 15 seconds.)
            
                  """.format(login_or_not=login_or_not), flush=True)
            if len(TestEnvironment) == 0:
                time.sleep(15)
            sys.stdout.flush()
            if len(TestEnvironment) == 0:
                if BadLanguage() == False:
                    while True:
                        DewIt = str(input("Type in 'I understand' then enter once you understand what you must do: "))
                        if "i understand" in DewIt.lower():
                            break
                else:
                    HandleOtherLanguages()
                time.sleep(1)
            if os.path.exists(os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe')) == False:# Makes sure nothing like Kaspersky has fucked us over, will make AutoDDU error out before doing anything annoying to recover from.
                print("Something went catastrophically wrong. For some reason DDU extraction failed.")
                print("We cannot continue like this, please report this to Evernow along with the log file in ")
                while True:
                    time.sleep(1)
            if RestartPending() == True and obtainsetting("disablewindowsupdatecheck") == 0:
                # User may have gotten an update since the beginning and now, so we check again right before we enable safe mode and create the DDU profile.
                    print("There is pending Windows Updates that require a Restart")
                    print("Due to possible issues that can occur with AutoDDU running")
                    print("with a pending restart please check Windows Settings for updates")
                    print("and then restart. You may need to restart, check for updates, then restart again.")
                    while True:
                        time.sleep(1)
            if obtainsetting("disablewindowsupdatecheck") == 0:
                    HandlePendingUpdates() # One last check to avoid annoying stuff, with same motivation as above check. Yes this happened in my testing.


            workaroundwindowsissues()  # TODO: this is REALLY FUCKING STUPID
            
            if VerifyDDUAccountCreated() == False:
                print("Something went wrong with creating user profile, unable to continue.")
                while True:
                    time.sleep(1)

            suspendbitlocker()
            if len(TestEnvironment) == 0:
                time.sleep(5)
                safemode(1)

            print("May seem frozen for a bit, do not worry, we're working in the background.")
            makepersist(True)
           # BackupLocalAccount()
            if len(TestEnvironment) == 0:
                 # Found in the NVIDIA Server that a malfunctioning network card can hang WMI for all eternity. Best add a timeout for that..
                print("Please wait ~10 seconds for us to disable the internet.")
                proc = multiprocessing.Process(target=enable_internet, args=(False,)) 
                proc.start()
                time.sleep(5)
                if proc.is_alive():
                    time.sleep(10)
                proc.terminate()
                
            changepersistent(2)
            autologin()
            if len(TestEnvironment) == 0:
                time.sleep(3)
                subprocess.call('shutdown /r -t 5', shell=True)
                time.sleep(2)
            print("Command to restart has been sent.")
            if len(TestEnvironment) == 0:
                while True:
                    time.sleep(1)
        if getpersistent() == 2:
            print("Welcome back, the hardest part is over.")
            print("This will take a minute or two, even though it may seem")
            print("like nothing is happening, please be patient.", flush=True)
            sys.stdout.flush()
            if len(TestEnvironment) == 0:
                try:
                    DDUCommands()
                except Exception as oof:
                    print("Error while doing DDU. You can still run manually.")
                    print("Please send this to Evernow:")
                    print(traceback.format_exc(), flush=True)
                    while True:
                        time.sleep(1)
            else:
                try:
                    DDUexeDirectory = os.path.exists(os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe'))
                except:
                    return("DDU file missing")
            print("DDU has been ran!", flush=True)
            cleanupAutoLogin()
            if obtainsetting("changegpumode") == 0:
                print(r"""
This will now boot you back into normal mode.
              
You can login to your normal user profile, no need for DDU.
              
Once you login you run this one last time where we will install
the drivers properly, then once finished turn on your internet.
NOTE AUTODDU WILL OPEN BY ITSELF AFTER YOU LOGIN, JUST WAIT TILL IT DOES.              
Will restart in 15 seconds.
              
                    """, flush=True)
            else:
                print(r"""
We will now completely SHUTDOWN your computer so that you can 
change the GPUs installed in your system to your new GPU.

Once you have installed your new GPU you can boot up your PC
like normal, then login login to your normal user profile, 
no need for DDU profile to be used.
              
Once you login you run this one last time where we will install
the drivers properly (if provided), then once finished turn 
on your internet. NOTE AUTODDU WILL OPEN BY ITSELF AFTER YOU 
LOGIN, JUST WAIT TILL IT DOES.              
              
                    """, flush=True)
                if BadLanguage() == False:
                    while True:
                        DewIt = str(input("Type in 'Do it' then press enter to begin: "))
                        if "do it" in DewIt.lower():
                            break
                else:
                    HandleOtherLanguages()
            if len(TestEnvironment) == 0:    
                safemode(0)
            makepersist(False)
            changepersistent(3)
            possible_error = ""
            try:
                possible_error = subprocess.Popen(
                    '{powershell} Remove-LocalUser -Name "{profile}"'.format(profile=obtainsetting("ProfileUsed"),powershell=powershelldirectory),
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    creationflags=CREATE_NEW_CONSOLE).communicate()
            except:
                logger(str(possible_error))
            if len(TestEnvironment) == 0:
                time.sleep(5)
                if obtainsetting("changegpumode") == 0:
                    subprocess.call('shutdown /r -t 10', shell=True)
                else:
                    subprocess.call('shutdown /s -t 10', shell=True)
                print("Command to restart has been sent.")
                while True:
                    time.sleep(1)

        if getpersistent() == 3:
            print("Please wait 5 seconds and we'll start the last process")
            changepersistent(0) 
            if len(TestEnvironment) == 0:
                time.sleep(5)
            print(r"""
Almost done. Only thing left now is install drivers
and then turn on your internet.
                  """, flush=True)
            try:
                os.remove(Script_Location_For_startup)
                logger("Removed script startup at first of 3rd call")
            except:
                pass
            mimicinstalleddrivers = [] # Used for testing to see if all drivers were correctly grabbed as expected
            if os.path.exists(os.path.join(Appdata, "AutoDDU_CLI", "Drivers")):
                s = os.listdir(os.path.join(Appdata, "AutoDDU_CLI", "Drivers"))
                for driver in s:
                        print("Please wait, we're verifying integrity of driver.")
                        publisherofdriver = CheckPublisherOfDriver(os.path.join(Appdata, "AutoDDU_CLI", "Drivers", driver))
                        if publisherofdriver == None:
                            print("Warning: We could not verify who published the driver ")
                            print("we were going to launch. This could be a result of some ")
                            print("sort of third party driver somehow making it in here.")
                            print("As a result we're not going to install this driver.")
                            continue
                        print("Launching driver installer, please install. If you are asked to restart click 'Restart later' then restart after AutoDDU is finished")
                        time.sleep(1)
                        logger("Opening driver executable: {}".format(driver))
                        if "igfx" in driver:
                            print("Note Intel driver installer can take")
                            print("up to 5 minutes just to appear")
                            print("and once it appears and it starts to install")
                            print("it can take up to 10 minutes to install.")
                        if len(TestEnvironment) == 0:
                            subprocess.call(str(os.path.join(Appdata, "AutoDDU_CLI", "Drivers", driver)), shell=True)
                        else:
                            mimicinstalleddrivers.append(driver)
                        logger("Sucessfully finished driver executable: {}".format(driver))
                print("All driver installations complete. Have a good day.")
            else:

                print("""
Due to no drivers being detected, our work is done.
Now it is up to you to install the drivers like you normally would.
Going to be turning on the internet now, then closing in ten minutes.
                """, flush=True)

            try:
                os.remove(Script_Location_For_startup)
            except:
                pass
            try:
                AutoStartupkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,"Software\Microsoft\Windows\CurrentVersion\RunOnce",0,winreg.KEY_ALL_ACCESS)
                winreg.DeleteValue(AutoStartupkey, '*AutoDDU_CLI')
            except:
                logger("No RunOnce key found, should be ok then?")
            if len(TestEnvironment) == 0:
                    proc = multiprocessing.Process(target=enable_internet, args=(True,)) 
                    proc.start()
                    print("Please wait ~10 seconds for us to enable the internet and do some cleanup.")
                    time.sleep(5)
                    if proc.is_alive():
                        time.sleep(10)

                    proc.terminate()

            cleanup()
            if os.path.exists(os.path.join(Users_directory,"Default", "AutoDDU_CLI.exe")):
                os.remove(os.path.join(Users_directory,"Default", "AutoDDU_CLI.exe"))
            # RIP Chika ASCII Art tormenting the lives of people at the beginning
            # March 2022 - September 2022
            # Killed at the hands of Arron who said "you're scaring people away, at least hide it at the end where it's too late for them to turn back"
            print(r"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%&................... @@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/,&%%%%%%%&........,............@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@...&%%%%%%%%%%%(.,......................./@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@%....(%%%%%%%%%%%%%&%#,..*#&&&&&&&&#,..............@@@@@@@
@@@@@@@@@@@@@@@@@@@@......&%%%%%%%%%%%%&%%%&&&%%%%%%%%%%%%%%&................@@@
@@@@@@@@@@@@@@@@@@@  ....%&&%%%%%%&&&&&&%%&%%%%%%%%%%%%%%%%%....................
@@@@@@@@@@@@@@@@@   ...*.......*.....,.,/(&%%%%%%%%%%%%%%%,.....................
@@@@@@@@@@@@@@. . ....*.,*....,....( .....*%&&%%%%%%%%%%%.......................
@@@@@@@@@@@*. . ..,../.((.../...,.% .....,.../&&&%%%%&&......./.................
@@@@@@@@@&.. ....*..%.(/...(,../,&...../ .....(.,&&&%....,....,.................
@@@@@@@%*.......*..&.##/,,((../,%.....#.....,(....,.,...,....(..................
@@@@@@&.......,*.(,#%.%..*% .*,*/....%,....,#,...*.*....,...%...................
@@@@@@@......**.%. ,, ( .*.../*//...(*....,(*.../,*...*.,..#*.....,.............
@@@@@@......,/.@.   ,*.          ...*,..,//,,*.(#*...#,...(*,....,..............
@@@@........(,#%  .&&&&./              .,*....,#(...*%..#***,....,..............
@@%.......,#/(/,(&,  ,%&,                  .**/,..(%/.*/(.,*...,/.........    .,
@@@......,,(#*%&.  (  (%                       .*(./.%  /.,*..,/........     ..#
@@@......//#*(,   &,%%#,                .         .*  . /.,,.*/........      .%.
@@......,*#**/   #. ,/                 ,%&@%,/          (.*.*#........      .#..
@@......**#*#    ,##,                      .,#&#(       #.,*#.......       .(...
@@,.....*/(#. .                          ,   #%&&#      #,(,.......      ..(....
@@&.....**(     .                      %((//(###%&%    ./&........  . ....#.....
@@@,....,&                            *#..#%%%###&%%   (*................%......
@@@%...../                            .%. ...,,#& (%  %................,/.......
@@@@*...,*       .                       /#((#&   *.&.................%.........
@@@@%...,(      %,,,*(             .  ..      .   &..................%,..,......
@@@@&...//,    (,,,,,,,,,#.                     &..*...............&,,../.......
@@&@&.,/*.%    #,,,,,,,,,,,/                .,%.*..............,,%.%.*./*.......
@@@@*///..*&    (,,,,,,,,,(                #.*,.............,/*%.(,.*.*/,......*
/@@%/(...((%#     .(///((               ,(#.............,///,&.%**..#.//,....*//
@#(*..*%((,  %                       *#............,///////&%////*..#,//....///*
.*/(&//(%,    #/,               .#(........,**///////%/,&(///////*..#*//,..////&
/,**#//&,,   ,&/%/////#&&&#/#&,...,*/////////////##*(&///#///////*,.(///,.////@@""", flush=True)
            print("We are done! Internet should be on now.")
            if len(TestEnvironment) == 0:
                time.sleep(600)
            else:
                return mimicinstalleddrivers
            sys.exit(0)
        while True:
            if len(TestEnvironment) == 0:
                print("ERROR CONFIGURATION ERROR CONFIGURATION")
                time.sleep(1)
            else:
                return ("Config error")
    except Exception:
        if len(TestEnvironment) == 0:
            print(unrecoverable_error_print)
            print(traceback.format_exc(), flush=True)
            logger(str(traceback.format_exc()))
            try:
                if getpersistent() == 1:
                    changepersistent(0)
                elif getpersistent() == 2:
                    changepersistent(1)
                elif getpersistent() == 3:
                    changepersistent(2)
            except:
                pass
            while True:
                time.sleep(1)
        else:
            return ("Exception " + str(traceback.format_exc()))

if __name__ == '__main__':
    multiprocessing.freeze_support() # Used for networking bullshit, required for frozen exes: https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
    print(mainpain([]))
