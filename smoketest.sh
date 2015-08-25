#!/bin/sh

systemctl stop gdm

sudo -u test behave -t minimal_smoketest -f html -k -o /tmp/minimal_smoketest.html -f plain; rc=$?
rhts-submit-log -l /tmp/minimal_smoketest.html

sudo -u test behave features/smoketest.feature -t ~minimal_smoketest -f html -k -o /tmp/full_smoketest.html -f plain
rhts-submit-log -l /tmp/full_smoketest.html

journalctl -b --no-pager -o short-monotonic > /tmp/journal.log
rhts-submit-log -l /tmp/journal.log

abrt-cli ls > /tmp/abrt.log
rhts-submit-log -l /tmp/abrt.log

rpm -qa | sort > /tmp/packages.list
rhts-submit-log -l /tmp/packages.list

exit $rc