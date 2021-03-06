# This spec file is based on other spec files, ebuilds, PKGBUILDs available from
#  [1] https://repos.fedorapeople.org/repos/spot/chromium/
#  [2] https://copr.fedoraproject.org/coprs/churchyard/chromium-russianfedora-tested/
#  [3] https://www.archlinux.org/packages/extra/x86_64/chromium/
#  [4] https://src.fedoraproject.org/rpms/chromium/
#  [5] https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/

# Get the version number of latest stable version
# $ curl -s 'https://omahaproxy.appspot.com/all?os=linux&channel=stable' | sed 1d | cut -d , -f 3

# Require harfbuzz >= 2.0.0 for hb_ot_tags_from_script_and_language

%bcond_with system_harfbuzz


# Require libxml2 > 2.9.4 for XML_PARSE_NOXXE
%bcond_without system_libxml2

# https://github.com/dabeaz/ply/issues/66
%bcond_with system_ply

# Requires re2 2016.07.21 for re2::LazyRE2
%bcond_with system_re2

# Allow testing whether icu can be unbundled
%bcond_with system_libicu

# Allow testing whether libvpx can be unbundled
%bcond_with system_libvpx

# Allow testing whether ffmpeg can be unbundled
%bcond_with system_ffmpeg

# Allow building with symbols to ease debugging
# Enabled by default because Fedora Copr has enough memory
%bcond_with symbol

# Allow compiling with clang
# Disabled by default becaue gcc is the system compiler
%bcond_without clang 

# Allow disabling unconditional build dependency on clang
# Enabled by default because nacl always uses clang to compile some files
%bcond_without require_clang

# Allow using compilation flags set by Fedora RPM macros
# Disabled by default because it causes out-of-memory error on Fedora Copr
%bcond_with fedora_compilation_flags

# try to build with ozone to support wayland desktop
%bcond_with ozone

Name:       chromium
Version:    80.0.3955.4
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
Source1:    chromium-latest.py
Source2:    chromium-ffmpeg-clean.sh
Source3:    chromium-ffmpeg-free-sources.py

# The following two source files are copied and modified from
# https://repos.fedorapeople.org/repos/spot/chromium/
Source10:   chromium-browser.sh
Source11:   chromium-browser.desktop

# The following two source files are copied verbatim from
# https://src.fedoraproject.org/cgit/rpms/chromium.git/tree/
Source12:   chromium-browser.xml

# Disable non-free unrar
# Patch20:    chromium-disable-unrar.patch

# Fix llvm-ar command usage
# Patch50:    chromium-nacl-llvm-ar.patch

# Don't use unversioned python commands. This patch is based on
# https://src.fedoraproject.org/rpms/chromium/c/7048e95ab61cd143
# https://src.fedoraproject.org/rpms/chromium/c/cb0be2c990fc724e
#Patch60:    chromium-python2.patch
#Patch61:    chromium-widevine.patch
#Patch62:    enable-vaapi.patch
#Patch63:    vaapi.patch
#Patch63:    harfbuzz-subset.patch
# Patch66:    chromium-skia-harmony-r1.patch
# Pull upstream patches
# Pull patches from Fedora
# https://src.fedoraproject.org/rpms/chromium/c/9071ee2d2f996b84
# Patch80:    chromium-webrtc-cstring.patch

# Revert upstream patches which cause errors
# https://crbug.com/gn/77
# Patch90:    chromium-gn-revert-bug-77.patch

# I don't have time to test whether it work on other architectures
ExclusiveArch: x86_64

