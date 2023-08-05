# ASSDialogueMerger
Program to merge the dialogue of one subtitle into the timings of another.

This tool merges the translations from one subtitle into the timings of another, ignoring non-dialogue lines such as signs & songs.
An example is to merge the translations from one fansub group with the timings (and remaining non-dialogue lines) of another group.

The script works by first iterating through all lines and detecting lines that have to be removed from the base subtitle file (the one with the correct timings) and lines that have to be copied over from the dialogue subtitle file (the one with the better dialogue/translations). These lines are logged in the console output, the script user will have to manually re-time the copied-over lines after the script has completely finished. 

Next, all changes are applied and the number of dialogue lines should match perfectly. Then the text is simply copied over from the dialogue subtitle into the base subtitle. Much like Paste From Pad from [Myaamori's Script Collection](https://github.com/TypesettingTools/Myaamori-Aegisub-Scripts). In addition, the style tag is copied over too in case the dialogue subtitle used an default-alt style where the base subtitle did not.

## Dependencies
- [Python 3.9 or higher](https://www.python.org/downloads/)
- [Python ass](https://pypi.org/project/ass/)

## Usage
```console
$ assdialoguemerger --help
usage: assdialoguemerger [-h] -bf BASE_FOLDER -df DIALOGUE_FOLDER [-nl]

optional arguments:
  -h, --help            show this help message and exit
  -bf BASE_FOLDER, --base-folder BASE_FOLDER
                        Directory path containing the base subtitle files
  -df DIALOGUE_FOLDER, --dialogue-folder DIALOGUE_FOLDER
                        Directory path containing the dialogue subtitle files
  -nl, --no-logs        Disable writing dialogue overwrites to log files
```

## Roadmap
- Verbose logging mode, disabling text logs by default.
- Allow for custom regex for style matching / recognizing the dialogue style.
- (Possibly) generate difference view (much like diffchecker.com) instead of text log.
- Copy over other fields such as actor.
- Customizable output filenames.
