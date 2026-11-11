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
; the installer is in English (default) or Polish – chosen at its start; the program starts in English
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
LicenseFile={#RootDir}\LICENSE
WizardStyle=modern
ChangesAssociations=yes
CloseApplications=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"

[CustomMessages]
english.AssocTask=Open .kayenn project files with KAYENN
english.AssocGroup=File associations:
english.FileTypeName=KAYENN project
polish.AssocTask=Otwieraj pliki projektu .kayenn programem KAYENN
polish.AssocGroup=Skojarzenia plików:
polish.FileTypeName=Projekt KAYENN

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "assoc"; Description: "{cm:AssocTask}"; GroupDescription: "{cm:AssocGroup}"

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\KAYENN"; Filename: "{app}\KAYENN.exe"
Name: "{autodesktop}\KAYENN"; Filename: "{app}\KAYENN.exe"; Tasks: desktopicon

[Registry]
Root: HKA; Subkey: "Software\Classes\.kayenn"; ValueType: string; ValueName: ""; ValueData: "KAYENN.Projekt"; Flags: uninsdeletevalue; Tasks: assoc
Root: HKA; Subkey: "Software\Classes\KAYENN.Projekt"; ValueType: string; ValueName: ""; ValueData: "{cm:FileTypeName}"; Flags: uninsdeletekey; Tasks: assoc
Root: HKA; Subkey: "Software\Classes\KAYENN.Projekt\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: """{app}\_internal\branding\kayenn.ico"",0"; Tasks: assoc
Root: HKA; Subkey: "Software\Classes\KAYENN.Projekt\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\KAYENN.exe"" ""%1"""; Tasks: assoc

[Run]
Filename: "{app}\KAYENN.exe"; Description: "{cm:LaunchProgram,KAYENN}"; Flags: nowait postinstall skipifsilent
; automatic update from the program (/SILENT /relaunch=1): the new version starts by itself, as the user
Filename: "{app}\KAYENN.exe"; Flags: nowait runasoriginaluser; Check: Relaunch

[Code]
function Relaunch: Boolean;
begin
  Result := ExpandConstant('{param:relaunch|0}') = '1';
end;
