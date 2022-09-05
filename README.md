# AutoDDU_CLI

![](Chikaftw_upscaled.png)


This is an attempt to automate as much as possible for the end user, while also being maintainable and requiring little time spent to maintain it overtime.

# User requirements (these are dependent of user install)
- Windows 8.1^ or higher (due to [Python requirements](https://docs.python.org/3/using/windows.html) and use of [MSFT_NetAdapter](https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/hh968170(v=vs.85)))
- Internet connection (that can access Github.com, NVIDIA.com, AMD.com, Intel.com, Microsoft.com, githubusercontent.com)
- Presence and functionality of  `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp` which is used to make AutoDDU_CLI startup on bootup when out of safe mode.
- AutoDDU makes heavy use of WMI, in particular it accesses Win32_UserAccount, Win32_Product, Win32_Group, Win32_ComputerSystem, Win32_Process, Win32_OperatingSystem, Win32_VideoController and MSFT_NetAdapter. If any of these have been altered in any way AutoDDU is likely to fail, sometimes in catastrophic and uncatched ways.
- No update service blocking, for example if out of date (ie a major release behind like 20H2 vs 21H1) AutoDDU will first attempt to launch the update assistant, if that fails then AutoDDU will be stuck in a loop of not being able to continue because updates fail.
- Presence and functionality of 'Software\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon' which is used to have the user auto login when entering safe mode.
- Win32 APIs like [SHGetKnownFolderPath](https://docs.microsoft.com/en-us/windows/win32/api/shlobj_core/nf-shlobj_core-shgetknownfolderpath) 
- Services required by [PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec) to be running. This is used to create user profile folders.
- 64-bit OS due to:
  - PyWin32 only [supporting 64-bit](https://github.com/mhammond/pywin32/issues/1805)
  - Display Driver Uninstaller executables being distributed in 64-bit only format.
  - NVIDIA, AMD and Intel only support 64-bit.
  - Non-existent demand for any other architectures.



^ Windows 8.1 users will be updated to Windows 10.
