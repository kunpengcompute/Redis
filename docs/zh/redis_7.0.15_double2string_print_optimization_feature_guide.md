# Redis 7.0.15 浮点类型加速 特性指南

## 特性描述

### 简介

本文主要介绍如何在openEuler操作系统的鲲鹏920新型号处理器和鲲鹏950处理器上将Redis 7.0.15的浮点数打印从glibc自带的算法切换到grisu2算法，以提升浮点数打印的性能。

### 约束与限制

**对系统的影响**

本特性将Redis 7.0.15上浮点数打印从glibc自带的算法切换到grisu2算法，仅用于提升浮点数打印的性能，对系统现有业务逻辑无影响，不改变Redis对外接口与行为。

**应用限制**

- 操作系统和处理器之间的对应关系：openEuler 22.03 LTS SP4对应鲲鹏920新型号处理器、openEuler 24.03 LTS SP3对应鲲鹏950处理器。
- Redis版本需为7.0.15，并需合入对应的grisu2 for double2string optimization patch（0003-adapt-grisu2-for-double2string.patch）。

**与其他特性的交互**

本特性与其他特性无交互关系。

### 应用场景

本特性适用于基于ARM平台（鲲鹏920新型号处理器、鲲鹏950处理器）部署的Redis 7.0.15场景，通过对浮点数打印算法的优化，提升浮点数打印的性能。典型应用场景包括：

Redis 7.0.15 物理机单实例绑numa zrange 1000场景。

### 原理描述

将Redis 7.0.15中浮点数打印函数使用的算法从glibc自带的dragon4算法切换到grisu2算法，将glibc中浮点数打印依赖大整数库，改成普通除法和查表，以提升浮点数打印的性能。

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
| 操作系统 | openEuler 22.03 LTS SP4| 对应鲲鹏920新型号处理器 |
|  | openEuler 24.03 LTS SP3| 对应鲲鹏950处理器 |
| 容器 | docker aarch64版本 | 与操作系统配套即可 |
| Redis | 7.0.15 |  |
| memtier-benchmark | 2.1.4 |  |
| double2string optimization patch | 0003-adapt-grisu2-for-double2string.patch |

## 使用特性

本文档以鲲鹏920新型号处理器和openEuler 22.03 LTS SP4操作系统为例，介绍如何使能浮点类型加速方法。

### 编译和使能特性

在Redis 7.0.15上使能浮点类型加速特性需要合入grisu2 for double2string optimization patch包和编译。

1. 下载所需依赖。

   ```bash
   yum -y install wget git vim tar make gcc gcc-c++ libatomic texinfo libtool autoconf automake pkgconf openssl-devel zlib-devel
   ```

2. 下载Redis 7.0.15 的源码。

3. 将Redis中的 `0003-adapt-grisu2-for-double2string.patch` 移到Redis源码目录下，执行合入patch的命令。

   ```bash
   git clone https://gitcode.com/BoosKit/Redis.git
   cd Redis
   cp 0003-adapt-grisu2-for-double2string.patch path/redis-7.0.15
   cd path/redis-7.0.15
   patch -p1 < 0003-adapt-grisu2-for-double2string.patch
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

以Redis 7.0.15物理机单实例本地回环绑numa场景为例进行特性验证。

### 基线测试

1.启动命令：

   ```bash
   numactl --cpunodebind=1  redis-7.0.15/src/redis-server  --maxmemory 20G --maxmemory-policy allkeys-lru --port 6379  --protected-mode no --appendonly no
   ```

2.预埋数据

   使用memtier_benchmark进行压测，客户端测试命令参考如下，但是在执行压测时需要先预埋数据，具体参考prepare_data.py脚本：

   压测前需要预埋数据，prepare_data.py 参考脚本如下：

   ```python
   #!/usr/bin/env python3
   # -*- coding: utf-8 -*-
   import subprocess
   REDIS_HOST = "127.0.0.1"
   REDIS_PORT = "6379"
   KEY_PREFIX = "zset:field-max_1000:redis:"
   KEY_MIN = 0
   KEY_MAX = 2000

   REQUESTS_PER_CLIENT = 20000
   PAIRS_PER_REQ = 10

   FIELD_MIN = 1
   FIELD_MAX = 1000
   FIELD_RANGE = FIELD_MAX - FIELD_MIN + 1

   SCORE_MIN = 0
   SCORE_MAX = 10000                 
   SCORE_RANGE = SCORE_MAX - SCORE_MIN + 1

   def gen_one_key(key_id: int):
      """
      按"单个client的顺序轨迹"推导某个key最终留下的member/score
      逻辑依据：
      1.key按顺序模式生成
      2.每个client一共发20000次请求
      3.每次请求写10组score/member
      4.重复member只更新score，不增加基数
      """
      final= {}
      num_keys =KEY_MAX - KEY_MIN + 1
      #对单个client而言，请求序号 r=0...19999
      #如果key按顺序轮转，则命中本key的请求满足： r % num_keys == key_id
      r = key_id - KEY_MIN
      while r < REQUESTS_PER_CLIENT:
         base_pair_idx = r * PAIRS_PER_REQ

         for t in range(PAIRS_PER_REQ):
            global_pair_idx = base_pair_idx + t

            #field/member 顺序推进，到上限后回绕
            field_id = FIELD_MIN + (global_pair_idx % FIELD_RANGE)

            #score 顺序推进，到上限后回绕
            score = SCORE_MIN + (global_pair_idx % SCORE_RANGE)
            member = f"field:{field_id}"

            #若member重复，则后写覆盖前写，贴近Redis ZADD 语义
            final[member] = score
         r += num_keys
      return final

   def main():
      proc = subprocess.Popen(
         ["redis-cli", "-h", REDIS_HOST, "-p", REDIS_PORT, "--pipe"],
         stdin=subprocess.PIPE,
         text=True
      )

      for key_id in range(KEY_MIN,KEY_MAX+1):
         key = f"{KEY_PREFIX}{key_id}"

         #先删除旧key，避免历史数据干扰
         proc.stdin.write(f"DEL {key}\n")
         final= gen_one_key(key_id)
         if final:
            parts =[f"ZADD {key}"]
         #为了输出稳定，按field 编号排序
         for member in sorted(final.keys(),key=lambda x:int(x.split(":")[1])):
            parts.append(str(final[member]))
            parts.append(member)
         proc.stdin.write(" ".join(parts) + "\n")

      proc.stdin.close()
      ret = proc.wait()
      if ret!= 0:
         raise SystemExit(ret)
      print("埋数完成")

   if __name__ == "__main__":
      main()
   ```

3.执行压测，记录压测结果QPS

   ```bash
   numactl --cpunodebind=1 memtier_benchmark/memtier_benchmark \
   --server=127.0.0.1 \
   --port=6379 \
   --threads=8 \
   --clients=50 \
   --test-time=360 \
   --key-prefix=zset:field-max_1000:redis: \
   --key-maximum=2000 \
   --command="zrange __key__ 0 -1 withscores" \
   --command-key-pattern=S
   ```

4.重复执行压测，取平均值。

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

|文档版本| 发布日期   | 修改说明         |
|----------| ---------- | ---------------- |
|01| 2026-09-30 | 第一次正式发布。 |
