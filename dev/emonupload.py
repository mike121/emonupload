#!/usr/bin/env python

# emonUpload

# By Glyn Hudson
# OpenEnergyMonitor.org
# GNU GPL V3

# $ pip install -r requirements.txt
# $ sudo apt-get install python-apt
from download_releases import debug, get_repos, update_download_releases, find_latest_version
from firmwareupload import serial_upload

import time, urllib, git, os, sys

#--------------------------------------------------------------------------------------------------
DEBUG = False
STARTUP_UPDATE = False
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
VERSION = 'V1.0.0'
download_folder = 'firmware/'
allowed_extensions = ['bin', 'hex']
repo_config_file = 'repos.conf'
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# Enable debug function
#--------------------------------------------------------------------------------------------------
if (DEBUG):
  print '\nDEBUG ENABLED\n'
  debug()
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# Check interent connectivity
#--------------------------------------------------------------------------------------------------
def interent_connected():
  try:
      stri = "https://api.github.com"
      data = urllib.urlopen(stri)
      print bcolors.OKGREEN + 'Internet connection detected' + bcolors.ENDC
      connected = True
  except:
      print bcolors.WARNING + 'CANNNOT CHECK FOR LATEST RELEASES: No internet connection detected\n' + bcolors.ENDC
      connected = False
  return connected
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# Update emonupload
#--------------------------------------------------------------------------------------------------
def update_emonupload(filename):
  print 'Checking for emonUpload updates...'
  dir_path=os.path.dirname(os.path.realpath(filename))
  if (DEBUG): print 'git abs path' + dir_path
  g = git.cmd.Git(dir_path)
  r = g.pull()
  if (DEBUG): print g
  if r != 'Already up-to-date.':
    print r
    print bcolors.WARNING + 'UPDATE FOUND....emonUpload RESTART REQUIRED\n' + bcolors.ENDC
    raw_input("\nPress Enter to continue...\n")
    os.execv(filename, sys.argv)
    sys.exit(0)
  else:
    print bcolors.OKGREEN + 'Already up-to-date.' + bcolors.ENDC
    raw_input("\nPress Enter to continue...\n")
  return r
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# Shutdown RasPi
#--------------------------------------------------------------------------------------------------
def shutdown_pi():
  cmd = 'sudo halt'
  subprocess.call(cmd, shell=True)
  sys.exit
#--------------------------------------------------------------------------------------------------

def invalid_selection():
  os.system('clear') # clear terminal screen Linux specific
  print bcolors.FAIL + '\nInvalid selection, please try again\n' + bcolors.ENDC
  return

def exit():
  sys.exit()

#--------------------------------------------------------------------------------------------------
# Find latest downloaded firmware release
#--------------------------------------------------------------------------------------------------
def find_latest_release(repo, download_folder):
  return
  

# Terminal colours
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#--------------------------------------------------------------------------------------------------


# STARTUP
os.system('clear') # clear terminal screen Linux specific

# get repo release info from GitHub for the repos listed in repo config file
repo = get_repos(repo_config_file)
number_repos = len(repo)
  
if (STARTUP_UPDATE):
  print 'Checking network connectivity...'
  if interent_connected():
    update_emonupload('emonupload.py')
    # update / download releaes for each repo and save to download folder
    update_download_releases(repo, number_repos, download_folder, allowed_extensions)
    
  

print '\n-------------------------------------------------------------------------------'

