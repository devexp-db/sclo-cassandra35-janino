# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
Name:          janino
Version:       2.6.1
Release:       11%{?dist}
Summary:       An embedded Java compiler
Group:         Development/Tools
License:       BSD
URL:           http://docs.codehaus.org/display/JANINO/Home
Source0:       http://dist.codehaus.org/%{name}/%{name}-%{version}.zip
Source1:       http://repo1.maven.org/maven2/org/codehaus/%{name}/%{name}-parent/%{version}/%{name}-parent-%{version}.pom
Source2:       http://repo1.maven.org/maven2/org/codehaus/%{name}/commons-compiler/%{version}/commons-compiler-%{version}.pom
Source3:       http://repo1.maven.org/maven2/org/codehaus/%{name}/commons-compiler-jdk/%{version}/commons-compiler-jdk-%{version}.pom
Source4:       http://repo1.maven.org/maven2/org/codehaus/%{name}/%{name}/%{version}/%{name}-%{version}.pom
# remove org.codehaus.mojo findbugs-maven-plugin 1.1.1, javancss-maven-plugin 2.0, jdepend-maven-plugin 2.0-beta-2
# change artifactId ant-nodeps in ant
Patch0:        %{name}-%{version}-poms.patch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: jpackage-utils

BuildRequires: ant
BuildRequires: junit4

BuildRequires: buildnumber-maven-plugin
BuildRequires: maven
BuildRequires: maven-compiler-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-source-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit4

Requires:      ant

Requires:      java >= 1:1.6.0
Requires:      jpackage-utils
BuildArch:     noarch

%description
Janino is a super-small, super-fast Java compiler. Not only can it compile
a set of source files to a set of class files like the JAVAC tool, but also
can it compile a Java expression, block, class body or source file in
memory, load the bytecode and execute it directly in the same JVM. Janino
is not intended to be a development tool, but an embedded compiler for
run-time compilation purposes, e.g. expression evaluators or "server pages"
engines like JSP.

%package javadoc
Group:         Documentation
Summary:       Javadoc for %{name}
Requires:      jpackage-utils

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q

find . -name "*.jar" -delete
find . -name "*.class" -delete

for m in commons-compiler \
  commons-compiler-jdk \
  %{name};do
  mkdir -p ${m}/src
  (
    cd ${m}/src/
    unzip -qq  ../../${m}-src.zip
    if [ -f org.codehaus.commons.compiler.properties ]; then
      mkdir -p main/resources
      mv org.codehaus.commons.compiler.properties main/resources
    fi
  )
done

cp -p %{SOURCE1} pom.xml
cp -p %{SOURCE2} commons-compiler/pom.xml
cp -p %{SOURCE3} commons-compiler-jdk/pom.xml
cp -p %{SOURCE4} %{name}/pom.xml

%patch0 -p1

perl -pi -e 's/\r$//g' new_bsd_license.txt README.txt

%build

mvn-rpmbuild install javadoc:aggregate

%install

mkdir -p %{buildroot}%{_mavenpomdir}
install -m 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-parent.pom
%add_maven_depmap JPP.%{name}-parent.pom

mkdir -p %{buildroot}%{_javadir}/%{name}

for m in \
  commons-compiler\
  commons-compiler-jdk \
  %{name};do
    install -m 644 ${m}/target/${m}-%{version}.jar %{buildroot}%{_javadir}/%{name}/${m}.jar
    install -m 644 ${m}/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-${m}.pom
    %add_maven_depmap JPP.%{name}-${m}.pom %{name}/${m}.jar
done

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}/*.jar
%{_mavenpomdir}/JPP.%{name}-*.pom
%{_mavendepmapfragdir}/%{name}
%doc new_bsd_license.txt README.txt

%files javadoc
%{_javadocdir}/%{name}
%doc new_bsd_license.txt

%changelog
* Thu Apr 19 2012 gil cattaneo <puntogil@libero.it> 2.6.1-11
- Remove janino-parent as a BuildRequirement

* Wed Apr 18 2012 gil cattaneo <puntogil@libero.it> 2.6.1-10
- moved all of the jar files into janino subdirectory

* Wed Apr 18 2012 gil cattaneo <puntogil@libero.it> 2.6.1-9
- merged commons-compiler, commons-compiler-jdk and janino-parent in main package

* Wed Apr 18 2012 gil cattaneo <puntogil@libero.it> 2.6.1-8
- add janino-parent

* Mon Apr 16 2012 gil cattaneo <puntogil@libero.it> 2.6.1-7
- Remove commons-compiler as a BuildRequirement
- Add janino-parent as a Requirement

* Fri Apr 13 2012 gil cattaneo <puntogil@libero.it> 2.6.1-6
- removed BR unzip

* Fri Apr 13 2012 gil cattaneo <puntogil@libero.it> 2.6.1-5
- commons-compiler spec file merged

* Fri Apr 13 2012 gil cattaneo <puntogil@libero.it> 2.6.1-4
- added missing BR maven-surefire-provider-junit4 for prevent mock build failure

* Tue Apr 10 2012 gil cattaneo <puntogil@libero.it> 2.6.1-3
- removed janino-parent commons-compiler modules.

* Sun Mar 25 2012 gil cattaneo <puntogil@libero.it> 2.6.1-2
- janino janino-parent commons-compiler spec file merged

* Tue Mar 20 2012 Mary Ellen Foster <mefoster at gmail.com> - 2.6.1-1
- Update to 2.6.1, with new build system and all
- Prepare for re-review

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 27 2009 Mary Ellen Foster <mefoster at gmail.com> - 2.5.15-3
- Changed group tag on main package and sub-package
- Fixed default attribute on files section

* Mon Oct 26 2009 Mary Ellen Foster <mefoster at gmail.com> - 2.5.15-2
- Removed gcj bits

* Sun Oct 25 2009 Mary Ellen Foster <mefoster at gmail.com> - 2.5.15-1
- Initial package, based on Alexander Kurtakov's JPackage and Mandriva package
