# This spec file is based on other spec files, ebuilds, PKGBUILDs available from
#  [1] https://repos.fedorapeople.org/repos/spot/chromium/
#  [2] https://copr.fedoraproject.org/coprs/churchyard/chromium-russianfedora-tested/
#  [3] https://www.archlinux.org/packages/extra/x86_64/chromium/
#  [4] https://src.fedoraproject.org/rpms/chromium/
#  [5] https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/

# Get the version number of latest stable version
# $ curl -s 'https://omahaproxy.appspot.com/all?os=linux&channel=stable' | sed 1d | cut -d , -f 3

# Require harfbuzz >= 1.8.6 for hb_font_funcs_set_glyph_h_advances_func
%if 0%{?fedora} >= 29
%bcond_without system_harfbuzz
%else
%bcond_with system_harfbuzz
%endif

# Require libxml2 > 2.9.4 for XML_PARSE_NOXXE
%bcond_without system_libxml2

# https://github.com/dabeaz/ply/issues/66
%bcond_without system_ply

# Allow testing whether icu can be unbundled
%bcond_with system_libicu

# Allow testing whether libvpx can be unbundled
%bcond_with system_libvpx

# Allow building with symbols to ease debugging
# Enabled by default because Fedora Copr has enough memory
%bcond_without symbol

# Allow compiling with clang
# Disabled by default becaue gcc is the system compiler
%bcond_with clang

# Allow disabling unconditional build dependency on clang
# Enabled by default because nacl always uses clang to compile some files
%bcond_without require_clang

# Allow using compilation flags set by Fedora RPM macros
# Disabled by default because it causes out-of-memory error on Fedora Copr
%bcond_with fedora_compilation_flags

Name:       chromium-wayland
Version:    74.0.3718.0
Release:    100%{?dist}
Summary:    A WebKit (Blink) powered web browser

License:    BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)
URL:        https://www.chromium.org/Home

# Unfortunately, Fedora Copr forbids uploading sources with patent-encumbered
# ffmpeg code even if they are never compiled and linked to target binraies,
# so we must repackage upstream tarballs to satisfy this requirement. However,
# we cannot simply delete all code of ffmpeg because this will disable support
# for some commonly-used free codecs such as Ogg Theora. Instead, helper
# scripts included in official Fedora packages are copied, modified, and used
# to automate the repackaging work.
#
# If you don't use Fedora services, you can uncomment the following line and
# use the upstream source tarball instead of the repackaged one.
Source0:    https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
#
# The repackaged source tarball used here is produced by:
# ./chromium-latest.py --stable --ffmpegclean --ffmpegarm --deleteunrar
#Source0:    chromium-%{version}-clean.tar.xz
Source1:    chromium-latest.py
Source2:    chromium-ffmpeg-clean.sh
Source3:    chromium-ffmpeg-free-sources.py

# The following two source files are copied and modified from
# https://repos.fedorapeople.org/repos/spot/chromium/
Source10:   chromium-browser.sh
Source11:   chromium-wayland.desktop

# The following two source files are copied verbatim from
# https://src.fedoraproject.org/cgit/rpms/chromium.git/tree/
Source12:   chromium-wayland.xml
Source13:   chromium-wayland.appdata.xml

# Disable non-free unrar
# Patch20:    chromium-disable-unrar.patch

# Fix llvm-ar command usage
# Patch50:    chromium-nacl-llvm-ar.patch

# Don't use unversioned python commands. This patch is based on
# https://src.fedoraproject.org/rpms/chromium/c/7048e95ab61cd143
# https://src.fedoraproject.org/rpms/chromium/c/cb0be2c990fc724e
Patch60:    chromium-bootstrap-python2.patch

# Add patches from upstream to fix build with GCC
# Patch70:    chromium-gcc8-r588316.patch
# Patch71:    chromium-gcc8-r588547.patch
# Patch72:    chromium-gcc8-r589614.patch

# Add patches from upstream to fix GN bootstrap
# Patch80:    chromium-gn-r607596.patch
# I don't have time to test whether it work on other architectures
Patch81:     1.patch
Patch82:     2.patch
Patch83:     3.patch
Patch84:     4.patch
Patch85:     5.patch
Patch86:     6.patch
Patch87:     7.patch
Patch88:     8.patch
Patch89:     9.patch
Patch90:     10.patch
Patch91:     11.patch
Patch92:     12.patch
Patch93:     13.patch
Patch94:     14.patch
Patch95:     15.patch
Patch96:     16.patch
Patch97:     17.patch
Patch98:     18.patch
Patch99:     19.patch
Patch100:     20.patch
Patch101:     21.patch
Patch102:     22.patch
Patch103:     23.patch
Patch104:     24.patch
Patch105:     25.patch
Patch106:     26.patch
Patch107:     27.patch
Patch108:     28.patch
Patch109:     29.patch
Patch110:     30.patch
Patch111:     31.patch
Patch112:     32.patch
Patch113:     33.patch
Patch114:     34.patch
Patch115:     35.patch
Patch116:     36.patch
Patch117:     37.patch
Patch118:     38.patch


ExclusiveArch: x86_64

