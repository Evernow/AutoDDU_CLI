import urllib.request
import json
# NVIDIA driver source loading
with urllib.request.urlopen(
        "https://github.com/24HourSupport/CommonSoftware/raw/main/nvidia_gpu.json") as url:
    data_nvidia = json.loads(url.read().decode())
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

with urllib.request.urlopen(
        "https://github.com/24HourSupport/CommonSoftware/raw/main/amd_gpu.json") as url:
    data_amd = json.loads(url.read().decode())
AMD_Consumer = data_amd["consumer"]["link"]
AMD_Professional = data_amd["professional"]["link"]
# Intel driver source loading
with urllib.request.urlopen(
        "https://github.com/24HourSupport/CommonSoftware/raw/main/intel_gpu.json") as url:
    data_intel = json.loads(url.read().decode())
Intel_Consumer = data_intel["consumer"]["link"]
Intel_Consumer_Supported = json.loads(data_intel["consumer"]["SupportedGPUs"].replace('\'', '"')) # See comments here for replace reasoning: https://stackoverflow.com/a/35461204/17484902
# For testing you pass in a list with
# [{'NVIDIA GeForce RTX 3080': ['GA102', '10de', '2206']}, []]
#                   GPU infos                           , 

import subprocess
subprocess.run('py -m pip install tqdm',shell=True)
subprocess.run('py -m pip install requests',shell=True)
import requests

def download_helper(url, fname):
    from tqdm.auto import tqdm
    my_referer = "https://www.amd.com/en/support/graphics/amd-radeon-6000-series/amd-radeon-6700-series/amd-radeon-rx-6700-xt"
    resp = requests.get(url, stream=True, headers={'referer': my_referer,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'})
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

download_helper("https://raw.githubusercontent.com/Evernow/AutoDDU_CLI/main/AutoDDU_CLI.py", "AutoDDU_CLI.py")
download_helper("https://raw.githubusercontent.com/Evernow/AutoDDU_CLI/main/requirements.txt", "requirements.txt")
subprocess.run('py -m pip install -r requirements.txt',shell=True)

from AutoDDU_CLI import mainpain
import requests


List_of_tests = [
    [{'GeForce RTX 3080': ['GA102', '10de', '2206']}, [NVIDIA_Consumer]],
    [{'GeForce GT 630': ['GF108', '10de', '0f00']},["Incompatible GPU"]], # https://github.com/Evernow/AutoDDU_CLI/issues/18
    [{'NVIDIA GeForce GTX 690': ['GK104', '10de', '1188'], 'Intel(R) UHD Graphics 630': ['CoffeeLake-S', '8086', '3e92']}, [NVIDIA_R470_Consumer, Intel_Consumer]], # Thank you Reki 
    [{'Intel(R) UHD Graphics 620': ['UHD', '8086', '5917']},[Intel_Consumer]]
]

for test in List_of_tests:
    print(test)
    try:
        result = (mainpain(test))
        if type(result) == str:
            if List_of_tests[index(test)][0] == result:
                print("Passed test " + test)
            else:
                raise Exception("I am at the end of my rope")
        else:
            for gpudriver in List_of_tests[index(test)][0]:
                if gpudriver not in list(result):
                    raise Exception("I am at the end of my rope")

    except:
        raise Exception("I am at the end of my rope with " + test)
