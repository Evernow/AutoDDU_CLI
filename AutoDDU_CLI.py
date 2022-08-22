Version_of_AutoDDU_CLI = "0.0.9"
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
import requests
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


advanced_options_dict_global = {"disablewindowsupdatecheck": 0, "bypassgpureq": 0, "provideowngpuurl": [],
                                "disabletimecheck": 0, "disableinternetturnoff": 0, "donotdisableoverclocks": 0,
                                "disabledadapters": [], "avoidspacecheck": 0, "amdenterprise" : 0,
                                "nvidiastudio" : 0, "startedinsafemode" : 0, "inteldriverassistant" : 0,
                                "dnsoverwrite" : 0} # ONLY USE FOR INITIALIZATION IF PERSISTENTFILE IS TO 0. NEVER FOR CHECKING IF IT HAS CHANGED.

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
Script_Location_For_startup = os.path.join(shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0), 'Microsoft',
                                           'Windows', 'Start Menu', 'Programs', 'Startup', 'AutoDDUStartup.vbs')

log_file_location = os.path.join(Appdata_AutoDDU_CLI, "AutoDDU_LOG.txt")
PROGRAM_FILESX86 = shell.SHGetFolderPath(0, shellcon.CSIDL_PROGRAM_FILESX86, 0, 0)

# Only Fermi professional (NVS, Quadro, Tesla) is supported, and only till the end of 2022.
FERMI_NVIDIA = ['GF100', 'GF100M', 'GF100G', 'GF100GL', 'GF100GLM', 'GF106', 'GF108', 'GF104', 'GF116', 'GF106M', 'GF106GL', 'GF106GLM', 'GF108M', 'GF108GL', 'GF108GLM', 'GF119', 'GF110', 'GF114', 'GF104M', 'GF104GLM', 'GF11', 'GF119M', 'GF110GL', 'GF117M', 'GF114M', 'GF116M']


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
    'Xavier', 'MCP78U', 'MCP72P' , 'MCP72XE']

KEPLER_NVIDIA = ['GK104', 'GK106', 'GK208', 'GK110', 'GK107', 'GK107M', 'GK107GL', 'GK107GLM', 'GK110B',
                 'GK110GL', 'GK110BGL', 'GK180GL', 'GK210GL', 'GK104GL', 'GK104M', 'GK104GLM', 'GK106M', 
                 'GK106GL', 'GK106GLM', 'GK208B', 'GK208M', 'GK208BM', 'GK20', 'GK208GLM']

Professional_NVIDIA_GPU = ["Quadro", "NVS", "RTX A"]

Datacenter_NVIDIA_GPU = ["Tesla", "HGX", "M", "T"] 


Exceptions_laptops = ["710A", "745A", "760A", "805A", "810A", "810A", "730A",
                      "740A"]  # Kepler laptops GPUs with no M in the name.

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
yourself manually.
"""

AutoDDU_CLI_Settings = os.path.join(Appdata_AutoDDU_CLI, "AutoDDU_CLI_Settings.json")

# Suggestion by Arron to bypass fucked PATH environment variable
powershelldirectory = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"

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


def GPUDriversFallback(url):
        # For bad DNS issues encountered on NVIDIA server, very rare but never hurts to have a fallback for this event.
        # Credit to RandoNando for figuring this out
        from dns import resolver
        res = resolver.Resolver()
        res.nameservers = ['8.8.8.8'] # Google DNS
        answers = res.resolve('raw.githubusercontent.com')
        for rdata in answers:
            address = (rdata.address)
        r = requests.get(f'http://{address}/{url}', headers={'Host' : 'raw.githubusercontent.com'})
    #r = requests.get(f'http://{address}/24HourSupport/CommonSoftware/main/nvidia_gpu.json', headers={'Host' : 'raw.githubusercontent.com'})

        return r.json()

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
    # in german.
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
    print(query_obj)
    try:
        res = getDispDrvrByDevid(query_obj, timeout)
    except urllib.error.HTTPError as e:
        print(e)
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



def returnpendingupdates():
    CheckPendingUpdates = os.path.join(Appdata_AutoDDU_CLI, "CheckPendingUpdates.vbs")
    OutputOfPendingUpdates = os.path.join(Appdata_AutoDDU_CLI, "OutputOfPendingUpdates.txt")
    # https://stackoverflow.com/questions/70792656/how-do-i-get-pending-windows-updates-in-python
    # https://github.com/Evernow/AutoDDU_CLI/issues/14
    try:
        vbsfile = ['Set updateSession = CreateObject("Microsoft.Update.Session")\n', 
        'Set updateSearcher = updateSession.CreateupdateSearcher()        \n', 
        'Set searchResult = updateSearcher.Search("IsInstalled=0 and Type=\'Software\'")\n', '\n', '\n',
        'If searchResult.Updates.Count <> 0 Then \n', '\n', 'For i = 0 To searchResult.Updates.Count - 1\n',
        '    Set update = searchResult.Updates.Item(i)\n', '    \n', 'Next\n', 'End If\n', '\n', 'Main\n', '\n', 'Sub Main()\n',
        '    Dim result, fso, fs\n', '    result = 1 / Cos(25)\n', '    Set fso = CreateObject("Scripting.FileSystemObject")\n',
            '    Set fs  = fso.CreateTextFile("{output}", True)\n'.format(output=OutputOfPendingUpdates),
            '    fs.Write searchResult.Updates.Count\n',
            '    fs.Close\n', 'End Sub'] 
        with open(CheckPendingUpdates, 'w') as f:
            for item in vbsfile:
                f.write(item)
        os.system(CheckPendingUpdates)
        with open(OutputOfPendingUpdates,'r') as file:
            lines = file.readlines()     
            if lines[0] == "0":
                return False
            else:
                return True
    except:
        print("""
