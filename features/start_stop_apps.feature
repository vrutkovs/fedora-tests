@requires_smoketest
Feature: GNOME Application start stop tests

    Background:
        * Make sure "basic-desktop-environment" package group is installed
        * Make sure "gnome" package group is installed
        * Start gdm for "test" user and "gnome" session

    Scenario Outline: Start-stop application
        * Start "<app>" application

    Examples:
        | app                     |
        | Adobe Flash Player      |
        | Archive Manager         |
        | Boxes                   |
        | Builder                 |
        | Calculator              |
        | Calendar                |
        | California              |
        | Character Map           |
        | Cheese                  |
        | Clocks                  |
        | Color Profile Viewer    |
        | Contacts                |
        | D-Feet                  |
        | dconf Editor            |
        | DevAssistant            |
        | Devhelp                 |
        | Disk Usage Analyzer     |
        | Disks                   |
        | Document Viewer         |
        | Documents               |
        | EasyTAG                 |
        | Empathy                 |
        | Evolution               |
        | Files                   |
        | Firefox                 |
        | Font Viewer             |
        | Geary                   |
        | gedit                   |
        | gitg                    |
        | GNOME Build Tool        |
        | GNOME System Monitor    |
        | Image Viewer            |
        | LibreOffice Calc        |
        | LibreOffice Draw        |
        | LibreOffice Impress     |
        | LibreOffice Writer      |
        | Maps                    |
        | Music                   |
        | Network Connections     |
        | Notes                   |
        | Passwords and Keys      |
        | Polari                  |
        | Power Statistics        |
        | Problem Reporting       |
        | Remote Desktop Viewer   |
        | Rhythmbox               |
        | Rygel Preferences       |
        | Screen Reader           |
        | Screenshot              |
        | SELinux Troubleshooter  |
        | Settings                |
        | Shotwell                |
        | Shutter                 |
        | Skype                   |
        | Software                |
        | Sound Converter         |
        | Sublime Text 3          |
        | System Monitor          |
        | Telegram Desktop        |
        | Telegram                |
        | Terminal                |
        | Transmission            |
        | Tweak Tool              |
        | Videos                  |
        | Virtual Machine Manager |
        | Weather                 |
        | Web                     |
        | Help                    |