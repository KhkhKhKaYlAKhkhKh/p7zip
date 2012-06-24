Summary:	File archiver with highest compression ratio
Summary(pl):	Paker plik�w z najwy�szym stopniem kompresji
Name:		p7zip
Version:	4.33
Release:	1
License:	LGPL
Group:		Applications/Archiving
Source0:	http://dl.sourceforge.net/p7zip/%{name}_%{version}_src_all.tar.bz2
# Source0-md5:	6333633173f6bcd851ed087402af60d2
Patch0:		%{name}-opt.patch
URL:		http://p7zip.sourceforge.net/
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
7-Zip is a file archiver with highest compression ratio.

The main features of 7z format:
- Open architecture
- High compression ratio
- Strong AES-256 encryption
- Ability of using any compression, conversion or encryption method
- Supporting files with sizes up to 16000000000 GB
- Unicode file names
- Solid compressing
- Archive headers compressing

%description -l pl
7-Zip jest pakerem plik�w z najwy�szym stopniem kompresji.

G��wne cechy formatu 7z:
- otwarta architektura,
- wysoki stopie� kompresji,
- silne kodowanie AES-256,
- mo�liwo�� u�ywania dowolnych metod kodowania, kompresji, konwersji,
- obs�uga bardzo du�ych plik�w (powy�ej 16000000000 GB),
- obs�uga nazw plik�w w unikodzie,
- kompresja upakowana,
- kompresja nag��wk�w archiwum.

%package standalone
Summary:	Standalone 7zip executable
Summary(pl):	Samodzielny plik wykonywalny 7zip
Group:		Applications/Archiving
Obsoletes:	p7zip-stand-alone

%description standalone
Standalone version of 7zip. It handles less archive formats than
plugin capable version.

%description standalone -l pl
Samodzielna wersja 7zip-a. Obs�uguje mniej format�w archiw�w ni�
wersja obs�uguj�ca wtyczki.

%prep
%setup -q -n %{name}_%{version}
%patch0 -p1

cp -f makefile.linux_x86_ppc_alpha makefile.machine

%{__sed} -i "s@Formats@%{_libdir}/%{name}/&@" \
	7zip/UI/Common/ArchiverInfo.cpp
%{__sed} -i 's,return GetBaseFolderPrefix.*,return TEXT("%{_libdir}/%{name}/Codecs/");,g' \
	7zip/Archive/Common/CodecsPath.cpp

%build
%{__make} all2 \
	_CC="%{__cc} %{rpmcflags}" \
	_CXX="%{__cxx} %{rpmcxxflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name}/{Codecs,Formats},%{_mandir}/man1}

install bin/7z* $RPM_BUILD_ROOT%{_bindir}
install bin/Codecs/* $RPM_BUILD_ROOT%{_libdir}/%{name}/Codecs
install bin/Formats/* $RPM_BUILD_ROOT%{_libdir}/%{name}/Formats

install man1/7z* $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc DOCS/{MANUAL,{7zFormat,Methods,history,lzma,readme}.txt} ChangeLog README TODO
%attr(755,root,root) %{_bindir}/7z
%attr(755,root,root) %{_bindir}/7zCon.sfx
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/Codecs
%attr(755,root,root) %{_libdir}/%{name}/Codecs/*
%dir %{_libdir}/%{name}/Formats
%attr(755,root,root) %{_libdir}/%{name}/Formats/*
%{_mandir}/man1/7z.*

%files standalone
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/7za
%{_mandir}/man1/7za.*
