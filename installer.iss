#define MyAppName "LT Aimbot"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Joseph Stadum"
#define MyAppURL "https://github.com/shreksojoe/lt_aimbot"
#define MyAppExeName "lt_aimbot.bat"
#define MyAppId "{{F1A34B56-C78D-4E92-8F01-A5B6C7D8E9F0}}"

[Setup]
; Basic setup information
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=LICENSE.txt
; By default, we require admin privileges for installation and updates
PrivilegesRequired=admin
; Allow users to choose non-admin install if needed
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=installer_output
OutputBaseFilename=LTAimbot_Setup_{#MyAppVersion}
SolidCompression=yes
WizardStyle=modern
; SetupIconFile=app_icon.ico  ; Commented out as icon file is missing

; Minimize Windows Defender false positives
Compression=lzma2/ultra64
InternalCompressLevel=ultra
; Sign the installer - uncomment and configure if you have a code signing certificate
;SignTool=signtool sign /f "certificate.pfx" /p password /t http://timestamp.comodoca.com/authenticode $f

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main source files
Source: "main.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\*.py"; DestDir: "{app}\src"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "version.json"; DestDir: "{app}"; Flags: ignoreversion

; Include the updater script
Source: "src\updater.py"; DestDir: "{app}\src"; Flags: ignoreversion

; Create batch file launcher
Source: "lt_aimbot.bat"; DestDir: "{app}"; Flags: ignoreversion

; Download and include Python embedded package
#define PythonEmbedded "python-3.11.7-embed-amd64.zip"
Source: "{tmp}\{#PythonEmbedded}"; DestDir: "{app}"; Flags: external deleteafterinstall

; Note: The Python package will be extracted during post-install

; Include version info file
Source: "version.json"; DestDir: "{app}"; Flags: ignoreversion

; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Registry]
; Add registry entries for auto-update
Root: HKLM; Subkey: "SOFTWARE\{#MyAppName}"; Flags: uninsdeletekeyifempty
Root: HKLM; Subkey: "SOFTWARE\{#MyAppName}"; ValueType: string; ValueName: "InstallLocation"; ValueData: "{app}"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\{#MyAppName}"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"; Flags: uninsdeletevalue

; Add entry to run updater at startup to check for updates
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "{#MyAppName}UpdateCheck"; ValueData: """{app}\updater.bat"" --silent"; Flags: uninsdeletevalue

[Code]
// Prepare the installation and download Python embedded package
procedure InitializeWizard();
var
  PythonURL: String;
  DownloadPage: TDownloadWizardPage;
begin
  // Create the download page
  DownloadPage := CreateDownloadPage(SetupMessage(msgWizardPreparing), SetupMessage(msgPreparingDesc), nil);
  
  // Download Python embedded package
  PythonURL := 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-embed-amd64.zip';
  DownloadPage.Clear;
  DownloadPage.Add(PythonURL, '{#PythonEmbedded}', '');
  DownloadPage.Show;
  
  try
    DownloadPage.Download;
    
    // We'll handle the Python embedded package directly without extracting it
    // The file will be included as an external source in the [Files] section
  except
    MsgBox('Failed to download Python embedded package. Please check your internet connection.', mbError, MB_OK);
  finally
    DownloadPage.Hide;
  end;
end;

// Include the Windows Shell Application object for extracting ZIP files
type
  TCallback = procedure (OverwriteFlag: Boolean);

// Function to extract ZIP file using Windows Shell
procedure ExtractZIPFile(ZipFile, TargetPath: string);
var
  ShellObj, ZipFileObj, Items: Variant;
begin
  // Create the target directory if it doesn't exist
  if not DirExists(TargetPath) then
    ForceDirectories(TargetPath);
    
  // Use Windows Shell to extract the ZIP file
  try
    ShellObj := CreateOleObject('Shell.Application');
    ZipFileObj := ShellObj.NameSpace(ZipFile);
    Items := ZipFileObj.Items;
    ShellObj.NameSpace(TargetPath).CopyHere(Items, 4 or 16);
  except
    MsgBox('Failed to extract Python embedded package. Please try installing again.', mbError, MB_OK);
  end;
end;

// Create the updater batch file and handle post-installation tasks
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Extract the Python embedded package
    ExtractZIPFile(ExpandConstant('{app}\{#PythonEmbedded}'), ExpandConstant('{app}\python'));
    
    // Create batch file for the updater
    SaveStringToFile(ExpandConstant('{app}\updater.bat'), 
      '@echo off\r\n' +
      'set PYTHONPATH={app}\r\n' +
      '{app}\python\python.exe {app}\src\updater.py %*', False);

    // Create first-run settings file
    SaveStringToFile(ExpandConstant('{app}\first_run'), 'This file indicates first run after installation.', False);
    
    // Configure Python to find installed packages
    SaveStringToFile(ExpandConstant('{app}\python\_pth'), 
      'python311.zip\r\n' +
      '.\\\r\n' +
      '..\\\r\n' +
      'import site', False);
      
    // Delete the ZIP file after extraction
    DeleteFile(ExpandConstant('{app}\{#PythonEmbedded}'));
  end;
end;

