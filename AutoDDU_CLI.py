advanced_options_dict_global = {"disablewindowsupdatecheck" : 0, "bypassgpureq" : 0, "provideowngpuurl" : [], "disabletimecheck" : 0, "disableinternetturnoff" : 0, "donotdisableoverclocks": 0}
# Default settings
from datetime import datetime, timezone, date
import os,time    
import wmi
import sys
import subprocess
import requests
from win32com.shell import shell, shellcon
import shutil
import platform
#import wexpect
import zipfile
import traceback
import json
import urllib.request
from subprocess import CREATE_NEW_CONSOLE
clear = lambda: os.system('cls')

Appdata = shell.SHGetFolderPath(0, shellcon.CSIDL_COMMON_APPDATA, 0, 0) 
Appdata_AutoDDU_CLI = os.path.join(Appdata, "AutoDDU_CLI")
Persistent_File_location = os.path.join(Appdata, "AutoDDU_CLI", "PersistentDDU_Log.txt")
root_for_ddu_assembly = os.path.join(Appdata, "AutoDDU_CLI", "DDU_Parser")
ddu_AssemblyInfo = os.path.join(Appdata, "AutoDDU_CLI", "DDU_Parser\\", "AssemblyInfo.vb")
ddu_zip_path = os.path.join(Appdata, "AutoDDU_CLI", "DDU_Parser\\", "DDU.exe")
seven_zip = os.path.join(Appdata, "AutoDDU_CLI", "DDU_Parser\\", "7z.exe")
ddu_extracted_path = os.path.join(Appdata, "AutoDDU_CLI", "DDU_Extracted")

