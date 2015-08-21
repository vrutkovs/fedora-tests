Feature: GNOME Smoketest

  Background:
    * Make sure "gnome" package group is installed

  Scenario: Automatic login
    * Set gdm options:
        | section | key                  | value |
        | daemon  | AutomaticLogin       | true  |
        | daemon  | AutomaticLoginEnable | test  |
        | debug   | Enable               | true  |
    * Start gdm service
    * Wait for process "gdm" to appear
    * Wait for process "gnome-session" to appear
    * Wait for "GNOME Shell started at" message in journalctl