Make sure when we launch the update assistant
that the option to keep files and apps is selected
when asked.""")
        time.sleep(5)
        logger("Failed in returnpendingupdates with error")
        logger(str(traceback.format_exc()))
        return False


def suspendbitlocker():
    try:
        p = str(subprocess.Popen(
            "{powershell} Suspend-BitLocker -MountPoint 'C:' -RebootCount 3".format(powershell=powershelldirectory),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=CREATE_NEW_CONSOLE).communicate())
        logger("Suspended bitlocker with output " + str(p))
    except:
        logger("Did not suspend bitlocker with output " + p)
    
def handleoutofdate():
    response = requests.get("https://github.com/Evernow/AutoDDU_CLI/raw/main/version.txt")
    data = response.text
    if (Version_of_AutoDDU_CLI) != (data):
        logger("Version did not match, version in local variable is {local} while version on GitHub is {git}".format(git=data, local=Version_of_AutoDDU_CLI))
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
    try:
        urllib.request.urlopen('https://www.google.com/', timeout=3)
        return True
    except:
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
    while option != "11":
        clear()
        time.sleep(1)
        print("WARNING: THIS MAY BEHAVE UNEXPECTADLY!", flush=True)
        print('1 --' + AdvancedMenu_Options(1), flush=True)  # Disable Windows Updates check
        print('2 --' + AdvancedMenu_Options(2), flush=True)  # Bypass supported GPU requirement
        print('3 --' + AdvancedMenu_Options(3), flush=True)  # Provide my own driver URLs
        print('4 --' + AdvancedMenu_Options(4), flush=True)  # Disable time check
        print('5 --' + AdvancedMenu_Options(5), flush=True)  # Do not turn internet off when needed
        print('6 --' + AdvancedMenu_Options(6), flush=True)  # Do not disable overclocking/undervolts/fan curves
        print('7 --' + AdvancedMenu_Options(7), flush=True)  # Disable 20GB free storage requirement
        print('8 --' + AdvancedMenu_Options(8), flush=True)  # Use AMD Enterprise driver
        print('9 --' + AdvancedMenu_Options(9), flush=True)  # Use NVIDIA Studio driver (Pascal and up)
        print('10 --' + AdvancedMenu_Options(10), flush=True)  # Manual DNS Resolving
        print('11 -- Start', flush=True)
        option = str(input('Enter your choice: '))
        change_AdvancedMenu(option)


def AdvancedMenu_Options(num):
    logger("User is changing option " + str(num))
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
            if advanced_options_dict["disabletimecheck"] == 0:
                return " Placeholder (ignore)"
            else:
                return " Placeholder (ignore)"

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
        f.seek(0)
        json.dump(advanced_options_dict, f, indent=4)
        f.truncate()
        logger("Advanced options are now: " + str(advanced_options_dict))


def change_AdvancedMenu(num):
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
            if advanced_options_dict["disabletimecheck"] == 0:
                advanced_options_dict["disabletimecheck"] = 1
            else:
                advanced_options_dict["disabletimecheck"] = 0

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


def print_menu1():
    print('Press Enter Key -- Start', flush=True)
    print('2 -- Advanced Options', flush=True)
    option = str(input('Enter your choice: '))
    if option == "2":
        AdvancedMenu()


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


def PCIID(vendor, device):
    try:
        if obtainsetting("dnsoverwrite") == 1:
            raise ValueError('Purposeful error.')
        url = urllib.request.urlopen("https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/PCI-IDS.json")
        data = json.loads(url.read().decode())
    except:
        from dns import resolver
        res = resolver.Resolver()
        res.nameservers = ['8.8.8.8']
        answers = res.resolve('raw.githubusercontent.com')
        for rdata in answers:
            address = (rdata.address)
        import requests
        r = requests.get(f'http://{address}/24HourSupport/CommonSoftware/main/PCI-IDS.json', headers={'Host' : 'raw.githubusercontent.com'})
        data = r.json()
    try:
        return data[vendor]['devices'][device]['name']
    except KeyError:
        return None

def logger(log):
    # The goal is to log everything that is practical to log. 
    # I'm at the end of my rope! 
    # Why do I have to coach someone incompetent like you every single time?
    # I'm done with it! If you ever need help with anything else, please don't ask me!
    if not os.path.exists(Appdata_AutoDDU_CLI):
        os.makedirs(Appdata_AutoDDU_CLI)
    file_object = open(log_file_location, 'a+')
    file_object.write(datetime.now(timezone.utc).strftime("UTC %d/%m/%Y %H:%M:%S ") + log)
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


def makepersist():
    time.sleep(0.5)
    try:
        shutil.copyfile(sys.executable, exe_location)
        logger("Successfully copied executable to Appdata directory")
    except:
        logger("Falled back to downloading from github method for going to Appdata directory due to error: " + str(traceback.format_exc()))
        try:

            logger("Directory name of where executable is located is: " + str(os.path.dirname(sys.executable)))
            logger("Contents of directory are: " + str(os.listdir(os.path.dirname(sys.executable))))
        except:
            logger("Failed to log info about directory where sys.executable is located with error: " +  str(traceback.format_exc()))
        download_helper("https://github.com/Evernow/AutoDDU_CLI/raw/main/signedexecutable/AutoDDU_CLI.exe", exe_location)
    lines = ['Set WshShell = CreateObject("WScript.Shell" )',
             'WshShell.Run """{directory}""", 1'.format(directory=exe_location), "Set WshShell = Nothing"]
    with open(Script_Location_For_startup, 'w') as f:
        for line in lines:
            f.write(line)
            f.write('\n')

    print("INFO: Successfully created autorun task for in normal mode.")
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
                time.sleep(30)
        except: # Fails when key does not exist, aka when someone does not have AutoLogin setup on their own.
            pass
        
        winreg.SetValueEx(Winlogon_key, 'AutoAdminLogon', 0, winreg.REG_SZ, '1')

        winreg.SetValueEx(Winlogon_key, 'DefaultUserName', 0, winreg.REG_SZ, '{}'.format(obtainsetting("ProfileUsed")))

        winreg.SetValueEx(Winlogon_key, 'DefaultPassword', 0, winreg.REG_SZ, '1234')

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
    subprocess.call('NET USER {profile} 1234 '.format(profile=obtainsetting("ProfileUsed")), shell=True,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if insafemode():
        change_AdvancedMenu("99")
        logger("In Safemode while working around windows issues, falling back to Default folder copying method")
        try:
            time.sleep(0.5)
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
            download_helper("https://github.com/Evernow/AutoDDU_CLI/raw/main/signedexecutable/AutoDDU_CLI.exe",
                            os.path.join(Users_directory,"Default", "Desktop","AutoDDU_CLI.exe"))
    else:
        if os.path.exists(os.path.join(Users_directory,"Default","Desktop", "AutoDDU_CLI.exe")):
                os.remove(os.path.join(Users_directory,"Default","Desktop", "AutoDDU_CLI.exe"))
        try:
            time.sleep(0.5)
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
                download_helper("https://github.com/Evernow/AutoDDU_CLI/raw/main/signedexecutable/AutoDDU_CLI.exe",
                                os.path.join(Users_directory,"Default", "Desktop","AutoDDU_CLI.exe"))
            except:
                logger("Failed to also download to Default folder, going to back to PSExec method.")
        if not os.path.exists(os.path.join(Users_directory,"Default","Desktop", "AutoDDU_CLI.exe")):
        ### Old Approach but unfortunately Kaspersky (and like others) did not like PSTools. Now only here as a backup because people always seem to do fucky things with crap like this.
            logger("Fell back to PSExec logic because this idiot did something to his user folders, probably some 'But I don't use these folders so lemme delete them' mentality")
            download_helper("https://download.sysinternals.com/files/PSTools.zip",
                            os.path.join(Appdata_AutoDDU_CLI, "PsTools.zip"))
            with zipfile.ZipFile(os.path.join(Appdata_AutoDDU_CLI, "PsTools.zip")) as zip_ref:
                zip_ref.extractall(os.path.join(Appdata_AutoDDU_CLI, "PsTools"))
            try:
                subprocess.call(
                    '{directory_to_exe} -accepteula -u {profile} -p 1234 i- exit'.format(profile=obtainsetting("ProfileUsed"),
                                                                                        directory_to_exe=os.path.join(
                                                                                            Appdata_AutoDDU_CLI, "PsTools",
                                                                                            "PsExec.exe")), shell=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass  

            logger("Did prep work for working around Windows issue")
            try:
                time.sleep(0.5)
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

                download_helper("https://github.com/Evernow/AutoDDU_CLI/raw/main/signedexecutable/AutoDDU_CLI.exe",
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


def getgpuinfos():
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
                gpu_dictionary[name] = [Arch, Vendor_ID, Device_ID]
    logger(str(gpu_dictionary))
    return gpu_dictionary


todays_date = date.today().year


def getsupportstatus(parsed_gpus):  # parsed_gpus[name] = [Arch, Vendor_ID, Device_ID]
    gpu_dictionary = dict()  # GPU NAME = [VENDOR ID, DEVICE ID, ARCHITECTURE , RAW OUTPUT (for troubleshooting purposes), supportstatus (0=unchecked, 1=supported, 2=kepler, 3=fermiprof, 4=EOL), professional/consumer]
    logger("Working in getsupportstatus with this wmi output: ")
    for gpu in parsed_gpus:

        todays_date = date.today().year
        name = gpu
        Arch = parsed_gpus[gpu][0]
        Vendor_ID = parsed_gpus[gpu][1]
        Device_ID = parsed_gpus[gpu][2]
        supportstatus = 0
        Consumer_or_Professional = ""
        if Vendor_ID == '121a':  # Voodoo (wtf lol)
            logger("Got Voodoo GPU")
            supportstatus = 4
            Consumer_or_Professional = "Consumer"
        if Vendor_ID == '8086':  # Intel
            logger("Got Intel GPU")
            supportstatus = 1
            Consumer_or_Professional = "Consumer"
        if Vendor_ID == '1002':  # AMD
            logger("Got AMD GPU")
            try:
                if obtainsetting("dnsoverwrite") == 1:
                    raise ValueError('Purposeful error.')
                url = urllib.request.urlopen("https://github.com/24HourSupport/CommonSoftware/raw/main/amd_gpu.json")
                supported_amd = json.loads(url.read().decode())
                supported_amd = supported_amd["consumer"]["SupportedGPUs"] + supported_amd["professional"]["SupportedGPUs"]
            except:
                from dns import resolver
                res = resolver.Resolver()
                res.nameservers = ['8.8.8.8']
                answers = res.resolve('raw.githubusercontent.com')
                for rdata in answers:
                    address = (rdata.address)
                r = requests.get(f'http://{address}/24HourSupport/CommonSoftware/main/amd_gpu.json', headers={'Host' : 'raw.githubusercontent.com'})
                supported_amd = r.json()
                supported_amd = supported_amd["consumer"]["SupportedGPUs"] + supported_amd["professional"]["SupportedGPUs"]


            if Arch != None and Device_ID.upper() not in supported_amd:
                logger("Got EOL AMD GPU with code " + Arch)
                supportstatus = 4
            if supportstatus != 4:
                logger("Got Supported AMD GPU with code " + Arch)
                supportstatus = 1
            Consumer_or_Professional = "Consumer"  # There are professional AMD GPUs but are EXTREMELY rare and I haven't built a driver search for them, nor intend to.

        if Vendor_ID == '10de':  # NVIDIA
            logger("Got NVIDIA GPU with code " + str(Arch))

            # Check if professional or consumer
            for seeifprof in Professional_NVIDIA_GPU:
                if seeifprof.lower() in name.lower():
                    logger("Got NVIDIA prof")
                    Consumer_or_Professional = "Professional"
            if Consumer_or_Professional == "":
                for seeifdatacenter in Datacenter_NVIDIA_GPU:
                    if len(seeifdatacenter) >= len(name):
                        if name[:len(seeifdatacenter)].lower() == seeifdatacenter.lower():
                            logger("Got NVIDIA datacenter")
                            Consumer_or_Professional = "Datacenter"
            if Consumer_or_Professional == "":
                logger("Got NVIDIA consumer")
                Consumer_or_Professional = "Consumer"
            # Nightmare begins
            for possibility in EOL_NVIDIA:
                if Arch != None and Arch in possibility:
                    logger("Got EOL NVIDIA")
                    supportstatus = 4  # EOL
            for possibility in FERMI_NVIDIA:
                if Arch != None and Arch in possibility:
                    logger("Got NVIDIA FERMI")
                    for _ in Professional_NVIDIA_GPU:

                        if Consumer_or_Professional == "Professional" and todays_date < 2023:  # EOL For Fermi prof
                            logger("Got professional fermi")
                            supportstatus = 3  # fermiprof
                    if supportstatus != 3:
                        logger("Got consumer fermi")
                        supportstatus = 4  # EOL
            for possibility in KEPLER_NVIDIA:
                if Arch != None and Arch in possibility:
                    logger("Got Kepler")
                    if "M" in name.upper():
                        logger("Got laptop kepler (main)")
                        supportstatus = 4  # EOL
                    else:
                        for exception_fuckinglaptops in Professional_NVIDIA_GPU:
                            if exception_fuckinglaptops in name.upper():
                                logger("Got laptop kepler (secondary)")
                                supportstatus = 4  # EOL
                        if supportstatus != 4 and todays_date < 2025:  # In reality it ends in mid 2024, but this is fine.
                            if "GRID" not in name:
                                logger("Got desktop supported kepler")
                                supportstatus = 2  # kepler
                            else:
                                logger("Got GRID GPU with {}".format(name))
                                supportstatus = 4  # EOL, all GRID GPUs are EOL now

            if supportstatus == 0:
                logger("Got supported NVIDIA")
                supportstatus = 1

        # This approach covers for stupid SLI or dual GPUs (looking at you Anderson)
        gpu_dictionary[name] = [Vendor_ID, Device_ID, Arch, gpu, supportstatus, Consumer_or_Professional]
    logger("Finished getsupportstatus with this dictionary: " + str(gpu_dictionary))
    return gpu_dictionary


# supportstatus = 0=unchecked, 1=supported, 2=kepler, 3=fermiprof, 4=EOL
# [VENDOR ID, DEVICE ID, ARCHITECTURE , RAW OUTPUT, supportstatus, professional/consumer] 
def checkifpossible(getgpus):  # Checks edge GPU cases and return list of GPU drivers to downloaded

    # if getgpus == None:
    #     performing_DDU_on = "Cannot perform AutoDDU due to GPU not being in our database. \n"
    #     return 0, performing_DDU_on, None

    # WIP to prevent different driver branches being installed (like R470 and R510 or R510 prof and R510 consumer)
    Consumer = 0
    Professional = 0
    Fermi = 0
    Kepler = 0

    dict_of_GPUS = getgpus
    logger(str(dict_of_GPUS))
    #  print(dict_of_GPUS)
    drivers_to_download = list()
    # NVIDIA driver source loading
    if obtainsetting("dnsoverwrite") == 0:
        try:
            with urllib.request.urlopen(
                    "https://github.com/24HourSupport/CommonSoftware/raw/main/nvidia_gpu.json") as url:
                data_nvidia = json.loads(url.read().decode())
        except: # For bad DNS issues
            data_nvidia = GPUDriversFallback('24HourSupport/CommonSoftware/main/nvidia_gpu.json')
    else:
        data_nvidia = GPUDriversFallback('24HourSupport/CommonSoftware/main/nvidia_gpu.json')
    NVIDIA_Consumer = data_nvidia["consumer"]["link"]
    NVIDIA_Consumer_Studio = data_nvidia["consumer_studio"]["link"]
    NVIDIA_Professional = data_nvidia["professional"]["link"]
    NVIDIA_Datacenter = data_nvidia["datacenter"]["link"]
    NVIDIA_Datacenter_Kepler = data_nvidia["datacenter_kepler"]["link"]
    NVIDIA_R390 = data_nvidia["r390"]["link"]
    NVIDIA_R470_Consumer = data_nvidia["r470_consumer"]["link"]
    NVIDIA_R470_Professional = data_nvidia["r470_professional"]["link"]
    NVIDIA_Supported_Products = data_nvidia["consumer"]["SupportedGPUs"] + data_nvidia["professional"]["SupportedGPUs"] + data_nvidia["datacenter"]["SupportedGPUs"] + data_nvidia["datacenter_kepler"]["SupportedGPUs"] + data_nvidia["r390"]["SupportedGPUs"] + data_nvidia["r470_consumer"]["SupportedGPUs"] + data_nvidia["r470_professional"]["SupportedGPUs"]
    # AMD driver source loading
    if obtainsetting("dnsoverwrite") == 0:
        try:
            with urllib.request.urlopen(
                    "https://github.com/24HourSupport/CommonSoftware/raw/main/amd_gpu.json") as url:
                data_amd = json.loads(url.read().decode())
        except:
            data_amd = GPUDriversFallback('24HourSupport/CommonSoftware/main/amd_gpu.json')
    else:
        data_amd = GPUDriversFallback('24HourSupport/CommonSoftware/main/amd_gpu.json')
    AMD_Consumer = data_amd["consumer"]["link"]
    AMD_Professional = data_amd["professional"]["link"]
    # Intel driver source loading
    if obtainsetting("dnsoverwrite") == 0:
        try:
            with urllib.request.urlopen(
                    "https://github.com/24HourSupport/CommonSoftware/raw/main/intel_gpu.json") as url:
                data_intel = json.loads(url.read().decode())
        except:
            data_intel = GPUDriversFallback('24HourSupport/CommonSoftware//main/intel_gpu.json')
    else:
        data_intel = GPUDriversFallback('24HourSupport/CommonSoftware//main/intel_gpu.json')
    Intel_Consumer = data_intel["consumer"]["link"]
    Intel_Consumer_Supported = json.loads(data_intel["consumer"]["SupportedGPUs"].replace('\'', '"')) # See comments here for replace reasoning: https://stackoverflow.com/a/35461204/17484902


    performing_DDU_on = "DDU will be performed on the following GPUs: \n"
    logger("Successfully grabbed NVIDIA drivers from CommonSoftware repo")
    for gpu in dict_of_GPUS:
        name = gpu
        gpu = dict_of_GPUS[gpu]
        # print(gpu)
        if (gpu[2] == None or gpu[1].upper() not in NVIDIA_Supported_Products) and gpu[0] == '10de' :
            try:
                vendorid_deviceid = gpu[1].upper() + "_" + gpu[0].upper()
                possibledriver = FindOutOfBranchDriver(vendorid_deviceid)
                if possibledriver != None:
                    performing_DDU_on = performing_DDU_on + name + "({Arch}) \n".format(Arch=str(gpu[2]))
                    drivers_to_download.append(possibledriver) 
                    continue
                else:
                    performing_DDU_on = "Cannot perform AutoDDU due to GPU not being in our database. \n"
                    return 0, performing_DDU_on, None
            except:
                performing_DDU_on = "Cannot perform AutoDDU due to GPU not being in our database. \n"
                return 0, performing_DDU_on, None
        elif gpu[2] == None:
            performing_DDU_on = "Cannot perform AutoDDU due to GPU not being in our database. \n"
            return 0, performing_DDU_on, None
        if gpu[-2] == 4:  # EOL
            performing_DDU_on = "Cannot perform DDU due to the following incompatible GPU found: \n"
            performing_DDU_on = performing_DDU_on + name + "({Arch}) \n".format(Arch=str(gpu[2]))
            return 0, performing_DDU_on, None
        if gpu[-2] == 3:  # fermiprof
            performing_DDU_on = performing_DDU_on + name + "({Arch}) \n".format(Arch=str(gpu[2]))
            drivers_to_download.append(NVIDIA_R390)
            Fermi += 1
        if gpu[-2] == 2:  # Kepler
            if gpu[-1] == "Consumer":
                performing_DDU_on = performing_DDU_on + name + "({Arch}) \n".format(Arch=str(gpu[2]))
                if NVIDIA_R470_Consumer not in drivers_to_download:  # Damn you Anderson. Damn you. It sucks we even need to check for this but.. god dammit...
                    drivers_to_download.append(NVIDIA_R470_Consumer)
                Kepler += 1
                Consumer += 1
            elif gpu[-1] == "Datacenter":
                if NVIDIA_Datacenter_Kepler not in drivers_to_download:
                    drivers_to_download.append(NVIDIA_Datacenter_Kepler)
            else:  # Professional.. probably (edge cases, TODO)
                performing_DDU_on = performing_DDU_on + name + "({Arch}) \n".format(Arch=str(gpu[2]))
                if NVIDIA_R470_Professional not in drivers_to_download:  # Damn you Anderson. Damn you. It sucks we even need to check for this but.. god dammit...
                    drivers_to_download.append(NVIDIA_R470_Professional)
                Kepler += 1
                Professional += 1
        if gpu[-2] == 1:  # Supported
            # print("test")
            performing_DDU_on = performing_DDU_on + name + "({Arch}) \n".format(Arch=str(gpu[2]))
            if gpu[0] == '10de':  # NVIDIA
                if gpu[-1] == 'Professional':
                    if NVIDIA_Professional not in drivers_to_download:  # Damn you Anderson. Damn you. It sucks we even need to check for this but.. god dammit...
                        drivers_to_download.append(NVIDIA_Professional)
                    Professional += 1
                elif gpu[-1] == "Datacenter":
                    if NVIDIA_Datacenter not in drivers_to_download:
                        drivers_to_download.append(NVIDIA_Datacenter)
                        Professional += 1
                else:
                    if NVIDIA_Consumer not in drivers_to_download:  # Damn you Anderson. Damn you. It sucks we even need to check for this but.. god dammit...
                        if obtainsetting("nvidiastudio") == 1 and ("GK" not in str(gpu[2]) and "GM" not in str(gpu[2])): # Unlike normal driver, Studio only supports Pascal and above
                            drivers_to_download.append(NVIDIA_Consumer_Studio)
                        else:
                            drivers_to_download.append(NVIDIA_Consumer)
                    Consumer += 1
            if gpu[0] == '1002':  # AMD
                if AMD_Consumer not in drivers_to_download:  # Damn you Anderson. Damn you. It sucks we even need to check for this but.. god dammit...
                    if obtainsetting("amdenterprise") == 1:
                        drivers_to_download.append(AMD_Professional)
                    else:
                        drivers_to_download.append(AMD_Consumer)
                    # Consumer += 1
            if gpu[0] == '8086':  # Intel
                if gpu[1].upper() in Intel_Consumer_Supported:
                    if Intel_Consumer not in drivers_to_download:
                        drivers_to_download.append(Intel_Consumer)
                else:
                    if "https://dsadata.intel.com/installer" not in drivers_to_download:  # Damn you Anderson. Damn you. It sucks we even need to check for this but.. god dammit...
                        drivers_to_download.append("https://dsadata.intel.com/installer")
                        if obtainsetting("inteldriverassistant") == 0:
                            # We need to record this, because we handle installation a bit differently
                            # in this case.
                            change_AdvancedMenu("98")
                        # Consumer += 1
    if Consumer > 0 and Professional > 0:
        performing_DDU_on = "Cannot perform DDU due to seeing Professional and Consumer GPUs \n Which is not supported by NVIDIA: https://nvidia.custhelp.com/app/answers/detail/a_id/2280/~/can-i-use-a-geforce-and-quadro-card-in-the-same-system%3F \n For troubleshooting purposes please show this if this is a mistake: \n"
        performing_DDU_on = performing_DDU_on + dict_of_GPUS
        return 0, performing_DDU_on, None
    if Fermi > 0 and Kepler > 0:
        performing_DDU_on = "Cannot perform DDU due to seeing Fermi and Kepler GPUs \n For troubleshooting purposes please show this if this is a mistake: \n"
        performing_DDU_on = performing_DDU_on + dict_of_GPUS
        return 0, performing_DDU_on, None
    if len(drivers_to_download) == 0:
        performing_DDU_on = """
