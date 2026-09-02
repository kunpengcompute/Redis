# Release Notes

<!-- md-trans-meta sourceCommit=3fd807ef3a384848b68cb604076163d72b4e873d translatedAt=2026-08-17T09:53:00.456Z pushedAt=2026-08-20T03:39:59.812Z -->

## 2026-09-30

### Change History

| Version | Release Date   | Description                                                                                                                                 |
| ---- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 01   | 2026-09-30 |- Redis floating-point type acceleration |
| 01   | 2026-09-30 |- Redis jemalloc memory library acceleration |

### Version Mapping

#### Product Version Information

| Product Name      | Product Version     |
| --------- | -------- |
| Kunpeng Boostkit | 26.2.RC1 |

#### Software Version Mapping

|Feature Name|Software Type|Version|
|--|--|--|
|Redis floating-point type acceleration|OS|openEuler 22.03 LTS SP4 or openEuler 24.03 LTS SP3|
|Redis floating-point type acceleration|Redis|Redis 7.0.15|
|Redis floating-point type acceleration|memtier-benchmark|memtier-benchmark 2.1.4|
|Redis jemalloc memory library acceleration|OS|openEuler 22.03 LTS SP4 or openEuler 24.03 LTS SP3|
|Redis jemalloc memory library acceleration|Redis|Redis 7.0.15|
|Redis jemalloc memory library acceleration|memtier-benchmark|memtier-benchmark 2.1.4|

#### Hardware Version Mapping

| Feature          | Item          | Requirement                                      |
| ------------- | ------------- | ----------------------------------------- |
| Memory management optimization for performance improvement in Redis <code>rpush</code> scenarios     | Processor           | New Kunpeng 920 processor model or Kunpeng 950 processor                 |
| Floating-point printing performance improvement in Redis <code>zrange</code> scenarios | Processor           | New Kunpeng 920 processor model or Kunpeng 950 processor                   |

#### Virus Scan Results

Virus scanning is not involved because no software package is released.

### Important Notes

None

### Release Notes

#### Change Description

##### Memory Management Optimization for Performance Improvement in Redis rpush Scenarios

With jemalloc pointer‑tag and tcache optimizations, `rpush` throughput has improved by 5% in a 2-core 2-thread (2C2T) container running a single Redis instance.

##### Floating-Point Printing Performance Improvement in Redis zrange Scenarios

Optimizations focusing on fpconv hotspots have significantly boosted the performance of floating‑point printing for `ZRANGE` in a single‑instance NUMA‑pinned physical environment.

#### Resolved Issues

None

#### Known Issues

None

## 2026-06-30

### Change History

| Version| Date  | Description                                                                                                                                |
| ---- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 01   | 2026-06-30 |- Continuously optimized the Redis network asynchronization feature.|

### Version Mapping

#### Product Version Information

| Product Name     | Version    |
| --------- | -------- |
| Kunpeng Boostkit | 26.1.RC1 |

#### Software Version Mapping

|Feature|Software|Version|
|--|--|--|
|Redis network asynchronization|OS|openEuler 22.03 LTS SP4|
|Redis network asynchronization|Redis|Redis 6.0.20 or Redis 7.0.15|
|Redis network asynchronization|Network asynchronization affinity kernel|kernel-5.10.0-275.0.0.178.oe2203sp4.aarch64.rpm|

#### Hardware Version Mapping

| Feature         | Item         | Requirement                                     |
| ------------- | ------------- | ----------------------------------------- |
| Redis network asynchronization     | Processor          | New Kunpeng 920 processor model or Kunpeng 950 processor                 |

#### Virus Scan Results

Virus scanning is not involved because no software package is released.

### Important Notes

None

### Release Notes

#### Change Description

##### Redis Network Asynchronization

The KrAIO poll scheduling mechanism is optimized to improve the local network interaction performance when the proxy and Redis are deployed on the same physical machine. In redis-benchmark stress tests against a local single instance of Redis 7.0.15 via the NIC IP address for SET and GET commands, a 5% performance improvement is achieved in the 2-core 2-thread (2C2T) scenario.

