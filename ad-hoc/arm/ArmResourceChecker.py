"""
Check that any scanned ARM file describes resources from a whitelist
Command line parameters:
--conf, -c <path-to-whitelist-file>
--dir, -d <path-to-ARM-files>
--file, -f <path-to-single-ARM-file>
-h (help)
"""
import getopt
import glob
import json
import os
import sys

"""
Load ARM files as json and inspect their resource element.
If all resources are within a given whitelist, exit with success (0)
Else exit with failure (1)
"""
def scan_arm_files(config: str, files: list) -> None:
    # Load whitelist 
    with open(config, 'r') as cfg:
        whitelist = tuple(cfg.read().splitlines())

    passing = True
    # Scan all files
    for f in files:
        with open(f, 'r') as cfile:
            template = json.load(cfile)

        if template and 'resources' in template:
            print(f"[INFO] Checking {f}")
            for r in template['resources']:
                rtype = r['type']
                if rtype.startswith(whitelist):
                    print(f"[PASS] {f}: {rtype}")
                else:
                    print(f"[FAIL] {f}: {rtype}")
                    passing = False
        else:
            print(f"[INFO] Not processing {f}")

    if not passing:
        print("Unapproved resources found.")
        sys.exit(1)
    else:
        print("Successfully scanned for unapproved resources.")

if __name__ == "__main__":
    files = []
    config = ""
    opts, args = getopt.getopt(sys.argv[1:],"hc:f:d:",["conf=","file=","dir="])
    for opt, arg in opts:
        if opt == '-h':
            print('python3 ArmResourceChecker.py [-h] <-c <config-file> -d <directory> | -f <file>>')
            sys.exit(0)

        if opt in ('-c', '--conf'):
            config = os.path.join(arg)

        if opt in ('-f', '--file'):
            files.append(os.path.join(arg))
        elif opt in ('-d', '--dir'):
            json_files = glob.glob(os.path.join(arg,'*.json'))
            for f in json_files:
                files.append(f)
    
    if len(files) == 0:
        print("No ARM files supplied to scan")
        sys.exit(1)
    
    if len(config) < 1:
        print(f"Please supply a configuration (whitelist) file.")
        sys.exit(1)

    scan_arm_files(config, files)