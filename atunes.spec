Name:		atunes
Summary:	Audio player and manager
Version:	1.7.2
Release:	%mkrel 2
URL:		http://www.atunes.org/
License:	GPLv2+
Group:		Sound
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0:	aTunes_%{version}.tgz
Source1:	atunes-mini.png
Source2:	atunes.png
Source3:	atunes-large.png
Patch0:		atunes-default_theme.patch
Requires:	java >= 1.6.0
Requires:	mplayer vorbis-tools
Requires:	jakarta-commons-io jakarta-commons-logging entagged-audioformats-java
Requires:	jcommon jdic jfreechart jhlabs-filters log4j jakarta-oro
BuildArch:	noarch
BuildRequires:	java-devel >= 1.7.0 ant
BuildRequires:	unzip
BuildRequires:	jakarta-commons-io jakarta-commons-logging entagged-audioformats-java
BuildRequires:	jcommon jdic jfreechart jhlabs-filters log4j jakarta-oro
%description
aTunes is a full-featured audio player and manager, developed in Java
programming language.

Currently plays mp3, ogg, wma, wav and mp4 files, allowing users to
easily edit tags, organize music and rip Audio CDs.

This software is released under GPL. It is however included in the
non-free section because we have not yet been able to build some of its
dependencies (swingx.jar) using only free software.

%prep
%setup -q -n aTunes
%patch0 -p1
# TODO:
# swingx.jar antBuildNumber.jar and substance.jar need to be built separatly later
%{__find} . -name '*.jar' ! -name swingx.jar ! -name antBuildNumber.jar \
	    ! -name substance.jar -exec %{__rm} -f {} \;
%{__find} . -name '*.class' -exec %{__rm} -f {} \;

%{__mkdir} build

%{__cat} > build.xml <<EOF
<project name="aTunes" basedir="." default="build-jar">
	<target name="build-jar">
		<javac srcdir="src" destdir="build">
			<classpath>
				<fileset dir="%{_javadir}" includes="*.jar"/>
				<fileset dir="lib" includes="*.jar"/>
			</classpath>
		</javac>
		<copy todir="build">
			<fileset dir="src" includes="net/sourceforge/atunes/gui/images/*.*"
					   excludes="net/sourceforge/atunes/gui/images/*.java"/>
		</copy>
		<jar basedir="build" destfile="aTunes.jar">
			<fileset dir="build" includes="*/*.*"/>
		</jar>
	</target>
</project>
EOF

cd translations
%{__mv} fran*.png francais.png
%{__mv} fran*.properties francais.properties
%{__mv} espa*ol.png espanol.png
%{__mv} espa*ol.properties espanol.properties
%{__mv} portu*brasil.png 'portuges brasil.png'
%{__mv} portu*brasil.properties 'portuges brasil.properties'
%{__mv} portu*s.png portuges.png
%{__mv} portu*s.properties portuges.properties
%{__mv} slovensk*.properties slovenska.properties
# this file cause the program to crash :
%{__rm} slovensk*.png

%build
ant build-jar

%install
%{__rm} -Rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -p aTunes.jar %{buildroot}%{_javadir}
cd lib
for file in swingx.jar antBuildNumber.jar substance.jar
do
	%{__cp} -p $file %{buildroot}%{_javadir}/%{name}-$file
done
cd ..

%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__cp} -a translations %{buildroot}%{_datadir}/%{name}
%{__cp} -a build.properties extendedLog.properties log4j.properties \
	   %{buildroot}%{_datadir}/%{name}

%{__mkdir_p} %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/sh
cd %{_datadir}/%{name}
java -cp %{_javadir}/aTunes.jar:%{_javadir}/commons-io.jar:%{_javadir}/jcommon.jar:%{_javadir}/jfreechart.jar:%{_javadir}/entagged-audioformats.jar:%{_javadir}/log4j.jar:%{_javadir}/commons-logging.jar:%{_javadir}/jdic.jar:%{_javadir}/%{name}-antBuildNumber.jar:%{_javadir}/%{name}-substance.jar:%{_javadir}/oro.jar:%{_javadir}/%{name}-swingx.jar:%{_javadir}/Filters.jar net.sourceforge.atunes.Main "\$1"
EOF

%{__mkdir_p} %{buildroot}%{_iconsdir}/mini %{buildroot}%{_iconsdir}/large
%{__cp} -p %{SOURCE1} %{buildroot}%{_miconsdir}/%{name}.png
%{__cp} -p %{SOURCE2} %{buildroot}%{_iconsdir}/%{name}.png
%{__cp} -p %{SOURCE3} %{buildroot}%{_liconsdir}/%{name}.png

%{__mkdir_p} %{buildroot}%{_datadir}/applications
%{__cat} > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=aTunes
Comment=Full featured audio player and manager
GenericName=Audio player
Exec=soundwrapper %{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
MimeType=audio/x-mp3;audio/x-ogg;application/x-ogg;audio/x-mpegurl;audio/x-wav;audio/x-scpls;audio/mpegurl;audio/mp3;audio/mpeg;audio/x-mpeg;application/x-flac;audio/x-flac;
Categories=Audio;Player;X-MandrivaLinux-Multimedia-Sound;AudioVideo;Java;X-MandrivaLinux-CrossDesktop;
EOF

%post
%{update_menus}

%postun
%{clean_menus}

%files
%doc license.txt
%attr(0755,root,root) %{_bindir}/%{name}
%{_datadir}/%{name}
%{_javadir}/aTunes.jar
%{_javadir}/%{name}-*.jar
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