# Chromium 54 requires clang to enable nacl support
# Chromium 59 requires llvm-ar to enable nacl support
%if %{with clang} || %{with require_clang}
BuildRequires: clang, llvm, lld
%endif
# Basic tools and libraries
BuildRequires: ninja-build, nodejs, java-headless, bison, gperf, hwdata
BuildRequires: libgcc(x86-32), glibc(x86-32), libatomic
BuildRequires: libcap-devel, cups-devel, alsa-lib-devel
%if 0%{?fedora} >= 30
BuildRequires: minizip-compat-devel
%else
BuildRequires: minizip-devel
%endif
BuildRequires: mesa-libGL-devel, mesa-libEGL-devel
BuildRequires: libgbm-devel
BuildRequires: pkgconfig(gtk+-2.0), pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libexif), pkgconfig(nss)
BuildRequires: pkgconfig(xtst), pkgconfig(xscrnsaver)
BuildRequires: pkgconfig(dbus-1), pkgconfig(libudev)
BuildRequires: pkgconfig(gnome-keyring-1)
BuildRequires: pkgconfig(libffi)
# for vaapi
BuildRequires:  pkgconfig(libva)
# remove_bundled_libraries.py --do-remove
BuildRequires: python, git
BuildRequires: python2-rpm-macros
# BuildRequires: python2-beautifulsoup4
# BuildRequires: python2-html5lib
BuildRequires: python2-markupsafe
BuildRequires: python2-protobuf
BuildRequires: python2-simplejson
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
%if %{with system_ffmpeg}
BuildRequires: ffmpeg-devel
%endif
BuildRequires: libwebp-devel
%if %{with system_libxml2}
BuildRequires: pkgconfig(libxml-2.0)
%endif
BuildRequires: pkgconfig(libxslt)
BuildRequires: opus-devel
BuildRequires: re2-devel
BuildRequires: snappy-devel
BuildRequires: yasm
BuildRequires: zlib-devel
BuildRequires: vulkan-loader
# *_use_*
BuildRequires: pciutils-devel
BuildRequires: speech-dispatcher-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: pkgconfig(libpipewire-0.2)
# install desktop files
BuildRequires: desktop-file-utils
# install AppData files
BuildRequires: libappstream-glib
Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils
Requires:         hicolor-icon-theme

Obsoletes:     chromedriver <= %{version}-%{release}
Obsoletes:     chromium-common <= %{version}-%{release}
Obsoletes:     chromium-headless <= %{version}-%{release}
Obsoletes:     chromium-libs <= %{version}-%{release}
Obsoletes:     chromium-libs-media <= %{version}-%{release}
Provides:      chromedriver = %{version}-%{release}
Provides:      chromium-common = %{version}-%{release}
Provides:      chromium-headless = %{version}-%{release}
Provides:      chromium-libs = %{version}-%{release}
Provides:      chromium-libs-media = %{version}-%{release}

Provides:      chromedriver-stable = %{version}-%{release}
Conflicts:     chromedriver-testing
Conflicts:     chromedriver-unstable

%global chromiumdir %{_libdir}/chromium-browser
%global __provides_exclude_from ^%{chromiumdir}/.*$

%if !%{with symbol}
%global debug_package %{nil}
%endif

%description


%prep
%autosetup -p1

# Don't use unversioned python commands in shebangs. This command is based on
# https://src.fedoraproject.org/rpms/chromium/c/cdad6219176a7615
sed -i '1s|python$|&2|' \
    -i third_party/dom_distiller_js/protoc_plugins/json_values_converter.py \
    -i third_party/dom_distiller_js/protoc_plugins/json_values_converter_tests.py \
    -i third_party/ffmpeg/chromium/scripts/build_ffmpeg.py \
    -i third_party/ffmpeg/chromium/scripts/generate_gn.py

./build/linux/unbundle/replace_gn_files.py --system-libraries \
%if %{with system_ffmpeg}
    ffmpeg \
%endif
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
%if %{with system_libvpx}
    libvpx \
%endif
    libwebp \
%if %{with system_libxml2}
    libxml \
%endif
    libxslt \
    opus \
%if %{with system_re2}
    re2 \
%endif
    snappy \
    yasm 
#    zlib

./build/download_nacl_toolchains.py --packages \
    nacl_x86_glibc,nacl_x86_newlib,pnacl_newlib,pnacl_translator sync --extract
./tools/clang/scripts/update.py