WARNING: NO GPUS HAVE BEEN DETECTED BY WINDOWS.
THIS PROCESS WILL CONTINUE BUT YOU WILL NEED TO
INSTALL DRIVERS MANUALLY YOURSELF AFTER THIS PROCESS 
IS OVER. 
        
PLEASE REPORT THIS TO EVERNOW IF IT IS A BUG.
        
Chika is mad and confused at the same time."""
    # logger("Finished checkifpossible with these values: " + 1 + " " + performing_DDU_on + " " + drivers_to_download)
    return 1, performing_DDU_on, drivers_to_download


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


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_helper(url, fname):
    while not internet_on():
        logger("Saw no internet, asking user to connect")
        print("No internet connection")
        print("Please make sure internet is enabled")
        print("Retrying in 30 seconds")
        time.sleep(30)
    logger("Downloading  file from {url} to location {fname}".format(url=url, fname=fname))
    print("Downloading file {}".format(fname.split("\\")[-1]))
    remaining_download_tries = 15
    while remaining_download_tries > 0:
        if os.path.exists(fname):
            os.remove(fname)
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'),
                                ('Referer', "https://www.amd.com/en/support/graphics/amd-radeon-6000-series/amd-radeon-6700-series/amd-radeon-rx-6700-xt")]
            urllib.request.install_opener(opener)
            with DownloadProgressBar(unit='B', unit_scale=True,
                                    miniters=1, desc=url.split('/')[-1]) as t:
                urllib.request.urlretrieve(url, filename=fname, reporthook=t.update_to)
            break
        except:
            if remaining_download_tries < 0:
                raise Exception("Could not download file after 15 tries.")
            logger("Failed to download file, {} retries left".format(remaining_download_tries))
            print("Download failed, retrying in 5 seconds")
            time.sleep(5)
            remaining_download_tries = remaining_download_tries - 1

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


def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok



def ddu_download():
    if os.path.exists(ddu_extracted_path) and os.path.isdir(ddu_extracted_path):
        shutil.rmtree(ddu_extracted_path)
    if not os.path.exists(os.path.join(root_for_ddu_assembly)):
        os.makedirs(os.path.join(root_for_ddu_assembly))
    logger("Starting simple DDU search")
    download_helper(
        'https://raw.githubusercontent.com/Wagnard/display-drivers-uninstaller/WPF/display-driver-uninstaller/Display%20Driver%20Uninstaller/My%20Project/AssemblyInfo.vb',
        ddu_AssemblyInfo)

    my_file = open(ddu_AssemblyInfo, "r")

    content = my_file.readlines()

    Latest_DDU_Version_Raw = ""

    for DDU_Version_Candidate in content:
        if 'AssemblyFileVersion' in DDU_Version_Candidate:
            Latest_DDU_Version_Raw = DDU_Version_Candidate[
                                     DDU_Version_Candidate.find('("') + 2:DDU_Version_Candidate.find('")')]
    logger("Almost done with simple DDU search")
    countofloop = 0
    
    while not exists('https://www.wagnardsoft.com/DDU/download/DDU%20v' + Latest_DDU_Version_Raw + '.exe'):  # Normal error checking would not catch the error that would occur here.
        # You don't really need to understand this, basically
        # I have been looking at commit history, and there are instances where
        # he updates the github repos with a new version but doesn't make a release
        # yet, so this accounts for that possibility. Why is it so complicated?
        # It accounts for stuff like this:

        # 18.0.4.0 -> 18.0.3.9

        # 18.0.4.7 -> 18.0.4.6

        # Doesn't work for all cases (and I don't think it's possible for it to do so)
        # but it works 99.99% of the time.
        logger("Landed in complicated DDU search with number " + str(Latest_DDU_Version_Raw))
        logger("Trying complicated DDU search")
        nums = Latest_DDU_Version_Raw.split(".")

        skip = 0

        for ind in range(skip, len(nums)):
            curr_num = nums[-1 - ind]
            if int(curr_num) > 0:
                nums[-1 - ind] = str(int(curr_num) - 1)
                break
            else:
                nums[
                    -1 - ind] = "9"  # DDU seems to stop at 9th versions: https://www.wagnardsoft.com/content/display-driver-uninstaller-ddu-v18039-released

        Latest_DDU_Version_Raw = '.'.join(nums)
        logger("Almost finished with complicated DDU search....")
        countofloop += 1
        if countofloop > 5:
            raise ValueError('Unable to find DDU version after 5 tries.')
        time.sleep(2)

    download_helper(
            'https://www.wagnardsoft.com/DDU/download/DDU%20v' + Latest_DDU_Version_Raw + '.exe',
            ddu_zip_path
        )

    if not os.path.exists(ddu_extracted_path):
        os.makedirs(ddu_extracted_path)
    subprocess.call((ddu_zip_path + " -o{}".format(ddu_extracted_path) + " -y"), shell=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Moves everything one directory up, mainly just to avoid crap with versioning, don't want to have to deal with
    # version numbers in the DDU method doing the command calling.
    where_it_is = os.path.join(ddu_extracted_path, "DDU v{}".format(Latest_DDU_Version_Raw))
    file_names = os.listdir(where_it_is)

    for file_name in file_names:
        shutil.move(os.path.join(where_it_is, file_name), ddu_extracted_path)


def latest_windows_version(majorversion):
    with urllib.request.urlopen(
            "https://github.com/24HourSupport/CommonSoftware/raw/main/WindowsReleases.json") as url:
        WindowsReleases = json.loads(url.read().decode())

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
            logger("I do not believe it is up to date")
            if returnpendingupdates() == True:
                print("There are pending Windows Updates.")
                print("Please check for Windows Updates and apply updates.")
                print("If you need to restart to apply please do so.")
                print("In that case just reopen AutoDDU_CLI once restarted.")
                print("If no restart is needed, we'll show option to continue in 60 seconds.")
                time.sleep(60)
                if BadLanguage() == False:
                    while True:
                        DewIt = str(input("Type in 'Continue' then press enter to begin: "))
                        if "continue" in DewIt.lower():
                            break
                else:
                    HandleOtherLanguages()
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
        subprocess.call([os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe'), '-silent', '-RemoveMonitors',
                        '-RemoveVulkan', '-RemoveGFE', '-Remove3DTVPlay', '-RemoveNVCP', '-RemoveNVBROADCAST',
                        '-RemoveNvidiaDirs', '-cleannvidia', '-logging'])
        print("1/3 finished with DDU", flush=True)
        sys.stdout.flush()
        subprocess.call([os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe'), '-silent', '-RemoveMonitors',
                        '-RemoveVulkan', '-RemoveAMDDirs', '-RemoveCrimsonCache', '-RemoveAMDCP', '-cleanamd', '-logging'])
        print("2/3 finished with DDU", flush=True)
        sys.stdout.flush()
        subprocess.call([os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe'), '-silent', '-RemoveMonitors',
                        '-RemoveVulkan', '-RemoveINTELCP', '-cleanintel', '-logging'])
        print("3/3 finished with DDU", flush=True)
        sys.stdout.flush()
        logger("Successfully finished DDU commands in safe mode.")
    else:
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

# For testing you pass in a list with
# [{'NVIDIA GeForce RTX 3080': ['GA102', '10de', '2206']}, []]
#                   GPU infos                           , 
def mainpain(TestEnvironment):

    print(TestEnvironment)
    # Wine Easter Egg
    try: # Tries to open key only present when running under Wine
        aKey = winreg.OpenKey(winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER), r"Software\Wine", 0, winreg.KEY_READ)

        subprocess.run("winebrowser https://funny.computer/linux/", shell=True) # Nobody actually installs IE in their prefixes right?
        print("Someone actually ran this on Linux lol")
        while True:
            time.sleep(1)
    except:
        pass
    if len(TestEnvironment) == 0:
        os.system('mode con: cols=80 lines=40')
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x00|0x100))
        accountforoldcontinues(0)
    else:
        accountforoldcontinues(1)
    myapp = singleinstance()
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
    sys.stdout.flush()
    print("This software comes with no warranty as stated in the MIT License.")
    print("Copyright (c) 2022-present Daniel Suarez")
    print("\n", flush=True)
    checkBatteryLevel()
    try:
        logger("Version " + Version_of_AutoDDU_CLI)
        logger("Running under user {}".format(os.getlogin()))
        try:
            logger("Directory name of where executable is located is: " + str(os.path.dirname(sys.executable)))
            logger("Contents of directory contain executable: " + str("AutoDDU_CLI.exe" in os.listdir(os.path.dirname(sys.executable)))  )
        except:
            logger("Failed to log info about directory where sys.executable is located with error: " +  str(traceback.format_exc()))
        if not insafemode():
            if internet_on():
                try:
                    handleoutofdate()
                except:
                    logger("Failed to check if up to date with error " + str(traceback.format_exc()) )
        if myapp.alreadyrunning():
            print(r"""
