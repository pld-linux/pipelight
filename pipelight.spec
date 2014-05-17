
%define commit	487f8db5a03d

Summary:	Browser plugin to load Windows browser plugins
Summary(pl.UTF-8):	Wtyczka przeglądarki do wczytywania wtyczek przeglądarek z systemu Windows
Name:		pipelight
Version:	0.2.6
Release:	0.1
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		Applications/WWW
Source0:	https://bitbucket.org/mmueller2012/pipelight/get/v%{version}.tar.bz2
# Source0-md5:	265747e08a3b2dd806c47a228f03df5b
Source1:	http://repos.fds-team.de/pluginloader/v%{version}/pluginloader.tar.gz
# Source1-md5:	5931da0500aed46f875b28cec2160cfe
Patch0:		%{name}-lib64.patch
Patch1:		%{name}-pld.patch
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
%if "%{_lib}" == "lib64"
%patch0 -p1
%endif
%patch1 -p1

%build
# not autoconf-generated
./configure \
	--prefix=%{_prefix} \
	--wine-path=%{_bindir}/wine \
	--moz-plugin-path=%{_browserpluginsdir} \
	--win32-prebuilt \
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
%attr(755,root,root) %{_datadir}/%{name}/hw-accel-default
%attr(755,root,root) %{_datadir}/%{name}/install-dependency
%attr(755,root,root) %{_datadir}/%{name}/pluginloader.exe
%ifarch %{x8664}
%attr(755,root,root) %{_datadir}/%{name}/pluginloader64.exe
%endif
%{_datadir}/%{name}/sig-install-dependency.gpg
%{_datadir}/%{name}/configs
%{_datadir}/%{name}/licenses
%dir %{_datadir}/%{name}/scripts
%attr(755,root,root) %{_datadir}/%{name}/scripts/*