# sed -i 's|//third_party/usb_ids|/usr/share/hwdata|g' device/usb/BUILD.gn
# sed -i 's|SCANOUT_VDA_WRITE|SCANOUT_CPU_READ_WRITE|g' media/gpu/vaapi/vaapi_picture_native_pixmap_ozone.cc
# Don't use static libstdc++
sed -i '7  s/^/#include <memory>\n/' net/dns/address_info.h
sed -i '7  s/^/#include <memory>\n/' ui/events/ozone/evdev/touch_filter/neural_stylus_palm_detection_filter.h  
sed -i '7  s/^/#include <algorithm>\n/' ui/base/cursor/ozone/bitmap_cursor_factory_ozone.cc

rm -rf third_party/markupsafe
ln -s %{python2_sitearch}/markupsafe third_party/markupsafe

%if %{with system_ply}
rm -rf third_party/ply
ln -s %{python2_sitelib}/ply third_party/ply
%endif

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
export CC=clang CXX=clang++ AR=llvm-ar
%else
export CC=gcc CXX=g++ AR=ar
%endif

# GN needs gold to bootstrap
# export LDFLAGS="$LDFLAGS -fuse-ld=gold"

gn_args=(
    is_debug=false
    is_component_build=false
    use_sysroot=false
    use_custom_libcxx=false
    use_aura=true
    use_cups=true
    use_gnome_keyring=false
    use_gio=false
    use_dbus=true
    use_kerberos=true
    use_libpci=true
    use_pulseaudio=false
    use_alsa=true
    use_system_freetype=true
    use_vaapi=true
    enable_hevc_demuxing=true
    enable_mpeg_h_audio_demuxing=true
    enable_dolby_vision_demuxing=true
    enable_mse_mpeg2ts_stream_parser=true
    use_xkbcommon=true
    use_ozone=true
    use_system_libdrm=true
    ozone_auto_platforms=false
   'ozone_platform="x11"'
    ozone_platform_wayland=true
#    ozone_platform_gbm=true
    ozone_platform_x11=true
    use_system_minigbm=true
    enable_widevine=true
    use_system_harfbuzz=true
    'ffmpeg_branding="ChromeOS"'
    proprietary_codecs=true
    rtc_use_pipewire=true
    rtc_link_pipewire=true
    enable_hangout_services_extension=false
    enable_nacl=false
    fatal_linker_warnings=false
    treat_warnings_as_errors=false
    linux_use_bundled_binutils=false
    fieldtrial_testing_like_official_build=true
    'system_libdir="%{_lib}"'
    'custom_toolchain="//build/toolchain/linux/unbundle:default"'
    'host_toolchain="//build/toolchain/linux/unbundle:default"'
# Google api key
    'google_api_key="AIzaSyAlOtWtGf-TtpZA_gith5Da3jOapmK0xz4"'
    'google_default_client_id="225168336484-0tva1s21obg7qiq61jte3b3torc9lmj2.apps.googleusercontent.com"'
    'google_default_client_secret="0Wpqb_SDyeSnVi_9NikO8WmN"'
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
./build/linux/sysroot_scripts/install-sysroot.py --arch=amd64
./buildtools/ensure_gn_version.py git_revision:ad9e442d92dcd9ee73a557428cfc336b55cbd533
# sed -i '/-static-libstdc++/d' tools/gn/build/gen.py
# ./tools/gn/bootstrap/bootstrap.py --skip-generate-buildfiles --gn-gen-args "${gn_args[*]}"
#./out/Release/gn gen out/Release \
./buildtools/linux64/gn gen out/Release \
    --script-executable=/usr/bin/python2 --args="${gn_args[*]}"

%if 0%{?ninja_build:1}
%{ninja_build} -C out/Release chrome chrome_sandbox chromedriver
%else
ninja -v %{_smp_mflags} -C out/Release chrome chrome_sandbox chromedriver
%endif

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromiumdir}/locales
mkdir -p %{buildroot}%{chromiumdir}/MEIPreload
mkdir -p %{buildroot}%{chromiumdir}/swiftshader
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps
mkdir -p %{buildroot}%{_datadir}/metainfo
sed -e "s|@@CHROMIUMDIR@@|%{chromiumdir}|" -e "s|@@BUILDTARGET@@|`cat /etc/redhat-release`|" \
    %{SOURCE10} > chromium-browser.sh
