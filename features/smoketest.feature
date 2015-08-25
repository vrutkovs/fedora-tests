Feature: GNOME Smoketest

  Background:
    * Make sure "basic-desktop-environment" package group is installed
    * Make sure "gnome" package group is installed

  @minimal_smoketest
  Scenario: Timed login
    * Set gdm options:
        | section | key              | value |
        | daemon  | TimedLogin       | test  |
        | daemon  | TimedLoginEnable | true  |
        | daemon  | TimedLoginDelay  | 10    |
        | debug   | Enable           | true  |
    * Start gdm service
    * Wait for process "gdm" to appear
    * Wait for process "gnome-session" to appear
    * Wait for "Entering running state" message in journalctl
    * Wait for GNOME Shell to startup
    * Make screenshot

  Scenario: Timed login - wayland disabled
    * Set gdm options:
        | section | key              | value |
        | daemon  | TimedLogin       | test  |
        | daemon  | TimedLoginEnable | true  |
        | daemon  | TimedLoginDelay  | 10    |
        | daemon  | WaylandEnable    | false |
        | debug   | Enable           | true  |
    * Start gdm service
    * Wait for process "gdm" to appear
    * Wait for process "gnome-session" to appear
    * Wait for "Entering running state" message in journalctl
    * Wait for GNOME Shell to startup
    * Make screenshot

  Scenario: Automatic login
    * Set gdm options:
        | section | key                  | value |
        | daemon  | AutomaticLogin       | test  |
        | daemon  | AutomaticLoginEnable | true  |
        | debug   | Enable               | true  |
    * Start gdm service
    * Wait for process "gdm" to appear
    * Wait for process "gnome-session" to appear
    * Wait for "Entering running state" message in journalctl
    * Wait for GNOME Shell to startup
    * Make screenshot
    * Touch "/smoketest_passed" file

  Scenario: Automatic login - wayland disabled
    * Set gdm options:
        | section | key                  | value |
        | daemon  | AutomaticLogin       | test  |
        | daemon  | AutomaticLoginEnable | true  |
        | daemon  | WaylandEnable        | false |
        | debug   | Enable               | true  |
    * Start gdm service
    * Wait for process "gdm" to appear
    * Wait for process "gnome-session" to appear
    * Wait for "Entering running state" message in journalctl
    * Wait for GNOME Shell to startup
    * Make screenshot

  Scenario: Gnome-classic
    * Set gdm options:
        | section | key                  | value |
        | daemon  | AutomaticLogin       | test  |
        | daemon  | AutomaticLoginEnable | true  |
        | debug   | Enable               | true  |
    * Set gdm to use "gnome-classic" session
    * Start gdm service
    * Wait for process "gdm" to appear
    * Wait for process "gnome-session" to appear
    * Wait for "Entering running state" message in journalctl
    * Wait for GNOME Shell to startup
    * Make screenshot

  Scenario: Gnome-wayland
    * Set gdm options:
        | section | key                  | value |
        | daemon  | AutomaticLogin       | test  |
        | daemon  | AutomaticLoginEnable | true  |
        | debug   | Enable               | true  |
    * Set gdm to use "gnome-wayland" session
    * Start gdm service
    * Wait for process "gdm" to appear
    * Wait for process "gnome-session" to appear
    * Wait for "Entering running state" message in journalctl
    * Wait for GNOME Shell to startup
    * Make screenshot