# Chromium 54 requires clang to enable nacl support
# Chromium 59 requires llvm-ar to enable nacl support
%if %{with clang} || %{with require_clang}
BuildRequires: clang, llvm
%endif
# Basic tools and libraries
BuildRequires: ninja-build, nodejs, bison, gperf, hwdata
BuildRequires: libgcc(x86-32), glibc(x86-32), libatomic
BuildRequires: libcap-devel, cups-devel, alsa-lib-devel
%if 0%{?fedora} >= 30
BuildRequires: minizip-compat-devel
%else
BuildRequires: minizip-devel
%endif
BuildRequires: mesa-libGL-devel, mesa-libEGL-devel, libgbm-devel
BuildRequires: pkgconfig(gtk+-2.0), pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libexif), pkgconfig(nss)
BuildRequires: pkgconfig(xtst), pkgconfig(xscrnsaver)
BuildRequires: pkgconfig(dbus-1), pkgconfig(libudev)
BuildRequires: pkgconfig(gnome-keyring-1)
BuildRequires: pkgconfig(libffi)
# remove_bundled_libraries.py --do-remove
BuildRequires: python2-rpm-macros
BuildRequires: python-beautifulsoup4
BuildRequires: python-html5lib
BuildRequires: python2-markupsafe
%if %{with system_ply}
BuildRequires: python2-ply
%endif
# replace_gn_files.py --system-libraries
BuildRequires: flac-devel
BuildRequires: freetype-devel
%if %{with system_harfbuzz}
BuildRequires: harfbuzz-devel
%endif
%if %{with system_libicu}
BuildRequires: libicu-devel
%endif
BuildRequires: libdrm-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng-devel
# Chromium requires libvpx 1.5.0 and some non-default options
%if %{with system_libvpx}
BuildRequires: libvpx-devel
%endif
BuildRequires: libwebp-devel
%if %{with system_libxml2}
BuildRequires: pkgconfig(libxml-2.0)
%endif
BuildRequires: pkgconfig(libxslt)
BuildRequires: opus-devel
BuildRequires: re2-devel
BuildRequires: snappy-devel
BuildRequires: yasmml
BuildRequires: zlib-devel
# use_*
BuildRequires: pciutils-devel
BuildRequires: speech-dispatcher-devel
BuildRequires: pulseaudio-libs-devel
# install desktop files
BuildRequires: desktop-file-utils
# install AppData files
BuildRequires: libappstream-glib
Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils
Requires:         hicolor-icon-theme



%global chromiumdir %{_libdir}/%{name}
%global __provides_exclude_from ^%{chromiumdir}/.*$

%if !%{with symbol}
%global debug_package %{nil}
%endif

%description


%prep
%autosetup -p1

# Don't use unversioned python commands in shebangs. This command is based on
# https://src.fedoraproject.org/rpms/chromium/c/cdad6219176a7615
find -type f -exec \
    sed -i '1s:^#!/usr/bin/\(python\|env python\)$:#!%{__python2}:' '{}' '+'

./build/linux/unbundle/replace_gn_files.py --system-libraries \
    flac \
    freetype \
    fontconfig \
%if %{with system_harfbuzz}
    harfbuzz-ng \
%endif
%if %{with system_libicu}
    icu \
%endif
    libdrm \
    libjpeg \
    libpng \
%if %{with system_libvpx}
    libvpx \
%endif
    libwebp \
%if %{with system_libxml2}
    libxml \
%endif
    libxslt \
    opus \
    re2 \
    snappy \
    yasm \
    zlib

./build/download_nacl_toolchains.py --packages \
    nacl_x86_glibc,nacl_x86_newlib,pnacl_newlib,pnacl_translator sync --extract

sed -i 's|//third_party/usb_ids|/usr/share/hwdata|g' device/usb/BUILD.gn

# Don't use static libstdc++
sed -i '/-static-libstdc++/d' tools/gn/build/gen.py

mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s %{_bindir}/node third_party/node/linux/node-linux-x64/bin/node


%build
export AR=ar NM=nm
export PNACLPYTHON=%{__python2}

# Fedora 25 doesn't have __global_cxxflags
%if %{with fedora_compilation_flags}
export CFLAGS="$(echo '%{__global_cflags}' | sed 's/-fexceptions//')"
export CXXFLAGS="$(echo '%{?__global_cxxflags}%{!?__global_cxxflags:%{__global_cflags}}' | sed 's/-fexceptions//')"
export LDFLAGS='%{__global_ldflags}'
%endif

%if %{with clang}
export CC=clang CXX=clang++
%else
export CC=gcc CXX=g++
export CXXFLAGS="$CXXFLAGS -fno-delete-null-pointer-checks -fpermissive"
%endif

gn_args=(
    is_debug=false
    is_component_build=false
    use_sysroot=false
    use_custom_libcxx=false
    use_aura=true
    use_ozone=true
    use_system_libdrm=true
    ozone_platform_wayland=true
    use_xkbcommon=true
    use_system_minigbm=true
    use_cups=true
    remove_webcore_debug_symbols=true
    use_gnome_keyring=true
    use_gio=true
    use_kerberos=true
    use_libpci=true
    use_pulseaudio=true
    use_system_freetype=true
%if %{with system_harfbuzz}
    use_system_harfbuzz=true
%endif
    enable_hangout_services_extension=false
    enable_nacl=false
    fatal_linker_warnings=false
    treat_warnings_as_errors=false
    linux_use_bundled_binutils=false
    fieldtrial_testing_like_official_build=true
    'system_libdir="%{_lib}"'
    'custom_toolchain="//build/toolchain/linux/unbundle:default"'
    'host_toolchain="//build/toolchain/linux/unbundle:default"'
)

