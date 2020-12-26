# Baackup
That's right, with double a. It's a backup tool written in Django framework to automate the procedure of collecting all the required backup locations from local or remote (ssh) machines.

## Installation
The installation is very simple.
All that is needed is a linux machine with support for SystemD.
How else could it run as a service? :smirk:

Just type this on a terminal with a user that has super user privileges. The installation will take care of all dependencies that are needed and will update it if needed:
```bash
bash <(curl -s "https://raw.githubusercontent.com/bkbilly/AlarmPI/master/install.sh")
```

## Final Thoughts
With so many Backup applications out there, my application might seem obsolete Either way I could never resist on making an app on my own and to try new technologies. I haven't even checked if the features this application are already implemented on similar applications, but who cares... :stuck_out_tongue_winking_eye:

If only these features existed on the Baackup app, oh wait... They do exist! Check them out:

:heavy_check_mark: Easily install and upgrade.<br />
:heavy_check_mark: Support remote SSH servers.<br />
:heavy_check_mark: Exclude files or directories using glob-style patterns.<br />
:heavy_check_mark: AES encryption of each backup.<br />
:heavy_check_mark: Decrypt and zip files for download.<br />
:heavy_check_mark: Instantly check if the desired folder exists.<br />
:grey_question: Automatic backups are only possible through a 3rd party call like a Cron Job. This might help: ```curl --data "password=asdf" http://127.0.0.1:8000/start_backup```<br />
:x: Has a complete view of all files that have been backed up. Only the total size and the size of each backup location is displayed.<br />
:x: Problems if the debug setting is set to False.<br />
