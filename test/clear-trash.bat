@echo off
setlocal enabledelayedexpansion


REM 定义锁文件的位置，使用系统临时目录
set LOCK_FILE=%TEMP%\clear-trash.lock


REM 定义日志文件的位置
set LOG_FILE=%TEMP%\clear-trash.log


REM 定义备份目录，将删除的文件保存至此
set BACKUP_DIR=%USERPROFILE%\Desktop\DeletedFilesBackup


REM 检查备份目录是否存在，若不存在则创建
if not exist "%BACKUP_DIR%" (
    mkdir "%BACKUP_DIR%"
)


echo "1"
pause


REM 检查锁文件是否存在
if exist "%LOCK_FILE%" (
    echo Another instance of clear-trash.bat is already running.
    exit /b
)


REM 创建锁文件
echo 1 > "%LOCK_FILE%"


REM 以下是清除系统垃圾文件的代码部分
echo 请勿关闭本窗口！
echo 正在清除系统垃圾文件，请稍等...... >> "%LOG_FILE%"


echo "3"
pause


REM 定义要删除的文件和目录及其备份位置
set FILES[0]=%systemdrive%\*.tmp
set BACKUP[0]=%BACKUP_DIR%\*.tmp
set FILES[1]=%windir%\prefetch\*.*
set BACKUP[1]=%BACKUP_DIR%\prefetch\*.*
set FILES[2]=%userprofile%\Local Settings\Temp\*.*
set BACKUP[2]=%BACKUP_DIR%\UserTemp\*.*
set FILES[3]=%systemdrive%\*._mp
set BACKUP[3]=%BACKUP_DIR%\*._mp
set FILES[4]=%windir%\*.bak
set BACKUP[4]=%BACKUP_DIR%\*.bak
set FILES[5]=%systemdrive%\*.log
set BACKUP[5]=%BACKUP_DIR%\*.log
set FILES[6]=%systemdrive%\*.gid
set BACKUP[6]=%BACKUP_DIR%\*.gid
set FILES[7]=%systemdrive%\*.chk
set BACKUP[7]=%BACKUP_DIR%\*.chk
set FILES[8]=%systemdrive%\*.old
set BACKUP[8]=%BACKUP_DIR%\*.old
set FILES[9]=%systemdrive%\recycled\*.*
set BACKUP[9]=%BACKUP_DIR%\recycled\*.*
set FILES[10]=%userprofile%\cookies\*.*
set BACKUP[10]=%BACKUP_DIR%\cookies\*.*
set FILES[11]=%userprofile%\recent\*.*
set BACKUP[11]=%BACKUP_DIR%\recent\*.*
set FILES[12]=%userprofile%\Local Settings\Temporary Internet Files\*.*
set BACKUP[12]=%BACKUP_DIR%\InternetTemp\*.*


REM 循环处理要删除的文件和目录
for /l %%i in (0,1,12) do (
    REM 获取源文件或目录
    set SRC=!FILES[%%i]!
    REM 获取目标备份位置
    set DST=!BACKUP[%%i]!
    REM 确保目标备份子目录存在
    call :ensure_dir "!DST!"
    if exist "!SRC!" (
        move /y "!SRC!" "!DST!" >> "%LOG_FILE%"
        if errorlevel 1 (
            echo Failed to move!SRC! >> "%LOG_FILE%"
        )
    )
)


REM 删除 Windows 临时目录并重新创建
rd /s /q %windir%\temp & md %windir%\temp
if errorlevel 1 (
    echo Failed to delete and recreate temp directory >> "%LOG_FILE%"
)


echo 清除系统垃圾完成！ >> "%LOG_FILE%"


REM 删除锁文件
del "%LOCK_FILE%"


exit


:ensure_dir
setlocal
set dir_path=%~dp1
if not exist "%dir_path%" (
    mkdir "%dir_path%"
)
endlocal
goto :eof