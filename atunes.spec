Name:		atunes
Summary:	Audio player and manager
Version:	1.13.4
Release:	%mkrel 2
URL:		http://www.atunes.org/
License:	GPLv2+
Group:		Sound
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0:	aTunes_%{version}.tar.gz
Source1:	atunes-mini.png
Source2:	atunes.png
Source3:	atunes-large.png
Source4:	antBuildNumber.jar
Source5:	antCommenter.jar
Patch0:		atunes-default_theme.patch
#Patch1:		atunes-disable_jintellitype.patch
Patch1:		atunes-disable_jintellitype_Win32Hotkeys.patch
Requires:	java >= 1.6.0
Requires:	mplayer vorbis-tools
Requires:	jakarta-commons-io jakarta-commons-logging
Requires:	jcommon jfreechart jhlabs-filters log4j jakarta-oro
#Requires:	jna jna-examples substance swingx htmlparser xmlpull-api xstream
Requires:	jna substance swingx htmlparser xmlpull-api xstream
Suggests:	vorbis-tools flac cdrkit-icedax
BuildArch:	noarch
BuildRequires:	java-devel java-rpmbuild jpackage-utils ant
BuildRequires:	unzip
BuildRequires:	jakarta-commons-io jakarta-commons-logging
BuildRequires:	jcommon jfreechart jhlabs-filters log4j jakarta-oro jaudiotagger
#BuildRequires:	jna jna-examples substance swingx htmlparser xmlpull-api xstream
BuildRequires:	jna substance swingx htmlparser xmlpull-api xstream
%description
aTunes is a full-featured audio player and manager, developed in Java
programming language.

Currently plays mp3, ogg, wma, wav and mp4 files, allowing users to
easily edit tags, organize music and rip Audio CDs.

%prep
%setup -q -n aTunes
#%patch1 -p1
%patch1 -p0

# Clean unuseful files
%{__rm} -rf aTunes.exe
%{__rm} -rf mac_tools
%{__rm} -rf win_tools
%{__rm} -rf javadoc


find . -name '*.jar' -exec %{__rm} -f {} \;
find . -name '*.class' -exec %{__rm} -f {} \;

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

%{__mkdir_p} antBuildNumber/src antBuildNumber/build
%{__unzip} -d antBuildNumber/src %{SOURCE4}
find antBuildNumber/src -name '*.class' -exec %{__rm} -f {} \;

%{__cat} > antBuildNumber/build.xml <<EOF
<project name="antBuildNumber" basedir="." default="build-jar">
        <target name="build-jar">
                <javac srcdir="src" destdir="build" />
                <jar basedir="build" destfile="antBuildNumber.jar">
                        <fileset dir="build" includes="*/*.*"/>
                </jar>
        </target>
</project>
EOF

%{__mkdir_p} antCommenter/src antCommenter/build
%{__unzip} -d antCommenter/src %{SOURCE5}
find antCommenter/src -name '*.class' -exec %{__rm} -f {} \;

%{__cat} > antCommenter/build.xml <<EOF
<project name="aTunes" basedir="." default="build-jar">
        <target name="build-jar">
                <javac srcdir="src" destdir="build">
			<classpath>
				<fileset dir="%{_javadir}" includes="commons-io.jar"/>
			</classpath>
		</javac>
                <jar basedir="build" destfile="antCommenter.jar">
                        <fileset dir="build" includes="*/*.*"/>
                </jar>
        </target>
</project>
EOF

%build
(cd antBuildNumber; %ant build-jar)
%{__mv} antBuildNumber/antBuildNumber.jar lib

(cd antCommenter; %ant build-jar)
%{__mv} antCommenter/antCommenter.jar lib

CLASSPATH=`build-classpath swingx substance jna jna-examples jakarta-oro \
	   jcommon jhlabs-filters log4j jaudiotagger xmlpull-api \
	   htmlparser xstream` \
	 %ant build-jar

%install
%{__rm} -Rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -p aTunes.jar %{buildroot}%{_javadir}
%{__cp} -p lib/antBuildNumber.jar %{buildroot}%{_javadir}/%{name}-antBuildNumber.jar

%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__cp} -a translations %{buildroot}%{_datadir}/%{name}
%{__cp} -a build.properties extendedLog.properties log4j.properties \
	   %{buildroot}%{_datadir}/%{name}

%{__mkdir_p} %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/sh
cd %{_datadir}/%{name}
java -Xms18m -Xmx96m -cp %{_javadir}/aTunes.jar:%{_javadir}/commons-io.jar:%{_javadir}/jcommon.jar:%{_javadir}/jfreechart.jar:%{_javadir}/entagged-audioformats.jar:%{_javadir}/log4j.jar:%{_javadir}/commons-logging.jar:%{_javadir}/%{name}-antBuildNumber.jar:%{_javadir}/substance.jar:%{_javadir}/oro.jar:%{_javadir}/swingx.jar:%{_javadir}/Filters.jar:%{_javadir}/htmlparser.jar:%{_javadir}/substance-swing.jar:%{_javadir}/commons-codec.jar:%{_javadir}/xpp3.jar:%{_javadir}/xstream.jar:%{_javadir}/jna.jar:%{_javadir}/jna-examples.jar net.sourceforge.atunes.Main "\$1"
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
