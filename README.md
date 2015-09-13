# VMs
This repository contains Vagrant definitions for all targeted scanning
platforms.

# Usage
* Ensure you have created SSH key `~/.ssh/id_rsa.pub`
* Install Vagrant.
* Install plugins: `vagrant plugin install vagrant-cachier`
* Change to your targeted platform.
* Type `vagrant up`.

# Notes
These Vagrant files assume you have created an SSH key and corresponding
public key file `~/.ssh/id_rsa.pub`. This public key is read in during
VM provisioning, and trusted by the Vagrant VM.

# TODO
* Look for more places to find a permitted SSH public key
* Fail gracefully if no permitted SSH public key is found 
