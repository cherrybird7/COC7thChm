@echo off
setlocal

rem 设置目录
set "base_dir=你新设置的文件的路径"

rem 创建字母 A 到 Z 的文件夹
for %%D in (A B C D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    mkdir "%base_dir%\%%D"
)

endlocal