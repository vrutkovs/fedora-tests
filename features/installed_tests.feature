@requires_smoketest
Feature: GNOME Initial Tests

    Background:
        * Make sure "basic-desktop-environment" package group is installed
        * Make sure "gnome" package group is installed
        * Start gdm for "test" user and "gnome" session

    Scenario Outline: Package installed tests
        * Run installed tests for "<component>" from "<package>"

    Examples:
        | component | package     |
        | glib      | glib2-tests |
