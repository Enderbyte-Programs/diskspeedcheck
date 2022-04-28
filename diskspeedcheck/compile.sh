pyinstaller --onefile diskspeedcheck.py
cp ./dist/diskspeedcheck /home/pi/exe
rm -rf build
rm -rf dist