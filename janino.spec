%{?scl:%scl_package janino}
%{!?scl:%global pkg_name %{name}}

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
Name:          %{?scl_prefix}janino
Version:       2.7.8
Release:       7%{?dist}
Summary:       An embedded Java compiler
License:       BSD
URL:           http://unkrig.de/w/Janino
Source0:       http://%{pkg_name}.net/download/%{pkg_name}-%{version}.zip
Source1:       http://repo1.maven.org/maven2/org/codehaus/%{pkg_name}/%{pkg_name}-parent/%{version}/%{pkg_name}-parent-%{version}.pom
Source2:       http://repo1.maven.org/maven2/org/codehaus/%{pkg_name}/commons-compiler/%{version}/commons-compiler-%{version}.pom
Source3:       http://repo1.maven.org/maven2/org/codehaus/%{pkg_name}/commons-compiler-jdk/%{version}/commons-compiler-jdk-%{version}.pom
Source4:       http://repo1.maven.org/maven2/org/codehaus/%{pkg_name}/%{pkg_name}/%{version}/%{pkg_name}-%{version}.pom
# removes the de.unkrig.commons.nullanalysis annotations
# http://unkrig.de/w/Unkrig.de
# https://svn.code.sf.net/p/loggifier/code/tags/loggifier_0.9.9.v20140430-1829/de.unkrig.commons.nullanalysis/
Patch0:        %{pkg_name}-2.7.8-remove-nullanalysis-annotations.patch

BuildRequires: maven-local
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.ant:ant)
BuildRequires: mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires: mvn(org.codehaus:codehaus-parent:pom:)
BuildRequires: /usr/bin/perl
%{?scl:Requires: %scl_runtime}

BuildArch:     noarch

%description
Janino is a super-small, super-fast Java compiler. Not only can it compile
a set of source files to a set of class files like the JAVAC tool, but also
can it compile a Java expression, block, class body or source file in
memory, load the byte-code and execute it directly in the same JVM. Janino
is not intended to be a development tool, but an embedded compiler for
run-time compilation purposes, e.g. expression evaluators or "server pages"
engines like JSP.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{pkg_name}-%{version}

find . -name "*.jar" -delete
find . -name "*.class" -delete

for m in commons-compiler \
  commons-compiler-jdk \
  %{pkg_name};do
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

%patch0 -p1

install -m 644 %{SOURCE1} pom.xml
install -m 644 %{SOURCE2} commons-compiler/pom.xml
install -m 644 %{SOURCE3} commons-compiler-jdk/pom.xml
install -m 644 %{SOURCE4} %{pkg_name}/pom.xml

%{?scl_enable}
%pom_change_dep -r :ant-nodeps :ant

# RHBZ#842604
%pom_xpath_set "pom:plugin[pom:artifactId = 'maven-compiler-plugin']/pom:configuration/pom:source" 1.6
%pom_xpath_set "pom:plugin[pom:artifactId = 'maven-compiler-plugin']/pom:configuration/pom:target" 1.6

perl -pi -e 's/\r$//g' new_bsd_license.txt README.txt

# Cannot run program "svn"
%pom_remove_plugin :buildnumber-maven-plugin

%pom_remove_plugin :maven-clean-plugin
%pom_remove_plugin :maven-deploy-plugin
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-source-plugin
%{?scl_disable}

%build
%{?scl_enable}
%mvn_build
%{?scl_disable}

%install
%{?scl_enable}
%mvn_install
%{?scl_disable}

%files -f .mfiles
%doc README.txt
%license new_bsd_license.txt

%files javadoc -f .mfiles-javadoc
%license new_bsd_license.txt

%changelog
* Tue Sep 27 2016 Tomas Repik <trepik@redhat.com> - 2.7.8-7
- scl conversion

* Thu Jul 21 2016 gil cattaneo <puntogil@libero.it> 2.7.8-6
- add missing BR

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 29 2015 gil cattaneo <puntogil@libero.it> 2.7.8-4
- update URL field
- remove duplicate files
- use BRs mvn()-like

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 11 2015 gil cattaneo <puntogil@libero.it> 2.7.8-2
- remove nullanalysis annotations (with PATCH0)

* Mon Feb 09 2015 gil cattaneo <puntogil@libero.it> 2.7.8-1
- Update to 2.7.8

* Fri Feb 06 2015 gil cattaneo <puntogil@libero.it> 2.6.1-21
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.6.1-19
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 gil cattaneo <puntogil@libero.it> 2.6.1-17
- switch to XMvn
- minor changes to adapt to current guideline

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.6.1-15
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jul 24 2012 gil cattaneo <puntogil@libero.it> 2.6.1-14
- Rebuilt RHBZ #842604 (compile with -target 1.5 or greater)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 08 2012 gil cattaneo <puntogil@libero.it> 2.6.1-12
- add codehaus-parent to BR

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