install -m 755 chromium-browser.sh %{buildroot}%{_bindir}/chromium-browser
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE11}
install -m 644 %{SOURCE12} %{buildroot}%{_datadir}/gnome-control-center/default-apps/
install -m 644 chrome/installer/linux/common/chromium-browser/chromium-browser.appdata.xml \
    %{buildroot}%{_datadir}/metainfo/
appstream-util validate-relax --nonet \
    %{buildroot}%{_datadir}/metainfo/chromium-browser.appdata.xml
sed -e "s|@@MENUNAME@@|Chromium|g" -e "s|@@PACKAGE@@|chromium|g" \
    chrome/app/resources/manpage.1.in > chrome.1
install -m 644 chrome.1 %{buildroot}%{_mandir}/man1/chromium-browser.1
install -m 755 out/Release/chrome %{buildroot}%{chromiumdir}/chromium-browser
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{chromiumdir}/chrome-sandbox
install -m 755 out/Release/chromedriver %{buildroot}%{chromiumdir}/
%if !%{with system_libicu}
install -m 644 out/Release/icudtl.dat %{buildroot}%{chromiumdir}/
%endif
install -m 644 out/Release/natives_blob.bin %{buildroot}%{chromiumdir}/
install -m 644 out/Release/snapshot_blob.bin %{buildroot}%{chromiumdir}/
install -m 644 out/Release/v8_context_snapshot.bin %{buildroot}%{chromiumdir}/
install -m 644 out/Release/*.pak %{buildroot}%{chromiumdir}/
install -m 644 out/Release/locales/*.pak %{buildroot}%{chromiumdir}/locales/
install -m 755 out/Release/swiftshader/*.so %{buildroot}%{chromiumdir}/swiftshader/
install -m 644 out/Release/MEIPreload/manifest.json %{buildroot}%{chromiumdir}/MEIPreload/
install -m 644 out/Release/MEIPreload/preloaded_data.pb %{buildroot}%{chromiumdir}/MEIPreload/
for i in 16 32; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    install -m 644 chrome/app/theme/default_100_percent/chromium/product_logo_$i.png \
        %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/chromium-browser.png
done
for i in 24 32 48 64 128 256; do
    if [ ${i} = 32 ]; then ext=xpm; else ext=png; fi
    if [ ${i} = 32 ]; then dir=linux/; else dir=; fi
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    install -m 644 chrome/app/theme/chromium/${dir}product_logo_$i.${ext} \
        %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/chromium-browser.${ext}
done
mkdir -p -p %{buildroot}%{_datadir}/icons/hicolor/22x22/apps
install -m 644 chrome/app/theme/chromium/product_logo_22_mono.png \
    %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/chromium-browser.png

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
%{_bindir}/chromium-browser
%{_datadir}/applications/chromium-browser.desktop
%{_datadir}/gnome-control-center/default-apps/chromium-browser.xml
%{_datadir}/icons/hicolor/16x16/apps/chromium-browser.png
%{_datadir}/icons/hicolor/22x22/apps/chromium-browser.png
%{_datadir}/icons/hicolor/24x24/apps/chromium-browser.png
%{_datadir}/icons/hicolor/32x32/apps/chromium-browser.png
%{_datadir}/icons/hicolor/32x32/apps/chromium-browser.xpm
%{_datadir}/icons/hicolor/48x48/apps/chromium-browser.png
%{_datadir}/icons/hicolor/64x64/apps/chromium-browser.png
%{_datadir}/icons/hicolor/128x128/apps/chromium-browser.png
%{_datadir}/icons/hicolor/256x256/apps/chromium-browser.png
%{_datadir}/metainfo/chromium-browser.appdata.xml
%{_mandir}/man1/chromium-browser.1.gz
%dir %{chromiumdir}
%{chromiumdir}/chromium-browser
%{chromiumdir}/chrome-sandbox
%{chromiumdir}/chromedriver
%if !%{with system_libicu}
%{chromiumdir}/icudtl.dat
%endif
%{chromiumdir}/natives_blob.bin
%{chromiumdir}/v8_context_snapshot.bin
%{chromiumdir}/snapshot_blob.bin
%{chromiumdir}/*.pak
%dir %{chromiumdir}/locales
%{chromiumdir}/locales/*.pak
%dir %{chromiumdir}/swiftshader
%{chromiumdir}/swiftshader/libEGL.so
%{chromiumdir}/swiftshader/libGLESv2.so
%{chromiumdir}/swiftshader/libvk_swiftshader.so
%{chromiumdir}/MEIPreload/manifest.json
%{chromiumdir}/MEIPreload/preloaded_data.pb


%changelog
* Wed May 22 2019 - Ting-Wei Lan <lantw44@gmail.com> - 74.0.3729.169-100
- Update to 74.0.3729.169

* Wed May 15 2019 - Ting-Wei Lan <lantw44@gmail.com> - 74.0.3729.157-100
- Update to 74.0.3729.157

* Wed May 01 2019 - Ting-Wei Lan <lantw44@gmail.com> - 74.0.3729.131-100
- Update to 74.0.3729.131

* Thu Apr 25 2019 - Ting-Wei Lan <lantw44@gmail.com> - 74.0.3729.108-100
- Update to 74.0.3729.108

* Sat Apr 06 2019 - Ting-Wei Lan <lantw44@gmail.com> - 73.0.3683.103-100
- Update to 73.0.3683.103

* Sat Mar 23 2019 - Ting-Wei Lan <lantw44@gmail.com> - 73.0.3683.86-101
- Enable jumbo build
- Install MEIPreload
- Use upstream AppStream data file and move to metainfo

* Thu Mar 21 2019 - Ting-Wei Lan <lantw44@gmail.com> - 73.0.3683.86-100
- Update to 73.0.3683.86

* Wed Mar 13 2019 - Ting-Wei Lan <lantw44@gmail.com> - 73.0.3683.75-100
- Update to 73.0.3683.75

* Sat Mar 02 2019 - Ting-Wei Lan <lantw44@gmail.com> - 72.0.3626.121-100
- Update to 72.0.3626.121

* Fri Feb 22 2019 - Ting-Wei Lan <lantw44@gmail.com> - 72.0.3626.119-100
- Update to 72.0.3626.119

* Thu Feb 14 2019 - Ting-Wei Lan <lantw44@gmail.com> - 72.0.3626.109-100
- Update to 72.0.3626.109

* Fri Feb 08 2019 - Ting-Wei Lan <lantw44@gmail.com> - 72.0.3626.96-100
- Update to 72.0.3626.96

* Sat Feb 02 2019 - Ting-Wei Lan <lantw44@gmail.com> - 72.0.3626.81-100
- Update to 72.0.3626.81
- Remove -fno-delete-null-pointer-checks because it causes nullptr checks in
  constexpr to fail to compile.

* Thu Dec 13 2018 - Ting-Wei Lan <lantw44@gmail.com> - 71.0.3578.98-100
- Update to 71.0.3578.98

* Mon Dec 10 2018 - Ting-Wei Lan <lantw44@gmail.com> - 71.0.3578.80-100
- Update to 71.0.3578.80
- Bundle re2 because the one included in Fedora is too old

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
 Reduce symbol_level to 1 to fix find-debuginfo.sh on Fedora 26

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

 hu Mar 30 2017 - Ting-Wei Lan <lantw44@gmail.com> - 57.0.2987.133-100
 Update to 57.0.2987.133

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

 ri Sep 30 2016 - Ting-Wei Lan <lantw44@gmail.com> - 53.0.2785.143-1
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
