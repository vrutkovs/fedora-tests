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


echo "Running behave tests"
dnf install -y python-behave
sudo -u test behave -f plain