exe_location = os.path.join(Appdata_AutoDDU_CLI, "AutoDDU_CLI.exe")
Script_Location_For_startup = os.path.join(shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup' , 'AutoDDUStartup.vbs')

log_file_location = os.path.join(Appdata_AutoDDU_CLI, "AutoDDU_LOG.txt")

#Only Fermi professional (NVS, Quadro, Tesla) is supported, and only till the end of 2022.
FERMI_NVIDIA = "GF108","GF108","GF108-300-A1","GF106","GF106-250","GF116-200","GF104-225-A1","GF104","GF104-300-KB-A1","GF114","GF100-030-A3","GF100-275-A3","GF100-375-A3","GF119","GF108","GF118","GF116","GF116-400","GF114-200-KB-A1","GF114-325-A1","GF114-400-A1","GF110","GF110-270-A1","GF110-275-A1","GF110-375-A1","2x GF110-351-A1","GF100","GF108","GF106","GF106","GF108","GF119-300-A1","GF108-100-KB-A1","GF108-400-A1","GF119 (N13M-GE)","GF117 (N13M-GS)","GF108 (N13P-GL)","GF117","GF106 (N12E-GE2)","GF116","GF108","GF114 (N13E-GS1-LP)","GF114 (N13E-GS1)","GF117","GF108","GF117","GF108",""

EOL_NVIDIA = "G98","G96b","G94b","G92b","MCP79XT","N10M-GE2(G98)","N10M-GE1(G98)","N10M-GE1(G96b)","N10P-GV1(G96b)","N10P-GE1(G96b)","N10E-GE1(G94b)","N10E-GS1(G94b)","GT218","GT216","GT215","MCP89","GT215-301-A3","G92","GT216","GT218","MCP68S","MCP67QV","MCP73","MCP76","NV44","G72","G73","G73-B1","G70","G71","2x G71","MCP78","G86","G84","G80","GM108","GM107","NB8M(G86)","NB8P(G84)","NB8P(G92)","C77","MCP79","MCP7A-S","MCP7A-U","G96-200-c1","G96a","G96b","G96-300-C1","G94a","G92-150-A2","G94a","G94b","G94-300-A1","G92a2 G92b","G92a","G92b","G92-420-A2","2x G92","MCP77MH","MCP79MH","NB9M-GE(G98)","NB9M-GE(G86)","MCP79MX","NB9P(G96)","NB9P-GV(G96)","NB9P-GE2(G96)","NB9P-GS(G96)","NB9P-GS1(G84)","NB9P-GT(G96)","NB9E-GE(G96)","NB9E-GS(G94)","NB9E-GT(G94)","NB9E-GT2(G92)","NB9E-GTX(G92)","NV34","NV34B","NV31","NV36","NV30","NV35","NV38","NV34M","NV31M","NV36M","C51M","NV44M","NV43M","NV41M","MCP67MV","MCP67M","G72M","G73M","G73-N-B1","G70M","G71M","NV11M","NV1A (IGP) / NV11 (MX)","NV15","NV16","NV1A","NV11","NV20","NV17M","NV18M","NV28M","NV11","G72GLM","G86M","G98M","G84M","GT218M","GT216M","NV1","NV3","NV4","NV6","NV5","NV37GL","NV43GL","NV41","NV45GL","NV40","NV45GL A3","NV40","NV43","G71GLM","G73GL","G73GLM","G92M","G84GL","G96M","G94M","G96","GT218GL","G100GL-U","G94","GT200GL","GT215M","NV34GL","NV35GL","NV30GL","NV36GL","NV40GL","NV17","NV28","NV18","MCP51","2xG98","2xNV43","G94","G100GL","G100GL-U","N13M-GE","NV45GL","NV40","NV45GL A3","NV11GL ","G96C","G94GLM"

KEPLER_NVIDIA = "GK107","GK208-301-A1","GK208","GK208-400-A1","GK106","GK107-450-A2","GK-106-400-A1","GK106-220-A1","GK106-240-A1","GK106-400-A1","GK104-200-KD-A2","GK104-300-KD-A2","GK104-325-A2","GK104-400-A2","2x GK104-355-A2","GK107 (N13P-LP)","GK107 (N13P-GS)","GK107 (N13P-GT)","GK107 (N13E-GE)","GK104 (N13E-GR)","GK104 (N13E-GSR)","GK104 (N13E-GTX)","GK104","GK208-203-B1","GK208-201-B1","GK107-425-A2","GK104-225-A2","GK104-425-A2","GK110-300-A1","GK110-425-B1","GK110-400-A1","GK110-430-B1","2x GK110-350-B1","GK110","GK110B", "GK110GL"

Professional_NVIDIA_GPU = ["Quadro", "Tesla", "NVS"]

Exceptions_laptops = "710A","745A","760A","805A","810A","810A","730A","740A" # Kepler laptops GPUs with no M in the name.

EOL_AMD = "16899-0" , "Tahiti", "Tahiti XT",  "Malta",  "18800-1" , "28800-5" , "28800-6" , "Broadway" , "CW16800-A" , "CW16800-B" , "Cedar" , "Cypress" , "ES1000" , "Flipper" , "Hemlock" , "Hollywood" , "IBM" , "Juniper" , "M1" , "M10" , "M11" , "M12" , "M18" , "M22" , "M24" , "M26" , "M28" , "M3" , "M4" , "M52" , "M54" , "M56" , "M58" , "M6" , "M62" , "M64" , "M66" , "M68" , "M7" , "M71" , "M72" , "M74" , "M76" , "M82" , "M86" , "M88" , "M9" , "M9+" , "M92" , "M93" , "M96" , "M97" , "M98" , "Mach32" , "Mach64" , "Mach64 GT" , "Mach64 GT-B" , "Mach64 LT" , "Mach8" , "Madison" , "Park" , "Pinewood" , "R100" , "R200" , "R250" , "R300" , "R350" , "R360" , "R420" , "R423" , "R430" , "R480" , "R481" , "R520" , "R580" , "R580+" , "R600" , "R680" , "R700" , "RC1000" , "RC300" , "RC410" , "RS100" , "RS200" , "RS250" , "RS300" , "RS350" , "RS400" , "RS480" , "RS482" , "RS485" , "RS600" , "RS690" , "RS740" , "RS780" , "RS880" , "RV100" , "RV200" , "RV250" , "RV280" , "RV350" , "RV370" , "RV380" , "RV410" , "RV505" , "RV515" , "RV516" , "RV530" , "RV535" , "RV560" , "RV570" , "RV610" , "RV620" , "RV630" , "RV635" , "RV670" , "RV710" , "RV730" , "RV740" , "RV770" , "RV790" , "Rage 2" , "Rage 3" , "Rage 3 Turbo" , "Rage 4" , "Rage 4 PRO" , "Rage 6" , "Rage Mobility" , "Redwood" , "Turks" , "Xenos Corona" , "Xenos Falcon" , "Xenos Jasper" , "Xenos Vejle" , "Xenos Xenon"

unrecoverable_error_print = (r"""
   An unrecoverable error has occured in this totally bug free 
   software.
   
   Chika is dissapointed, but at least this error shows what is wrong.
   Please share the below stacktrace to Evernow so he can fix it.
   In addition above the stacktrace is the directory of where
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

def obtainsetting(index):
    with open(AutoDDU_CLI_Settings, 'r+') as f:
        advanced_options_dict = json.load(f)
        return(advanced_options_dict[index])


def default_config():
    if not os.path.exists(Appdata_AutoDDU_CLI):
        os.makedirs(Appdata_AutoDDU_CLI)
    with open(AutoDDU_CLI_Settings, "w+") as outfile:
        json.dump(advanced_options_dict_global, outfile)

def AdvancedMenu():
    logger("User entered AdvancedMenu")
    option = -1
    while option != "7":
         clear()
         time.sleep(1)
         print ("WARNING: THIS MAY BEHAVE UNEXPECTADLY!",flush=True)
         print ('1 --' + AdvancedMenu_Options(1),flush=True) # Disable Windows Updates check
         print ('2 --' + AdvancedMenu_Options(2),flush=True) # Bypass supported GPU requirement
         print ('3 --' + AdvancedMenu_Options(3),flush=True) # Provide my own driver URLs
         print ('4 --' + AdvancedMenu_Options(4),flush=True) # Disable time check
         print ('5 --' + AdvancedMenu_Options(5),flush=True) # Do not turn internet off when needed
         print ('6 --' + AdvancedMenu_Options(6),flush=True) # Do not disable overclocking/undervolts/fan curves
         print ('7 -- Start',flush=True )
         option = str(input('Enter your choice: '))
         change_AdvancedMenu(option)
         
def AdvancedMenu_Options(num):
  logger("User is changing option " + str(num))
  with open(AutoDDU_CLI_Settings, 'r+') as f:
    advanced_options_dict = json.load(f)
    if num == 1:
        if advanced_options_dict["disablewindowsupdatecheck"] == 0:
            return(" Disable Windows Updates check")
        else:
            return(" Enable Windows Updates check")
        
    if num == 2:
        if advanced_options_dict["bypassgpureq"] == 0:
            return(" Bypass supported GPU requirement")
        else:
            return(" Enable supported GPU requirement")
        
    if num == 3:
        if len(advanced_options_dict["provideowngpuurl"]) == 0:
            return(" Provide my own driver URLs")
        else:
            return(" Let AutoDDU look for drivers")
        
    if num == 4:
        if advanced_options_dict["disabletimecheck"] == 0:
            return(" Disable time check")
        else:
            return(" Enable time check")
        
    if num == 5:
        if advanced_options_dict["disableinternetturnoff"] == 0:
            return(" Do not turn internet off when needed")
        else:
            return("Turn internet off when needed")
        
    if num == 6:
        if advanced_options_dict["donotdisableoverclocks"] == 0:
            return(" Do not disable overclocking/undervolts/fan curves")
        else:
            return(" Disable overclocking/undervolts/fan curves")
    f.seek(0)
    json.dump(advanced_options_dict, f, indent=4)
    f.truncate()
    advanced_options_dict_global = advanced_options_dict
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
            option = str(input('Type in the driver download URL: '))
            advanced_options_dict["provideowngpuurl"].append(option)
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
    f.seek(0)
    json.dump(advanced_options_dict, f, indent=4)
    f.truncate()
        

def print_menu1():
    print ('Press Enter Key -- Start' ,flush=True)
    print ('2 -- Advanced Options' ,flush=True)    
    option = str(input('Enter your choice: '))
    if option == "2":
        AdvancedMenu()



def returnifduplicate():
    # TODO: If someone downloads this twice the process name will be "AutoDDU_CLI.exe (1) , which won't be caught by this
    processes = list() 
    for process in wmi.WMI().Win32_Process():
        processes.append(process.Name)
    return(processes.count("AutoDDU_CLI.exe") > 2)


def BadLanguage():
    lang = wmi.WMI().Win32_OperatingSystem()[0].OSLanguage
    # https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/win32-operatingsystem
    ok_languages = [9, 1033, 2057, 3081, 4105, 5129, 6153, 7177, 8201, 10249, 11273] # Basically all english versions
    logger("Language is " + str(lang))
    if lang in ok_languages:
        return False
    else:
        return True
def HandleOtherLanguages():
    # Due to some languages not having correct letters on their keyboards
    # Instead of doing the "I do" shit, we just have them press enter on their keyboards
    # twice. Much safer, since I assume every keyboard has this.. right?
    howmany = 0
    while howmany < 2 :
        input("Press your enter key {n} more time(s)".format(n = 2 - howmany))
        howmany +=1
    print("Starting!")


def PCIID(vendor, device):
    with urllib.request.urlopen("https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/PCI-IDS.json") as url:
        data = json.loads(url.read().decode())
        return(data[vendor]['devices'][device]['name'])


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
    os.remove(os.remove(Script_Location_For_startup))
    try:
        os.rmdir(os.path.join(Appdata, "AutoDDU_CLI", "Drivers")) 
    except:
        pass
    logger("Finished cleanup")
def makepersist():
    download_helper("https://github.com/Evernow/AutoDDU_CLI/raw/main/dist/AutoDDU_CLI.exe", exe_location)
    lines = ['Set WshShell = CreateObject("WScript.Shell" )', 'WshShell.Run """{directory}""", 1'.format(directory=exe_location), "Set WshShell = Nothing"]
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
        subprocess.call('reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_SZ /d 1 /f', shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        subprocess.call('reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName /t REG_SZ /d DDU /f', shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        
        subprocess.call('reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword /t REG_SZ /d 1234 /f', shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        
        
        subprocess.call('reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoLogonCount /t REG_DWORD /d 1 /f', shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        print("INFO: Successfully created autologin task")
        logger("Finished autologin successfully")
    except Exception as f:
        logger("Failed autologin with this: " + str(f))
        global login_or_not
        login_or_not = """
        You will need to login manually to the DDU
        profile account we created."""
def workaroundwindowsissues():
    download_helper("https://download.sysinternals.com/files/PSTools.zip", os.path.join(Appdata_AutoDDU_CLI, "PsTools.zip"))
    with zipfile.ZipFile(os.path.join(Appdata_AutoDDU_CLI, "PsTools.zip"), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(Appdata_AutoDDU_CLI, "PsTools"))
    subprocess.call('NET USER DDU 1234 ', shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        subprocess.call('{directory_to_exe} -accepteula -u DDU -p 1234 i- exit'.format(directory_to_exe=os.path.join(Appdata_AutoDDU_CLI, "PsTools", "PsExec.exe")), shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except:
        pass # This is meant to fail.
    logger("Did prep work for working around Windows issue")
    download_helper("https://github.com/Evernow/AutoDDU_CLI/raw/main/dist/AutoDDU_CLI.exe", r"C:\Users\DDU\Desktop\AutoDDU_CLI.exe")    
    logger("Downloaded DDU to DDU profile")
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
    #TODO: this is dumb
    
    #TODO: investigate this workaround later: https://community.spiceworks.com/topic/247395-create-a-user-profile-without-logon?page=1#entry-6915365
    
    

def getsupportstatus():
    controllers = wmi.WMI().Win32_VideoController()
    gpu_dictionary = dict() # GPU NAME = [VENDOR ID, DEVICE ID, ARCHITECTURE , RAW OUTPUT (for troubleshooting purposes), supportstatus (0=unchecked, 1=supported, 2=kepler, 3=fermiprof, 4=EOL), professional/consumer] 
    logger("Working in getsupportstatus with this wmi output: ")
    for controller in controllers:
       name = controller.wmi_property('Name').value.encode("ascii", "ignore").decode("utf-8")
       gpu_list_to_parse = controller.wmi_property('PNPDeviceID').value.encode("ascii", "ignore").decode("utf-8").lower().split("\\") # .lower() is due to Windows not following PCI naming convention.
       logger(name)
       logger(''.join(gpu_list_to_parse))
       for gpu in gpu_list_to_parse:
           # We need to filter out by vendor or else we can parse in shit like Citrix or capture cards.
           if "dev_" in gpu and ("ven_10de" in gpu or "ven_121a" in gpu or "ven_8086" in gpu
                                                           or "ven_1002" in gpu): # 1002 = AMD ; 8086 = Intel ; 10de = NVIDIA ; 121a = Voodoo (unlikely but I mean.. doesn't hurt?)
                   
                   todays_date = date.today().year
                   
                   # Us assuming a ven and dev ID is 4 characters long is a safe one: https://docs.microsoft.com/en-us/windows-hardware/drivers/install/identifiers-for-pci-devices
                   Arch = PCIID(gpu[gpu.find('ven_')+4:gpu.find('ven_')+8], gpu[gpu.find('dev_')+4:gpu.find('dev_')+8])
                   Arch = Arch[:Arch.find(' ')]
                   Vendor_ID = gpu[gpu.find('ven_')+4:gpu.find('ven_')+8]
                   Device_ID = gpu[gpu.find('dev_')+4:gpu.find('dev_')+8]
                   supportstatus = 0
                   Consumer_or_Professional = ""
                   if Vendor_ID == '121a': # Voodoo (wtf lol)
                       logger("Got Voodoo GPU")
                       supportstatus = 4
                       Consumer_or_Professional = "Consumer"
                   if Vendor_ID == '8086': # Intel
                       logger("Got Intel GPU") 
                       supportstatus = 1
                       Consumer_or_Professional = "Consumer"
                   if Vendor_ID == '1002': # AMD
                       logger("Got Voodoo GPU")
                       for possibility in EOL_AMD:
                           if Arch in possibility:
                               logger("Got EOL AMD GPU with code " + Arch)
                               supportstatus = 4
                       if supportstatus != 4:
                            logger("Got Supported AMD GPU with code " + Arch)
                            supportstatus = 1
                       Consumer_or_Professional = "Consumer" # There are professional AMD GPUs but are EXTREMELY rare and I haven't built a driver search for them, nor intend to.
                   
                   
                   if Vendor_ID == '10de': # NVIDIA
                       logger("Got NVIDIA GPU with code " + Arch)
                   
                       # Check if professional or consumer
                       for seeifprof in Professional_NVIDIA_GPU:
                           if seeifprof.lower() in name.lower():
                               logger("Got NVIDIA prof")
                               Consumer_or_Professional = "Professional"
                       if Consumer_or_Professional != "Professional":
                           logger("Got NVIDIA consumer")
                           Consumer_or_Professional = "Consumer"
                       # Nightmare begins
                       for possibility in EOL_NVIDIA:
                           if Arch in possibility:
                               logger("Got EOL NVIDIA")
                               supportstatus = 4 # EOL
                       for possibility in FERMI_NVIDIA:
                           if Arch in possibility:
                               logger("Got NVIDIA FERMI")
                               for seeifprof in Professional_NVIDIA_GPU:
                                   
                                   if Consumer_or_Professional == "Professional" and todays_date < 2023: # EOL For Fermi prof
                                       logger("Got professional fermi")
                                       supportstatus = 3 # fermiprof
                               if supportstatus != 3: 
                                   logger("Got consumer fermi")
                                   supportstatus = 4 # EOL
                       for possibility in KEPLER_NVIDIA:
                            if Arch in possibility:
                                logger("Got Kepler")
                                if "M" in name.upper():
                                    logger("Got laptop kepler (main)")
                                    supportstatus = 4 # EOL
                                else:
                                    for exception_fuckinglaptops in Professional_NVIDIA_GPU:
                                        if exception_fuckinglaptops in name.upper():
                                            logger("Got laptop kepler (secondary)")
                                            supportstatus = 4 # EOL
                                    if supportstatus != 4 and todays_date < 2025: # In reality it ends in mid 2024, but this is fine.
                                        logger("Got desktop supported kepler")
                                        supportstatus = 2 # kepler
                       if supportstatus == 0:
                            logger("Got supported NVIDIA")
                            supportstatus = 1
                               
                           
                   # This approach covers for stupid SLI or dual GPUs (looking at you Anderson)            
                   gpu_dictionary[name] = [Vendor_ID, Device_ID, Arch, gpu, supportstatus, Consumer_or_Professional]
    logger("Finished getsupportstatus with this dictionary: " + str(gpu_dictionary))               
    return(gpu_dictionary) 


# supportstatus = 0=unchecked, 1=supported, 2=kepler, 3=fermiprof, 4=EOL
# [VENDOR ID, DEVICE ID, ARCHITECTURE , RAW OUTPUT, supportstatus, professional/consumer] 
def checkifpossible(): # Checks edge GPU cases and return list of GPU drivers to downloaded
    # WIP to prevent different driver branches being installed (like R470 and R510 or R510 prof and R510 consumer)
    Consumer = 0
    Professional = 0
    Fermi = 0
    Kepler = 0
    
    dict_of_GPUS = getsupportstatus()
  #  print(dict_of_GPUS)
    drivers_to_download = list()
    with urllib.request.urlopen("https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/nvidia_gpu.json") as url:
        data_nvidia = json.loads(url.read().decode())
    NVIDIA_Consumer = data_nvidia["consumer"]["link"]
    NVIDIA_Professional = data_nvidia["professional"]["link"]
    NVIDIA_R390 = data_nvidia["r390"]["link"]
    NVIDIA_R470_Consumer = data_nvidia["r470_consumer"]["link"]
    NVIDIA_R470_Professional = data_nvidia["r470_professional"]["link"]
    with urllib.request.urlopen("https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/amd_gpu.json") as url:
        data_nvidia = json.loads(url.read().decode())
    AMD_Consumer = data_nvidia["consumer"]["link"] 
    performing_DDU_on = "DDU will be performed on the following GPUs: \n"
    logger("Successfully grabbed NVIDIA drivers from CommonSoftware repo")
    for gpu in dict_of_GPUS:
        name = gpu
        gpu = dict_of_GPUS[gpu]
        #print(gpu)
        if gpu[-2] == 4: # EOL
            performing_DDU_on = "Cannot perform DDU due to the following incompatible GPU found: \n"
            performing_DDU_on = performing_DDU_on + name + "({Arch}) \n".format(Arch = gpu[2])
            return(0, performing_DDU_on, None)
        if gpu[-2] == 3:  # fermiprof
            performing_DDU_on = performing_DDU_on + name + "({Arch}) \n".format(Arch = gpu[2])
            drivers_to_download.append(NVIDIA_R390) 
            Fermi += 1
        if gpu[-2] == 2: # Kepler
            if gpu[-1] == "Consumer":
                performing_DDU_on = performing_DDU_on + name + "({Arch}) \n".format(Arch = gpu[2])
                if NVIDIA_R470_Consumer not in drivers_to_download: # Damn you Anderson. Damn you. It sucks we even need to check for this but.. god dammit...
                    drivers_to_download.append(NVIDIA_R470_Consumer) 
                Kepler += 1
                Consumer += 1
            else: # Professional.. probably (edge cases, TODO)
                performing_DDU_on = performing_DDU_on + name + "({Arch}) \n".format(Arch = gpu[2])
                if NVIDIA_R470_Professional not in drivers_to_download: # Damn you Anderson. Damn you. It sucks we even need to check for this but.. god dammit...
                    drivers_to_download.append(NVIDIA_R470_Professional) 
                Kepler += 1
                Professional += 1
        if gpu[-2] == 1: # Supported
            #print("test")
            performing_DDU_on = performing_DDU_on + name + "({Arch}) \n".format(Arch = gpu[2])
            if gpu[0] == '10de': # NVIDIA
                if gpu[-1] == 'Professional': 
                    if NVIDIA_Professional not in drivers_to_download: # Damn you Anderson. Damn you. It sucks we even need to check for this but.. god dammit...
                        drivers_to_download.append(NVIDIA_Professional) 
                    Professional += 1
                else:
                    if NVIDIA_Consumer not in drivers_to_download: # Damn you Anderson. Damn you. It sucks we even need to check for this but.. god dammit...
                        drivers_to_download.append(NVIDIA_Consumer) 
                    Consumer += 1
            if gpu[0] == '1002': # AMD 
                if AMD_Consumer not in drivers_to_download: # Damn you Anderson. Damn you. It sucks we even need to check for this but.. god dammit...
                    drivers_to_download.append(AMD_Consumer) 
                Consumer += 1
            if gpu[0] == '8086': # Intel 
                if "https://dsadata.intel.com/installer" not in drivers_to_download: # Damn you Anderson. Damn you. It sucks we even need to check for this but.. god dammit...
                    drivers_to_download.append("https://dsadata.intel.com/installer") 
                Consumer += 1
    if Consumer > 0 and Professional > 0:
      performing_DDU_on = "Cannot perform DDU due to seeing Professional and Consumer GPUs \n Which is not supported by NVIDIA: https://nvidia.custhelp.com/app/answers/detail/a_id/2280/~/can-i-use-a-geforce-and-quadro-card-in-the-same-system%3F \n For troubleshooting purposes please show this if this is a mistake: \n"
      performing_DDU_on = performing_DDU_on + dict_of_GPUS
      return(0, performing_DDU_on, None)   
    if Fermi > 0 and Kepler > 0:
      performing_DDU_on = "Cannot perform DDU due to seeing Fermi and Kepler GPUs \n For troubleshooting purposes please show this if this is a mistake: \n"
      performing_DDU_on = performing_DDU_on + dict_of_GPUS
      return(0, performing_DDU_on, None)           
    if len(drivers_to_download) == 0:
        performing_DDU_on = """
WARNING: NO GPUS HAVE BEEN DETECTED BY WINDOWS.
THIS PROCESS WILL CONTINUE BUT YOU WILL NEED TO
INSTALL DRIVERS MANUALLY YOURSELF AFTER THIS PROCESS 
IS OVER. 
        
PLEASE REPORT THIS TO EVERNOW IF IT IS A BUG.
        
Chika is mad and confused at the same time."""
   # logger("Finished checkifpossible with these values: " + 1 + " " + performing_DDU_on + " " + drivers_to_download)
    return(1, performing_DDU_on, drivers_to_download)  

# This keeps track of where we are in the process in a text file. 
def changepersistent(num):
    logger("Changing persistent file to: " + str(num))
    open(Persistent_File_location, 'w').close()
    with open(Persistent_File_location, 'r') as file:
        data = file.readlines()
    
    data.append(str(num))
    with open(Persistent_File_location, 'w') as file:
     file.writelines( data )
     
def getpersistent():
    try:
        with open(Persistent_File_location) as f:
            lines = f.read() 
            first = lines.split('\n', 1)[0]
            logger("Got persistent file to be " + str(first))
            return(int(first))
    except:
        logger("Tried to get persistent file but did not exist or failed")
        return(-1)

def BackupProfile():
    try:
     firstcommand = "net user /add DDU"
     secondcommand = "net localgroup administrators DDU /add"
     subprocess.run(firstcommand, shell=True, check=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)  
     logger("Running command to add created to user to administrators")
     subprocess.run(secondcommand, shell=True, check=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)  
     logger("Successfully created DDU account")
     print("INFO: Created backup profile")
     logger("Created backup profile")
    except Exception as f:
        print("INFO: Did not create backup profile (not an error)")
        logger("Failed creating backup profile with error: " + str(f))
        logger("Failed to create DDU account, likely already existed")


def download_helper(link, file_name):
    logger("Downloading  file from {link} to location {file_name}".format(link=link, file_name=file_name))
    with open(file_name, "wb") as f:
        print("Downloading %s" % file_name)
        my_referer =  "https://www.amd.com/en/support/graphics/amd-radeon-6000-series/amd-radeon-6700-series/amd-radeon-rx-6700-xt"
        # WHY AMD???? WHY???? 
        response = requests.get(link, allow_redirects=True, stream=True,headers={'referer': my_referer, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'})
        total_length = response.headers.get('content-length')
    
        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                sys.stdout.flush()

    logger("Successfully finished download")
    

def download_drivers(list_to_download):
    for driver in list_to_download:
        url = driver.rstrip() # Newline character is grabbed sometimes
        if "intel.com" in url.lower():
            fileextension = "inteldriver.exe"
        else:
            fileextension = url.split("/")[-1]
        if not os.path.exists(os.path.join(Appdata, "AutoDDU_CLI", "Drivers\\")):
            os.makedirs(os.path.join(Appdata, "AutoDDU_CLI", "Drivers\\"))
        download_helper(url, os.path.join(Appdata, "AutoDDU_CLI", "Drivers\\", fileextension))
        
def ddu_download():
    if os.path.exists(ddu_extracted_path) and os.path.isdir(ddu_extracted_path):
        shutil.rmtree(ddu_extracted_path)  
    if not os.path.exists(os.path.join(root_for_ddu_assembly)):
        os.makedirs(os.path.join(root_for_ddu_assembly))
    logger("Starting simple DDU search")
    download_helper('https://raw.githubusercontent.com/Wagnard/display-drivers-uninstaller/WPF/display-driver-uninstaller/Display%20Driver%20Uninstaller/My%20Project/AssemblyInfo.vb',
            ddu_AssemblyInfo)
    
    my_file = open(ddu_AssemblyInfo, "r")

    content = my_file.readlines()

    Latest_DDU_Version_Raw = "" 

    for DDU_Version_Candidate in content:
        if 'AssemblyFileVersion' in DDU_Version_Candidate:
            Latest_DDU_Version_Raw = DDU_Version_Candidate[DDU_Version_Candidate.find('("')+2:DDU_Version_Candidate.find('")')]
    logger("Almost done with simple DDU search")
    try:
        download_helper(
            'https://www.wagnardsoft.com/DDU/download/DDU%20v' + Latest_DDU_Version_Raw + '.exe',
            ddu_zip_path
        )
        logger("Finished DDU search")
    except: # Normal error checking would not catch the error that would occur here.
            # You don't really need to understand this, basically
    # I have been looking at commit history, and there are instances where 
    # he updates the github repos with a new version but doesn't make a release
    # yet, so this accounts for that possibility. Why is it so complicated?
    # It accounts for stuff like this:

    # 18.0.4.0 -> 18.0.3.9

    # 18.0.4.7 -> 18.0.4.6

    # Doesn't work for all cases (and I don't think it's possible for it to do so)
    # but it works 99.99% of the time. 
        logger("Trying complicated DDU search")
        nums = Latest_DDU_Version_Raw.split(".")

        skip = 0 

        for ind in range(skip,len(nums)):
         curr_num = nums[-1-ind]
         if int(curr_num) > 0:
            nums[-1-ind] = str(int(curr_num) - 1)
            break
         else:
            nums[-1-ind] = "9" # DDU seems to stop at 9th versions: https://www.wagnardsoft.com/content/display-driver-uninstaller-ddu-v18039-released

        Latest_DDU_Version_Raw = '.'.join(nums)
        logger("Almost finished with complicated DDU search....")
        try:

         download_helper(
            'https://www.wagnardsoft.com/DDU/download/DDU%20v' + Latest_DDU_Version_Raw + '.exe',
            ddu_zip_path)
         logger("Finished with complicated DDU search....")
        except Exception as f:
                logger("Failed complicated DDU search with error " + str(f))
                print('DDU Download failed! Check your internet connection, if it works please contact Evernow and share with him this error:')
                print(f)
                while True:
                    time.sleep(5)






    #TODO: Automate 7zip download, should always get latest version.

    download_helper(
            'https://github.com/24HourSupport/CommonSoftware/raw/main/7za.exe',
            seven_zip

        )
    print(seven_zip + ' -o' + ddu_extracted_path+ ' x ' + ddu_zip_path +  ' -y > nul')

    subprocess.call(str(seven_zip + ' -o' + ddu_extracted_path+ ' x ' + ddu_zip_path +  ' -y > nul'), shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    # Moves everything one directory up, mainly just to avoid crap with versioning, don't want to have to deal with
    # version numbers in the DDU method doing the command calling.

    where_it_is = ddu_extracted_path + '\\' + 'DDU v' + Latest_DDU_Version_Raw

    file_names = os.listdir(where_it_is)
        
    for file_name in file_names:
        shutil.move(os.path.join(where_it_is, file_name), ddu_extracted_path)

def latest_windows_version():
    download_helper("https://raw.githubusercontent.com/pbatard/Fido/master/Fido.ps1", os.path.join(Appdata_AutoDDU_CLI, "Fido.ps1"))
    p = str(subprocess.Popen("powershell.exe -ExecutionPolicy RemoteSigned -file {directorytofido} -Win {version} -Rel List".format(version = platform.release(), directorytofido = os.path.join(Appdata_AutoDDU_CLI, "Fido.ps1")), 
                   shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=CREATE_NEW_CONSOLE).communicate())
    #p = str(subprocess.Popen('powershell.exe -ExecutionPolicy RemoteSigned -file "C:\\Users\\Daniel\\Videos\\Ps7\ps7\\Fido.ps1" -Win 7 -Rel List', stdout=sys.stdout, shell=True).communicate())
    logger("Got following output from FIDO " + str(p))
    dictionarytest = {}
    for release in p.split('\\n'):
        release = release.replace('build', 'Build')
        if "Build" in release:
            logger("Parsing this line into the release dictionary: " + release)
            dictionarytest[release[3:release.index("(Build")-1]] = release[release.index("(Build")+ 7:release.rfind("-", release.index("(Build"))].split(".", 1)[0]
    
    logger("Working with this finished dictionary: " + str(dictionarytest))    
    return(list(dictionarytest.values())[0])


def uptodate():
    # TODO: Switch to platform.release() once this is fixed: https://bugs.python.org/issue46869
    if "11" not in wmi.WMI().Win32_OperatingSystem()[0].Caption.encode("ascii", "ignore").decode("utf-8"): # No update assistant for W11 yet afaik
        logger("Going to be comparing {current} to {believedlatest}".format(current=str(platform.version().split('.')[2]), believedlatest=str(latest_windows_version())))
        if int(platform.version().split('.')[2]) >= int(latest_windows_version()): #We should consider insider builds. But that's outside the scope of v1 at least.
            print("System up to date already", flush=True)  
            logger("I believe it is up to date")              
    
        else:
            logger("I do not believe it is up to date")
            print("System is out of date, downloading Microsoft Update Assistant.", flush=True)
            download_helper('https://go.microsoft.com/fwlink/?LinkID=799445', os.path.join(Appdata, "MicrosoftUpdater.exe"))
            print("This window will now open the Microsoft Update Assistant to help you update to the latest version.", flush=True)
            print("Once it is done you will have to restart, it should restart automatically when it is done.", flush=True)
            print("If it doesn't, restart yourself. Once you are booted back up you open this utility again.", flush=True)
            print("Update assistant will open in 15 seconds.")
            time.sleep(15)
            subprocess.run(Appdata + "\\MicrosoftUpdater.exe /auto upgrade /passive /warnrestart:30 /skipeula", shell=True, check=True)
            print("You need to restart after Update Assistant is finished, then once logged back in open this again.", flush=True)
            changepersistent(1)
            while True:
                time.sleep(1)
def disable_clocking():
        
        try:
            subprocess.call(
                'powershell.exe  Unregister-ScheduledTask -TaskName "MSIAfterburner" -Confirm:$false',
                shell=True, creationflags=CREATE_NEW_CONSOLE)
        except:
            pass
        try:
            subprocess.call(
                'powershell.exe  Remove-Item -Path HKLM:\SYSTEM\CurrentControlSet\Services\RTCore64',
                shell=True, creationflags=CREATE_NEW_CONSOLE)
        except:
            pass
        try:
            subprocess.call(
                'powershell.exe Unregister-ScheduledTask -TaskName "EVGAPrecisionX" -Confirm:$false',
                shell=True, creationflags=CREATE_NEW_CONSOLE)
        except:
            pass
        try:
            subprocess.call(
                'powershell.exe Unregister-ScheduledTask -TaskName "GPU Tweak II" -Confirm:$false',
                shell=True, creationflags=CREATE_NEW_CONSOLE)
        except:
            pass
        try:
            subprocess.call(
                'powershell.exe Unregister-ScheduledTask -TaskName "Launcher GIGABYTE AORUS GRAPHICS ENGINE" -Confirm:$false',
                shell=True, creationflags=CREATE_NEW_CONSOLE)
        except:
            pass

def safemode(ONorOFF):
        if ONorOFF == 1:
            subprocess.call('bcdedit /set {default} safeboot minimal', shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if ONorOFF == 0:
            subprocess.call('bcdedit /deletevalue {default} safeboot', shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def DDUCommands():
        subprocess.call([os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe'), '-silent','-RemoveMonitors' , '-RemoveVulkan', '-RemoveGFE', '-Remove3DTVPlay', '-RemoveNVCP', '-RemoveNVBROADCAST','-RemoveNvidiaDirs', '-cleannvidia', '-logging'])
        print("1/3 finished with DDU", flush=True)
        subprocess.call([os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe'), '-silent','-RemoveMonitors' , '-RemoveVulkan', '-RemoveAMDDirs','-RemoveCrimsonCache','-RemoveAMDCP','-cleanamd', '-logging'])
        print("2/3 finished with DDU", flush=True)
        subprocess.call([os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe'), '-silent', '-RemoveMonitors' , '-RemoveVulkan','-RemoveINTELCP','-cleanintel', '-logging'])
        print("3/3 finished with DDU", flush=True)
def enable_internet(enable):
  if obtainsetting("donotdisableoverclocks") == 0:
    network_adapters = wmi.WMI().Win32_NetworkAdapter(PhysicalAdapter=True)
    try:
        for adapter in network_adapters:
            if enable:
                adapter.Enable()
            else:
                adapter.Disable()
    except:
        pass # Ugly way, but some adapters in specific configs cannot be disabled.
        # TODO: Verify if internet is actually disabled

def mainpain():
    
    os.system('mode con: cols=80 lines=40')
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
/,**#//&,,   ,&/%/////#&&&#/#&,...,*/////////////##*(&///#///////*,.(///,.////@@
    """, flush=True)
    print("\n", flush=True)
    try:
        if returnifduplicate() == True:
            print(r"""
THERE IS A POSSIBILITY YOU OPENED THIS MORE THAN ONCE BY ACCIDENT. PLEASE 
CLOSE THIS WINDOW AS IT IS VERY RISKY TO HAVE MORE THAN ONE OPEN.                  
                  """)
            while True:
                time.sleep(1)
        if not os.path.exists(Persistent_File_location) or getpersistent() == -1 or getpersistent() == 0:
            default_config()
            print_menu1()
            
    
            print("This process will attempt to perform DDU automatically.", flush=True)
            time.sleep(1)
            mainshit = ""
            if obtainsetting("bypassgpureq") == 0: 
                try:
                    mainshit = checkifpossible()
                except Exception as mainshit:
                    print("ERROR UNRECOVERABLE PLEASE REPORT THIS TO EVERNOW: \n", flush=True)
                    print(traceback.format_exc())
                    while True:
                        time.sleep(1)
                print(mainshit[1])
                if mainshit[0] ==0:
                    print(r"""
    INCOMPATIBLE GPU CONFIGURATION FOUND.
    
    CURRENTLY NO WAY TO RUN AUTODDU WITH THIS CONFIGURATION.
    
    IF THIS IS A MISTAKE PLEASE SHARE THIS WITH EVERNOW:
        """, flush=True)
                    print(mainshit)
                    while True:
                        time.sleep(1)
            
            print(r"""
This will update Windows if out of date, download needed drivers,
disable internet (needed to prevent Windows from fucking it up), 
and push you into safe mode.
            
This will also disable all GPU overclocks/undervolts/custom fan curves.
Do not worry if you do not know what this is, it won't affect you.
                    
When you are ready (this process can take up to 30 minutes 
and CANNOT be paused) please type "Do it" 
                    
Save all documents and prepare for your computer to restart
without warning. 
 """, flush=True)
            if BadLanguage() == False:
                while True:
                    DewIt = str(input("Type in 'Do it' then press enter to begin: "))
                    if "do it" in DewIt.lower():
                        break
            else:
                HandleOtherLanguages()
            time.sleep(5)
            BackupProfile()
            if len(obtainsetting("provideowngpuurl")) != 0:
                download_drivers(obtainsetting("provideowngpuurl"))
                
            elif len(obtainsetting("provideowngpuurl")) == 0 and obtainsetting("bypassgpureq") == 0:
                download_drivers(mainshit[2])
            ddu_download()
            if obtainsetting("disablewindowsupdatecheck") == 0:
                uptodate()
            changepersistent(1)
        if getpersistent() == 1:        
            print("Now going to disable any oveclocks/undervolts/fan curves if any on the GPU. (If not changed to do otherwise)")
            print("If you had one you will have to reapply after this process is done.")
            print("If you do not know what any of this is, don't worry, you don't have to do anything.")
            print("We will resume in 5 seconds.", flush=True)
            time.sleep(5)
            if obtainsetting("donotdisableoverclocks") == 0:
                disable_clocking() 
            print(r"""
                  
----------------------------NOTICE----------------------------

This application will now enable safe mode, disable the internet
and then reboot you.
Safe mode is a state of Windows where no GPU Drivers are loaded,
this is needed so they we can do a proper clean install.
            
You wallpaper will be black, the resolution will look
messed up, this is normal.
            
In addition we're going to turn off the internet so
Windows cannot install drivers while we're installing them.
            
{login_or_not}

After once you are at a black wallpaper you will need to launch
the "AutoDDU_CLI.exe" on your desktop to let us start working again.
            
(Read what is above, window to continue will appear in 15 seconds.)
            
                  """.format(login_or_not=login_or_not), flush=True)
            time.sleep(15)
            if BadLanguage() == False:
                while True:
                     DewIt = str(input("Type in 'I understand' then enter once you understand what you must do: "))
                     if "i understand" in DewIt.lower():
                         break     
            else:
                HandleOtherLanguages()
            time.sleep(5)
            safemode(1)
            
            print("May seem frozen for a bit, do not worry, we're working in the background.")
            workaroundwindowsissues() # TODO: this is REALLY FUCKING STUPID
            makepersist()
              
            download_helper("https://github.com/Evernow/AutoDDU_CLI/raw/main/AutoDDU_CLI.exe", r"C:\Users\DDU\Desktop\AutoDDU_CLI.exe")
            subprocess.call('shutdown /r -t 5', shell=True)
            enable_internet(False)
            changepersistent(2)
            autologin()
            time.sleep(2)
            print("Command to restart has been sent.")
            while True:
                time.sleep(1)
        if getpersistent() == 2:  
              print("Welcome back, the hardest part is over.")
              print("This will take a minute or two, even though it may seem")
              print("like nothing is happening, please be patient.", flush=True)
              try:
                  DDUCommands()
              except Exception as oof:
                  print("Error while doing DDU. You can still run manually.")
                  print("Please send this to Evernow:")
                  print(traceback.format_exc(), flush=True)
                  while True:
                      time.sleep(1)
              print("DDU has been ran!", flush=True)
              print(r"""
This will now boot you back into normal mode.
              
You can login to your normal user profile, no need for DDU.
              
Once you login you run this one last time where we will install
the drivers properly, then once finished turn on your internet.
              
Will restart in 15 seconds.
              
                    """, flush=True)
              
              
              safemode(0)
              changepersistent(3)
              try:
                  subprocess.Popen('powershell.exe Remove-LocalUser -Name "DDU"', 
                             shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=CREATE_NEW_CONSOLE).communicate()
              except:  
                  pass
              time.sleep(5)
              subprocess.call('shutdown /r -t 10', shell=True)
              print("Command to restart has been sent.")
              while True:
                  time.sleep(1)
              
        if getpersistent() == 3:  
            print(r"""
Almost done. Only thing left now is install drivers
and then turn on your internet.
                  """, flush=True)
            try:
                subprocess.Popen('reg delete HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v AutoDDU_CLI /f', 
                           shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).communicate()
            except:  
                pass
            if os.path.exists(os.path.join(Appdata, "AutoDDU_CLI", "Drivers")):
                s = os.listdir(os.path.join(Appdata, "AutoDDU_CLI", "Drivers"))
                intel = 0
                for driver in s:
                    if "radeon" or "-desktop-" in driver:
                        print("Launching driver installer, please install.")
                        time.sleep(1)
                        subprocess.call(str(os.path.join(Appdata, "AutoDDU_CLI", "Drivers", driver)), shell=True)
                    if "intel" in driver:
                        intel = 1
                if intel == 1:
                    print("Intel driver needed, will turn on internet (needed for installer)", flush=True)
                    enable_internet(True)
                    time.sleep(1)
                    subprocess.call(str(os.path.join(Appdata, "AutoDDU_CLI", "Drivers", "inteldriver.exe")), shell=True)
                print("All driver installations complete. Have a good day.")
                print("Closing in ten minutes. Feel free to close early if no problems", flush=True)
            else:
                
                print("""
Due to no drivers being detected, our work is done.
Now it is up to you to install the drivers like you normally would.
Closing in ten minutes. Feel free to close early if no problems
                """, flush=True)
            enable_internet(True)
            cleanup() # TODO: Very basic, does not fully cleanup (DDU user folder remains, our executable remains... but everything that occupies space is gone)
            changepersistent(0)
            time.sleep(600)
            sys.exit(0)
        while True:
            print("ERROR CONFIGURATION ERROR CONFIGURATION")
            time.sleep(1)
    except Exception as oof:
        print(unrecoverable_error_print)
        print(traceback.format_exc(), flush=True)
        while True:
            time.sleep(1)
    
    
print(mainpain())                 
