@requires_smoketest
Feature: GNOME Initial Tests

    Background:
        * Make sure "basic-desktop-environment" package group is installed
        * Make sure "gnome" package group is installed
        * Start gdm for "test" user and "gnome" session

    @stop_gdm
    Scenario Outline: Package installed tests
        * Run installed tests for "<component>" from "<package>"

    Examples:
        | component             | package                     |
#        | appstream-glib        | libappstream-glib-tests     |
        | clutter               | clutter-tests               |
        | cogl                  | cogl-tests                  |
        | eog                   | eog-tests                   |
        | evolution-data-server | evolution-data-server-tests |
        | evolution             | evolution-tests             |
#        | folks                 | folks-tests                 |
#        | gdk-pixbuf            | gdk-pixbuf-tests            |
        | gjs                   | gjs-tests                   |
        | glib-networking       | glib-networking-tests       |
#        | glib                  | glib2-tests                 |
#        | gnome-calculator      | gnome-calculator-tests      |
        | gnome-desktop         | gnome-desktop3-tests        |
#        | gnome-software        | gnome-software-tests        |
        | gtk+                  | gtk3-tests                  |
        | gtksourceview         | gtksourceview3-tests        |
        | gvfs                  | gvfs-tests                  |
        | json-glib             | json-glib-tests             |
        | libmediaart           | libmediaart-tests           |
        | mutter                | mutter-tests                |
        | org.gnome.Weather     | gnome-weather-tests         |
#        | ostree                | ostree-tests                |
#        | Photos                | gnome-photos-tests          |