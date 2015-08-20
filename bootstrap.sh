#!/bin/sh

# Update the system
dnf clean expire-cache
dnf update -y

# Setup passwordless sudo

# Add test user
useradd test
echo "redhat" | passwd test --stdin
usermod -aG wheel test


# Install behave
dnf install -y python-behave

# Run behave tests
# sudo -u test behave