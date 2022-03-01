
# ⚡ Xopher ⚡
slightly better version of winstealer 🤷‍♀️
 
<img src="https://flat.badgen.net/badge/LOL/BANS: 0/red?icon=terminal">

Supported regions: NA-EU-RU-BR-TR (KR and JP client have an actual anticheat dont bother)


![image](https://user-images.githubusercontent.com/26947031/156155768-17ef3fc0-5ccb-404f-8362-215e1a803f33.png)


### Building

some binary files have been removed and you will need to get them yourself.
boost_container-vc142-mt-gd-x32-1_75.dll
boost_container-vc142-mt-x32-1_75.dll
boost_json-vc142-mt-gd-x32-1_75.dll
boost_json-vc142-mt-x32-1_75.dll
boost_python39-vc142-mt-gd-x32-1_75.dll
boost_python39-vc142-mt-x32-1_75.dll
python39.dll
python39_d.dll
testing-resources.dll

You need Visual Studio 2017 to compile this.
Dependencies:
  1. python39: dlls and includes are already in project. You need to install python 3.9 for 32bits (Make sure you check the Add to PATH checkbox in the installer: https://www.python.org/ftp/python/3.9.0/python-3.9.0.exe)
  3. aws-lambda: dlls and includes are already in project (was used for authentication)
  3. directx 11: Must install directx end user runtimes: https://www.microsoft.com/en-us/download/details.aspx?id=35 .Extract this and run dxsetup
  4. boost::python. Due to the size of the boost libraries you must compile boost::python yourself:
      1. Download boost 1.75.0 
      2. Unarchive it in LView/boost
      3. Go into boost
      4. Run `bootstrap.bat`
      5. Run `b2 --with-python link=shared toolset=msvc-14.1 address-model=32 variant=release`
  5. You are done now compile the app on Release x86 (you need to compile boost::python on debug to compile on debug, which I didn't).


For educational purposes only xd
