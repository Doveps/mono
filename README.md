# Scanner
This Ansible playbook opens an SSH connection to a targeted host or IP
address, retrieves information about the host, and turns that
information into Ansible playbooks.

# Usage
Install Ansible.

## SSH trust
You will need to add a permitted SSH key to your keychain. For Vagrant
VMs, this is the Vagrant insecure key. To add this key to your keychain,
run:

```bash
ssh-add vagrant_insecure_key
```

## Running the scan
```bash
ansible-playbook scan.yml
```
* By default, this scans a Vagrant box with ip `33.33.33.50`.
    * To scan a different user or host, use argument `-e 'host=thehost
      user=theuser'`.
* For the duration of the scan, the host SSH fingerprint is trusted.
    * Once the scan is complete, the host SSH fingerprint is removed
      from your `known_hosts` file.

# Scan results
Once the scanner has completed, it creates a directory named after the
scanned host within the `local` directory. It writes its scan results to
multiple files within this directory.

These results are suitable for input into another, separate analysis
script.

# TODO
* Keep the scanned-host fingerprint somewhere other than
  `~/.ssh/known_hosts`.
* Retrieve the scanned-host fingerprint from somewhere other than
  `ssh-keyscan`.
* Find a better way to manage SSH key access to scanned hosts.
