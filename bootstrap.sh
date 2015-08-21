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
abrt-auto-reporting enabled

echo "Running behave tests"
sudo -u test behave -f plain -f html -o /tmp/report.html; rc =$?

rhts-submit-log -l /tmp/report.html

exit $rc