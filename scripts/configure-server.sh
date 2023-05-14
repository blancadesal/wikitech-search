#!/usr/bin/env bash

# Update the system package list
sudo apt update

# Install localization files
sudo apt install locales-all

# Install Nginx
sudo apt install -y nginx

# Enable Nginx to start at boot, and start it immediately
sudo systemctl enable nginx
sudo systemctl start nginx

# Update the system package list again
sudo apt update

# Install necessary packages for adding the Docker repository
sudo apt install ca-certificates curl gnupg

# Create a directory for the Docker keyring if it doesn't exist
sudo install -m 0755 -d /etc/apt/keyrings

# Download Docker's GPG key and save it in the Docker keyring directory
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Change the permissions of the Docker keyring file to make it readable for everyone
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker's repository to the system's list of APT sources
# We're using the current system's architecture and codename (like 'bullseye' for Debian 11) to specify the Docker repository
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update the system package list with the new Docker repository
sudo apt update

# Install Docker and related packages
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Enable Docker and Containerd to start at boot
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
