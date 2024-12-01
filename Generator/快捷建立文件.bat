@echo off
setlocal enabledelayedexpansion

rem 设置模板文件路径
set "templatePath=C:\Users\Administrator\Desktop\全白页.htm"
rem 设置目标文件夹
set "outputFolder=C:\Users\Administrator\Desktop\1"

rem 创建输出文件并写入模板内容，将要创建的文件名贴近下方的括号中
for %%f in (文件1 文件2 文件3 文件4 文件5) do (
    set "fileName=%%f.htm"
    copy /y "!templatePath!" "!outputFolder!\!fileName!"
)

endlocal