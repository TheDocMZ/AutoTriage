import os, argparse, subprocess, requests, colorama
from colorama import Fore

colorama.init()

RR_DEFAULT = "C:\\Tools\\RegRipper\\"
EZ_DEFAULT = "C:\\Tools\\ZimmermanTools\\net6\\"
LENGTH = 70

# Border print function
def printBorder():
    print(Fore.BLUE + "-" * LENGTH)


# Title printing function for tool info
def printTitle(str1, str2):
    printBorder()
    printstr1 = str1.center(LENGTH)
    print(Fore.MAGENTA + printstr1)

    printstr2 = str2.center(LENGTH)
    print(Fore.MAGENTA + printstr2)
    printBorder()


# Checks if the specified directory or file exists. If the directory is a destination directory, provides the option to create it.
def checkPath(path, type, dst):
    pathVar = path
    pathexists = False
    firstCheck = True
    while not pathexists:
        if type == 'f':
            pathexists = os.path.isfile(pathVar)
        elif type == 'd':
            pathexists = os.path.isdir(pathVar)
        if not pathexists and not dst:    
            firstCheck = False
            print(Fore.RED + "[X] Error: {} does not exist. Check path and try again".format(pathVar))
            pathVar = input(Fore.CYAN + "Enter the specified path: ")
        elif not pathexists and dst:
            firstCheck = False
            choice = False
            create = input(Fore.YELLOW + "[!] Directory does not exist! Would you like to create \'{}\' ? Y/N: ".format(pathVar))
            while not choice:
                if create.lower() == 'y':
                    choice = True
                    os.mkdir(pathVar)
                    print(Fore.GREEN + "[✓] Directory created! {}".format(pathVar))
                    return pathVar
                elif create.lower() == 'n':
                    choice = True
                    pathVar = input(Fore.CYAN + "Enter the specified path: ")
                else:
                    create = input(Fore.RED + "[X] Invalid input! Y/N: ")
    if not firstCheck:
        printBorder()
    return pathVar


# Install zip files containing tools
def installTool(url, dst):
    x = requests.get(url)
    with open(dst, 'wb') as f:
	    f.write(x.content)
    if os.path.isfile(dst):
        print(Fore.GREEN + "[✓] Success!")
    else:
        print(Fore.RED + "[X] Download Failed!")
        

# Check if tools are installed in the default locations
def checkTools(rr, rrPath, ez, ezPath):

    # if rr == True, checks if RegRipper is installed at the specified path
    if rr:
        print(Fore.CYAN + "[?] Checking RegRipper...")
        if not os.path.isfile(rrPath + "rip.exe"):
            choice = False
            install = input( Fore.YELLOW + "[!] RegRipper not found. Would you like to install? Y/N: ")
            while not choice:
                if install.lower() == 'y':
                    choice = True
                    print(Fore.CYAN + "[%] Installing RegRipper...")
                    installTool("https://github.com/keydet89/RegRipper3.0/archive/refs/heads/master.zip", "C:\\Tools\\RegRipper.zip")
                elif install.lower() == 'n':
                    choice = True
                    print(Fore.RED + "[X] RegRipper not installed. Unable to proceed.")
                    exit()
                else:
                    install = input(Fore.RED + "[X] Invalid input! Y/N ")
        else:
            print(Fore.GREEN + "[✓] Installed!\n")

    # If ez == True, checks if EZ tools are installed at the specified path
    if ez:
        print(Fore.CYAN + "[?] Checking EZ Tools...")
        tools = ["MFTECmd.exe", "AppCompatCacheParser.exe", "AmcacheParser.exe", "PECmd.exe", "EvtxECmd\\EvtxECmd.exe"]
        exist = True
        for tool in tools:
            if not os.path.isfile(ezPath + tool):
               exist = False
               break
        if not exist:
            choice = False
            install = input(Fore.YELLOW + "[!] EZ Tools not found. Would you like to install? Y/N: ")
            while not choice:
                if install.lower() == 'y':
                    print(Fore.CYAN + "[%] Installing EZ Tools...")
                    installTool("https://f001.backblazeb2.com/file/EricZimmermanTools/Get-ZimmermanTools.zip", "C:\\Tools\\Get-ZimmermanTools.zip")
                elif install.lower() == 'n':
                        choice = True
                        print(Fore.RED + "[X] RegRipper not installed. Unable to proceed.")
                        exit()
                else:
                    install = input(Fore.RED + "[X] Invalid input! Y/N ")
        elif exist:
            print(Fore.GREEN + "[✓] Installed!\n")


