# AutoDDU_CLI

![](Chikaftw_upscaled.png)


This is an attempt to automate as much as possible for the end user, while also being maintainable and requiring little time spent to maintain it overtime.

## Dependencies (these are all handled automatically):
- [FIDO](https://github.com/pbatard/Fido): Used to know which is the latest Windows release
- [24HS-CommonSoftware](https://github.com/24HourSupport/CommonSoftware) - Used to grab latest GPU drivers
- [PCI ID Database](http://pci-ids.ucw.cz/) - Used to know what GPU we're working with

# User requirements (these are dependent of user install)
- Windows 8.1 or higher (due to [Python requirements](https://docs.python.org/3/using/windows.html) and use of [MSFT_NetAdapter](https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/hh968170(v=vs.85)))
- Internet connection (that can access Github.com, NVIDIA.com, AMD.com, Intel.com, Microsoft.com, sysinternals.com, wagnardsoft.com, githubusercontent.com)
