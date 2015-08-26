#!/bin/sh

systemctl stop gdm

sudo -u test behave features/installed_tests.feature -f html -k -o /tmp/tests.html -f plain; rc=$?
rhts-submit-log -l /tmp/tests.html

journalctl -b --no-pager -o short-monotonic > /tmp/journal.log
rhts-submit-log -l /tmp/journal.log

abrt-cli ls > /tmp/abrt.log
rhts-submit-log -l /tmp/abrt.log

rpm -qa | sort > /tmp/packages.list
rhts-submit-log -l /tmp/packages.list

exit 0