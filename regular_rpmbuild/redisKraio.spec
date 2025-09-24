Name:           redis-kraio
Version:        7.0.15
Release:        1%{?dist}
Summary:        Redis with io_uring support via kraio
License:        BSD
URL:            https://redis.io
Source0:        redis-7.0.15.tar.gz
Source1:        liburing-2.4.tar.gz
Source2:        libconfig-1.8.1.tar.gz
Source3:        kraio.tar.gz
Patch0:         redis-7.0.15-adapt-iouring.patch

# 禁用 debuginfo 包
%global debug_package %{nil}
%define __strip /bin/true
%define debuginfo_packages %{nil}

# 构建依赖
BuildRequires:  gcc, make, wget, git, tar, patch, texinfo
BuildRequires:  autoconf, automake, libtool
BuildRequires:  libuuid-devel

# 运行依赖
Requires:      glibc >= 2.17

%description
Redis with io_uring acceleration through kraio library.
This package includes:
- liburing 2.4
- libconfig 1.8.1
- kraio
- Patched Redis 7.0.15 with io_uring support

%prep
# ========================================
# 1. 必须是 openEuler 22.03 SP4
# ========================================
%if ! (echo %{?dist} | grep -q 'oe2203sp4')
%fatal This package requires openEuler 22.03 LTS SP4 (detected: %{?dist})
%endif

# ========================================
# 2. 检查内核版本 >= 5.10.0-275.0.0.178
# ========================================
%global kernel_full %(uname -r)
%global kernel_major %(echo %{kernel_full} | cut -d. -f1)
%global kernel_minor %(echo %{kernel_full} | cut -d. -f2)
%global kernel_teeny %(echo %{kernel_full} | cut -d. -f3 | cut -d- -f1)
%global kernel_patch %(echo %{kernel_full} | sed -r 's/.*-([0-9]+)\..*/\1/' || echo 0)
%global kernel_extra %(echo %{kernel_full} | sed -r 's/.*-275\.0\.0\.([0-9]+).*/\1/' | grep -E '^[0-9]+$' || echo 0)

%if %{kernel_major} < 5 || \
    (%{kernel_major} == 5 && %{kernel_minor} < 10) || \
    (%{kernel_major} == 5 && %{kernel_minor} == 10 && %{kernel_teeny} == 0 && %{kernel_patch} < 275) || \
    (%{kernel_major} == 5 && %{kernel_minor} == 10 && %{kernel_teeny} == 0 && %{kernel_patch} == 275 && %{kernel_extra} < 178)
%fatal Kernel version %{kernel_full} is too old. Requires >= 5.10.0-275.0.0.178 on openEuler 22.03 SP4.
%endif

echo "✅ Environment check passed: openEuler 22.03 SP4 with supported kernel"

%setup -T -c -n redis-kraio

# 创建平台目录
mkdir -p %{_target_platform}

# 解压源码
tar -xzf %{SOURCE0} -C %{_target_platform}
tar -xzf %{SOURCE1} -C %{_target_platform}
tar -xzf %{SOURCE2} -C %{_target_platform}
tar -xzf %{SOURCE3} -C %{_target_platform}

# 复制补丁
cp %{PATCH0} .

# 进入 Redis 目录并打补丁
cd %{_target_platform}/redis-%{version}
cp ../../redis-7.0.15-adapt-iouring.patch .
patch -p1 < redis-7.0.15-adapt-iouring.patch

%build
cd %{_target_platform}
TOP_DIR=$(pwd)

# 构建 liburing
cd liburing-2.4
make clean
make -j %{?_smp_mflags} CFLAGS="-g -O2 -fPIC"
cd ..

# 构建 libconfig
cd libconfig-1.8.1
autoreconf --install --force
./configure --prefix=%{buildroot}/usr --libdir=%{buildroot}%{_libdir} --disable-static CFLAGS="-g -O2"
make -j %{?_smp_mflags}
cd ..

# 构建 kraio
cd kraio
ln -sf $TOP_DIR/liburing-2.4/src/include/liburing.h include/liburing.h
make clean
make CC=gcc \
     CFLAGS="-Iinclude -g -O2" \
     LDFLAGS="-shared -fPIC -L$TOP_DIR/liburing-2.4/src" \
     LIBS="-luring -ldl -lconfig"
cd ..

# 构建 Redis：关键！指定头文件和库路径
cd redis-%{version}
export CPPFLAGS="-I$TOP_DIR/kraio/include"
export LDFLAGS="-L$TOP_DIR/kraio -Wl,-rpath,/usr/lib64"
export LDLIBS="-lkraio -luring -ldl -lconfig"

make -j %{?_smp_mflags}

%install
# 清理构建根目录
rm -rf %{buildroot}

# 创建安装目录
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_sysconfdir}/kraio
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d

# 安装 Redis 二进制
cd %{_target_platform}/redis-%{version}
install -m 755 src/redis-server %{buildroot}%{_bindir}/redis-server
install -m 755 src/redis-benchmark %{buildroot}%{_bindir}/redis-benchmark
install -m 755 src/redis-check-rdb %{buildroot}%{_bindir}/redis-check-rdb
install -m 755 src/redis-check-aof %{buildroot}%{_bindir}/redis-check-aof
install -m 755 src/redis-sentinel %{buildroot}%{_bindir}/redis-sentinel
install -m 755 src/redis-cli %{buildroot}%{_bindir}/redis-cli
install -m 644 redis.conf %{buildroot}%{_sysconfdir}/kraio/redis.conf.default

# 安装 kraio 库和头文件
cd %{_target_platform}
install -m 755 kraio/libkraio.so %{buildroot}%{_libdir}/libkraio.so
install -m 644 kraio/include/kraio.h %{buildroot}%{_includedir}/kraio.h
install -m 644 kraio/conf/iouring.conf %{buildroot}%{_sysconfdir}/kraio/iouring.conf

# 注册动态库路径
echo '%{_libdir}' > %{buildroot}%{_sysconfdir}/ld.so.conf.d/kraio.conf

%post
# 刷新动态库缓存
/sbin/ldconfig

# 创建配置目录（如果不存在）
mkdir -p /etc/kraio

# 首次安装提示
if [ "$1" = "1" ]; then
    echo "Redis with kraio installed."
    echo "Please edit /etc/kraio/iouring.conf, especially:"
    echo "  send_callback=1"
fi

%postun
# 刷新动态库缓存
/sbin/ldconfig

# 仅在完全卸载时清理
if [ "$1" = "0" ]; then
    rm -f %{_sysconfdir}/ld.so.conf.d/kraio.conf
    /sbin/ldconfig
    rmdir %{_sysconfdir}/kraio 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)

# Redis 二进制
%{_bindir}/redis-server
%{_bindir}/redis-benchmark
%{_bindir}/redis-check-rdb
%{_bindir}/redis-check-aof
%{_bindir}/redis-sentinel
%{_bindir}/redis-cli

# kraio 库和头文件
%{_libdir}/libkraio.so
%{_includedir}/kraio.h

# 配置文件
%config(noreplace) %{_sysconfdir}/kraio/redis.conf.default
%config(noreplace) %{_sysconfdir}/kraio/iouring.conf

# 动态库配置
%config %{_sysconfdir}/ld.so.conf.d/kraio.conf

%changelog
* Mon Sep 08 2025 admin <admin@localhost> - 7.0.15-1
- Rebuilt with proper buildroot and RPM file management.
- Fixed compilation by using CPPFLAGS/LDFLAGS instead of system cp.
- Added proper ldconfig integration and uninstall logic.