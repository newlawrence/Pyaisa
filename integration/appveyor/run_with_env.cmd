:: To build extensions for 64 bit Python 3, we need to configure environment
:: variables to use the MSVC 2010 C++ compilers from GRMSDKX_EN_DVD.iso of:
:: MS Windows SDK for Windows 7 and .NET Framework 4 (SDK v7.1)
::
:: To build extensions for 64 bit Python 2, we need to configure environment
:: variables to use the MSVC 2008 C++ compilers from GRMSDKX_EN_DVD.iso of:
:: MS Windows SDK for Windows 7 and .NET Framework 3.5 (SDK v7.0)
::
:: 32 bit (and 64 bit Python 3.5) builds do not require specific environment
:: configurations.
:: 
:: Note: this script needs to be run with the /E:ON and /V:ON flags for the
:: cmd interpreter, at least for (SDK v7.0)
::
:: More details at:
:: https://github.com/cython/cython/wiki/64BitCythonExtensionsOnWindows
:: http://stackoverflow.com/a/13751649/163740
::
:: Author: Olivier Grisel
:: License: CC0 1.0 Universal: http://creativecommons.org/publicdomain/zero/1.0/
:: Modified by: Alberto Lorenzo

@ECHO OFF
SET COMMAND_TO_RUN=%*
SET SDK_ROOT=C:\Program Files\Microsoft SDKs\Windows

SET MAJOR="%PYTHON:~0,1%"
IF %MAJOR% == "2" (
    SET WIN_SDK="v7.0"
) ELSE IF %MAJOR% == "3" (
    SET WIN_SDK="v7.1"
) ELSE (
    ECHO Unsupported Python version: "%MAJOR%"
    EXIT 1
)

IF %ARCH%=="32" (
    ECHO Using default MSVC build environment for 32 bit arch
    ECHO Executing: %COMMAND_TO_RUN%
    call %COMMAND_TO_RUN% || EXIT 1
) ELSE IF %PYTHON%=="3.5" (
    ECHO Using default MSVC build environment for 64 bit arch
    ECHO Executing: %COMMAND_TO_RUN%
    call %COMMAND_TO_RUN% || EXIT 1
) ELSE (
    ECHO Configuring Windows SDK %WIN_SDK% for Python %MAJOR% on a 64 bit arch
    SET DISTUTILS_USE_SDK=1
    SET MSSdk=1
    "%SDK_ROOT%\%WIN_SDK%\Setup\WindowsSdkVer.exe" -q -version:%WIN_SDK%
    "%SDK_ROOT%\%WIN_SDK%\Bin\SetEnv.cmd" /x64 /release
    ECHO Executing: %COMMAND_TO_RUN%
    call %COMMAND_TO_RUN% || EXIT 1
)
