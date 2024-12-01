@echo off
setlocal

rem 设置目录
set "base_dir=C:\Users\Administrator\Desktop\1"

rem 创建A-Z的文件夹，将要创建的文件夹名替换下方的括号中的字母
for %%D in (A B C D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    mkdir "%base_dir%\%%D"
)

endlocal