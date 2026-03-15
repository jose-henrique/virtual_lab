import platform
import subprocess
import os
import pathlib

class LocationGetter:
    def __init__(self):
        pass
    
    def get_location(self):
        system = platform.system()
        
        try:
            if system == "Windows":
                return self.__get_on_windows()
            elif system == "Darwin":
                return self.__get_on_mac()
            elif system == "Linux":
                return self.__get_on_linux()
        except Exception as e:
            print(f"Error opening dialog: {e}")
            return ""
            
        
    
    
    def __get_on_windows(self):
        command = (
            '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; '
            'Add-Type -AssemblyName System.Windows.Forms; '
            '$f = New-Object System.Windows.Forms.FolderBrowserDialog; '
            'if($f.ShowDialog() -eq "OK") { $f.SelectedPath }'
        )
        result = subprocess.run(['powershell', '-Command', command], 
                                 capture_output=True, text=True, encoding='utf-8')
        
        return result.stdout.strip()
    
    def __get_on_mac(self):
        command = 'osascript -e "POSIX path of (choose folder)"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    
    def __get_on_linux(self):
        try:
            result = subprocess.run(['zenity', '--file-selection', '--directory'], 
                                     capture_output=True, text=True)
            return result.stdout.strip()
        except FileNotFoundError:
            result = subprocess.run(['kdialog', '--getexistingdirectory'], 
                                     capture_output=True, text=True)
            return result.stdout.strip()