# this file contains the base vagrant config
# include it from a Vagrantfile using "load 'vagrant_base.rb'"

# get local ssh public key
# dopey assumption: OSX/Unix user created ~/.ssh/id_rsa.pub
# http://stackoverflow.com/questions/1490138/reading-the-first-line-of-a-file-in-ruby
$my_key = File.open(ENV['HOME']+'/.ssh/id_rsa.pub', &:readline)

$full_script = <<SCRIPT
echo disabling apt auto-updates
echo 'APT::Periodic::Update-Package-Lists "0";' > /etc/apt/apt.conf.d/20auto-upgrades
echo 'APT::Periodic::Unattended-Upgrade "0";' >> /etc/apt/apt.conf.d/20auto-upgrades
apt-get update

echo permitting external SSH connection
echo '#{$my_key}' >> .ssh/authorized_keys

#{$script}
SCRIPT

Vagrant.configure('2') do |config|

# Plugin-specific configurations
  # Detects vagrant-cachier plugin
  if Vagrant.has_plugin?('vagrant-cachier')
    puts 'INFO:  Vagrant-cachier plugin detected. Optimizing caches.'
    config.cache.auto_detect = true
    config.cache.enable :apt
  else
    puts 'WARN:  Vagrant-cachier plugin not detected. Continuing unoptimized.'
  end

  config.vm.hostname = $hostname

  config.vm.box = 'opscode-ubuntu-14.04'
  config.vm.box_url = 'http://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_ubuntu-14.04_chef-provisionerless.box'

  config.vm.network :private_network, :ip => $ip

  config.vm.provider :virtualbox do |vb|
    vb.customize [
      'modifyvm', :id,
      '--memory', '256',
      '--cpus', '1',
    ]
  end

  # Enable SSH agent forwarding for git clones
  config.ssh.forward_agent = true

  config.vm.provision "shell", inline: $full_script

end

