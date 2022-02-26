def PCIID(vendor, device):
    import urllib.request, json 
    with urllib.request.urlopen("https://raw.githubusercontent.com/24HourSupport/CommonSoftware/main/PCI-IDS.json") as url:
        data = json.loads(url.read().decode())
        return(data[vendor]['devices'][device]['name'])
import os,time    
import wmi
import sys
import subprocess
import requests
from win32com.shell import shell, shellcon
import shutil
import platform

Appdata = shell.SHGetFolderPath(0, shellcon.CSIDL_COMMON_APPDATA, 0, 0) 
Appdata_AutoDDU_CLI = os.path.join(Appdata, "AutoDDU_CLI")
Persistent_File_location = os.path.join(Appdata, "AutoDDU_CLI", "PersistentDDU_Log.txt")
root_for_ddu_assembly = os.path.join(Appdata, "AutoDDU_CLI", "DDU_Parser")
ddu_AssemblyInfo = os.path.join(Appdata, "AutoDDU_CLI", "DDU_Parser\\", "AssemblyInfo.vb")
ddu_zip_path = os.path.join(Appdata, "AutoDDU_CLI", "DDU_Parser\\", "DDU.exe")
seven_zip = os.path.join(Appdata, "AutoDDU_CLI", "DDU_Parser\\", "7z.exe")
ddu_extracted_path = os.path.join(Appdata, "AutoDDU_CLI", "DDU_Extracted")

exe_location = os.path.join(Appdata_AutoDDU_CLI, "AutoDDU_CLI.exe")

#Only Fermi professional (NVS, Quadro, Tesla) is supported, and only till the end of 2022.
FERMI_NVIDIA = "GF108","GF108","GF108-300-A1","GF106","GF106-250","GF116-200","GF104-225-A1","GF104","GF104-300-KB-A1","GF114","GF100-030-A3","GF100-275-A3","GF100-375-A3","GF119","GF108","GF118","GF116","GF116-400","GF114-200-KB-A1","GF114-325-A1","GF114-400-A1","GF110","GF110-270-A1","GF110-275-A1","GF110-375-A1","2x GF110-351-A1","GF100","GF108","GF106","GF106","GF108","GF119-300-A1","GF108-100-KB-A1","GF108-400-A1","GF119 (N13M-GE)","GF117 (N13M-GS)","GF108 (N13P-GL)","GF117","GF106 (N12E-GE2)","GF116","GF108","GF114 (N13E-GS1-LP)","GF114 (N13E-GS1)","GF117","GF108","GF117","GF108",""

EOL_NVIDIA = "G98","G96b","G94b","G92b","MCP79XT","N10M-GE2(G98)","N10M-GE1(G98)","N10M-GE1(G96b)","N10P-GV1(G96b)","N10P-GE1(G96b)","N10E-GE1(G94b)","N10E-GS1(G94b)","GT218","GT216","GT215","MCP89","GT215-301-A3","G92","GT216","GT218","MCP68S","MCP67QV","MCP73","MCP76","NV44","G72","G73","G73-B1","G70","G71","2x G71","MCP78","G86","G84","G80","GM108","GM107","NB8M(G86)","NB8P(G84)","NB8P(G92)","C77","MCP79","MCP7A-S","MCP7A-U","G96-200-c1","G96a","G96b","G96-300-C1","G94a","G92-150-A2","G94a","G94b","G94-300-A1","G92a2 G92b","G92a","G92b","G92-420-A2","2x G92","MCP77MH","MCP79MH","NB9M-GE(G98)","NB9M-GE(G86)","MCP79MX","NB9P(G96)","NB9P-GV(G96)","NB9P-GE2(G96)","NB9P-GS(G96)","NB9P-GS1(G84)","NB9P-GT(G96)","NB9E-GE(G96)","NB9E-GS(G94)","NB9E-GT(G94)","NB9E-GT2(G92)","NB9E-GTX(G92)","NV34","NV34B","NV31","NV36","NV30","NV35","NV38","NV34M","NV31M","NV36M","C51M","NV44M","NV43M","NV41M","MCP67MV","MCP67M","G72M","G73M","G73-N-B1","G70M","G71M","NV11M","NV1A (IGP) / NV11 (MX)","NV15","NV16","NV1A","NV11","NV20","NV17M","NV18M","NV28M","NV11","G72GLM","G86M","G98M","G84M","GT218M","GT216M","NV1","NV3","NV4","NV6","NV5","NV37GL","NV43GL","NV41","NV45GL","NV40","NV45GL A3","NV40","NV43","G71GLM","G73GL","G73GLM","G92M","G84GL","G96M","G94M","G96","GT218GL","G100GL-U","G94","GT200GL","GT215M","NV34GL","NV35GL","NV30GL","NV36GL","NV40GL","NV17","NV28","NV18","MCP51","2xG98","2xNV43","G94","G100GL","G100GL-U","N13M-GE","NV45GL","NV40","NV45GL A3","NV11GL ","G96C","G94GLM"

