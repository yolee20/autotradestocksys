@echo off
setlocal enabledelayedexpansion


REM 先进行条件判断，再定义锁文件、日志文件和备份目录的位置
set LOCK_FILE=
set LOG_FILE=
set BACKUP_DIR=


REM 检查系统临时目录是否存在
if not defined TEMP (
    echo Error: TEMP environment variable is not defined.
    exit /b
)


REM 检查用户配置文件目录是否存在
if not defined USERPROFILE (
    echo Error: USERPROFILE environment variable is not defined.
    exit /b
)


REM 检查并设置锁文件的位置，使用系统临时目录
set LOCK_FILE=%TEMP%\clear-trash.lock


REM 检查锁文件是否存在
if exist "%LOCK_FILE%" (
    echo 对不起，clear-trash.bat 程序正在运行，请等待其完成或手动终止后再尝试运行。
    pause
    exit /b
)


REM 检查并设置日志文件的位置，使用系统临时目录
if defined TEMP (
    set LOG_FILE=%TEMP%\clear-trash.log
)


REM 检查并设置备份目录，将删除的文件保存至此
if defined USERPROFILE (
    set BACKUP_DIR=%USERPROFILE%\Desktop\DeletedFilesBackup
)


REM 获取当前系统时间
for /F "tokens=1-4 delims=:.," %%a in ("%time%") do (
    set CURRENT_TIME=%%a:%%b:%%c.%%d
)


REM 获取当前登录用户
for /F "usebackq tokens=*" %%a in (`whoami`) do (
    set CURRENT_USER=%%a
)


REM 创建锁文件，将 del 命令、当前系统时间和登录用户写入其中
echo del & echo Time:!CURRENT_TIME! & echo User:!CURRENT_USER! > "%LOCK_FILE%"


REM 记录程序开始时间
set START_TIME=%time%


REM 以下是清除系统垃圾文件的代码部分
echo 请勿关闭本窗口！
echo 正在清除系统垃圾文件，请稍等...... >> "%LOG_FILE%"


echo 3
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


echo 4
pause


REM 循环处理要删除的文件和目录
echo Starting the loop to move files... >> "%LOG_FILE%"
for /l %%i in (0,1,12) do (
    REM 获取源文件或目录
    set SRC=!FILES[%%i]!
    REM 获取目标备份位置
    set DST=!BACKUP[%%i]!
    REM 确保目标备份子目录存在
    call :ensure_dir "!DST!"
    echo Processing file: "!SRC!" >> "%LOG_FILE%"
    REM 给源文件和目标文件加双引号
    if exist "!SRC!" (
        REM 尝试多次移动操作，最多 3 次
        set retry_count=0
        :retry_move
        move /y "!SRC!" "!DST!" >> "%LOG_FILE%"
        if errorlevel 1 (
            set /a retry_count+=1
            if!retry_count! leq 3 (
                echo Failed to move "!SRC!" to "!DST!", retrying... >> "%LOG_FILE%"
                goto retry_move
            ) else (
                echo Failed to move "!SRC!" to "!DST!" after 3 attempts >> "%LOG_FILE%"
            )
        ) else (
            echo Successfully moved "!SRC!" to "!DST!" >> "%LOG_FILE%"
        )
    ) else {
        echo Source file or directory "!SRC!" does not exist. >> "%LOG_FILE%"
    }
)


echo 5
pause


REM 删除 Windows 临时目录并重新创建
echo Deleting and recreating Windows temp directory... >> "%LOG_FILE%"
rd /s /q %windir%\temp & md %windir%\temp
if errorlevel 1 (
    echo Failed to delete and recreate temp directory >> "%LOG_FILE%"
) else (
    echo Successfully deleted and recreated temp directory >> "%LOG_FILE%"
}


echo 清除系统垃圾完成！ >> "%LOG_FILE%"


REM 删除锁文件
del "%LOCK_FILE%"


REM 记录程序结束时间
set END_TIME=%time%


REM 计算程序执行时长
call :calculate_duration %START_TIME% %END_TIME%


exit


:ensure_dir
setlocal
set dir_path=%~dp1
if not exist "%dir_path%" (
    mkdir "%dir_path%"
)
endlocal
goto :eof


:calculate_duration
setlocal
set "start_hours=%~1:~0,2%"
set "start_minutes=%~1:~3,2%"
set "start_seconds=%~1:~6,2%"
set "start_hundredths=%~1:~9,2%"


set "end_hours=%~2:~0,2%"
set "end_minutes=%~2:~3,2%"
set "end_seconds=%~2:~6,2%"
set "end_hundredths=%~2:~9,2%"


set /a "start_total=(100*((100*((100*%start_hours%)+%start_minutes%))+%start_seconds%)+%start_hundredths%)"
set /a "end_total=(100*((100*((100*%end_hours%)+%end_minutes%))+%end_seconds%)+%end_hundredths%)"


set /a "duration_total=%end_total%-%start_total%"


set /a "duration_hundredths=%duration_total% %% 100"
set /a "duration_total=%duration_total% / 100"
set /a "duration_seconds=%duration_total% %% 60"
set /a "duration_total=%duration_total% / 60"
set /a "duration_minutes=%duration_total% %% 60"
set /a "duration_hours=%duration_total% / 60"


echo 程序执行时长：%duration_hours%:%duration_minutes%:%duration_seconds%.%duration_hundredths% >> "%LOG_FILE%"


endlocal
goto :eof