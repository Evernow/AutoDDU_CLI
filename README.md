# AutoDDU_CLI

![](Chikaftw_upscaled.png)


This is an attempt to automate as much as possible for the end user, while also being maintainable and requiring little time spent to maintain it overtime.

## Dependencies (these are all handled automatically):
- [FIDO](https://github.com/pbatard/Fido): Used to know which is the latest Windows release
- [24HS-CommonSoftware](https://github.com/24HourSupport/CommonSoftware) - Used to grab latest GPU drivers
- [PCI ID Database](http://pci-ids.ucw.cz/) - Used to know what GPU we're working with

# User requirements (these are dependent of user install)
- Windows 8.1^ or higher (due to [Python requirements](https://docs.python.org/3/using/windows.html) and use of [MSFT_NetAdapter](https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/hh968170(v=vs.85)))
- Internet connection (that can access Github.com, NVIDIA.com, AMD.com, Intel.com, Microsoft.com, sysinternals.com, wagnardsoft.com, githubusercontent.com)
- Presence and functionality of  `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp` which is used to make AutoDDU_CLI startup on bootup when out of safe mode.
- Services required by [PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec) to be running. This is used to create user profile folders.
- 64-bit OS due to:
  - PyWin32 only [supporting 64-bit](https://github.com/mhammond/pywin32/issues/1805)
  - Display Driver Uninstaller executables being distributed in 64-bit only format.
  - NVIDIA, AMD and Intel only support 64-bit.
  - Non-existent demand for any other architectures.



^ Windows 8.1 users will be updated to Windows 10.