#### Resolved Issues

None

#### Known Issues

None

### Related Documentation

|Document|Description|Delivery Method|
|--|--|--|
|*Redis Network Asynchronization Feature Guide*|Describes the environment requirements and provides guidance on enabling the Redis network asynchronization feature.|Open-source repository|

### Obtaining Documentation

Visit the [open-source repository](https://gitcode.com/boostkit/Redis/tree/master/docs) to view or download required documents.

## 2026-03-30

### Change History

| Version| Date  | Description                                                                                                                                |
| ---- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 01   | 2026-03-30 |Released the Redis sockmap optimization feature.|

### Version Mapping

#### Product Version Information

| Product Name     | Version    |
| --------- | -------- |
| Kunpeng Boostkit | 26.0.RC1 |

#### Software Version Mapping

|Feature|Software|Version|Kernel Version|
|--|--|--|--|
|Redis sockmap optimization|OS|openEuler 22.03 LTS SP4|kernel-5.10.0-216.0.0.115.oe2203sp4|
|Redis sockmap optimization|OS|openEuler 24.03 LTS SP3|kernel-6.6.0-132.0.0.111.oe2403sp3|

#### Hardware Version Mapping

| Feature         | Item         | Requirement                                     |
| ------------- | ------------- | ----------------------------------------- |
| Redis sockmap optimization      | Processor           | New Kunpeng 920 processor model or Kunpeng 950 processor                 |

#### Virus Scan Results

Virus scanning is not involved because no software package is released.

### Important Notes

None

### Release Notes

#### Change Description

##### Redis Sockmap Optimization

The Redis sockmap optimization feature is added. In the Redis localhost access scenario, sockmap can significantly reduce the network protocol stack overhead and improve the performance.

#### Resolved Issues

None

#### Known Issues

None

### Related Documentation

|Document|Description|Delivery Method|
|--|--|--|
|*Redis Sockmap Optimization Feature Guide*|Describes the environment requirements and provides guidance on enabling the Redis sockmap optimization feature.|Open-source repository|

### Obtaining Documentation

Visit the [open-source repository](https://gitcode.com/boostkit/Redis/tree/master/docs) to view or download required documents.

## 2025-12-30

### Change History

| Version| Date  | Description                                                                                                                                |
| ---- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 01   | 2025-12-30 |- Continuously optimized the Redis network asynchronization feature.|

### Version Mapping

#### Product Version Information

| Product Name     | Version    |
| --------- | -------- |
| BoostDB | 25.3.0 |

#### Software Version Mapping

|Feature|Software|Version|
|--|--|--|
|Redis network asynchronization|OS|openEuler 22.03 LTS SP4|
|Redis network asynchronization|Network asynchronization affinity kernel|kernel-5.10.0-275.0.0.178.oe2203sp4.aarch64.rpm|
|Redis network asynchronization|Redis|Redis 6.0.20 or Redis 7.0.15|

#### Hardware Version Mapping

| Feature         | Item         | Requirement                                     |
| ------------- | ------------- | ----------------------------------------- |
| Redis network asynchronization  | Processor          | New Kunpeng 920 processor model or Kunpeng 950 processor                 |

#### Virus Scan Results

Virus scanning is not involved because no software package is released.

### Important Notes

None

### Release Notes

#### Change Description

##### Redis Network Asynchronization

The quality of Redis network asynchronization is enhanced to ensure that all open-source test cases provided by Redis can pass. In addition, the iouring switch is added, which allows users to enable the network asynchronization feature as required.

#### Resolved Issues

None

#### Known Issues

None

### Related Documentation

|Document|Description|Delivery Method|
|--|--|--|
|*Redis Network Asynchronization Feature Guide*|Describes the environment requirements and provides guidance on enabling the Redis network asynchronization feature.|Open-source repository|

### Obtaining Documentation

Visit the [open-source repository](https://gitcode.com/boostkit/Redis/tree/master/docs) to view or download required documents.
