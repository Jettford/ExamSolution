:: delete previous publish 
rmdir /s /q publish

:: run our python build
py C:/Users/tlevelexam4/AppData/Roaming/Python/Python311/site-packages/PyInstaller/__main__.py --onefile --name website ./website/__main__.py

:: make a publish directory
mkdir publish
mkdir publish\release

:: move the exe to the publish directory
copy .\dist\website.exe .\publish\release\

:: copy the static and template directory from website to publish
xcopy .\website\static\ .\publish\release\static\ /s /e
xcopy .\website\templates\ .\publish\release\templates\ /s /e 

:: copy the config file to the publish directory
copy .\website\config.json .\publish\release\

:: delete the dist and build directories
rmdir /s /q dist
rmdir /s /q build

del website.spec