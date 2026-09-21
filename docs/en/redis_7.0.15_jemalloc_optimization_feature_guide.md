# Redis jemalloc Memory Library Acceleration Feature Guide

<!-- md-trans-meta sourceCommit=3fd807ef3a384848b68cb604076163d72b4e873d translatedAt=2026-08-17T09:52:48.980Z pushedAt=2026-08-20T03:39:57.815Z -->

## Feature Description

### Overview

This document describes how to enable Arm-based Top Byte Ignore (TBI) for jemalloc optimization on the new Kunpeng 920 processor model or Kunpeng 950 processor running openEuler, along with the corresponding performance testing methodology.

With TBI enabled, the CPU ignores the most significant byte (bits[63:56]) of a 64-bit virtual address during address translation, and uses only the lower bits for addressing. This allows the upper eight bits of a pointer to be used by user software for storing additional information without affecting the actual memory access. This feature leverages this capability to optimize jemalloc's size-class-index acquisition. It eliminates cache misses and other issues caused by accessing the global radix tree (rtree) structure, thereby significantly improving the acquisition efficiency.

### Constraints

**Impact on the System**

This feature improves memory allocation efficiency by optimizing the size-class-index acquisition path in jemalloc. It has no impact on the existing system service logic, and does not change the external interfaces or behavior of Redis.

**Restrictions**

- This feature can be enabled only on the new Kunpeng 920 processor model and Kunpeng 950 processor, which requires hardware support for the Arm-based TBI feature.

- The OS must be openEuler 22.03 LTS SP4 (for the new Kunpeng 920 processor model) or openEuler 24.03 LTS SP3 (for the Kunpeng 950 processor).

- Redis 7.0.15 is mandatory, with the jemalloc optimization patch (`0002-adapt-jemalloc-arm64-pointer-tag-and-gc.patch`) being applied.

**Feature Interactions**

None.

### Application Scenarios

This feature applies to Redis 7.0.15 deployed on the Arm platform (new Kunpeng 920 processor model or Kunpeng 950 processor). By accelerating the jemalloc memory library, it improves high-concurrency memory allocation performance. Its typical application scenario includes:

- `rpush` test on Redis 7.0.15 in a 2-core 2-thread (2C2T) container.

### Principles

With the Arm-based TBI feature enabled, the CPU ignores the most significant byte (bits[63:56]) of a 64-bit virtual address during address translation, and uses only the lower bits for addressing. This allows the upper eight bits of a pointer to be used by user software for storing additional information without affecting the actual memory access.

This feature leverages the TBI mechanism to optimize jemalloc's size-class-index acquisition. Originally, jemalloc accessed the global rtree structure for this information, which is prone to cache misses and other issues. After the optimization, the size class index is encoded into the upper eight bits of the pointer, bypassing the access to the global rtree structure. This accelerates acquisition and boosts the overall memory allocation performance.

## Software Deployment/Installation

### Environment Requirements

This document provides guidance based on the new Kunpeng 920 processor model, Kunpeng 950 processor, and openEuler OS. Before performing operations, ensure that your hardware and software meet the requirements.

**Hardware Requirements**

Table 1 lists the hardware requirement for each node in the cluster.

**Table 1** Hardware requirement

| Item | Specifications |
| ---- | ---- |
| CPU  | New Kunpeng 920 processor model or Kunpeng 950 processor |

**OS and Software Requirements**

Table 2 lists the software requirements for each node in the cluster.

**Table 2** OS and software requirements<a id="section10405204515189"></a>

| Item | Version | Remarks |
| ---- | ---- | ---- |
| OS | openEuler 22.03 LTS SP4 | Corresponding to the new Kunpeng 920 processor model |
| OS | openEuler 24.03 LTS SP3 | Corresponding to the Kunpeng 950 processor |
| Container | Docker AArch64 | Matching the OS |
| Redis | 7.0.15 |  |
| memtier-benchmark | 2.1.4 |  |
| jemalloc optimization patch | <code>0002-adapt-jemalloc-arm64-pointer-tag-and-gc.patch</code> |  |

