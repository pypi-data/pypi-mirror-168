# autorun.inf Deobfuscator
A cli script to deobfuscate obfuscated ```autorun.inf``` files as used by the Conficker / Downadup malware for example.

Such an ```autorun.inf``` file can be quite big since the malware authors can add junk to the configfile which will not be evaluated by Windows. 
This scripts only shows the important parts of the config which will be evaluated by Windows.
More information about ```autorun.inf``` files you can find on [Wikipedia](https://en.wikipedia.org/wiki/Autorun.inf).

## Installation

Install the package with pip

    pip install autorun-inf-deobfuscator

or 

    pip install git+https://github.com/wahlflo/AutorunInfDeobfuscator

## Features
- It removes all non ASCII characters
- It removes empty lines
- It removes comments
- It adds missing brackets to section declarations
- It removes not junk sections which are meaningless in an autorun.inf file 

## Usage
Type ```deobfuscate-autorun-inf --help``` to view the help.

```
usage: deobfuscate-autorun-inf [OPTION]... -i FILE

A cli script to deobfuscate obfuscated autorun.inf files as used by the Conficker / Downadup malware for example.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        path to the eml-file (is required)
  --no-deobfuscation    No deobfuscation
  --remove-comments     Remove comments
  --remove-empty-lines  Remove empty lines
  --fix-missing-brackets
                        Fix missing section brackets
  --remove-junk-sections
                        Remove junk sections by filtering on the legitimate sections of an autorun.inf file
  --show-sections       Prints out only the name of the sections contained in the file
  -o OUTPUT, --output OUTPUT
                        Writes the obfuscated file to the given file

```

## Example deobfuscation of an autorun.inf file

excerpt of an obfuscated autorun.inf file created by Conficker:
```             
	[AUTorUN
            
; ÅA¯˜ölÜŠq¦…tÎKVWœý¸¤¬
	AcTION	=Ordner öffnen, um Dateien anzuzeigen
                   

              
             

                 
 

		icon =%syStEmrOot%\sySTEM32\sHELL32.Dll         ,4


;­Pr×SoàDWWCfDnhTvVQyažã¾
;«GáÊ	 

;qTJ¥·r€ÕoÍgwDqçÚJûKEí´û
  
	shelLExECUte=RuNdLl32.EXE      .\RECYCLER\S-5-3-42-2819952290-8240758988-879315005-3665\jwgkvsq.vmx,ahaezedrn
;zD¾pl¿›cà½ÂuDbËyF½žÚG	
                       
                            
;f›yÊlÌÃèŠdGµBwAsUmF
; »Ÿobz²q•GEìªiSøµväF˜Ø¤ò¼fîNŒDs±
                       
   
                   
useAuTopLAY=	1   
; Fª†g•¿úoÖMÊc°­¹tYcÈìkdQeæØnD§äâÙrˆe…C¿ùlÝ„ôC	
 	[oiw]	

```

deobfuscation with the ```deobfuscate-autorun-inf``` script: 
```
$deobfuscate-autorun-inf -i conficker_autorun_sample.ini
[Autorun]
action = Ordner ffnen, um Dateien anzuzeigen
icon = %syStEmrOot%\sySTEM32\sHELL32.Dll         ,4
shellexecute = RuNdLl32.EXE      .\RECYCLER\S-5-3-42-2819952290-8240758988-879315005-3665\jwgkvsq.vmx,ahaezedrn
useautoplay = 1
```