THERE IS A POSSIBILITY YOU OPENED THIS MORE THAN ONCE BY ACCIDENT. PLEASE 
CLOSE THIS WINDOW AS IT IS VERY RISKY TO HAVE MORE THAN ONE OPEN.                  
                  """)
            sys.stdout.flush()
            while True:
                if len(TestEnvironment) == 0:
                    time.sleep(1)
                else:
                    return("Duplicate app instance")
        if not os.path.exists(Persistent_File_location) or getpersistent() == -1 or getpersistent() == 0:
            default_config()
            if len(TestEnvironment) == 0:
                if not internet_on(): 
                    # There is a code path for handling this in safe mode when we have an internet connection. It's when there's not an internet connection that we have a problem.
                    print("You DO NOT RUN AUTODDU IN SAFE MODE THE FIRST TIME. WE ALSO NEED AN INTERNET CONNECTION.")
                    print("AutoDDU should be first launched outside of safe mode in a normal user profile LIKE THE WIKI SAYS TO.")
                    print("AutoDDU will put itself in safe mode when it needs to, stop assuming and")
                    print("instead read the wiki you were sent.")
                    print("Get out of safe mode if you're in it, login to the user profile you always use THEN LAUNCH THIS.")
                    print("MAKE SURE TO HAVE AN INTERNET CONNECTION")
                    while True:
                        time.sleep(1)
                # if IsKasperskyInstalled() == True:
                #     print("Kaspersky is installed. This software is known to cause")
                #     print(" issues with running AutoDDU at multiple steps, and has")
                #     print(" caused many headaches. Highly recommended to either fully")
                #     print(" uninstall Kaspersky or at the very least completely ")
                #     print( " disabling it. I've tried to send AutoDDU for analysis")
                #     print(" to Kaspersky multiple times but they keep saying all is good.")
                #     print(" We'll continue in 3 minutes, between now and 3 minutes please disable it.")
                #     time.sleep(180)
                #     print("Continuing with normal setup now with the assumption you disabled it.")
                #     print(" ")
                print_menu1()
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
            time.sleep(1)
            mainshit = ""
            if obtainsetting("bypassgpureq") == 0:
                try:
                    # For testing you replace getgpuinfos() with proper dict such as:
                    # {'NVIDIA GeForce RTX 3080': ['GA102', '10de', '2206']}
                    if len(TestEnvironment) == 0:
                        mainshit = checkifpossible(getsupportstatus(getgpuinfos()))
                    else:
                        mainshit = checkifpossible(getsupportstatus(TestEnvironment[0]))
                except Exception:
                    print("ERROR UNRECOVERABLE PLEASE REPORT THIS TO EVERNOW: \n", flush=True)
                    print(traceback.format_exc())
                    while True:
                        if len(TestEnvironment) == 0:
                            time.sleep(1)
                        else:
                            return("GPU REQ TEST  "  + str(traceback.format_exc())   )

                print(mainshit[1])
                if mainshit[0] == 0:
                    print(r"""
    INCOMPATIBLE GPU CONFIGURATION FOUND.
    
    CURRENTLY NO WAY TO RUN AUTODDU WITH THIS CONFIGURATION.
    
    IF THIS IS A MISTAKE PLEASE SHARE THIS WITH EVERNOW:
        """, flush=True)
                    print(mainshit)
                    while True:
                        if len(TestEnvironment) == 0:
                            time.sleep(1)
                        else:
                            return("Incompatible GPU")

            print(r"""
