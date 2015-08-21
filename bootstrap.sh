#!/bin/sh

echo "Updating the system"
dnf clean expire-cache
dnf update -y

echo "Enabling passwordless sudo"
sed -i s/#\ %wheel/%wheel/g /etc/sudoers

echo "Adding a new test user"
useradd test
echo "redhat" | passwd test --stdin
usermod -aG wheel test

echo "Installing test requirements"
dnf install -y python-behave systemd-python

echo "Enable abrt autoreporting"
dnf install -y abrt abrt-addon*
abrt-auto-reporting enabled
systemctl start abrtd

echo "Running behave tests"
sudo -u test behave -f html -o /tmp/report.html -f plain; rc =$?

abrt-cli ls > /tmp/abrt.log
rhts-submit-log -l /tmp/abrt.log
rhts-submit-log -l /tmp/report.html

exit $rc