while(1):
  print '-------------------------------------------------------------------------------'
  now = time.strftime("%c")
  print bcolors.HEADER + bcolors.UNDERLINE + '\nemonUpload: ' + VERSION + bcolors.ENDC
  print 'Part of the OpenEnergyMonitor.org project'
  print 'Now: ' + time.strftime("%c") + '\n'
  
  print bcolors.UNDERLINE + '\nChoose from the following options:\n' + bcolors.ENDC
  
  print bcolors.OKBLUE + '\n1. Flash AVR Bootloader' + bcolors.ENDC
  
  print bcolors.OKBLUE + '\n2. Upload latest firmware via serial'
  for repo_index in range(number_repos):
      repo[repo_index] = repo[repo_index].rstrip('\n')
      print bcolors.WARNING + '   ' + str(chr(ord('a') + repo_index)) + '. ' + repo[repo_index] + bcolors.ENDC
  
  print bcolors.OKBLUE + '\n3. Upload specific firmware version' + bcolors.ENDC
  print bcolors.OKBLUE + '\n4. Perform unit test' + bcolors.ENDC
  print bcolors.OKBLUE + '\n5. Update firmware releases' + bcolors.ENDC
  print bcolors.OKBLUE + '\n6. Update emonUpload' + bcolors.ENDC
  print bcolors.OKBLUE + '\n7. Enable DEBUG output' + bcolors.ENDC
  print bcolors.OKBLUE + '\n8. Exit' + bcolors.ENDC
  print bcolors.OKBLUE + '\n9. Exit & Shutdown Pi' + bcolors.ENDC
  user_selection = raw_input('\n> ')
  if (DEBUG): print user_selection
  
  # Breakout user selection into first numberical (0-9) then second alpahumeric selection & error check
  first_selection = user_selection[:1]
  if len(user_selection) > 1:
    second_selection = user_selection[-1]
    # check to see if second selection is a character, if not error
    if second_selection.isalpha() == False:
      invalid_selection()
      if (DEBUG): print '2nd selection is not an str: '+ second_selection
  else:
    second_selection=False
   
  # check if first choose is integer if not error
  if first_selection.isdigit() == False:
    invalid_selection()
    if (DEBUG): print '1st selection is not an integer: '+ first_selection
  else:
    first_selection = int(first_selection)
  

  os.system('clear')
  
  if first_selection == 1:
    print bcolors.OKBLUE + '\n1. Flash AVR Bootloader' + bcolors.ENDC
     
  elif first_selection == 2:
    print bcolors.OKBLUE + '\n2. Upload latest firmware via serial'
    if second_selection != False:
      # convert alpha numberic selection to number e.g. a=0, b=2.
      index = ord(str(second_selection)) - 97
      print number_repos
      if index < number_repos:
        find_latest_version(repo[index], repo_config_file, download_folder)
      else: invalid_selection()
    else: invalid_selection()
  
  elif first_selection == 3:
    print bcolors.OKBLUE + '\n3. Upload specific firmware version' + bcolors.ENDC
    
  elif first_selection == 4:
    print bcolors.OKBLUE + '\n4. Perform unit test' + bcolors.ENDC
  
  elif first_selection == 5:
    print bcolors.OKBLUE + '\n5. Update firmware releases' + bcolors.ENDC
    if interent_connected():
      repo = get_repos(repo_config_file)
      number_repos = len(repo)
      update_download_releases(repo, number_repos, download_folder, allowed_extensions)
    
  elif first_selection == 6:
    print bcolors.OKBLUE + '\n6. Update emonUpload' + bcolors.ENDC
    if interent_connected():
      update_emonupload('emonupload.py')

    
  elif first_selection == 7:
    print bcolors.OKBLUE + '\n7. Enable DEBUG output' + bcolors.ENDC
    DEBUG = True
    debug()
    print 'Debug output enabled.'
    raw_input("\nPress Enter to continue...\n")
  
  elif first_selection == 8:
    print bcolors.OKBLUE + '\n8. Exit' + bcolors.ENDC
    exit()
  elif first_selection == 9:
    print bcolors.OKBLUE + '\n9. Exit & Shutdown Pi' + bcolors.ENDC
    shutdown_pi()
  else:
     invalid_selection()
  


print '\n-------------------------------------------------------------------------------'
print bcolors.WARNING + '\nDONE.\n' + bcolors.ENDC

