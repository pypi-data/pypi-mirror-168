"""
The command-line interface for assDialogueMerger
"""
import os
import glob
import argparse
from .assdialoguemerger import DialogueMerger, InputCountException


def main():
    """ Main Function """
    parser = argparse.ArgumentParser()
    parser.add_argument('-bf', '--base-folder', required=True,
                        help='Directory path containing the base subtitle files')
    parser.add_argument('-df', '--dialogue-folder', required=True,
                        help='Directory path containing the dialogue subtitle files')
    parser.add_argument('-nl', '--no-logs', default=False, action="store_true",
                        help='Disable writing dialogue overwrites to log files')
    # parser.add_argument('-o', '--output', required = True,
    #                     help='''Output format string. %F0 = filename of 1st given input file,
    # 			        %I2+1 = index of file in directory with minimum of 2 digits and offset +1''')
    args = parser.parse_args()

    if args.base_folder and not os.path.isdir(args.base_folder):
        raise argparse.ArgumentTypeError(
            "--base-folder must be a valid directory")
    if args.dialogue_folder and not os.path.isdir(args.dialogue_folder):
        raise argparse.ArgumentTypeError(
            "--dialogue-folder must be a valid directory")

    base_files = glob.glob(f"{args.base_folder}{os.path.sep}*.ass")
    dialogue_files = glob.glob(f"{args.dialogue_folder}{os.path.sep}*.ass")

    base_file_count = len(base_files)
    dialogue_file_count = len(dialogue_files)
    if base_file_count != dialogue_file_count:
        raise InputCountException(base_file_count, dialogue_file_count)

    dialogue_merger = DialogueMerger(not args.no_logs)
    print()
    for i, (base_file, dialogue_file) in enumerate(zip(base_files, dialogue_files)):
        dialogue_merger.merge(base_file, dialogue_file,
                              f"{str(i+1).zfill(2)}.ass")


if __name__ == "__main__":
    main()
