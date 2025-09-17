# 项目介绍
**Kunpeng Redis是鲲鹏参与开源社区的redis，做了网络异步化优化，提升Redis 吞吐量**
KRAIO（Kunpeng Redis Asynchronous I/O）是鲲鹏自研的批量异步IO算法，Redis网络异步化通过将Redis中网络IO操作交由KRAIO异步批量执行，减少系统调用和上下文交换，实现Redis业务无阻塞执行，从而提高Redis吞吐量。通过自动配置sqpoll模式，KRAIO启用一个内核线程，自动处理网络IO事件，实现无需系统调用完成IO操作。

# 版本说明
**当前版本适用于Redis 6.0.20和Redis 7.0.15**
| Kunpeng Redis |开源 Redis|特性|
|----------------|----------------|----------------|
|7.0.15 |7.0.15|新增网络异步化特性，提高Redis吞吐量|
|6.0.20 |6.0.20|新增网络异步化特性，提高Redis吞吐量|

# 环境部署
本文基于鲲鹏服务器和OpenEuler操作系统提供指导，在正式操作前请确保软硬件均满足要求。
## 硬件要求
   如表1所示。
   表1 硬件要求
   |项目|规格|
   |----------------|----------------|
   |CPU| 鲲鹏920系列处理器 |
   | 网卡|25GE网卡*2 |

## 操作系统和软件要求   
 如表2所示。
 表2操作系统和软件要求
 |项目|名称|获取地址|
 |----------------|----------------|----------------|
 |操作系统|openEuler 22.03 LTS SP4|[获取链接](https://www.openeuler.org/zh/download/archive/detail/?version=openEuler%252022.03%2520LTS%2520SP4)|
 |容器|openEuler-docker.aarch64.tar.xz|[获取链接](https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP4/docker_img/aarch64/openEuler-docker.aarch64.tar.xz)|
 |KRAIO 亲和内核|kernel-5.10.0-275.0.0.178.oe2203sp4.aarch64.rpm|[获取链接](https://repo.openeuler.org/openEuler-22.03-LTS-SP4/update/aarch64/Packages/kernel-5.10.0-275.0.0.178.oe2203sp4.aarch64.rpm)
本特性建议基于“Docker+Bond4+IPVLAN”的组网环境进行优化。安装和使用该特性之前，请参考[搭建环境和组网](https://www.hikunpeng.com/document/detail/zh/kunpengdbs/appAccelFeatures/redisna/kunpeng_redis_yb_zn_64_006.html)完成相应组网环境的搭建。

# 快速上手

 **源码编译,以7.0.15版本为例**
```shell
cd kraio
cp ./libkbaio.so /usr/lib64
cp ./include/kbaio.h /usr/include
cd redis-7.0.15
cp path/Redis/redis-7.0.15-adapt-iouring.patch .
patch -p1 < redis-7.0.15-adapt-iouring.patch
make distclean & make -j #从这里开始参考Redis编译

**测试功能(单机模式)**
**步骤1** 在Server端环境分别进入4个Docker容器，每个Docker容器上启动一个网络异步优化的redis-server实例，共启动4个网络异步优化后的redis-sever实例。
```shell
docker exec -it {容器名} bash 
``` 
##对应Redis 7.0.15版本
```shell
cd path/redis-7.0.15
./src/redis-server ./redis.conf --bind 0.0.0.0 --port 6379
``` 
**步骤2** 在Client端环境上进入Redis目录，准备压力压测脚本，可参考以下脚本内容并按实际情况修改相应参数。
说明：Client端可以Server端在同机器，但性能会受影响；建议远端压测，在远端机器安装标准版Redis6.0.20进行测试，安装可参见Redis移植指南。

以下参数请按实际情况进行修改：

REDIS_SERVER_IP_PREFIX为IP网段。
redis_server_ip_suffix为起始ip后缀。
instances=4。
client为-c参数，设为最优并发数。
size为-d参数，默认3字节，也可改为256字节或其他。
```shell
#!/bin/bash 
 
REDIS_PATH="xxx1" # redis所在目录
REDIS_PORT=6379 
REDIS_SERVER_IP_PREFIX="192.168.xx" 
redis_server_ip_suffix=128 # server端起始IP后缀 
instances=4 # 实例数 
client=200 #-c参数 
size=3  # -d参数，默认3 
 
# 关闭redis-benchmark进程，清空测试数据日志 
pkill redis-benchmark 
DATA_LOG="xxx2" # 性能数据结果存放目录
mkdir -p $DATA_LOG 
rm -rf ${DATA_LOG}/* 
 
# 在client端进行redis-benchmark压测 
job_ids="" 
for (( instance=1; instance<=instances; instance++ )); do 
    REDIS_SERVER_IP="${REDIS_SERVER_IP_PREFIX}.${redis_server_ip_suffix}" 
    echo "Running redis-benchmark on ${REDIS_SERVER_IP}:$REDIS_PORT" 
    echo "${REDIS_PATH}/src/redis-benchmark -h ${REDIS_SERVER_IP} -p $REDIS_PORT" 
    ${REDIS_PATH}/src/redis-benchmark -h ${REDIS_SERVER_IP} -p $REDIS_PORT -c $client -d $size -n 10000000 -r 10000000 -t set,get --threads 20 -q >> ${DATA_LOG}/${instances}_c${client}_d${size}_${REDIS_SERVER_IP}_${REDIS_PORT}.log & 
    job_ids="$job_ids $!" 
    ((redis_server_ip_suffix++)) 
done 
 
# 等待 redis-benchmark 执行完毕 
echo "Waiting for the $instances jobs: SET, GET" 
wait $job_ids
``` 
**步骤3**
执行压测脚本同时对四个实例进行redis-benchmark压测。
性能结果会记录在规定路径DATA_LOG下，用cat*命令查看，取四个实例的平均值为四实例性能。


# 贡献指南
如果使用过程中有任何问题，或者需要反馈特性需求和bug报告，可以提交issues联系我们，具体贡献方法可参考[这里](https://gitcode.com/boostkit/community/blob/master/docs/contributor/contributing.md)

# 免责声明
此代码仓计划参与redis软件开源，仅作Redis网络异步化IO性能提升，编码风格遵照原生开源软件，继承原生开源软件安全设计，不破坏原生开源软件设计及编码风格和方式，软件的任何漏洞与安全问题，均由相应的上游社区根据其漏洞
和安全响应机制解决。请密切关注上游社区发布的通知和版本更新。鲲鹏计算社区对软件的漏洞及安全问题不承担任何责任。

# 许可证书
[LICENSE](LICENSE.txt)
通过下载并使用此源码及其附带的软件，您即同意遵守软件许可协议中的条款和条件。
# 参考文档
The dependent library libkraio.so is accessible via a link as :https://gitcode.com/BoostKit/kraio  
The dependent redis-7.0.15 source code is accessible via a link as :https://download.redio.io/releases/redis-7.0.15.tar.gz
The dependent redis-6.0.20 source code is accessible via a link as :https://download.redio.io/releases/redis-6.0.20.tar.gz
