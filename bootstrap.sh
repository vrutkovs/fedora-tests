#!/bin/sh

echo ">> Updating the system"
dnf update -y

echo ">> Enabling passwordless sudo"
sed -i s/#\ %wheel/%wheel/g /etc/sudoers

echo ">> Adding a new test user"
useradd test
echo "redhat" | passwd test --stdin
usermod -aG wheel test
usermod -aG adm test

echo ">> Installing test requirements"
dnf install -y python-behave systemd-python gnome-desktop-testing pygobject2 \
    pygobject3

echo ">> Enable abrt autoreporting"
dnf install -y abrt abrt-tui abrt-addon*
abrt-auto-reporting enabled
abrt-install-ccpp-hook install

echo ">> Enable abrt FAF reporting"
sed -i 's/# URL/URL/' /etc/libreport/plugins/ureport.conf
sed -i 's/# SSLVerify/SSLVerify/' /etc/libreport/plugins/ureport.conf
sed -i 's/# ContactEmail = foo@example.com/ContactEmail = vrutkovs@redhat.com/'\
       /etc/libreport/plugins/ureport.conf

echo ">> Restarting abrt"
systemctl restart abrtd
systemctl restart abrt-journal-core
systemctl restart abrt-oops
