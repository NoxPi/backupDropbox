#! /usr/bin/env python
import subprocess
import os
import time
import syslog
import sys

def write_to_log(priority, message):
    if priority == "info":
        syslog.syslog(syslog.LOG_INFO, message)
    elif priority == "error":
        syslog.syslog(syslog.LOG_ERR, message)

def handle_error(Exception, e):
    write_to_log("error", e)
    print "\n" + e
    print "Exiting..."
    exit()

def to_number(input):
    try:
        return int(input)
    except ValueError:
        return False

def log_info(message):
    write_to_log("info", message)
    return message

def check_env():
    try:
        out = subprocess.Popen(["which", "dropbox"], stdout=subprocess.PIPE)
    except Exception:
        raise Exception("The \"which\" command didn't work")

    if not out.stdout.read():
        raise Exception("Can't find \"dropbox\" command in path")

def run_command(command):
    try:
        output = subprocess.Popen(command.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return output.stdout.read().strip()
    except Exception, e:
        handle_error(Exception, e)

def main():
    log_info("Syncing started")
    try:
        check_env()
    except Exception, e:
        handle_error(Exception, e)

    # Start dropboxd
    print "Attempting to start dropboxd"
    try:
        if not subprocess.call("dropbox running".split()):
            subprocess.call("dropbox start".split())
    except Exception, e:
        handle_error(Exception, "Couldn't run the \"dropbox\" command")

    # Ensure that dropbox is running
    timeout = 10
    while not subprocess.call("dropbox running".split()):
        if timeout == 0:
            handle_error(Exception, "Couldn't start dropboxd")
        else:
            sys.stdout.write(".")
            sys.stdout.flush()
            timeout -= 1
            time.sleep(1)

    # Check status
    print "Sync status:\n"
    print "Initializing..."

    timeout = 60
    downloaded = False
    files = 0

    while True:
        status = run_command("dropbox status")
        if downloaded and status.lower() == "up to date":
            if to_number(files):
                print log_info("Done syncing. " + files + " files synced up")
            else:
                print log_info("Done syncing. " + files + " synced up")

            break
        elif timeout == 0:
            print log_info("Nothing to sync. Everything up to date")
            break
        elif status == "Up to date":
            print status
            timeout -= 1
            time.sleep(1)
        else:
            if ("downloading" in status.lower().split() and
                "downloading file list..." not in status.lower()):
                downloaded = True
                if files < status.split()[1]:
                    files = status.split()[1].replace("(", "")

            print status
            time.sleep(1)

    # Stop dropboxd
    subprocess.call(["dropbox", "stop"])
    print "Finished"
    exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if subprocess.call("dropbox running".split()):
            print "\n"
            subprocess.call(["dropbox", "stop"])
            handle_error(KeyboardInterrupt, "The script was interrupted by user")
        sys.exit(1)

