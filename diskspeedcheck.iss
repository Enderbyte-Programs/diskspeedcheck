#define MyAppName "Diskspeedcheck"
#define MyAppVersion "1.2.1"
#define MyAppPublisher "Enderbyte Programs"
#define MyAppURL "https://enderbyte09.wixsite.com/programs"
#define MyAppExeName "diskspeedcheck.exe"

[Setup]
AppId={{3142D004-9F57-460E-A7DF-86CB7BB809DE}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
InfoAfterFile=C:\Python310\Scripts\fin.txt
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=C:\Users\jorda\Installer
OutputBaseFilename=diskspeedcheck-1.2.1-installer
SetupIconFile=C:\Python310\Scripts\speedometer.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ChangesEnvironment=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "shortcut"; Description: "Make a start menu shortcut"; GroupDescription: "Shortcuts"
Name: "reg"; Description: "Register program on PATH"; GroupDescription: "Registry"

[Files]
Source: "C:\Python310\Scripts\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Python310\Scripts\speedometer.ico"; DestDir: "{app}";
Source: "C:\Python310\Scripts\trash.ico"; DestDir: "{app}";

[Icons]
Name: "{group}\Diskspeedcheck Help"; Filename: "{app}\{#MyAppExeName}"; Parameters: "--help"; Tasks: shortcut
Name: "{group}\Check Disk Speed"; Filename: "{app}\{#MyAppExeName}"; Parameters: "--remain"; Tasks: shortcut
Name: "{group}\Uninstall"; Filename: "{app}\unins000.exe"; IconFilename: "{app}\trash.ico";Tasks: shortcut

[Registry]
Root: HKCU; Subkey: "Environment"; \
    ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Tasks: reg
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Flags: noerror; Tasks: reg

