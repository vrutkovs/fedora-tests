@requires_smoketest
Feature: GNOME Application start stop tests

    @setup
    Scenario: Make sure gnome-shell is started
        * Make sure "basic-desktop-environment" package group is installed
        * Make sure "gnome" package group is installed
        * Make sure misc gnome packages are installed
        * Start gdm for "test" user and "gnome" session

    Scenario Outline: Start-stop application
        * Start "<app>" application

    Examples:
        | app                    |
        | AisleRiot Solitaire    |
        | Archive Manager        |
        | Backups                |
        | Boxes                  |
        | Brasero                |
        | Calculator             |
        | Character Map          |
        | Cheese                 |
        | Clocks                 |
        | Color Profile Viewer   |
        | Contacts               |
        | Dictionary             |
        | Disk Usage Analyzer    |
        | Disks                  |
        | Document Viewer        |
        | Documents              |
        | Empathy                |
        | Evolution              |
        | Files                  |
        | Firewall               |
        | Font Viewer            |
        | gedit                  |
        | Help                   |
        | Image Viewer           |
        | Logs                   |
        | Maps                   |
        | Network Connections    |
        | Notes                  |
        | Passwords and Keys     |
        | Remote Desktop Viewer  |
        | Rhythmbox              |
        | rxvt-unicode           |
        | Rygel Preferences      |
        | Screen Reader          |
        | Screenshot             |
        | Settings               |
        | Shotwell               |
        | Simple Scan            |
        | Software               |
        | Sound Recorder         |
        | System Monitor         |
        | Terminal               |
        | Transmission           |
        | Videos                 |
        | Weather                |
        | XTerm                  |
# Disabled
# Requires a server
#        | Emacs                  |
#        | Emacs Client           |
# doesn't start
#        | Fedora Release Notes   |
#        | GNOME System Monitor   |
#        | Problem Reporting      |
#        | SELinux Troubleshooter |