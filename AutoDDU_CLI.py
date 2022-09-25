Version_of_AutoDDU_CLI = "0.1.1"
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

advanced_options_dict_global = {"disablewindowsupdatecheck": 0, "bypassgpureq": 0, "provideowngpuurl": [],
                                "disabletimecheck": 0, # Kept here even though it does nothing. This is for backwards compatibility reason
                                # For example lets say someone runs latest version but it has a problem, then they're told to try an old version,
                                # if it's old enough it will expect this to be in config, and it will fail if it isn't, even though there was
                                # never a public AutoDDU release that actually did something with this variable.
                                "RemovePhysX": 0, "disableinternetturnoff": 0, "donotdisableoverclocks": 0,
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



def returnpendingupdates():
    # https://stackoverflow.com/questions/70792656/how-do-i-get-pending-windows-updates-in-python
    # https://github.com/Evernow/AutoDDU_CLI/issues/14
        return False

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
            urllib.request.urlopen('https://www.google.com/', timeout=3)
            return True
        except:
            time.sleep(1)
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
    while option != "11":
        clear()
        time.sleep(1)
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
            AutoStartupkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,"Software\Microsoft\Windows\CurrentVersion\Run",0,winreg.KEY_ALL_ACCESS)
            winreg.DeleteValue(AutoStartupkey, '*AutoDDU_CLI')
        except:
            pass


        # Setup registry key to enable startup
        open = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,"Software\Microsoft\Windows\CurrentVersion\Run",0,winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(open,"*AutoDDU_CLI",0,winreg.REG_SZ,exe_location)
        winreg.CloseKey(open)
    except:
        print("Failed to enable the ability for AutoDDU to startup by itself")
        print("when out of safe mode. You'll have to start it manually in safe mode and")
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

    DictOfGPUs = getgpuinfos(testing)
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


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_helper(url, fname,showbar=True):
    while not internet_on():
        logger("Saw no internet, asking user to connect")
        print("No internet connection")
        print("Please make sure internet is enabled")
        print("Retrying in 30 seconds")
        time.sleep(30)
    logger("Downloading  file from {url} to location {fname}".format(url=url, fname=fname))
    if showbar==True:
        print("Downloading file {}".format(fname.split("\\")[-1]))
    remaining_download_tries = 16
    while remaining_download_tries > 0:
        if os.path.exists(fname):
            os.remove(fname)
        try:
            if (remaining_download_tries % 3 == 0 or obtainsetting('dnsoverwrite') == 1) and 'microsoft' not in url.lower(): # Microsoft has this fake javascript form crap, that while urlretrieve can handle, urlopen does not.
                # For bad DNS issues encountered on NVIDIA server, very rare but never hurts to have a fallback for this event.
                # Credit to RandoNando for figuring this out, and the referenced GitHub issues for the issues I encountered while testing this.

                logger("Landed in DNSFallback")
                HOST = url.replace('https://','').replace('http://','').replace('www.','').split('/')[0]
                logger(str(HOST))
                urlparsing = url.replace('https://','').replace('http://','').replace('www.','')
                urlparsing = url.replace('https://','').replace('http://','').replace('www.','')[urlparsing.find('/')+1:]
                logger(str(urlparsing))
                if importlib.metadata.version('dnspython') == '2.2.1': # https://github.com/rthalley/dnspython/issues/834
                    import dns.win32util
                    dns.win32util._getter_class = dns.win32util._RegistryGetter
                res = dns.resolver.Resolver()
                res.nameservers = ['8.8.8.8'] # Google DNS
                answers = res.resolve(HOST)
                for rdata in answers:
                    address = (rdata.address)
                logger("Got the folloing IP address from resolver" + str(address))
                url_dnsfallback = (f'http://{address}/{urlparsing}')
                logger(url_dnsfallback)
                headers = dict( 
                                [
                                    (
                                        "User-agent",
                                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
                                    ),
                                    (
                                        "Referer",
                                        "https://www.amd.com/en/support/graphics/amd-radeon-6000-series/amd-radeon-6700-series/amd-radeon-rx-6700-xt",
                                    ),
                                    ("Host", HOST), # https://github.com/python/cpython/issues/96287 which means no progress bar for dns fallback, but not much else that comes to mind that is practical
                                    ("test", "test"),
                                ]
                            )
                request = urllib.request.Request(url=url_dnsfallback, headers=headers)

                with urllib.request.urlopen(request,timeout=3) as response:
                    with open(fname, "wb") as file_:
                        shutil.copyfileobj(response, file_)
                break
            else:
                opener = urllib.request.build_opener()

                opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'),
                                    ('Referer', "https://www.amd.com/en/support/graphics/amd-radeon-6000-series/amd-radeon-6700-series/amd-radeon-rx-6700-xt")]
                urllib.request.install_opener(opener)
                if showbar==True:
                    with DownloadProgressBar(unit='B', unit_scale=True,
                                            miniters=1, desc=url.split('/')[-1]) as t:
                        urllib.request.urlretrieve(url, filename=fname, reporthook=t.update_to)
                    print("\n")
                else:
                    urllib.request.urlretrieve(url, filename=fname)
                break
        except:
            logger(str(traceback.format_exc()))
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
    subprocess.call((ddu_zip_path + " -o{}".format(ddu_extracted_path) + " -y"), shell=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
            if obtainsetting("bypassgpureq") == 0:
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
                download_drivers(mainshit[1])
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
            makepersist()
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
                AutoStartupkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,"Software\Microsoft\Windows\CurrentVersion\Run",0,winreg.KEY_ALL_ACCESS)
                winreg.DeleteValue(AutoStartupkey, '*AutoDDU_CLI')
            except:
                print("We failed for some reason to make sure we aren't setup to start on restart everytime.")
                print("If we still start on restart delete the AutoDDU executable in:")
                print(str(exe_location))
                print("Delete it after we are done enabling the internet.")
                print("We;re going to start the process of enabling the internet in 15 seconds.")
                time.sleep(15)
                logger("Failed to remove autorun registry key")
                logger(str(traceback.format_exc()))
            changepersistent(0)
            if len(TestEnvironment) == 0:
                    proc = multiprocessing.Process(target=enable_internet, args=(True,)) 
                    proc.start()
                    print("Please wait ~10 seconds for us to enable the internet and do some cleanup.")
                    time.sleep(5)
                    if proc.is_alive():
                        time.sleep(10)

                    proc.terminate()

            cleanup()
            changepersistent(0)
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
