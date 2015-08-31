#!/bin/sh

systemctl stop gdm

sudo -u test behave features/wayland_start_stop_apps.feature -f html -k -o /tmp/wayland_start_stop.html -f plain; rc=$?
rhts-submit-log -l /tmp/wayland_start_stop.html

systemctl stop gdm

journalctl -b --no-pager -o short-monotonic > /tmp/journal.log
rhts-submit-log -l /tmp/journal.log

abrt-cli ls > /tmp/abrt.log
rhts-submit-log -l /tmp/abrt.log

rpm -qa | sort > /tmp/packages.list
rhts-submit-log -l /tmp/packages.list

exit 0