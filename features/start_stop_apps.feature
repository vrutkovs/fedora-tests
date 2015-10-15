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
        | app                   |
        | Accerciser            |
        | AisleRiot Solitaire   |
        | Anjuta                |
        | Archive Manager       |
        | Backups               |
        | Boxes                 |
        | Brasero               |
        | Calculator            |
        | Character Map         |
        | Cheese                |
        | Chess                 |
        | Clocks                |
        | Color Profile Viewer  |
        | Contacts              |
        | dconf Editor          |
        | Desktop Search        |
        | Devhelp               |
        | Dictionary            |
        | Disk Usage Analyzer   |
        | Disks                 |
        | Document Viewer       |
        | Documents             |
        | Empathy               |
        | Evolution             |
        | Files                 |
        | Firewall              |
        | Five or More          |
        | Font Viewer           |
        | Four-in-a-row         |
        | gedit                 |
        | GHex                  |
        | Help                  |
        | Iagno                 |
        | Image Viewer          |
        | Klotski               |
        | Lights Off            |
        | Logs                  |
        | Mahjongg              |
        | Main Menu             |
        | Maps                  |
        | Mines                 |
        | Music                 |
        | Nemiver               |
        | Network Connections   |
        | Nibbles               |
        | Notes                 |
        | Passwords and Keys    |
        | Photos                |
        | Quadrapassel          |
        | Remote Desktop Viewer |
        | Rhythmbox             |
        | Robots                |
        | Rygel Preferences     |
        | Screen Reader         |
        | Screenshot            |
        | Settings              |
        | Simple Scan           |
        | Sound Recorder        |
        | Sudoku                |
        | Swell Foop            |
        | System Monitor        |
        | Tali                  |
        | Terminal              |
        | Tetravex              |
        | Videos                |
        | Weather               |
        | Web                   |
# Moving those to bottom to get better screenshot, as those cannot be closed properly
        | Pitivi                |
        | Shotwell              |
        | Software              |
        | Transmission          |
        | XTerm                 |
        | Glade                 |
# Missing
#        | rxvt-unicode          |
# Disabled
#        | Fedora Release Notes   |
#        | GNOME System Monitor   |
#        | Problem Reporting      |
#        | SELinux Troubleshooter |
