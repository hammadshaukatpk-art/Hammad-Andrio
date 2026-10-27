#define MyAppName "MH Andrio"
#define MyAppVersion "0.1.0"
[Setup]
AppId={{D4758959-E5C5-4EB2-A5D1-BFA50B165A95}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\MH Andrio
DefaultGroupName=MH Andrio
OutputDir=..\dist-installer
OutputBaseFilename=MH-Andrio-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
[Files]
Source: "..\dist\MH-Andrio\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion
[Icons]
Name: "{autoprograms}\MH Andrio"; Filename: "{app}\MH-Andrio.exe"
Name: "{autodesktop}\MH Andrio"; Filename: "{app}\MH-Andrio.exe"
[Run]
Filename: "{app}\MH-Andrio.exe"; Description: "Launch MH Andrio"; Flags: nowait postinstall skipifsilent