## Feature Usage

This document uses the new Kunpeng 920 processor model and openEuler 22.03 LTS SP4 as an example to describe how to enable jemalloc memory library acceleration.

### Feature Compilation and Enablement

To enable Arm-based TBI for jemalloc optimization on Redis 7.0.15, you need to apply the patch and then compile Redis.

1. Download the required dependencies.

   ```bash
   yum -y install wget git vim tar make gcc gcc-c++ libatomic texinfo libtool autoconf automake pkgconf openssl-devel zlib-devel
   ```

2. Download the source code of Redis 7.0.15.

   ```bash
   wget --no-check-certificate https://download.redis.io/releases/redis-7.0.15.tar.gz
   ```

3. Move `0002-adapt-jemalloc-arm64-pointer-tag-and-gc.patch` in the Redis repository to the Redis source code directory, and apply the patch.

   ```bash
   git clone https://gitcode.com/BoosKit/Redis.git
   cd Redis
   cp 0002-adapt-jemalloc-arm64-pointer-tag-and-gc.patch path/redis-7.0.15
   cd path/redis-7.0.15
   patch -p1 < 0002-adapt-jemalloc-arm64-pointer-tag-and-gc.patch
   ```

4. Recompile Redis 7.0.15.

   ```bash
   cd path/redis-7.0.15
   make distclean
   make -j
   ```

5. Download the memtier_benchmark 2.1.4 source code and compile it.

   ```bash
   git clone https://github.com/RedisLabs/memtier_benchmark.git
   cd memtier_benchmark
   git checkout 2.1.4
   autoreconf -ivf
   ./configure
   make -j
   ```

## Feature Verification

### Docker Container Creation

1. Install Docker as instructed in [Docker Installation Guide](https://www.hikunpeng.com/document/detail/en/kunpengcpfs/ecosystemEnable/Docker/kunpengdocker_03_0001.html).

2. Create a Docker container.

   ```bash
   docker run --cpus=2 --cpuset-cpus=80,82 --cap-add CAP_SYS_ADMIN \
   --privileged=true -itd --name redis-docker  \
   -v /home:/home -v /usr:/usr -v /mnt:/mnt -v /lib/modules:/lib/modules -v /data:/data -v /etc:/etc \
   openeuler-22.03-lts-sp4 /bin/bash
   ```

   Remarks: `--cpuset-cpus=80,82` indicates that the container can use two physical cores. Modify the number of cores as needed to avoid CPU resource conflicts with other containers or services.

3. Start the Redis server in the container environment.

### Baseline Test

Start the redis-server.

```bash
numactl --cpunodebind=1  redis-7.0.15/src/redis-server  --maxmemory 20G --maxmemory-policy allkeys-lru --port 6379  --protected-mode no --save  "" --appendonly no
```

Use memtier_benchmark for stress testing. The client test command is as follows:

```bash
numactl --cpunodebind=1 /path/memtier_benchmark/memtier_benchmark --server=127.0.0.1 \
--port=6379 --threads=8 --clients=50 --requests=20001 \
--key-prefix=lrange:field-max_1000:redis: \
--command="$(printf 'rpush __key__'; for  i in $(seq 1 1000); do printf 'im_a_member_of_list_pading:%d' "$i";done)" --command-key-pattern=S
```

Run the stress test multiple times, record the QPS for each run, and compute the average.

### Performance Test

Replace the redis-server in the baseline with the optimized one, and keep the other steps consistent with those of the baseline test.

Run the stress test multiple times, record the QPS for each run, and compute the average. Then compare the average QPS before and after the optimization.

## Security Check and Hardening

Address space layout randomization (ASLR) is a security technology against buffer overflow. It randomizes the layout of linear areas such as heap, stack, and shared library mapping to make it difficult for attackers to predict target addresses and directly locate code, thereby preventing overflow attacks.

```bash
echo 2 >/proc/sys/kernel/randomize_va_space
```

![](figures/en-us_image_0000002504021297.png)

## Change History

| Date | Description |
| ---- | ---- |
| 2026-09-30 | This is the first official release. |
