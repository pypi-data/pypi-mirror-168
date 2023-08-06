:: ============================================================================
:: Copyright 2022 Intel Corporation All Rights Reserved.
::
:: The source code,  information and material ("Material")  contained herein is
:: owned by Intel Corporation or its suppliers or licensors,  and title to such
:: Material remains with Intel Corporation or its suppliers  or licensors.  The
:: Material contains  proprietary  information  of Intel  or its  suppliers and
:: licensors.  The Material is protected by worldwide copyright laws and treaty
:: provisions.  No part  of the  Material   may be  used,  copied,  reproduced,
:: modified,  published,   uploaded,   posted,   transmitted,   distributed  or
:: disclosed in any way without Intel's prior  express written  permission.  No
:: license under any patent,  copyright  or other intellectual  property rights
:: in the Material is granted to or conferred upon you,  either  expressly,  by
:: implication,  inducement,  estoppel  or otherwise.  Any  license  under such
:: intellectual  property  rights must  be  express and  approved  by  Intel in
:: writing.
::
:: Unless otherwise  agreed by  Intel in writing,  you may not  remove or alter
:: this notice or  any other notice  embedded in Materials by  Intel or Intel's
:: suppliers or licensors in any way.
:: ============================================================================
@echo off

IF EXIST "%CONDA_PREFIX%\Library\bin\" (
    set "TBB_DLL_PATH_CONDA_BACKUP=%TBB_DLL_PATH%"
    set "TBB_DLL_PATH=%CONDA_PREFIX%\Library\bin"
    set "OCL_CPU_RT_PATH=%BUILD_PREFIX%\compiler\lib\x64"
) ELSE (
  IF EXIST "%PREFIX%\Library\bin\" (
    set "TBB_DLL_PATH_CONDA_BACKUP=%TBB_DLL_PATH%"
    set "TBB_DLL_PATH=%PREFIX%\Library\bin"
    set "OCL_CPU_RT_PATH=%PREFIX%\compiler\lib\x64"
  )
)

IF EXIST "%OCL_CPU_RT_PATH%\cl.cfg" (
:: Remove old line contains CL_CONFIG_TBB_DLL_PATH in config file
    findstr /v /i /c:"CL_CONFIG_TBB_DLL_PATH"  %OCL_CPU_RT_PATH%\cl.cfg > %OCL_CPU_RT_PATH%\cl.cfg.tmp
    copy /Y %OCL_CPU_RT_PATH%\cl.cfg.tmp %OCL_CPU_RT_PATH%\cl.cfg  > NUL
    del %OCL_CPU_RT_PATH%\cl.cfg.tmp

:: Add a new line for TBB DLL PATH
    echo CL_CONFIG_TBB_DLL_PATH = %TBB_DLL_PATH% >> %OCL_CPU_RT_PATH%\cl.cfg
)

IF EXIST "%OCL_CPU_RT_PATH%\cl.fpga_emu.cfg" (
:: Remove old line contains CL_CONFIG_TBB_DLL_PATH in config file
    findstr /v /i /c:"CL_CONFIG_TBB_DLL_PATH"  %OCL_CPU_RT_PATH%\cl.fpga_emu.cfg > %OCL_CPU_RT_PATH%\cl.fpga_emu.cfg.tmp
    copy /Y %OCL_CPU_RT_PATH%\cl.fpga_emu.cfg.tmp %OCL_CPU_RT_PATH%\cl.fpga_emu.cfg  > NUL
    del %OCL_CPU_RT_PATH%\cl.fpga_emu.cfg.tmp

:: Add a new line for TBB DLL PATH
    echo CL_CONFIG_TBB_DLL_PATH = %TBB_DLL_PATH% >> %OCL_CPU_RT_PATH%\cl.fpga_emu.cfg
)
