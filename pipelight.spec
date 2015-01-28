
%define commit	b7b5e5471d52

Summary:	Browser plugin to load Windows browser plugins
Summary(pl.UTF-8):	Wtyczka przeglądarki do wczytywania wtyczek przeglądarek z systemu Windows
Name:		pipelight
Version:	0.2.8
Release:	0.1
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		Applications/WWW
Source0:	https://bitbucket.org/mmueller2012/pipelight/get/v%{version}.tar.bz2
# Source0-md5:	9fcbc7019a49eb0c2f613eaba0e96df6
Source1:	http://repos.fds-team.de/pluginloader/v%{version}/pluginloader.tar.gz
# Source1-md5:	71b595924b8c8d91c830c2a897362ad2
Source2:	http://repos.fds-team.de/pluginloader/v%{version}/pluginloader.tar.gz.sig
# Source2-md5:	e0b2467752881ac2735594d4ba8fe179
Patch0:		%{name}-pld.patch
URL:		https://launchpad.net/pipelight
BuildRequires:	libstdc++-devel
BuildRequires:	xorg-lib-libX11-devel
Requires:	browser-plugins
Requires:	wine
Suggests:	wine(compholio)(32bit)
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pipelight is a special browser plugin which allows one to use Windows
only plugins inside Linux browsers. We are currently focusing on
Silverlight, Flash, Shockwave and the Unity Webplayer. The project
needs a patched version of Wine to execute the Silverlight DLL.

%description -l pl.UTF-8
Pipelight to specjalna wtyczka przeglądarki, pozwalająca na
korzystanie z wtyczek przeznaczonych tylko dla systemu Windows w
przeglądarce na Linuksie. Obecnie skupia się na wtyczkach Silverlight,
Flash, Shockwave oraz Unity Webplayer. Do uruchamiania bibliotek DLL
Silverlighta niezbędna jest załatana wersja Wine.

%prep
%setup -q -a1 -n mmueller2012-%{name}-%{commit}
%patch0 -p1

ln -s %{SOURCE1} pluginloader-v%{version}.tar.gz
ln -s %{SOURCE2} pluginloader-v%{version}.tar.gz.sig

%build
# not autoconf-generated
./configure \
	--prefix=%{_prefix} \
	--wine-path=%{_bindir}/wine \
	--moz-plugin-path=%{_browserpluginsdir} \
	--libdir=%{_libdir} \
	--win32-prebuilt \
	--downloader=/bin/false \
%ifarch %{x8664}
	--with-win64 \
%endif
	--win64-prebuilt

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pipelight-plugin
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/libpipelight.so
%{_mandir}/man1/pipelight-plugin.1*
%dir %{_datadir}/%{name}
%attr(755,root,root) %{_datadir}/%{name}/install-dependency
%attr(755,root,root) %{_datadir}/%{name}/pluginloader.exe
%attr(755,root,root) %{_datadir}/%{name}/wine
%attr(755,root,root) %{_datadir}/%{name}/winecheck.exe
%ifarch %{x8664}
%attr(755,root,root) %{_datadir}/%{name}/pluginloader64.exe
%attr(755,root,root) %{_datadir}/%{name}/wine64
%attr(755,root,root) %{_datadir}/%{name}/winecheck64.exe
%endif
%{_datadir}/%{name}/sig-install-dependency.gpg
%{_datadir}/%{name}/configs
%{_datadir}/%{name}/licenses
%dir %{_datadir}/%{name}/scripts
%attr(755,root,root) %{_datadir}/%{name}/scripts/*