This will update Windows if out of date, download needed drivers,
disable internet (needed to prevent Windows from fucking it up), 
and push you into safe mode. IT WILL DO THIS FOR YOU. 
YOU DO NOT NEED TO DO ANYTHING EXCEPT LAUNCH THIS APP ONCE RESTARTED
IN SAFE MODE
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
            if len(obtainsetting("provideowngpuurl")) != 0:
                download_drivers(obtainsetting("provideowngpuurl"))

            elif len(obtainsetting("provideowngpuurl")) == 0 and obtainsetting("bypassgpureq") == 0:
                download_drivers(mainshit[2])
            if obtainsetting("disablewindowsupdatecheck") == 0 and not insafemode():
                if len(TestEnvironment) == 0:
                    uptodate()
            changepersistent(1)
        if getpersistent() == 1:
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
After once you are at a black wallpaper you will need to launch
the "AutoDDU_CLI.exe" on your desktop to let us start working again.
            
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
            os.path.exists(os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe')) # Makes sure nothing like Kaspersky has fucked us over, will make AutoDDU error out before doing anything annoying to recover from.
            suspendbitlocker()
            if len(TestEnvironment) == 0:
                time.sleep(5)
                safemode(1)

            print("May seem frozen for a bit, do not worry, we're working in the background.")
            workaroundwindowsissues()  # TODO: this is REALLY FUCKING STUPID
            makepersist()
           # BackupLocalAccount()
            if len(TestEnvironment) == 0:
                enable_internet(False)
                
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
            print(r"""
This will now boot you back into normal mode.
              
You can login to your normal user profile, no need for DDU.
              
Once you login you run this one last time where we will install
the drivers properly, then once finished turn on your internet.
NOTE AUTODDU WILL OPEN BY ITSELF AFTER YOU LOGIN, JUST WAIT TILL IT DOES.              
Will restart in 15 seconds.
              
                    """, flush=True)

            if len(TestEnvironment) == 0:    
                safemode(0)
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
                subprocess.call('shutdown /r -t 10', shell=True)
                print("Command to restart has been sent.")
                while True:
                    time.sleep(1)

        if getpersistent() == 3:
            print("Please wait 5 seconds and we'll start the last process")
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
                intel = 0
                for driver in s:
                    if "intel" not in driver or obtainsetting("inteldriverassistant") == 0:
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
                    else:
                        logger("I saw an Intel driver as {} to run later".format(driver))
                        intel = 1
                if intel == 1:
                    print("Intel driver needed, will turn on internet (needed for installer), please wait a bit",
                          flush=True)
                    if len(TestEnvironment) == 0:
                        enable_internet(True)
                    time.sleep(10)
                    if os.path.exists(os.path.join(PROGRAM_FILESX86,"Intel", "Driver and Support Assistant")):
                        print("Your Intel GPU driver will be pushed in by Windows Updates after this exists, we're done here")
                        logger("Found already installed Intel assistant driver")
                    else:
                        logger("Did not find Intel assistant driver, launching our own")
                        print("Installing Intel driver assistant")
                        if len(TestEnvironment) == 0:
                            subprocess.call(str(os.path.join(Appdata, "AutoDDU_CLI", "Drivers", "inteldriver.exe")), shell=True)
                        else:
                            mimicinstalleddrivers.append("inteldriver.exe")
                    try:
                        os.remove(Script_Location_For_startup)
                    except:
                        pass
                    changepersistent(0)
                print("All driver installations complete. Have a good day.")
                print("Closing in ten minutes. Feel free to close early if no problems", flush=True)
            else:

                print("""
Due to no drivers being detected, our work is done.
Now it is up to you to install the drivers like you normally would.
Closing in ten minutes. Feel free to close early if no problems
                """, flush=True)
            if len(TestEnvironment) == 0:
                enable_internet(True)
            cleanup()
            changepersistent(0)
            if os.path.exists(os.path.join(Users_directory,"Default", "AutoDDU_CLI.exe")):
                os.remove(os.path.join(Users_directory,"Default", "AutoDDU_CLI.exe"))
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


print(mainpain([]))
