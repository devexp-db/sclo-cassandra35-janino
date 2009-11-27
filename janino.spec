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
Name:           janino
Version:        2.5.15
Release:        3%{dist}
Summary:        An embedded Java compiler
License:        BSD
URL:            http://www.janino.net/
Group:          Development/Tools
Source0:        http://www.janino.net/download/%{name}-%{version}.zip
Source1:        janino-2.5.11.pom
Patch0:         janino-build_xml.patch

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  ant
BuildRequires:  jpackage-utils >= 0:1.5
BuildArch:      noarch

Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

%description
Janino is a compiler that reads a JavaTM expression, block, class body,
source file or a set of source files, and generates Java bytecode that is
loaded and executed directly. Janino is not intended to be a development
tool, but an embedded compiler for run-time compilation purposes, e.g.
expression evaluators or "server pages" engines like JSP.  Janino is
integrated with Apache Commons JCI ("Java Compiler Interface") and JBoss
Rules / Drools.  Janino can also be used for static code analysis. 

%package        javadoc
Summary:        Documentation for %{name}
Group:          Documentation

%description    javadoc
%{summary}.

%prep
%setup -q
rm -rf javadoc lib
%patch0 -b .sav

%build
%{ant} jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 build/lib/janino.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

%add_to_maven_depmap %{name} %{name} %{version} JPP %{name}

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom

# javadoc
install -p -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -sf %{name}-%{version} %{name})

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr (-,root,root,-)
%{_javadir}/*.jar
%{_datadir}/maven2/poms/*
%config(noreplace) %{_mavendepmapfragdir}/%{name}

%files javadoc
%defattr (-,root,root,-)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%dir %{_javadocdir}/%{name}

%changelog
* Tue Oct 27 2009 Mary Ellen Foster <mefoster at gmail.com> - 2.5.15-3
- Changed group tag on main package and sub-package
- Fixed default attribute on files section

* Mon Oct 26 2009 Mary Ellen Foster <mefoster at gmail.com> - 2.5.15-2
- Removed gcj bits

* Sun Oct 25 2009 Mary Ellen Foster <mefoster at gmail.com> - 2.5.15-1
- Initial package, based on Alexander Kurtakov's JPackage and Mandriva package
