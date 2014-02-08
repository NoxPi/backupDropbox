# backupDropbox.py
## Summary
This script backs up the Dropbox folder until it has finished syncing and then stops the Dropbox deamon. The intended use is to use a cron job to back up a Dropbox folder once every X.

For instance: I will use this script to back up my Dropbox folder once every 24 hours. The script will ensure that the Dropbox daemon doesn't run longer than neccessary.

Note: This is for Linux distributions.

## Installtion
1. Download and install dropbox: [See here for download link and instructions](https://www.dropbox.com/install?os=ln)
2. Download Dropbox's offical [CLI script] and install to PATH (Google it)
3. Use the Dropbox CLI to link your computer to your account
4. Use `dropbox exclude` to exlude the folders you don't want to back up
5. Set up a cron job running the script at your prefered interval.
6. Good to go

## Notes
The script is is just a personal project and is by on means a good one. I've just started using Python, so the coding standards and the way of coding it might be totally grotesque.

Use it at your own risk.
