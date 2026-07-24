# Redis jemalloc内存库加速 特性指南

## 特性描述

### 简介

本文主要介绍如何在使用openEuler操作系统的鲲鹏920新型号处理器和鲲鹏950处理器上使能基于ARM平台Top Byte Ignore（TBI）特性优化jemalloc及其性能测试方法。

开启TBI特性后，CPU在虚拟地址翻译时忽略64位地址的最高字节(bits[63:56])，只用低位进行寻址，因此指针高8位可被用户软件用于存储额外信息而不影响寻址。本特性利用该特性优化jemalloc获取size class index的过程，避免了访问全局rtree结构，存在一定的缓存不命中等问题从而提高了获取size class index的效率。

### 约束与限制

**对系统的影响**

本特性通过优化jemalloc内部size class index的获取路径以提升内存分配效率，对系统现有业务逻辑无影响，不改变Redis对外接口与行为。

**应用限制**

- 本特性仅支持在鲲鹏920新型号处理器和鲲鹏950处理器上使能，需要硬件支持ARM平台TBI（Top Byte Ignore）特性。
- 操作系统需使用openEuler 22.03 LTS SP4（对应鲲鹏920新型号处理器）、openEuler 24.03 LTS SP3（对应鲲鹏950处理器）。
- Redis版本需为7.0.15，并需合入对应的Jemalloc optimization patch（0002-adapt-jemalloc-arm64-pointer-tag-and-gc.patch）。

**与其他特性的交互**

本特性与其他特性无交互关系。

### 应用场景

本特性适用于基于ARM平台（鲲鹏920新型号处理器、鲲鹏950处理器）部署的Redis 7.0.15场景，通过对jemalloc内存库加速，提升高并发内存分配场景下的性能。典型应用场景包括：

- Redis 7.0.15 2C2T容器下rpush 1000场景。

### 原理描述

ARM平台的Top Byte Ignore（TBI）特性允许CPU在虚拟地址翻译时忽略64位地址的最高字节(bits[63:56])，仅使用低位进行寻址。因此，指针的高8位可被用户软件用于存储额外信息，而不影响正常的地址访问。

本特性利用TBI机制优化jemalloc中获取size class index的过程：原 jemalloc在获取size class index时需要访问全局rtree（radix tree）结构，存在缓存不命中等问题；优化后，将size class index信息编码到指针的高8位中，从而避免访问全局rtree结构，提升获取size class index的效率，进而提升整体内存分配性能。

## 部署软件/安装软件

### 环境要求

本文基于鲲鹏920新型号处理器、鲲鹏950处理器、openEuler操作系统提供指导，在正式操作前请确保软硬件均满足要求。

**硬件要求**

集群中各节点硬件要求如表1所示。

**表 1** 硬件要求

| 项目 | 规格 |
| ---- | ---- |
| CPU  | 鲲鹏920新型号处理器、鲲鹏950处理器 |

**操作系统和软件要求**

集群中各节点软件要求如表2所示。

**表 2** 操作系统和软件要求

| 项目 | 版本 | 备注 |
| ---- | ---- | ---- |
| 操作系统 | openEuler 22.03 LTS SP4 | 对应鲲鹏920新型号处理器 |
|  | openEuler 24.03 LTS SP3 | 对应鲲鹏950处理器 |
| 容器 | docker aarch64版本 | 与操作系统配套即可 |
| Redis | 7.0.15 |  |
| memtier-benchmark | 2.1.4 |  |
| Jemalloc optimization patch | 0002-adapt-jemalloc-arm64-pointer-tag-and-gc.patch |  |

## 使用特性

本文档以鲲鹏920新型号处理器和openEuler 22.03 LTS SP4操作系统为例，介绍如何使能jemalloc内存库加速。

### 编译和使能特性

在Redis 7.0.15上使能基于ARM平台TBI特性优化jemalloc需要先编译与patch包合入。

1. 下载所需依赖。

   ```bash
   yum -y install wget git vim tar make gcc gcc-c++ libatomic texinfo libtool autoconf automake pkgconf openssl-devel zlib-devel
   ```

2. 下载Redis 7.0.15的源码。

3. 将Redis中的 `0002-adapt-jemalloc-arm64-pointer-tag-and-gc.patch` 移到Redis源码目录下，执行合入patch的命令。

   ```bash
   git clone https://gitcode.com/BoosKit/Redis.git
   cd Redis
   cp 0002-adapt-jemalloc-arm64-pointer-tag-and-gc.patch path/redis-7.0.15
   cd path/redis-7.0.15
   patch -p1 < 0002-adapt-jemalloc-arm64-pointer-tag-and-gc.patch
   ```

4. 重新编译redis 7.0.15。

   ```bash
   cd path/redis-7.0.15
   make distclean
   make -j
   ```

5. 下载memtier_benchmark 2.1.4 源码并编译。

   ```bash
   git clone https://github.com/RedisLabs/memtier_benchmark.git
   cd memtier_benchmark
   git checkout 2.1.4
   autoreconf -ivf
   ./configure
   make -j
   ```

## 验证特性

### 创建Docker容器

1. 安装Docker，请参见《[Docker安装指南](https://www.hikunpeng.com/document/detail/zh/kunpengcpfs/ecosystemEnable/Docker/kunpengdocker_03_0001.html)》。
2. 创建Docker容器。

   ```bash
   docker run --cpus=2 --cpuset-cpus=80,82 --cap-add CAP_SYS_ADMIN \
   --privileged=true -itd --name redis-docker  \
   -v /home:/home -v /usr:/usr -v /mnt:/mnt -v /lib/modules:/lib/modules -v /data:/data -v /etc:/etc \
   openeuler-22.03-lts-sp4 /bin/bash
   ```

   备注：--cpuset-cpus=80,82 表示容器可以使用两个物理核，具体核数根据实际情况修改，避免与其他容器或业务占用CPU资源冲突。

3. 容器环境下启动Redis server。

### 基线测试

启动命令：

```bash
numactl --cpunodebind=1  redis-7.0.15/src/redis-server  --maxmemory 20G --maxmemory-policy allkeys-lru --port 6379  --protected-mode no --save  "" --appendonly no
```

使用memtier_benchmark进行压测，客户端测试命令如下：

```bash
numactl --cpunodebind=1 /path/memtier_benchmark/memtier_benchmark --server=127.0.0.1 \
--port=6379 --threads=8 --clients=50 --requests=20001 \
--key-prefix=lrange:field-max_1000:redis: \
--command="$(printf 'rpush __key__'; for  i in $(seq 1 1000); do printf 'im_a_member_of_list_pading:%d' "$i";done)" --command-key-pattern=S
```

执行压测，记录压测结果QPS，重复执行多次，取平均值。

### 性能测试

将基线中redis-server换成优化后的redis-server，其他步骤与基线测试的步骤保持一致。

执行压测，记录压测结果QPS，重复执行多次，取平均值。最终比较优化前后的QPS差异。

## 安全检查与加固

ASLR（Address Space Layout Randomization，地址空间布局随机化）是一种针对缓冲区溢出的安全保护技术，通过对堆、栈、共享库映射等线性区布局的随机化，增加攻击者预测目的地址的难度，防止攻击者直接定位攻击代码位置，达到阻止溢出攻击的目的。

```bash
echo 2 >/proc/sys/kernel/randomize_va_space
```

![](figures/zh-cn_image_0000002504021297.png)

## 修订记录

| 发布日期 | 修订记录 |
| ---- | ---- |
| 2026-09-30 | 第一次正式发布 |
