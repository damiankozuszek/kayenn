; Windows installer – Inno Setup 6. Run by packaging/build.py:
;   iscc /DAppVersion=0.1.0 /DSourceDir=...\build\dist\KAYENN /DOutDir=...\dist /DRootDir=... kayenn.iss
#ifndef AppVersion
  #define AppVersion "0.0.0"
#endif

[Setup]
AppId={{6B1F4A2E-6C1D-4C55-9A3B-2F7E0B9C4D17}
AppName=KAYENN
AppVersion={#AppVersion}
AppVerName=KAYENN {#AppVersion}
AppPublisher=KAYENN
DefaultDirName={autopf}\KAYENN
DefaultGroupName=KAYENN
DisableProgramGroupPage=yes
; install for the current user (no administrator rights) or for all users – chosen in the installer
; (the installer texts stay in Polish – they are part of the program interface)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir={#OutDir}
OutputBaseFilename=KAYENN-{#AppVersion}-windows-x64-setup
SetupIconFile={#RootDir}\branding\kayenn.ico
UninstallDisplayIcon={app}\KAYENN.exe
UninstallDisplayName=KAYENN {#AppVersion}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ChangesAssociations=yes
CloseApplications=yes

[Languages]
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "assoc"; Description: "Otwieraj pliki projektu .kayenn programem KAYENN"; GroupDescription: "Skojarzenia plików:"

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\KAYENN"; Filename: "{app}\KAYENN.exe"
Name: "{autodesktop}\KAYENN"; Filename: "{app}\KAYENN.exe"; Tasks: desktopicon

[Registry]
Root: HKA; Subkey: "Software\Classes\.kayenn"; ValueType: string; ValueName: ""; ValueData: "KAYENN.Projekt"; Flags: uninsdeletevalue; Tasks: assoc
Root: HKA; Subkey: "Software\Classes\KAYENN.Projekt"; ValueType: string; ValueName: ""; ValueData: "Projekt KAYENN"; Flags: uninsdeletekey; Tasks: assoc
Root: HKA; Subkey: "Software\Classes\KAYENN.Projekt\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: """{app}\_internal\branding\kayenn.ico"",0"; Tasks: assoc
Root: HKA; Subkey: "Software\Classes\KAYENN.Projekt\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\KAYENN.exe"" ""%1"""; Tasks: assoc

[Run]
Filename: "{app}\KAYENN.exe"; Description: "{cm:LaunchProgram,KAYENN}"; Flags: nowait postinstall skipifsilent