KEPLER_NVIDIA = "GK107","GK208-301-A1","GK208","GK208-400-A1","GK106","GK107-450-A2","GK-106-400-A1","GK106-220-A1","GK106-240-A1","GK106-400-A1","GK104-200-KD-A2","GK104-300-KD-A2","GK104-325-A2","GK104-400-A2","2x GK104-355-A2","GK107 (N13P-LP)","GK107 (N13P-GS)","GK107 (N13P-GT)","GK107 (N13E-GE)","GK104 (N13E-GR)","GK104 (N13E-GSR)","GK104 (N13E-GTX)","GK104","GK208-203-B1","GK208-201-B1","GK107-425-A2","GK104-225-A2","GK104-425-A2","GK110-300-A1","GK110-425-B1","GK110-400-A1","GK110-430-B1","2x GK110-350-B1","GK110","GK110B"

Professional_NVIDIA_GPU = ["Quadro", "Tesla", "NVS"]

Exceptions_laptops = "710A","745A","760A","805A","810A","810A","730A","740A" # Kepler laptops GPUs with no M in the name.

EOL_AMD = "16899-0" , "18800-1" , "28800-5" , "28800-6" , "Broadway" , "CW16800-A" , "CW16800-B" , "Cedar" , "Cypress" , "ES1000" , "Flipper" , "Hemlock" , "Hollywood" , "IBM" , "Juniper" , "M1" , "M10" , "M11" , "M12" , "M18" , "M22" , "M24" , "M26" , "M28" , "M3" , "M4" , "M52" , "M54" , "M56" , "M58" , "M6" , "M62" , "M64" , "M66" , "M68" , "M7" , "M71" , "M72" , "M74" , "M76" , "M82" , "M86" , "M88" , "M9" , "M9+" , "M92" , "M93" , "M96" , "M97" , "M98" , "Mach32" , "Mach64" , "Mach64 GT" , "Mach64 GT-B" , "Mach64 LT" , "Mach8" , "Madison" , "Park" , "Pinewood" , "R100" , "R200" , "R250" , "R300" , "R350" , "R360" , "R420" , "R423" , "R430" , "R480" , "R481" , "R520" , "R580" , "R580+" , "R600" , "R680" , "R700" , "RC1000" , "RC300" , "RC410" , "RS100" , "RS200" , "RS250" , "RS300" , "RS350" , "RS400" , "RS480" , "RS482" , "RS485" , "RS600" , "RS690" , "RS740" , "RS780" , "RS880" , "RV100" , "RV200" , "RV250" , "RV280" , "RV350" , "RV370" , "RV380" , "RV410" , "RV505" , "RV515" , "RV516" , "RV530" , "RV535" , "RV560" , "RV570" , "RV610" , "RV620" , "RV630" , "RV635" , "RV670" , "RV710" , "RV730" , "RV740" , "RV770" , "RV790" , "Rage 2" , "Rage 3" , "Rage 3 Turbo" , "Rage 4" , "Rage 4 PRO" , "Rage 6" , "Rage Mobility" , "Redwood" , "Turks" , "Xenos Corona" , "Xenos Falcon" , "Xenos Jasper" , "Xenos Vejle" , "Xenos Xenon"

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

def makepersist():
    download_helper("https://github.com/Evernow/AutoDDU_CLI/raw/main/AutoDDU_CLI.exe", exe_location)
    subprocess.call('REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /V "AutoDDU_CLI" /t REG_SZ /F /D "{directory}"'.format(directory=exe_location), shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)


