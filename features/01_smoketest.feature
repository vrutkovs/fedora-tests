Feature: GNOME Smoketest

  Background:
    * Make sure "basic-desktop-environment" package group is installed
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
    * Wait for "Entering running state" message in journalctl
    * Wait for "GNOME Shell started at .*" message in journalctl
    * Touch "/smoketest_passed" file

  Scenario: Automatic login - wayland disabled
    * Set gdm options:
        | section | key                  | value |
        | daemon  | AutomaticLogin       | true  |
        | daemon  | AutomaticLoginEnable | test  |
        | daemon  | WaylandEnable        | false |
        | debug   | Enable               | true  |
    * Start gdm service
    * Wait for process "gdm" to appear
    * Wait for process "gnome-session" to appear
    * Wait for "Entering running state" message in journalctl
    * Wait for "GNOME Shell started at .*" message in journalctl

  Scenario: Timed login
    * Set gdm options:
        | section | key              | value |
        | daemon  | TimedLogin       | true  |
        | daemon  | TimedLoginEnable | test  |
        | daemon  | TimedLoginDelay  | 10    |
        | debug   | Enable           | true  |
    * Start gdm service
    * Wait for process "gdm" to appear
    * Wait for process "gnome-session" to appear
    * Wait for "Entering running state" message in journalctl
    * Wait for "GNOME Shell started at .*" message in journalctl

  Scenario: Timed login - wayland disabled
    * Set gdm options:
        | section | key              | value |
        | daemon  | TimedLogin       | true  |
        | daemon  | TimedLoginEnable | test  |
        | daemon  | TimedLoginDelay  | 10    |
        | daemon  | WaylandEnable    | false |
        | debug   | Enable           | true  |
    * Start gdm service
    * Wait for process "gdm" to appear
    * Wait for process "gnome-session" to appear
    * Wait for "Entering running state" message in journalctl
    * Wait for "GNOME Shell started at .*" message in journalctl

  Scenario: Gnome-classic
    * Set gdm options:
        | section | key                  | value |
        | daemon  | AutomaticLogin       | true  |
        | daemon  | AutomaticLoginEnable | test  |
        | debug   | Enable               | true  |
    * Set gdm to use "gnome-classic" session
    * Start gdm service
    * Wait for process "gdm" to appear
    * Wait for process "gnome-session" to appear
    * Wait for "Entering running state" message in journalctl
    * Wait for "GNOME Shell started at .*" message in journalctl

  Scenario: Gnome-wayland
    * Set gdm options:
        | section | key                  | value |
        | daemon  | AutomaticLogin       | true  |
        | daemon  | AutomaticLoginEnable | test  |
        | debug   | Enable               | true  |
    * Set gdm to use "gnome-wayland" session
    * Start gdm service
    * Wait for process "gdm" to appear
    * Wait for process "gnome-session" to appear
    * Wait for "Entering running state" message in journalctl
    * Wait for "GNOME Shell started at .*" message in journalctl
