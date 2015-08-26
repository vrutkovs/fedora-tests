@requires_smoketest
Feature: GNOME Application start stop tests

    Background:
        * Make sure "basic-desktop-environment" package group is installed
        * Make sure "gnome" package group is installed
        * Start gdm for "test" user and "gnome" session

    Scenario Outline: Start-stop application
        * Start "<app>" application
        * Stop "<app>" application

    Examples:
        | app                |
        | org.gnome.Nautilus |