#  Execute the command line tool
def callExe(exe, name, arg1, src, arg2, dest, verbose):
    print(Fore.CYAN + "[*] Executing: {} on \'{}\'".format(name, src))
    callstr = exe + name + arg1 + src + arg2 + dest
    try:
        if verbose:
            subprocess.call(["cmd", "/c", callstr])
        elif not verbose:
            subprocess.call(["cmd", "/c", callstr], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except:
        print(Fore.RED + "[X] Error! {} is unable to execute. Check path and try again".format(exe))
        return()

    print(Fore.GREEN + "[✓] Complete! Results stored in \'{}\'\n".format(dest))


# Run Regripper on all registry hives 
def runRegRipper(defaults, verbose, case):
    printTitle("RegRipper3.0", "(https://github.com/keydet89/RegRipper3.0)")
    defaultsrc = "C:\\Cases\\" + case + "\\E\\"
    defaultdst = "C:\\Cases\\" + case + "\\Analysis\\Registry\\"

    if defaults:
        RegRipper = RR_DEFAULT
        src = defaultsrc
        dst = defaultdst
    else:
        RegRipper = input(Fore.CYAN + "Enter RegRipper location or blank for default ({}): ".format(RR_DEFAULT))
        src = input(Fore.CYAN + "Enter directory for source data or blank for default ({}): ".format(defaultsrc))
        dst = input(Fore.CYAN + "Enter directory for results destination or blank for default ({}): ".format(defaultdst))
        printBorder()
        if RegRipper == '':
             RegRipper = RR_DEFAULT
        if src == '':
             src = defaultsrc
        if dst == '':
             dst = defaultdst
 
    checkTools(True, RegRipper, False, None)
    src = checkPath(src,'d', False)
    dst = checkPath(dst, 'd', True)
    
    # Run rip.exe on the registry hives SAM, DEFAULT, SECURITY, SOFTWARE, and SYSTEM located in Windows\System32\config storing results in txt files
    hives = ["SAM", "DEFAULT", "SECURITY", "SOFTWARE", "SYSTEM"]
    for hive in hives:
        callExe(RegRipper, "rip.exe", " -r ", src + "Windows\\System32\\config\\" + hive, " -a > ", dst + hive + ".txt", verbose)
    
    # Checks if the Users directory exists at the specified path
    users = ""
    pathexists = False
    while not pathexists:
        pathexists = os.path.isdir(src + "Users\\")
        if not pathexists:    
            print(Fore.RED + "[X] Error: {} does not exist. Please check path and try again".format(users))

    # Creates a list of users within the specified directory and run rip.exe on each users NTUSER.dat and UsrClass.dat registry hives storing results in txt files
    users = os.listdir( src + "Users\\")
    for user in users:
        if not os.path.isdir(dst + user):
                os.mkdir(dst + user)
                print(Fore.GREEN + "[✓] Created directory {}".format(dst + user))
        callExe(RegRipper, "rip.exe", " -r ", src + "Users\\" + user + "\\NTUSER.dat", " -a > ", dst + user + "\\NTUSER.dat" + ".txt", verbose)
        callExe(RegRipper, "rip.exe", " -r ", src + "Users\\" + user + "\\AppData\\Local\\Microsoft\\Windows\\UsrClass.dat", " -a > ", dst + user + "\\UsrClass.dat" + ".txt", verbose,)


# Runs several EZ Tools
def runEZTools(defaults, verbose, case):
    printTitle("Eric Zimmerman Tools" , "(https://github.com/EricZimmerman)")
    defaultsrc = "C:\\Cases\\" + case + "\\E\\"
    defaultdst = "C:\\Cases\\" + case + "\\Analysis\\"
    
    if defaults:
        EZTools = EZ_DEFAULT
        src = defaultsrc
        dst = defaultdst
    else:
        EZTools = input(Fore.CYAN + "Enter EZ Tools location or blank for default ({}): ".format(EZ_DEFAULT))
        src = input(Fore.CYAN + "Enter directory for source data or blank for default ({}): ".format(defaultsrc))
        dst = input(Fore.CYAN + "Enter directory for results destination or blank for default ({}): ".format(defaultdst))
        printBorder()
        if EZTools == "":
             EZTools = EZ_DEFAULT
        if src == "":
             src = defaultsrc
        if dst == "":
             dst = defaultdst

    checkTools(False, None, True, EZTools)
    src = checkPath(src,'d', False)
    dst = checkPath(dst, 'd', True)

    # Runs the respective EZ Tools MFTEcmd.exe, AppCompatCacheParser.exe, AmcacheParser.exe, PECmd.exe, and EvtxECmd.exe to extract MFT, Shimcache, Amcache, Prefetch, and Event Log data as csv output files
    callExe(EZTools, "MFTECmd.exe", " -f ", src +"$Extend\\$J -m " + src + "$MFT", " --csv ", dst + "NTFS", verbose)
    callExe(EZTools, "AppCompatCacheParser.exe", " -f ", src + "Windows\\System32\\config\\SYSTEM", " --csv ", dst + "Execution\\Shimcache", verbose)
    callExe(EZTools, "AmcacheParser.exe", " -f ", src + "Windows\\AppCompat\\Programs\\Amcache.hve", " --csv ", dst + "Execution\\Amcache", verbose)
    callExe(EZTools, "PECmd.exe", " -d ", src + "Windows\\prefetch", " --csv ", dst + "Execution\\Prefetch", verbose)
    callExe(EZTools + "EvtxECmd\\", "EvtxECmd.exe", " -d ", src + "Windows\\System32\\winevt\\logs", " --csv ", dst + "EventLogs", verbose)


def main():
    # parser arguments
    # Usage: AutoTriage.py -r [regripper | eztools | all] [-y] [-v]
    parser = argparse.ArgumentParser(description='AutoTriage.py Triage Automation Script - TheDocMZ (https://github.com/TheDocMZ/AutoTriage)')
    parser.add_argument('-r', '--run', choices=['regripper', 'eztools', 'all'], help='Identify which tools to run: RegRipper, EZ Tools, or all', action='store', required=True)
    parser.add_argument('-y', '--yes', help='Accept default directories', default=False, action='store_true', required=False)
    parser.add_argument('-v', '--verbose', help='Verbose output', default=False, action='store_true', required=False)
    args = parser.parse_args()

    # Input case number used for default directory structure
    case = input(Fore.CYAN + "Enter case number: ")

    if args.run == 'regripper':
        runRegRipper(args.yes, args.verbose, case)
    elif args.run == 'eztools':
        runEZTools(args.yes,args.verbose, case)
    elif args.run == 'all':
        runRegRipper(args.yes, args.verbose, case)
        runEZTools(args.yes, args.verbose, case)

main()
