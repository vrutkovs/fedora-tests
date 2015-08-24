#!/bin/sh

echo ">> Updating the system"
dnf update -y

echo ">> Enabling passwordless sudo"
sed -i s/#\ %wheel/%wheel/g /etc/sudoers

echo ">> Adding a new test user"
useradd test
echo "redhat" | passwd test --stdin
usermod -aG wheel test

echo ">> Installing test requirements"
dnf install -y python-behave gnome-desktop-testing

echo ">> Enable abrt autoreporting"
dnf install -y abrt abrt-addon*
abrt-auto-reporting enabled
abrt-install-ccpp-hook install

echo ">> Enable abrt FAF reporting"
sed -i 's/# URL/URL/' /etc/libreport/plugins/ureport.conf
sed -i 's/# SSLVerify/SSLVerify/' /etc/libreport/plugins/ureport.conf
sed -i 's/# ContactEmail = foo@example.com/ContactEmail = vrutkovs@redhat.com/' /etc/libreport/plugins/ureport.conf

echo ">> Restarting abrt"
systemctl restart abrtd
systemctl restart abrt-journal-core
systemctl restart abrt-oops

echo ">> Running behave tests"
rm -rf /tmp/junit; mkdir /tmp/junit; chown test:test /tmp/junit
sudo -u test behave -f html -o /tmp/report.html -f plain --junit --junit-directory=/tmp/junit; rc=$?
rhts-submit-log -l /tmp/report.html
rhts-submit-log -l /tmp/junit/*

journalctl -b --no-pager -o short-monotonic > /tmp/journal.log
rhts-submit-log -l /tmp/journal.log

abrt-cli ls > /tmp/abrt.log
rhts-submit-log -l /tmp/abrt.log

rpm -qa | sort > /tmp/packages.list
rhts-submit-log -l /tmp/packages.list

exit $rc
