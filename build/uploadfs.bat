%LOCALAPPDATA%\Programs\Python\Python39\python.exe makefs.py
%LOCALAPPDATA%\Programs\Python\Python39\Scripts\esptool.exe -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x310000 ..\fs.bin
%USERPROFILE%\Downloads\putty.exe -load "mpy"