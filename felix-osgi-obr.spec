%global bundle org.osgi.service.obr

Name:           felix-osgi-obr
Version:        1.0.2
Release:        4
Summary:        Felix OSGi OBR Service API

Group:          Development/Java
License:        ASL 2.0
URL:            http://felix.apache.org/site/apache-felix-osgi-bundle-repository.html
Source0:        http://www.apache.org/dist/felix/org.osgi.service.obr-%{version}-project.tar.gz
Source1:        build.xml.tar.gz
BuildRequires:  ant
BuildRequires:  jpackage-utils
BuildRequires:  felix-osgi-core
Requires:       felix-osgi-core
Requires(post): jpackage-utils
Requires(postun): jpackage-utils
BuildArch: noarch

%description
OSGi OBR Service API.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{bundle}-%{version}

tar xf %{SOURCE1}

mkdir -p .m2/repository

%build
export CLASSPATH=$(build-classpath felix/org.osgi.core)
ant -Dbuild.sysclasspath=only \
    -Dmaven.settings.offline=true \
    -Dmaven.repo.local=.m2/repository \
    package javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}/felix
install -m 644 target/%{bundle}-%{version}.jar \
        %{buildroot}%{_javadir}/felix/%{bundle}.jar

%add_to_maven_depmap org.apache.felix %{bundle} %{version} JPP/felix %{bundle}

# poms
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -pm 644 pom.xml \
%{buildroot}%{_datadir}/maven2/poms/JPP.felix-%{bundle}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}/

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE
%{_javadir}/felix/*.jar
%{_datadir}/maven2/poms/JPP.felix-%{bundle}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

