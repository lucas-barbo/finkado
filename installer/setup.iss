[Setup]
AppName=Finkado
AppVersion=1.0.0
WizardStyle=modern
DefaultDirName={autopf}\Finkado
DefaultGroupName=Finkado
OutputDir=..\build_output
OutputBaseFilename=Finkado_Setup
Compression=lzma
SolidCompression=yes

[Files]
; Coleta o executável principal gerado pelo PyInstaller
Source: "..\dist\finkado\finkado.exe"; DestDir: "{app}"; Flags: ignoreversion
; Coleta todas as dependências e pastas geradas (incluindo as views e assets se houver)
Source: "..\dist\finkado\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Finkado"; Filename: "{app}\finkado.exe"
Name: "{autodesktop}\Finkado"; Filename: "{app}\finkado.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked