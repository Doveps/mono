# Scanner
This Ansible playbook opens an SSH connection to a targeted host or IP
address, retrieves information about the host, and turns that
information into Ansible playbooks.

# Usage
Install Ansible.

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
* Replace Ansible with our own scanner; features
    * don't assume python
    * don't assume root
    * multi-hop using identified connections to scanned host
    * does somethine else exist that we can reuse?
    * make smart decisions about what to scan (linux vs ios, etc)
    * don't assume ssh
    * save results someplace better (not "local" dir)
* Keep the scanned-host fingerprint somewhere other than
  `~/.ssh/known_hosts`.
* Retrieve the scanned-host fingerprint from somewhere other than
  `ssh-keyscan`.
