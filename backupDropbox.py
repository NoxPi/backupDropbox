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

def check_env():
    try:
        out = subprocess.Popen(["which", "dropbox"], stdout=subprocess.PIPE)
    except Exception:
        raise Exception("The \"which\" command didn't work")

    if not out.stdout.read():
        raise Exception("Can't find \"dropbox\" command in path")

def run_command(command):
    try:
        output = subprocess.Popen(command.split(), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        return output.stdout.read().strip()
    except Exception, e:
        handle_error(Exception, e)

def main():
    subprocess.call("clear")

    try:
        check_env()
    except Exception, e:
        handle_error(Exception, e)

    # Start dropboxd
    print "Attempting to start dropboxd"
    try:
        subprocess.call("dropbox start".split())
    except Exception, e:
        handle_error(Exception, "Couldn't run the \"dropbox\" command")

    # Ensure that dropbox is running
    running = False
    timeout = 10
    while not running:
        if run_command("dropbox status") != "Dropbox isn't running!":
            running = True
        elif timeout == 0:
            handle_error(Exception, "Couldn't start dropboxd")
        else:
            sys.stdout.write(".")
            sys.stdout.flush()
            timeout -= 1
            time.sleep(1)

    # Check status
    #subprocess.call(["dropbox", "status"])

    # Stop dropboxd
    subprocess.call(["dropbox", "stop"])
    #subprocess.call(["dropbox", "status"])

    print "At end"
    exit()

if __name__ == "__main__":
    main()

