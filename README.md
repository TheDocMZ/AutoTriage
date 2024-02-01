# AutoTriage
A Windows host forensics triage script that leverages several command line tools to automate the extraction of key data to perform an initial analysis. The data extracted includes Windows Registry Hives, MFT, Shimcache, Amcache, Prefetch, and Event Logs. 

## Dependencies:
This script utilizes [RegRipper3.0](https://github.com/keydet89/RegRipper3.0) and [Eric Zimmerman Tools](https://ericzimmerman.github.io/#!index.md). These can be downloaded from their respective links. Additionally, the script provides the option to automate downloading these tools. The default location assumed by the script is  `C:\Tools\`.

## Prerequisites
This script assumes data acquisition has been completed which can be completed utilizing [FTK Imager](https://www.exterro.com/digital-forensics-software/ftk-imager), and a forensic image has been mounted and/or key data extracted via tools such as [Arsenal Image Mounter](https://arsenalrecon.com/downloads/) and [KAPE](https://www.kroll.com/en/services/cyber-risk/incident-response-litigation-support/kroll-artifact-parser-extractor-kape).

## Usage
The `-r`/ `--run` argument accepts the options regripper, eztools, or all to run all.
`AutoTriage.py -r [regripper, eztools, all]`

Optional arguments:
- `-v` / `--verbose` for verbose output from the tools being executed
- `-y` / `--yes` for auto accepting the default source and destination directories
	- rip.exe - `C:\Tools\RegRipper\`
	- EZ Tools - `C:\Tools\ZimmermanTools\net6\"
	- Default source data - `C:\Cases\<Case#>\E\`
	- Default destination - `C:\Cases\<Case#>\Analysis\`

## Additional Resources
[Blue Cape Security PWF](https://github.com/bluecapesecurity/PWF) is a great resource that provides training on conducting a Windows forensic investigation, instructions for setting up a virtual environment, and how to leverage these tools and more as part of an investigation. 
