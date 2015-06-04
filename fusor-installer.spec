# We don't want to use SCL since we are missing some dependencies 
# in SCL and we still support 1.8 for installer
%global scl_ruby /usr/bin/ruby

# set and uncomment all three to set alpha tag
#global alphatag RC1
#global dotalphatag .%{alphatag}
#global dashalphatag -%{alphatag}

Name:       fusor-installer
Epoch:      1
Version:    0.0.14
Release:    1%{?dotalphatag}%{?dist}
Summary:    Foreman-installer plugin that allows you to install Fusor
Group:      Applications/System
License:    GPLv3+ and ASL 2.0
URL:        http://theforeman.org
Source0:    %{name}-%{version}%{?dashalphatag}.tar.gz

BuildArch:  noarch

Requires:   katello-installer
Requires:   ntp
Requires:   rubygem-kafo >= 0.6.4
Requires:   git
Requires:   ovirt-puppet

%description
This is a Foreman-Installer plugin that allows you to install and configure
the Fusor Foreman plugin

%prep
%setup -q -n %{name}-%{version}%{?dashalphatag}

%build
#replace shebangs for SCL
%if %{?scl:1}%{!?scl:0}
  sed -ri '1sX(/usr/bin/ruby|/usr/bin/env ruby)X%{scl_ruby}X' bin/fusor-installer
%endif

%install
install -d -m0755 %{buildroot}%{_datadir}/katello-installer
cp -R hooks modules %{buildroot}%{_datadir}/katello-installer
install -d -m0755 %{buildroot}%{_sbindir}
cp bin/fusor-installer %{buildroot}%{_sbindir}/fusor-installer
install -d -m0755 %{buildroot}%{_bindir}
cp bin/fusor-register-host %{buildroot}%{_bindir}/fusor-register-host
install -d -m0755 %{buildroot}%{_sysconfdir}/katello-installer/
cp config/fusor-installer.yaml %{buildroot}%{_sysconfdir}/katello-installer/fusor-installer.yaml
cp config/fusor-installer.answers.yaml %{buildroot}%{_sysconfdir}/katello-installer/fusor-installer.answers.yaml


%files
%defattr(-,root,root,-)
%doc LICENSE
%{_datadir}/katello-installer/hooks/boot/100-add_options.rb
%{_datadir}/katello-installer/hooks/lib/base_seeder.rb
%{_datadir}/katello-installer/hooks/lib/foreman.rb
%attr(755, root, root) %{_datadir}/katello-installer/hooks/lib/install_modules.sh
%{_datadir}/katello-installer/hooks/lib/base_wizard.rb
%{_datadir}/katello-installer/hooks/lib/provisioning_seeder.rb
%{_datadir}/katello-installer/hooks/lib/provisioning_wizard.rb
%{_datadir}/katello-installer/hooks/post/100-setup_provisioning.rb
%{_datadir}/katello-installer/hooks/pre_validations/100-gather_and_set_fusor_values.rb
%{_datadir}/katello-installer/hooks/pre_values/100-register_fusor_modules.rb
%{_datadir}/katello-installer/modules/network
%{_datadir}/katello-installer/modules/foreman/manifests/plugin/fusor.pp
%{_datadir}/katello-installer/modules/foreman/manifests/plugin/fusor_network.pp

%config %attr(600, root, root) %{_sysconfdir}/katello-installer/fusor-installer.yaml
%config(noreplace) %attr(600, root, root) %{_sysconfdir}/katello-installer/fusor-installer.answers.yaml
%{_sbindir}/fusor-installer
%{_bindir}/fusor-register-host

%changelog
* Thu Apr 09 2015 John Matthews <jwmatthews@gmail.com> 0.0.14-1
- answers: add gutterball plugin (bbuckingham@redhat.com)

* Tue Mar 31 2015 John Matthews <jwmatthews@gmail.com> 0.0.13-1
- seeding: fix the hostgroup seeding for 'Fusor Base' (bbuckingham@redhat.com)

* Tue Mar 31 2015 John Matthews <jwmatthews@gmail.com> 0.0.12-1
- Merge pull request #6 from bbuckingham/seeding_updates (jwmatthews@gmail.com)
- seeding: updates based on fusor-server updates for hostgroups
  (bbuckingham@redhat.com)

* Thu Mar 19 2015 John Matthews <jwmatthews@gmail.com> 0.0.11-1
- Updates from testing with Sat 6.1 3.11.1 compose  - Add stanza for gutterball
  config  - Hard code parameters for kernel/initrd of foreman plugin discovery
  since puppet params have been deleted  - Remove explicit enable of
  foreman_plugin_discovery (jwmatthews@gmail.com)

* Tue Mar 10 2015 John Matthews <jwmatthews@gmail.com> 0.0.10-1
- Comment out blocks in ks_snippets which break provisioning. Syntax issues
  with usage of:   @host.network_query   def custom_deployment_repositories
  (jwmatthews@gmail.com)

* Tue Mar 03 2015 John Matthews <jwmatthews@gmail.com> 0.0.9-1
- Remove extra https:// in PXE Template for specifying foreman URL
  (jwmatthews@gmail.com)

* Tue Mar 03 2015 John Matthews <jwmatthews@gmail.com> 0.0.8-1
- Updates for discovery to work with foreman-discovery-image-2.1.0
  (jwmatthews@gmail.com)
- spec - remove Requires on foreman_api (bbuckingham@redhat.com)
- spec - removing hack that required puppet 3.7.3 (bbuckingham@redhat.com)
- seeding: update use katello's content management (bbuckingham@redhat.com)
- seeding: update to use apipie bindings vs foreman api
  (bbuckingham@redhat.com)

* Fri Feb 20 2015 John Matthews <jwmatthews@gmail.com> 0.0.7-1
- Disable the download of discovery images. (jwmatthews@gmail.com)

* Thu Feb 12 2015 John Matthews <jwmatthews@gmail.com> 0.0.6-1
- Fix for when /etc/puppet/environments/production/ is missing
  (jwmatthews@gmail.com)

* Thu Feb 12 2015 John Matthews <jwmatthews@gmail.com> 0.0.5-1
- Adding requires for ovirt-puppet (jwmatthews@gmail.com)

* Thu Feb 12 2015 John Matthews <jwmatthews@gmail.com> 0.0.4-1
- Removed requirement of puppet 3.7.3 (jwmatthews@gmail.com)
- foreman discovery: updates to support discovery (bbuckingham@redhat.com)
- ovirt - initial seeding to support ovirt (bbuckingham@redhat.com)
- remove partitioning table seed that was specific to openstack with staypuft
  (bbuckingham@redhat.com)

* Tue Feb 03 2015 John Matthews <jwmatthews@gmail.com> 0.0.3-1
- Adding a HACK workaround to force puppet to be 3.7.3 Needed to address a
  known issue with puppet 3.7.4 (jwmatthews@gmail.com)

* Mon Jan 19 2015 John Matthews <jwmatthews@gmail.com> 0.0.2-1
- new package built with tito



