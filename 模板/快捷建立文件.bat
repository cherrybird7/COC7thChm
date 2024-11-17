@echo off
setlocal enabledelayedexpansion

rem 设置模板文件路径
set "templatePath=全白页所在的目录\全白页.htm"
rem 设置目标文件夹
set "outputFolder=你新设置的文件的路径"

rem 创建输出文件并写入模板内容
for %%f in (文件1 文件2 文件3 文件4 文件5) do (
    set "fileName=%%f.htm"
    copy /y "!templatePath!" "!outputFolder!\!fileName!"
)

endlocal