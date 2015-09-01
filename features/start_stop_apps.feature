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
        | Glade                 |
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
        | Pitivi                |
        | Quadrapassel          |
        | Remote Desktop Viewer |
        | Rhythmbox             |
        | Robots                |
        | rxvt-unicode          |
        | Rygel Preferences     |
        | Screen Reader         |
        | Screenshot            |
        | Settings              |
        | Shotwell              |
        | Simple Scan           |
        | Software              |
        | Sound Recorder        |
        | Sudoku                |
        | Swell Foop            |
        | System Monitor        |
        | Tali                  |
        | Terminal              |
        | Tetravex              |
        | Transmission          |
        | Videos                |
        | Weather               |
        | Web                   |
        | XTerm                 |
# Disabled
#        | Fedora Release Notes   |
#        | GNOME System Monitor   |
#        | Problem Reporting      |
#        | SELinux Troubleshooter |