def autologin():
    #TODO this requires the hacky workaround of deleting the DDU user so it stops auto logging in.
    # https://superuser.com/questions/514265/set-user-for-auto-logon-on-windows-via-batch-script
    try:
        subprocess.call('reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_SZ /d 1 /f', shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        subprocess.call('reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName /t REG_SZ /d DDU /f', shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        subprocess.call('reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoLogonCount /t REG_DWORD /d 1 /f', shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except:
        global login_or_not
        login_or_not = """
        You will need to login manually to the DDU
        profile account we created."""
def getsupportstatus():
    controllers = wmi.WMI().Win32_VideoController()
    gpu_dictionary = dict() # GPU NAME = [VENDOR ID, DEVICE ID, ARCHITECTURE , RAW OUTPUT (for troubleshooting purposes), supportstatus (0=unchecked, 1=supported, 2=kepler, 3=fermiprof, 4=EOL), professional/consumer] 
    
    for controller in controllers:
       name = controller.wmi_property('Name').value
       gpu_list_to_parse = controller.wmi_property('PNPDeviceID').value.lower().split("\\") # .lower() is due to Windows not following PCI naming convention.
       for gpu in gpu_list_to_parse:
           # We need to filter out by vendor or else we can parse in shit like Citrix or capture cards.
           if "dev_" in gpu and ("ven_10de" in gpu or "ven_121a" in gpu or "ven_8086" in gpu
                                                           or "ven_1002" in gpu): # 1002 = AMD ; 8086 = Intel ; 10de = NVIDIA ; 121a = Voodoo (unlikely but I mean.. doesn't hurt?)
                   from datetime import date
                   todays_date = date.today().year
                   
                   # Us assuming a ven and dev ID is 4 characters long is a safe one: https://docs.microsoft.com/en-us/windows-hardware/drivers/install/identifiers-for-pci-devices
                   Arch = PCIID(gpu[gpu.find('ven_')+4:gpu.find('ven_')+8], gpu[gpu.find('dev_')+4:gpu.find('dev_')+8])
                   Arch = Arch[:Arch.find(' ')]
                   Vendor_ID = gpu[gpu.find('ven_')+4:gpu.find('ven_')+8]
                   Device_ID = gpu[gpu.find('dev_')+4:gpu.find('dev_')+8]
                   supportstatus = 0
                   Consumer_or_Professional = ""
                   if Vendor_ID == '121a': # Voodoo (wtf lol)
                       supportstatus = 4
                       Consumer_or_Professional = "Consumer"
                   if Vendor_ID == '8086': # Intel
                       supportstatus = 1
                       Consumer_or_Professional = "Consumer"
                   if Vendor_ID == '1002': # AMD
                       for possibility in EOL_AMD:
                           if Arch in possibility:
                               supportstatus = 4
                       if supportstatus != 4:
                            supportstatus = 1
                       Consumer_or_Professional = "Consumer" # There are professional AMD GPUs but are EXTREMELY rare and I haven't built a driver search for them, nor intend to.
                   
                   
                   if Vendor_ID == '10de': # NVIDIA
                   
                       # Check if professional or consumer
                       for seeifprof in Professional_NVIDIA_GPU:
                           if seeifprof.lower() in name.lower(): 
                               Consumer_or_Professional = "Professional"
                       if Consumer_or_Professional != "Professional":
                           Consumer_or_Professional = "Consumer"
                       # Nightmare begins
                       for possibility in EOL_NVIDIA:
                           if Arch in possibility:
                               supportstatus = 4 # EOL
                       for possibility in FERMI_NVIDIA:
                           if Arch in possibility:
                               for seeifprof in Professional_NVIDIA_GPU:
                                   
                                   if Consumer_or_Professional == "Professional" and todays_date < 2023: # EOL For Fermi prof
                                       supportstatus = 3 # fermiprof
                               if supportstatus != 3: 
                                   supportstatus = 4 # EOL
                       for possibility in KEPLER_NVIDIA:
                            if Arch in possibility:
                                if "M" in name.upper():
                                    supportstatus = 4 # EOL
                                else:
                                    for exception_fuckinglaptops in Professional_NVIDIA_GPU:
                                        if exception_fuckinglaptops in name.upper():
                                            supportstatus = 4 # EOL
                                    if supportstatus != 4 and todays_date < 2025: # In reality it ends in mid 2024, but this is fine.
                                        supportstatus = 2 # kepler
                       if supportstatus == 0:
                            supportstatus = 1
                               
                           
                   # This approach covers for stupid SLI or dual GPUs (looking at you Anderson)            
                   gpu_dictionary[name] = [Vendor_ID, Device_ID, Arch, gpu, supportstatus, Consumer_or_Professional]
                   
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
    import urllib.request, json 
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
    return(1, performing_DDU_on, drivers_to_download)  

# This keeps track of where we are in the process in a text file. 
def changepersistent(num):
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
            return(int(first))
    except:
        return(-1)

def BackupProfile():
    try:
     firstcommand = "net user /add DDU"
     secondcommand = "net localgroup administrators DDU /add"
     subprocess.run(firstcommand, shell=True, check=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)  
    # logger("Running command to add created to user to administrators")
     subprocess.run(secondcommand, shell=True, check=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)  
    # changepersistent(2)
   #  logger("Successfully created DDU account")
     print("INFO: Created backup profile")
    except:
        print("INFO: Did not create backup profile (not an error)")
        
       # logger("Failed to create DDU account, likely already existed")


def download_helper(link, file_name):
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
    download_helper('https://raw.githubusercontent.com/Wagnard/display-drivers-uninstaller/WPF/display-driver-uninstaller/Display%20Driver%20Uninstaller/My%20Project/AssemblyInfo.vb',
            ddu_AssemblyInfo)
    
    my_file = open(ddu_AssemblyInfo, "r")

    content = my_file.readlines()

    Latest_DDU_Version_Raw = "" 

    for DDU_Version_Candidate in content:
        if 'AssemblyFileVersion' in DDU_Version_Candidate:
            Latest_DDU_Version_Raw = DDU_Version_Candidate[DDU_Version_Candidate.find('("')+2:DDU_Version_Candidate.find('")')]

    try:
        download_helper(
            'https://www.wagnardsoft.com/DDU/download/DDU%20v' + Latest_DDU_Version_Raw + '.exe',
            ddu_zip_path
        )
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

        try:

         download_helper(
            'https://www.wagnardsoft.com/DDU/download/DDU%20v' + Latest_DDU_Version_Raw + '.exe',
            ddu_zip_path)
        except Exception as f:
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

    subprocess.call(str(seven_zip + ' -o' + ddu_extracted_path+ ' x ' + ddu_zip_path +  ' -y > nul'), shell=True)
    # Moves everything one directory up, mainly just to avoid crap with versioning, don't want to have to deal with
    # version numbers in the DDU method doing the command calling.

    where_it_is = ddu_extracted_path + '\\' + 'DDU v' + Latest_DDU_Version_Raw

    file_names = os.listdir(where_it_is)
        
    for file_name in file_names:
        shutil.move(os.path.join(where_it_is, file_name), ddu_extracted_path)

def latest_windows_version():
    from subprocess import CREATE_NEW_CONSOLE
    p = str(subprocess.Popen("powershell.exe -ExecutionPolicy RemoteSigned -file C:\\Users\\Daniel\\Videos\\Ps7\ps7\\Fido.ps1 -Win {version} -Rel List".format(version = platform.release()), 
                   shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=CREATE_NEW_CONSOLE).communicate())
    #p = str(subprocess.Popen('powershell.exe -ExecutionPolicy RemoteSigned -file "C:\\Users\\Daniel\\Videos\\Ps7\ps7\\Fido.ps1" -Win 7 -Rel List', stdout=sys.stdout, shell=True).communicate())
    dictionarytest = {}
    for release in p.split('\\n'):
        release = release.replace('build', 'Build')
        if "Build" in release:
            dictionarytest[release[3:release.index("(Build")-1]] = release[release.index("(Build")+ 7:release.rfind("-", release.index("(Build"))].split(".", 1)[0]
    
        
    return(list(dictionarytest.values())[0])


def uptodate():
    if platform.release() != 11: # No update assistant for W11 yet afaik
    
        if int(platform.version().split('.')[2]) >= int(latest_windows_version()): #We should consider insider builds. But that's outside the scope of v1 at least.
            print("System up to date already")                
    
        else:
            print("System is out of date, downloading Microsoft Update Assistant.")
            download_helper('https://go.microsoft.com/fwlink/?LinkID=799445', os.path.join(Appdata, "MicrosoftUpdater.exe"))
            print("This window will now open the Microsoft Update Assistant to help you update to the latest version.")
            print("Once it is done you will have to restart, it should restart automatically when it is done.")
            print("If it doesn't, restart yourself. Once you are booted back up you open this utility again.")
            print("Update assistant will open in 15 seconds.")
            time.sleep(15)
            subprocess.run(Appdata + "\\MicrosoftUpdater.exe /auto upgrade /passive /warnrestart:30 /skipeula", shell=True, check=True)
            print("You need to restart after Update Assistant is finished, then once logged back in open this again.")
            changepersistent(1)
            while True:
                time.sleep(1)
def disable_clocking():
        from subprocess import CREATE_NEW_CONSOLE
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
        subprocess.call(os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe') + ' -silent -cleanamd ', shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        subprocess.call(os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe') + ' -silent -cleanintel ', shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        subprocess.call(os.path.join(ddu_extracted_path, 'Display Driver Uninstaller.exe') + ' -silent -cleannvidia ', shell=True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def enable_internet(enable):
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
    """)
    print("\n")
    try:
        if not os.path.exists(Persistent_File_location) or getpersistent() == -1 or getpersistent() == 0:
            
    
            print("This process will attempt to perform DDU automatically.", flush=True)
            time.sleep(1)
            mainshit = ""
            try:
                mainshit = checkifpossible()
            except Exception as mainshit:
                mainshit = mainshit
                print("ERROR UNRECOVERABLE PLEASE REPORT THIS TO EVERNOW: \n", flush=True)
                print(mainshit)
                while True:
                    time.sleep(1)
            print(mainshit[1])
            if mainshit[0] ==0:
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
                    
Type "Do it" then press your enter key once you are ready. """, flush=True)
            
            while True:
                DewIt = str(input("Type in 'Do it' then press enter to begin: "))
                if "do it" in DewIt.lower():
                    break
            time.sleep(5)
            BackupProfile()
            autologin()
            download_drivers(mainshit[2])
            ddu_download()
            uptodate()
            changepersistent(1)
        if getpersistent() == 1:        
            print("Now going to disable any oveclocks/undervolts/fan curves if any on the GPU.")
            print("If you had one you will have to reapply after this process is done.")
            print("If you do not know what any of this is, don't worry, you don't have to do anything.")
            print("We will resume in 5 seconds.", flush=True)
            time.sleep(5) 
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
            
Once you type in 'I understand' you will see the internet
turn off and shortly after reboot.
            
{login_or_not}
            
(Read what is above, window to continue will appear in 15 seconds.)
            
                  """.format(login_or_not=login_or_not), flush=True)
            time.sleep(15)
            while True:
                 DewIt = str(input("Type in 'I understand' then enter once you understand what you must do: "))
                 if "i understand" in DewIt.lower():
                     break     
            safemode(1)
            enable_internet(False)
            changepersistent(2)
            time.sleep(2)
            makepersist()
            subprocess.call('shutdown /r -t 5', shell=True)
            exit()
        if getpersistent() == 2:  
              print("Welcome back, the hardest part is over.")
              print("This will take a minute or two, even though it may seem")
              print("like nothing is happening, please be patient.", flush=True)
              try:
                  DDUCommands()
              except Exception as oof:
                  print("Error while doing DDU. You can still run manually.")
                  print("Please send this to Evernow:")
                  print(oof, flush=True)
                  while True:
                      time.sleep(1)
              time.sleep(30)
              print("DDU has been ran!")
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
                  from subprocess import CREATE_NEW_CONSOLE
                  subprocess.Popen('powershell.exe Remove-LocalUser -Name "DDU"', 
                             shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=CREATE_NEW_CONSOLE).communicate()
              except:  
                  pass
              try:
                  subprocess.Popen('reg delete HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v AutoDDU_CLI /f', 
                             shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
              except:  
                  pass
              time.sleep(5)
              subprocess.call('shutdown /r -t 10', shell=True)
        if getpersistent() == 3:  
            print(r"""
Almost done. Only thing left now is install drivers
and then turn on your internet.
                  """, flush=True)
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
            
            changepersistent(0)
            time.sleep(600)
            exit()
        while True:
            time.sleep(1)
    except Exception as oof:
        print(unrecoverable_error_print)
        print(oof, flush=True)
        while True:
            time.sleep(1)
    
    
print(mainpain())                 