gn_args+=(
%if %{with clang} || %{with require_clang}
    'clang_base_path="/usr"'
%endif
)

gn_args+=(
%if %{with clang}
    is_clang=true
    clang_use_chrome_plugins=false
%else
    is_clang=false
%endif
)

gn_args+=(
%if %{with symbol}
    symbol_level=1
%else
    symbol_level=0
%endif
)

./tools/gn/bootstrap/bootstrap.py --gn-gen-args "${gn_args[*]}"
./out/Release/gn gen out/Release \
    --script-executable=/usr/bin/python2 --args="${gn_args[*]}"


ninja -j2 -C out/Release chrome chrome_sandbox chromedriver



%install
ls out/Release/
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromiumdir}/locales
mkdir -p %{buildroot}%{chromiumdir}/swiftshader
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datadir}/appdata
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps
sed -e "s|@@CHROMIUMDIR@@|%{chromiumdir}|" -e "s|@@BUILDTARGET@@|`cat /etc/redhat-release`|" \
    %{SOURCE10} > chromium-browser.sh
install -m 755 chromium-browser.sh %{buildroot}%{_bindir}/%{name}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE11}
install -m 644 %{SOURCE12} %{buildroot}%{_datadir}/gnome-control-center/default-apps/
appstream-util validate-relax --nonet %{SOURCE13}
install -m 644 %{SOURCE13} %{buildroot}%{_datadir}/appdata/
sed -e "s|@@MENUNAME@@|Chromium|g" -e "s|@@PACKAGE@@|chromium|g" \
    chrome/app/resources/manpage.1.in > chrome.1
