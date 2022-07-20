---
title: "PowerShell 4104 Hunting"
excerpt: "Command and Scripting Interpreter
, PowerShell
"
categories:
  - Endpoint
last_modified_at: 2022-05-02
toc: true
toc_label: ""
tags:
  - Command and Scripting Interpreter
  - PowerShell
  - Execution
  - Execution
  - Splunk Enterprise
  - Splunk Enterprise Security
  - Splunk Cloud
---



[Try in Splunk Security Cloud](https://www.splunk.com/en_us/products/cyber-security.html){: .btn .btn--success}

#### Description

The following Hunting analytic assists with identifying suspicious PowerShell execution using Script Block Logging, or EventCode 4104. This analytic is not meant to be ran hourly, but occasionally to identify malicious or suspicious PowerShell. This analytic is a combination of work completed by Alex Teixeira and Splunk Threat Research Team.

- **Type**: [Hunting](https://github.com/splunk/security_content/wiki/Detection-Analytic-Types)
- **Product**: Splunk Enterprise, Splunk Enterprise Security, Splunk Cloud

- **Last Updated**: 2022-05-02
- **Author**: Michael Haag, Splunk
- **ID**: d6f2b006-0041-11ec-8885-acde48001122


#### Annotations

<details>
  <summary>ATT&CK</summary>

<div markdown="1">


| ID             | Technique        |  Tactic             |
| -------------- | ---------------- |-------------------- |
| [T1059](https://attack.mitre.org/techniques/T1059/) | Command and Scripting Interpreter | Execution |

| [T1059.001](https://attack.mitre.org/techniques/T1059/001/) | PowerShell | Execution |

</div>
</details>


<details>
  <summary>Kill Chain Phase</summary>

<div markdown="1">

* Exploitation


</div>
</details>


<details>
  <summary>NIST</summary>

<div markdown="1">



</div>
</details>

<details>
  <summary>CIS20</summary>

<div markdown="1">



</div>
</details>

<details>
  <summary>CVE</summary>

<div markdown="1">


</div>
</details>

#### Search 

```
`powershell` EventCode=4104 
| eval DoIt = if(match(ScriptBlockText,"(?i)(\$doit)"), "4", 0) 
| eval enccom=if(match(ScriptBlockText,"[A-Za-z0-9+\/]{44,}([A-Za-z0-9+\/]{4}
|[A-Za-z0-9+\/]{3}=
|[A-Za-z0-9+\/]{2}==)") OR match(ScriptBlockText, "(?i)[-]e(nc*o*d*e*d*c*o*m*m*a*n*d*)*\s+[^-]"),4,0) 
| eval suspcmdlet=if(match(ScriptBlockText, "(?i)Add-Exfiltration
|Add-Persistence
|Add-RegBackdoor
|Add-ScrnSaveBackdoor
|Check-VM
|Do-Exfiltration
|Enabled-DuplicateToken
|Exploit-Jboss
|Find-Fruit
|Find-GPOLocation
|Find-TrustedDocuments
|Get-ApplicationHost
|Get-ChromeDump
|Get-ClipboardContents
|Get-FoxDump
|Get-GPPPassword
|Get-IndexedItem
|Get-Keystrokes
|LSASecret
|Get-PassHash
|Get-RegAlwaysInstallElevated
|Get-RegAutoLogon
|Get-RickAstley
|Get-Screenshot
|Get-SecurityPackages
|Get-ServiceFilePermission
|Get-ServicePermission
|Get-ServiceUnquoted
|Get-SiteListPassword
|Get-System
|Get-TimedScreenshot
|Get-UnattendedInstallFile
|Get-Unconstrained
|Get-VaultCredential
|Get-VulnAutoRun
|Get-VulnSchTask
|Gupt-Backdoor
|HTTP-Login
|Install-SSP
|Install-ServiceBinary
|Invoke-ACLScanner
|Invoke-ADSBackdoor
|Invoke-ARPScan
|Invoke-AllChecks
|Invoke-BackdoorLNK
|Invoke-BypassUAC
|Invoke-CredentialInjection
|Invoke-DCSync
|Invoke-DllInjection
|Invoke-DowngradeAccount
|Invoke-EgressCheck
|Invoke-Inveigh
|Invoke-InveighRelay
|Invoke-Mimikittenz
|Invoke-NetRipper
|Invoke-NinjaCopy
|Invoke-PSInject
|Invoke-Paranoia
|Invoke-PortScan
|Invoke-PoshRat
|Invoke-PostExfil
|Invoke-PowerDump
|Invoke-PowerShellTCP
|Invoke-PsExec
|Invoke-PsUaCme
|Invoke-ReflectivePEInjection
|Invoke-ReverseDNSLookup
|Invoke-RunAs
|Invoke-SMBScanner
|Invoke-SSHCommand
|Invoke-Service
|Invoke-Shellcode
|Invoke-Tater
|Invoke-ThunderStruck
|Invoke-Token
|Invoke-UserHunter
|Invoke-VoiceTroll
|Invoke-WScriptBypassUAC
|Invoke-WinEnum
|MailRaider
|New-HoneyHash
|Out-Minidump
|Port-Scan
|PowerBreach
|PowerUp
|PowerView
|Remove-Update
|Set-MacAttribute
|Set-Wallpaper
|Show-TargetScreen
|Start-CaptureServer
|VolumeShadowCopyTools
|NEEEEWWW
|(Computer
|User)Property
|CachedRDPConnection
|get-net\S+
|invoke-\S+hunter
|Install-Service
|get-\S+(credent
|password)
|remoteps
|Kerberos.*(policy
|ticket)
|netfirewall
|Uninstall-Windows
|Verb\s+Runas
|AmsiBypass
|nishang
|Invoke-Interceptor
|EXEonRemote
|NetworkRelay
|PowerShelludp
|PowerShellIcmp
|CreateShortcut
|copy-vss
|invoke-dll
|invoke-mass
|out-shortcut
|Invoke-ShellCommand"),1,0) 
| eval base64 = if(match(lower(ScriptBlockText),"frombase64"), "4", 0) 
| eval empire=if(match(lower(ScriptBlockText),"system.net.webclient") AND match(lower(ScriptBlockText), "frombase64string") ,5,0) 
| eval mimikatz=if(match(lower(ScriptBlockText),"mimikatz") OR match(lower(ScriptBlockText), "-dumpcr") OR match(lower(ScriptBlockText), "SEKURLSA::Pth") OR match(lower(ScriptBlockText), "kerberos::ptt") OR match(lower(ScriptBlockText), "kerberos::golden") ,5,0) 
| eval iex = if(match(lower(ScriptBlockText),"iex"), "2", 0) 
| eval webclient=if(match(lower(ScriptBlockText),"http") OR match(lower(ScriptBlockText),"web(client
|request)") OR match(lower(ScriptBlockText),"socket") OR match(lower(ScriptBlockText),"download(file
|string)") OR match(lower(ScriptBlockText),"bitstransfer") OR match(lower(ScriptBlockText),"internetexplorer.application") OR match(lower(ScriptBlockText),"xmlhttp"),5,0) 
| eval get = if(match(lower(ScriptBlockText),"get-"), "1", 0) 
| eval rundll32 = if(match(lower(ScriptBlockText),"rundll32"), "4", 0) 
| eval suspkeywrd=if(match(ScriptBlockText, "(?i)(bitstransfer
|mimik
|metasp
|AssemblyBuilderAccess
|Reflection\.Assembly
|shellcode
|injection
|cnvert
|shell\.application
|start-process
|Rc4ByteStream
|System\.Security\.Cryptography
|lsass\.exe
|localadmin
|LastLoggedOn
|hijack
|BackupPrivilege
|ngrok
|comsvcs
|backdoor
|brute.?force
|Port.?Scan
|Exfiltration
|exploit
|DisableRealtimeMonitoring
|beacon)"),1,0) 
| eval syswow64 = if(match(lower(ScriptBlockText),"syswow64"), "3", 0) 
| eval httplocal = if(match(lower(ScriptBlockText),"http://127.0.0.1"), "4", 0) 
| eval reflection = if(match(lower(ScriptBlockText),"reflection"), "1", 0) 
| eval invokewmi=if(match(lower(ScriptBlockText), "(?i)(wmiobject
|WMIMethod
|RemoteWMI
|PowerShellWmi
|wmicommand)"),5,0) 
| eval downgrade=if(match(ScriptBlockText, "(?i)([-]ve*r*s*i*o*n*\s+2)") OR match(lower(ScriptBlockText),"powershell -version"),3,0) 
| eval compressed=if(match(ScriptBlockText, "(?i)GZipStream
|::Decompress
|IO.Compression
|write-zip
|(expand
|compress)-Archive"),5,0) 
| eval invokecmd = if(match(lower(ScriptBlockText),"invoke-command"), "4", 0) 
| addtotals fieldname=Score DoIt, enccom, suspcmdlet, suspkeywrd, compressed, downgrade, mimikatz, iex, empire, rundll32, webclient, syswow64, httplocal, reflection, invokewmi, invokecmd, base64, get 
| stats values(Score) by DoIt, enccom, compressed, downgrade, iex, mimikatz, rundll32, empire, webclient, syswow64, httplocal, reflection, invokewmi, invokecmd, base64, get, suspcmdlet, suspkeywrd 
| `powershell_4104_hunting_filter`
```

#### Macros
The SPL above uses the following Macros:
* [powershell](https://github.com/splunk/security_content/blob/develop/macros/powershell.yml)

> :information_source:
> **powershell_4104_hunting_filter** is a empty macro by default. It allows the user to filter out any results (false positives) without editing the SPL.

#### Required field
* _time
* ScriptBlockText
* Opcode
* Computer
* UserID
* EventCode


#### How To Implement
The following Hunting analytic requires PowerShell operational logs to be imported. Modify the powershell macro as needed to match the sourcetype or add index. This analytic is specific to 4104, or PowerShell Script Block Logging.

#### Known False Positives
Limited false positives. May filter as needed.

#### Associated Analytic story
* [Hermetic Wiper](/stories/hermetic_wiper)
* [Malicious PowerShell](/stories/malicious_powershell)




#### RBA

| Risk Score  | Impact      | Confidence   | Message      |
| ----------- | ----------- |--------------|--------------|
| 80.0 | 80 | 100 | An instance of $parent_process_name$ spawning $process_name$ was identified on endpoint $Computer$ by user $user$ executing suspicious commands. |


> :information_source:
> The Risk Score is calculated by the following formula: Risk Score = (Impact * Confidence/100). Initial Confidence and Impact is set by the analytic author. 

#### Reference

* [https://github.com/inodee/threathunting-spl/blob/master/hunt-queries/powershell_qualifiers.md](https://github.com/inodee/threathunting-spl/blob/master/hunt-queries/powershell_qualifiers.md)
* [https://docs.splunk.com/Documentation/UBA/5.0.4.1/GetDataIn/AddPowerShell](https://docs.splunk.com/Documentation/UBA/5.0.4.1/GetDataIn/AddPowerShell)
* [https://github.com/marcurdy/dfir-toolset/blob/master/Powershell%20Blueteam.txt](https://github.com/marcurdy/dfir-toolset/blob/master/Powershell%20Blueteam.txt)
* [https://devblogs.microsoft.com/powershell/powershell-the-blue-team/](https://devblogs.microsoft.com/powershell/powershell-the-blue-team/)
* [https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging?view=powershell-5.1](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging?view=powershell-5.1)
* [https://www.mandiant.com/resources/greater-visibilityt](https://www.mandiant.com/resources/greater-visibilityt)
* [https://hurricanelabs.com/splunk-tutorials/how-to-use-powershell-transcription-logs-in-splunk/](https://hurricanelabs.com/splunk-tutorials/how-to-use-powershell-transcription-logs-in-splunk/)
* [https://www.splunk.com/en_us/blog/security/hunting-for-malicious-powershell-using-script-block-logging.html](https://www.splunk.com/en_us/blog/security/hunting-for-malicious-powershell-using-script-block-logging.html)



#### Test Dataset
Replay any dataset to Splunk Enterprise by using our [replay.py](https://github.com/splunk/attack_data#using-replaypy) tool or the [UI](https://github.com/splunk/attack_data#using-ui).
Alternatively you can replay a dataset into a [Splunk Attack Range](https://github.com/splunk/attack_range#replay-dumps-into-attack-range-splunk-server)


* [https://media.githubusercontent.com/media/splunk/attack_data/master/datasets/attack_techniques/T1059.001/powershell_script_block_logging/sbl_xml.log](https://media.githubusercontent.com/media/splunk/attack_data/master/datasets/attack_techniques/T1059.001/powershell_script_block_logging/sbl_xml.log)



[*source*](https://github.com/splunk/security_content/tree/develop/detections/endpoint/powershell_4104_hunting.yml) \| *version*: **3**