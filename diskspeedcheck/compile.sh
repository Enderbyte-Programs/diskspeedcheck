pyinstaller --onefile diskspeedcheck.py
rm /home/pi/exe/diskspeedcheck
cp ./dist/diskspeedcheck /home/pi/exe
rm -rf build
rm -rf dist