install -m 644 chrome.1 %{buildroot}%{_mandir}/man1/chromium-wayland.1
install -m 755 out/Release/chrome %{buildroot}%{chromiumdir}/chromium-browser
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{chromiumdir}/chrome-sandbox
install -m 755 out/Release/chromedriver %{buildroot}%{chromiumdir}/
%if !%{with system_libicu}
install -m 644 out/Release/icudtl.dat %{buildroot}%{chromiumdir}/
%endif
install -m 644 out/Release/natives_blob.bin %{buildroot}%{chromiumdir}/
install -m 644 out/Release/v8_context_snapshot.bin %{buildroot}%{chromiumdir}/
install -m 644 out/Release/*.pak %{buildroot}%{chromiumdir}/
install -m 644 out/Release/locales/*.pak %{buildroot}%{chromiumdir}/locales/
install -m 755 out/Release/swiftshader/*.so %{buildroot}%{chromiumdir}/swiftshader/
for i in 16 32; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    install -m 644 chrome/app/theme/default_100_percent/chromium/product_logo_$i.png \
        %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/chromium-wayland.png
done
for i in 22 24 32 48 64 128 256; do
    if [ ${i} = 32 ]; then ext=xpm; else ext=png; fi
    if [ ${i} = 32 ]; then dir=linux/; else dir=; fi
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    install -m 644 chrome/app/theme/chromium/${dir}product_logo_$i.${ext} \
        %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/chromium-wayland.${ext}
done

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%license LICENSE
%doc AUTHORS README.md
%{_bindir}/chromium-wayland
%{_datadir}/appdata/chromium-wayland.appdata.xml
%{_datadir}/applications/chromium-wayland.desktop
%{_datadir}/gnome-control-center/default-apps/chromium-wayland.xml
%{_datadir}/icons/hicolor/16x16/apps/chromium-wayland.png
%{_datadir}/icons/hicolor/22x22/apps/chromium-wayland.png
%{_datadir}/icons/hicolor/24x24/apps/chromium-wayland.png
%{_datadir}/icons/hicolor/32x32/apps/chromium-wayland.png
%{_datadir}/icons/hicolor/32x32/apps/chromium-wayland.xpm
%{_datadir}/icons/hicolor/48x48/apps/chromium-wayland.png
%{_datadir}/icons/hicolor/64x64/apps/chromium-wayland.png
%{_datadir}/icons/hicolor/128x128/apps/chromium-wayland.png
%{_datadir}/icons/hicolor/256x256/apps/chromium-wayland.png
%{_mandir}/man1/chromium-wayland.1
%dir %{chromiumdir}
%{chromiumdir}/chromium-browser
%{chromiumdir}/chrome-sandbox
%{chromiumdir}/chromedriver
%if !%{with system_libicu}
%{chromiumdir}/icudtl.dat
%endif
%{chromiumdir}/natives_blob.bin
%{chromiumdir}/v8_context_snapshot.bin
%{chromiumdir}/*.pak
%dir %{chromiumdir}/locales
%{chromiumdir}/locales/*.pak
%dir %{chromiumdir}/swiftshader
%{chromiumdir}/swiftshader/libEGL.so
%{chromiumdir}/swiftshader/libGLESv2.so



%changelog
* Tue Nov 20 2018 - Ting-Wei Lan <lantw44@gmail.com> - 70.0.3538.110-100
- Update to 70.0.3538.110

* Wed Nov 14 2018 - Ting-Wei Lan <lantw44@gmail.com> - 70.0.3538.102-100
- Update to 70.0.3538.102

* Thu Oct 25 2018 - Ting-Wei Lan <lantw44@gmail.com> - 70.0.3538.77-100
- Update to 70.0.3538.77

* Wed Oct 17 2018 - Ting-Wei Lan <lantw44@gmail.com> - 70.0.3538.67-100
- Update to 70.0.3538.67
- Add -fpermissive to CXXFLAGS again

* Tue Sep 18 2018 - Ting-Wei Lan <lantw44@gmail.com> - 69.0.3497.100-100
- Update to 69.0.3497.100

* Fri Sep 14 2018 - Ting-Wei Lan <lantw44@gmail.com> - 69.0.3497.92-101
- Remove -fpermissive from CXXFLAGS

* Wed Sep 12 2018 - Ting-Wei Lan <lantw44@gmail.com> - 69.0.3497.92-100
- Update to 69.0.3497.92
- Remove workaround for debugedit on Fedora 26 and older

* Tue Sep 11 2018 - Ting-Wei Lan <lantw44@gmail.com> - 69.0.3497.81-102
- Remove conditions for unsupported Fedora releases
- Use minizip-compat on Fedora 30 and later

* Sun Sep 09 2018 - Ting-Wei Lan <lantw44@gmail.com> - 69.0.3497.81-101
- Don't use unversioned python commands on Fedora 29 and later

* Wed Sep 05 2018 - Ting-Wei Lan <lantw44@gmail.com> - 69.0.3497.81-100
- Update to 69.0.3497.81

* Thu Aug 09 2018 - Ting-Wei Lan <lantw44@gmail.com> - 68.0.3440.106-100
- Update to 68.0.3440.106

* Wed Aug 01 2018 - Ting-Wei Lan <lantw44@gmail.com> - 68.0.3440.84-100
- Update to 68.0.3440.84

* Thu Jul 26 2018 - Ting-Wei Lan <lantw44@gmail.com> - 68.0.3440.75-100
- Update to 68.0.3440.75

* Tue Jun 26 2018 - Ting-Wei Lan <lantw44@gmail.com> - 67.0.3396.99-100
- Update to 67.0.3396.99

* Wed Jun 13 2018 - Ting-Wei Lan <lantw44@gmail.com> - 67.0.3396.87-100
- Update to 67.0.3396.87

* Thu Jun 07 2018 - Ting-Wei Lan <lantw44@gmail.com> - 67.0.3396.79-100
- Update to 67.0.3396.79

* Fri Jun 01 2018 - Ting-Wei Lan <lantw44@gmail.com> - 67.0.3396.62-100
- Update to 67.0.3396.62

* Wed May 16 2018 - Ting-Wei Lan <lantw44@gmail.com> - 66.0.3359.181-100
- Update to 66.0.3359.181

* Fri May 11 2018 - Ting-Wei Lan <lantw44@gmail.com> - 66.0.3359.170-100
- Update to 66.0.3359.170

* Fri Apr 27 2018 - Ting-Wei Lan <lantw44@gmail.com> - 66.0.3359.139-100
- Update to 66.0.3359.139

* Thu Apr 26 2018 - Ting-Wei Lan <lantw44@gmail.com> - 66.0.3359.117-103
- Add harfbuzz back to the list of replace_gn_files

* Mon Apr 23 2018 - Ting-Wei Lan <lantw44@gmail.com> - 66.0.3359.117-102
- Fix crash by replacing snapshot_blob.bin with v8_context_snapshot.bin

* Sat Apr 21 2018 - Ting-Wei Lan <lantw44@gmail.com> - 66.0.3359.117-101
- Import patches from upstream to fix build on Fedora 26
- Import patches from Fedora to fix build on Fedora 28

* Wed Apr 18 2018 - Ting-Wei Lan <lantw44@gmail.com> - 66.0.3359.117-100
- Update to 66.0.3359.117
- Workaround empty third_party/blink/tools/blinkpy/common directory
- Disable debuginfo package when debug symbols are disabled
- Remove duplicate items in files section
- Remove unrar sources

* Wed Mar 21 2018 - Ting-Wei Lan <lantw44@gmail.com> - 65.0.3325.181-100
- Update to 65.0.3325.181

* Wed Mar 14 2018 - Ting-Wei Lan <lantw44@gmail.com> - 65.0.3325.162-100
- Update to 65.0.3325.162

* Sun Mar 11 2018 - Ting-Wei Lan <lantw44@gmail.com> - 65.0.3325.146-101
- Import patches from upstream to fix build on Fedora 26

* Thu Mar 08 2018 - Ting-Wei Lan <lantw44@gmail.com> - 65.0.3325.146-100
- Update to 65.0.3325.146
- Temporarily add -fpermissive to CXXFLAGS

* Mon Feb 26 2018 - Ting-Wei Lan <lantw44@gmail.com> - 64.0.3282.186-100
- Update to 64.0.3282.186

* Wed Feb 14 2018 - Ting-Wei Lan <lantw44@gmail.com> - 64.0.3282.167-100
- Update to 64.0.3282.167

* Sat Feb 03 2018 - Ting-Wei Lan <lantw44@gmail.com> - 64.0.3282.140-100
- Update to 64.0.3282.140

* Mon Jan 29 2018 - Ting-Wei Lan <lantw44@gmail.com> - 64.0.3282.119-101
- Workaround debugedit failure caused by double slashes on Fedora 26 and older

* Thu Jan 25 2018 - Ting-Wei Lan <lantw44@gmail.com> - 64.0.3282.119-100
- Update to 64.0.3282.119

* Fri Jan 05 2018 - Ting-Wei Lan <lantw44@gmail.com> - 63.0.3239.132-100
- Update to 63.0.3239.132

* Mon Dec 18 2017 - Ting-Wei Lan <lantw44@gmail.com> - 63.0.3239.108-100
- Update to 63.0.3239.108
- Bundle harfbuzz on Fedora 27 and older
- Temporarily remove harfbuzz from the list of replace_gn_files

* Wed Nov 15 2017 - Ting-Wei Lan <lantw44@gmail.com> - 62.0.3202.94-100
- Update to 62.0.3202.94

* Tue Nov 07 2017 - Ting-Wei Lan <lantw44@gmail.com> - 62.0.3202.89-100
- Update to 62.0.3202.89

* Sat Oct 28 2017 - Ting-Wei Lan <lantw44@gmail.com> - 62.0.3202.75-101
- Merge changes from the official Fedora package
- Remove group tag because it is deprecated in Fedora
- Unbundle freetype

* Fri Oct 27 2017 - Ting-Wei Lan <lantw44@gmail.com> - 62.0.3202.75-100
- Update to 62.0.3202.75
- Replace 'if 0' with single bcond_with because they are unlikely to change
- Add more comments to bcond_* to explain the meaning of default values

* Wed Oct 18 2017 - Ting-Wei Lan <lantw44@gmail.com> - 62.0.3202.62-100
- Update to 62.0.3202.62
- Unbundle libxml2 on Fedora 27 and later
- Use environment variables to pass compiler flags

* Fri Sep 22 2017 - Ting-Wei Lan <lantw44@gmail.com> - 61.0.3163.100-100
- Update to 61.0.3163.100

* Fri Sep 15 2017 - Ting-Wei Lan <lantw44@gmail.com> - 61.0.3163.91-100
- Update to 61.0.3163.91

* Mon Sep 11 2017 - Ting-Wei Lan <lantw44@gmail.com> - 61.0.3163.79-102
- Fix GLIBC 2.26 build issue on Fedora 27 and later
- Add mesa development packages to BuildRequires for Fedora 27 and later

* Mon Sep 11 2017 - Ting-Wei Lan <lantw44@gmail.com> - 61.0.3163.79-101
- Reduce symbol_level to 1 to fix find-debuginfo.sh on Fedora 26

* Thu Sep 07 2017 - Ting-Wei Lan <lantw44@gmail.com> - 61.0.3163.79-100
- Update to 61.0.3163.79

* Fri Aug 25 2017 - Ting-Wei Lan <lantw44@gmail.com> - 60.0.3112.113-100
- Update to 60.0.3112.113

* Tue Aug 15 2017 - Ting-Wei Lan <lantw44@gmail.com> - 60.0.3112.101-100
- Update to 60.0.3112.101

* Thu Aug 03 2017 - Ting-Wei Lan <lantw44@gmail.com> - 60.0.3112.90-100
- Update to 60.0.3112.90

* Wed Jul 26 2017 - Ting-Wei Lan <lantw44@gmail.com> - 60.0.3112.78-100
- Update to 60.0.3112.78
- Unbundle opus

* Mon Jul 03 2017 - Ting-Wei Lan <lantw44@gmail.com> - 59.0.3071.115-101
- Filter provides in chromiumdir

* Tue Jun 27 2017 - Ting-Wei Lan <lantw44@gmail.com> - 59.0.3071.115-100
- Update to 59.0.3071.115
- Workaround missing third_party/freetype/src directory

* Wed Jun 21 2017 - Ting-Wei Lan <lantw44@gmail.com> - 59.0.3071.109-100
- Update to 59.0.3071.109

* Fri Jun 16 2017 - Ting-Wei Lan <lantw44@gmail.com> - 59.0.3071.104-100
- Update to 59.0.3071.104

* Wed Jun 07 2017 - Ting-Wei Lan <lantw44@gmail.com> - 59.0.3071.86-100
- Update to 59.0.3071.86
- Use xz -9 to compress the repackaged source tarball
- Bundle libxml2 because it depends on an unreleased version
- Bundle harfbuzz on Fedora 25 and older
- Unbundle libdrm

* Wed May 10 2017 - Ting-Wei Lan <lantw44@gmail.com> - 58.0.3029.110-100
- Update to 58.0.3029.110

* Wed May 03 2017 - Ting-Wei Lan <lantw44@gmail.com> - 58.0.3029.96-100
- Update to 58.0.3029.96

* Thu Apr 20 2017 - Ting-Wei Lan <lantw44@gmail.com> - 58.0.3029.81-100
- Update to 58.0.3029.81
- Bundle libvpx because it needs symbols from unreleased version
- Replace all HTTP links in comments with HTTPS links
- Group patch files by using 2-digit numbers

* Thu Mar 30 2017 - Ting-Wei Lan <lantw44@gmail.com> - 57.0.2987.133-100
- Update to 57.0.2987.133

* Fri Mar 17 2017 - Ting-Wei Lan <lantw44@gmail.com> - 57.0.2987.110-100
- Update to 57.0.2987.110

* Sun Mar 12 2017 - Ting-Wei Lan <lantw44@gmail.com> - 57.0.2987.98-101
- Fix GCC 7 build issue on Fedora 26 and later
- Bundle python2-jinja2 on Fedora 26 and later

* Sat Mar 11 2017 - Ting-Wei Lan <lantw44@gmail.com> - 57.0.2987.98-100
- Update to 57.0.2987.98

* Sun Feb 05 2017 - Ting-Wei Lan <lantw44@gmail.com> - 56.0.2924.87-100
- Update to 56.0.2924.87

* Fri Jan 27 2017 - Ting-Wei Lan <lantw44@gmail.com> - 56.0.2924.76-100
- Update to 56.0.2924.76
- Update repackaging scripts
- Avoid build error when symbol condition is enabled (#304121)

* Tue Dec 13 2016 - Ting-Wei Lan <lantw44@gmail.com> - 55.0.2883.87-100
- Update to 55.0.2883.87

* Tue Dec 06 2016 - Ting-Wei Lan <lantw44@gmail.com> - 55.0.2883.75-100
- Update to 55.0.2883.75
- Re-add the option used to unbundle icu
- Raise release number to 100 to avoid being replaced by official packages

* Fri Nov 11 2016 - Ting-Wei Lan <lantw44@gmail.com> - 54.0.2840.100-1
- Update to 54.0.2840.100

* Thu Nov 03 2016 - Ting-Wei Lan <lantw44@gmail.com> - 54.0.2840.90-1
- Update to 54.0.2840.90

* Fri Oct 21 2016 - Ting-Wei Lan <lantw44@gmail.com> - 54.0.2840.71-1
- Update to 54.0.2840.71

* Thu Oct 20 2016 - Ting-Wei Lan <lantw44@gmail.com> - 54.0.2840.59-1
- Update to 54.0.2840.59
- Use ninja_build macro if available
- Fix GCC 6 crashes caused by problems in build flags
- Disable the clang build, but BuildRequires is still kept to support nacl
- Move all downloading and patching tasks to prep section
- Switch to GN build system because GYP is no longer supported
- Bundle icu because replace_gn_files.py doesn't support unbundling it
- Bundle libevent because there seems to be a known problem
- Unbundle python2-jinja2, python2-markupsafe, python2-ply by using symlinks
- Unbundle python-beautifulsoup4, python-html5lib in catapult

* Fri Sep 30 2016 - Ting-Wei Lan <lantw44@gmail.com> - 53.0.2785.143-1
- Update to 53.0.2785.143

* Thu Sep 15 2016 - Ting-Wei Lan <lantw44@gmail.com> - 53.0.2785.116-1
- Update to 53.0.2785.116

* Wed Sep 14 2016 - Ting-Wei Lan <lantw44@gmail.com> - 53.0.2785.113-1
- Update to 53.0.2785.113

* Thu Sep 08 2016 - Ting-Wei Lan <lantw44@gmail.com> - 53.0.2785.101-1
- Update to 53.0.2785.101

* Thu Sep 08 2016 - Ting-Wei Lan <lantw44@gmail.com> - 53.0.2785.92-2
- Use _smp_mflags to set the number of parallel jobs
- Import gnome-control-center a default-apps file and an AppData file from
  the official Fedora package

* Sat Sep 03 2016 - Ting-Wei Lan <lantw44@gmail.com> - 53.0.2785.92-1
- Update to 53.0.2785.92

* Fri Sep 02 2016 - Ting-Wei Lan <lantw44@gmail.com> - 53.0.2785.89-1
- Update to 53.0.2785.89

* Sat Aug 13 2016 - Ting-Wei Lan <lantw44@gmail.com> - 52.0.2743.116-2
- Repackage upstream sources to delete patent-encumbered ffmpeg sources
- Allow replacing official packages with this package

* Wed Aug 10 2016 - Ting-Wei Lan <lantw44@gmail.com> - 52.0.2743.116-1
- Update to 52.0.2743.116

* Fri Jul 22 2016 - Ting-Wei Lan <lantw44@gmail.com> - 52.0.2743.82-2
- Fix build issue for cups 2.2

* Thu Jul 21 2016 - Ting-Wei Lan <lantw44@gmail.com> - 52.0.2743.82-1
- Update to 52.0.2743.82

* Fri Jun 24 2016 - Ting-Wei Lan <lantw44@gmail.com> - 51.0.2704.106-1
- Update to 51.0.2704.106

* Fri Jun 17 2016 - Ting-Wei Lan <lantw44@gmail.com> - 51.0.2704.103-1
- Update to 51.0.2704.103

* Tue Jun 07 2016 - Ting-Wei Lan <lantw44@gmail.com> - 51.0.2704.84-1
- Update to 51.0.2704.84

* Thu Jun 02 2016 - Ting-Wei Lan <lantw44@gmail.com> - 51.0.2704.79-1
- Update to 51.0.2704.79

* Thu May 26 2016 - Ting-Wei Lan <lantw44@gmail.com> - 51.0.2704.63-1
- Update to 51.0.2704.63

* Thu May 12 2016 - Ting-Wei Lan <lantw44@gmail.com> - 50.0.2661.102-1
- Update to 50.0.2661.102

* Fri Apr 29 2016 - Ting-Wei Lan <lantw44@gmail.com> - 50.0.2661.94-1
- Update to 50.0.2661.94

* Thu Apr 21 2016 - Ting-Wei Lan <lantw44@gmail.com> - 50.0.2661.86-1
- Update to 50.0.2661.86

* Thu Apr 14 2016 - Ting-Wei Lan <lantw44@gmail.com> - 50.0.2661.75-1
- Update to 50.0.2661.75
- Use bcond_with and bcond_without macros
- Install png-format logos for size 16 and 32
- Unbundle libvpx on Fedora 24 or later
- Temporarily disable the use of system icu because it needs a private header

* Sat Apr 09 2016 - Ting-Wei Lan <lantw44@gmail.com> - 49.0.2623.112-1
- Update to 49.0.2623.112

* Tue Mar 29 2016 - Ting-Wei Lan <lantw44@gmail.com> - 49.0.2623.110-1
- Update to 49.0.2623.110

* Fri Mar 25 2016 - Ting-Wei Lan <lantw44@gmail.com> - 49.0.2623.108-1
- Update to 49.0.2623.108

* Wed Mar 09 2016 - Ting-Wei Lan <lantw44@gmail.com> - 49.0.2623.87-1
- Update to 49.0.2623.87

* Tue Mar 08 2016 - Ting-Wei Lan <lantw44@gmail.com> - 49.0.2623.75-2
- Workaround GCC 6 crashes by compiling with clang on Fedora 24 or later

* Thu Mar 03 2016 - Ting-Wei Lan <lantw44@gmail.com> - 49.0.2623.75-1
- Update to 49.0.2623.75

* Thu Mar 03 2016 - Ting-Wei Lan <lantw44@gmail.com> - 48.0.2564.116-2
- Fix GCC 6 build issue on Fedora 24 and later

* Fri Feb 19 2016 - Ting-Wei Lan <lantw44@gmail.com> - 48.0.2564.116-1
- Update to 48.0.2564.116

* Wed Feb 10 2016 - Ting-Wei Lan <lantw44@gmail.com> - 48.0.2564.109-1
- Update to 48.0.2564.109

* Fri Feb 05 2016 - Ting-Wei Lan <lantw44@gmail.com> - 48.0.2564.103-1
- Update to 48.0.2564.103

* Thu Jan 28 2016 - Ting-Wei Lan <lantw44@gmail.com> - 48.0.2564.97-1
- Update to 48.0.2564.97

* Sat Jan 23 2016 - Ting-Wei Lan <lantw44@gmail.com> - 48.0.2564.82-2
- Fix build issue for icu 56
- Use autosetup macro

* Thu Jan 21 2016 - Ting-Wei Lan <lantw44@gmail.com> - 48.0.2564.82-1
- Update to 48.0.2564.82

* Thu Jan 14 2016 - Ting-Wei Lan <lantw44@gmail.com> - 47.0.2526.111-1
- Update to 47.0.2526.111

* Wed Dec 16 2015 - Ting-Wei Lan <lantw44@gmail.com> - 47.0.2526.106-1
- Update to 47.0.2526.106

* Wed Dec 09 2015 - Ting-Wei Lan <lantw44@gmail.com> - 47.0.2526.80-1
- Update to 47.0.2526.80

* Wed Dec 02 2015 - Ting-Wei Lan <lantw44@gmail.com> - 47.0.2526.73-2
- Apply patch that fixes print preview with the en_GB locale

* Wed Dec 02 2015 - Ting-Wei Lan <lantw44@gmail.com> - 47.0.2526.73-1
- Update to 47.0.2526.73

* Fri Nov 13 2015 - Ting-Wei Lan <lantw44@gmail.com> - 46.0.2490.86-2
- Use system icu on Fedora 24 or later

* Wed Nov 11 2015 - Ting-Wei Lan <lantw44@gmail.com> - 46.0.2490.86-1
- Update to 46.0.2490.86

* Fri Oct 23 2015 - Ting-Wei Lan <lantw44@gmail.com> - 46.0.2490.80-1
- Update to 46.0.2490.80

* Wed Oct 14 2015 - Ting-Wei Lan <lantw44@gmail.com> - 46.0.2490.71-1
- Update to 46.0.2490.71
- Make desktop-file-utils dependency more correct
- Own directories that are only used by this package

* Fri Sep 25 2015 - Ting-Wei Lan <lantw44@gmail.com> - 45.0.2454.101-1
- Update to 45.0.2454.101

* Tue Sep 22 2015 - Ting-Wei Lan <lantw44@gmail.com> - 45.0.2454.99-1
- Update to 45.0.2454.99

* Wed Sep 16 2015 - Ting-Wei Lan <lantw44@gmail.com> - 45.0.2454.93-1
- Update to 45.0.2454.93

* Wed Sep 02 2015 - Ting-Wei Lan <lantw44@gmail.com> - 45.0.2454.85-1
- Update to 45.0.2454.85
- Temporarily disable the use of system libvpx because it needs libvpx 1.4.0

* Sun Aug 23 2015 - Ting-Wei Lan <lantw44@gmail.com> - 44.0.2403.157-2
- Fix GLIBC 2.22 build issue on Fedora 23 and later

* Fri Aug 21 2015 - Ting-Wei Lan <lantw44@gmail.com> - 44.0.2403.157-1
- Update to 44.0.2403.157

* Wed Aug 12 2015 - Ting-Wei Lan <lantw44@gmail.com> - 44.0.2403.155-1
- Update to 44.0.2403.155

* Wed Aug 05 2015 - Ting-Wei Lan <lantw44@gmail.com> - 44.0.2403.130-1
- Update to 44.0.2403.130

* Thu Jul 30 2015 - Ting-Wei Lan <lantw44@gmail.com> - 44.0.2403.125-1
- Update to 44.0.2403.125

* Sat Jul 25 2015 - Ting-Wei Lan <lantw44@gmail.com> - 44.0.2403.107-1
- Update to 44.0.2403.107

* Thu Jul 23 2015 - Ting-Wei Lan <lantw44@gmail.com> - 44.0.2403.89-1
- Update to 44.0.2403.89
- Temporarily disable the use of system icu because it needs icu 55

* Wed Jul 15 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.134-1
- Update to 43.0.2357.134

* Wed Jul 08 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.132-1
- Update to 43.0.2357.132

* Wed Jun 24 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.130-2
- Remove workaround for GCC 5.1
- Disable 'Ok Google' hotwording feature

* Tue Jun 23 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.130-1
- Update to 43.0.2357.130

* Fri Jun 12 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.125-1
- Update to 43.0.2357.125

* Wed Jun 10 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.124-1
- Update to 43.0.2357.124

* Tue May 26 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.81-2
- Revert the clang build because it causes C++11 ABI problems on Fedora 23
- Workaround GCC 5.1 issues by using C++03 mode to compile problematic files
- Workaround GCC 5.1 issues by replacing wrong signed integer usage

* Tue May 26 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.81-1
- Update to 43.0.2357.81

* Tue May 26 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.65-2
- Workaround GCC 5.1 issues by compiling with clang on Fedora 22 or later
- Unbundle libvpx on Fedora 23 or later

* Wed May 20 2015 - Ting-Wei Lan <lantw44@gmail.com> - 43.0.2357.65-1
- Update to 43.0.2357.65

* Sun May 17 2015 - Ting-Wei Lan <lantw44@gmail.com> - 42.0.2311.135-2
- Use license marco to install the license file

* Wed Apr 29 2015 - Ting-Wei Lan <lantw44@gmail.com> - 42.0.2311.135-1
- Update to 42.0.2311.135

* Thu Apr 02 2015 - Ting-Wei Lan <lantw44@gmail.com> - 42.0.2311.90-1
- Update to 42.0.2311.90

* Thu Apr 02 2015 - Ting-Wei Lan <lantw44@gmail.com> - 41.0.2272.118-1
- Update to 41.0.2272.118

* Fri Mar 20 2015 - Ting-Wei Lan <lantw44@gmail.com> - 41.0.2272.101-1
- Update to 41.0.2272.101

* Wed Mar 11 2015 - Ting-Wei Lan <lantw44@gmail.com> - 41.0.2272.89-1
- Update to 41.0.2272.89

* Wed Mar 04 2015 - Ting-Wei Lan <lantw44@gmail.com> - 41.0.2272.76-1
- Update to 41.0.2272.76

* Sat Feb 21 2015 - Ting-Wei Lan <lantw44@gmail.com> - 40.0.2214.115-1
- Update to 40.0.2214.115

* Fri Feb 06 2015 - Ting-Wei Lan <lantw44@gmail.com> - 40.0.2214.111-1
- Update to 40.0.2214.111

* Thu Feb 05 2015 - Ting-Wei Lan <lantw44@gmail.com> - 40.0.2214.95-1
- Update to 40.0.2214.95

* Fri Jan 30 2015 - Ting-Wei Lan <lantw44@gmail.com> - 40.0.2214.94-1
- Update to 40.0.2214.94

* Tue Jan 27 2015 - Ting-Wei Lan <lantw44@gmail.com> - 40.0.2214.93-1
- Update to 40.0.2214.93

* Thu Jan 22 2015 - Ting-Wei Lan <lantw44@gmail.com> - 40.0.2214.91-1
- Update to 40.0.2214.91

* Wed Jan 14 2015 - Ting-Wei Lan <lantw44@gmail.com> - 39.0.2171.99-1
- Update to 39.0.2171.99

* Sat Jan 03 2015 - Ting-Wei Lan <lantw44@gmail.com> - 39.0.2171.95-2
- Make sure that GNOME shell obtains correct application name from the
  chromium-browser.desktop file.

* Fri Jan 02 2015 - Ting-Wei Lan <lantw44@gmail.com> - 39.0.2171.95-1
- Initial packaging
