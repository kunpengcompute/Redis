# 项目介绍<a name="ZH-CN_TOPIC_0000002442989650"></a>

Kunpeng Redis是鲲鹏参与开源社区的Redis，做了网络异步化优化，提升Redis吞吐量。

KRAIO（Kunpeng Redis Asynchronous I/O）是鲲鹏自研的批量异步IO算法，Redis网络异步化通过将Redis中网络IO操作交由KRAIO异步批量执行，减少系统调用和上下文交换，实现Redis业务无阻塞执行，从而提高Redis吞吐量。通过自动配置sqpoll模式，KRAIO启用一个内核线程，自动处理网络IO事件，实现无需系统调用完成IO操作。

# 版本说明<a name="ZH-CN_TOPIC_0000002476976825"></a>

当前特性适用于Redis 6.0.20和Redis 7.0.15。

**表 1**  版本说明

<a name="table9742071178"></a>
<table><thead align="left"><tr id="row1174871570"><th class="cellrowborder" valign="top" width="33.33333333333333%" id="mcps1.2.4.1.1"><p id="p375187370"><a name="p375187370"></a><a name="p375187370"></a>鲲鹏Redis</p>
</th>
<th class="cellrowborder" valign="top" width="26.082608260826078%" id="mcps1.2.4.1.2"><p id="p7756712710"><a name="p7756712710"></a><a name="p7756712710"></a>开源Redis</p>
</th>
<th class="cellrowborder" valign="top" width="40.58405840584059%" id="mcps1.2.4.1.3"><p id="p13758719715"><a name="p13758719715"></a><a name="p13758719715"></a>特性</p>
</th>
</tr>
</thead>
<tbody><tr id="row127512711716"><td class="cellrowborder" valign="top" width="33.33333333333333%" headers="mcps1.2.4.1.1 "><p id="p1075157873"><a name="p1075157873"></a><a name="p1075157873"></a>7.0.15</p>
</td>
<td class="cellrowborder" valign="top" width="26.082608260826078%" headers="mcps1.2.4.1.2 "><p id="p14751172076"><a name="p14751172076"></a><a name="p14751172076"></a>7.0.15</p>
</td>
<td class="cellrowborder" valign="top" width="40.58405840584059%" headers="mcps1.2.4.1.3 "><p id="p475477717"><a name="p475477717"></a><a name="p475477717"></a>新增网络异步化特性，提高Redis吞吐量</p>
</td>
</tr>
<tr id="row35961631279"><td class="cellrowborder" valign="top" width="33.33333333333333%" headers="mcps1.2.4.1.1 "><p id="p2059615311679"><a name="p2059615311679"></a><a name="p2059615311679"></a>6.0.20</p>
</td>
<td class="cellrowborder" valign="top" width="26.082608260826078%" headers="mcps1.2.4.1.2 "><p id="p1259617314714"><a name="p1259617314714"></a><a name="p1259617314714"></a>6.0.20</p>
</td>
<td class="cellrowborder" valign="top" width="40.58405840584059%" headers="mcps1.2.4.1.3 "><p id="p175971931670"><a name="p175971931670"></a><a name="p175971931670"></a>新增网络异步化特性，提高Redis吞吐量</p>
</td>
</tr>
</tbody>
</table>

# 环境部署<a name="ZH-CN_TOPIC_0000002443617066"></a>

**硬件要求<a name="title104mcpsimp"></a>**

如[表1](#table361417304304)所示。

**表 1**  硬件要求

<a name="table361417304304"></a>
<table><thead align="left"><tr id="row20614130113013"><th class="cellrowborder" valign="top" width="50%" id="mcps1.2.3.1.1"><p id="p1961517300303"><a name="p1961517300303"></a><a name="p1961517300303"></a>项目</p>
</th>
<th class="cellrowborder" valign="top" width="50%" id="mcps1.2.3.1.2"><p id="p5615030103010"><a name="p5615030103010"></a><a name="p5615030103010"></a>规格</p>
</th>
</tr>
</thead>
<tbody><tr id="row15615930163017"><td class="cellrowborder" valign="top" width="50%" headers="mcps1.2.3.1.1 "><p id="p1261543073014"><a name="p1261543073014"></a><a name="p1261543073014"></a>CPU</p>
</td>
<td class="cellrowborder" valign="top" width="50%" headers="mcps1.2.3.1.2 "><p id="p161593043012"><a name="p161593043012"></a><a name="p161593043012"></a>鲲鹏920系列处理器</p>
</td>
</tr>
<tr id="row66151530143015"><td class="cellrowborder" valign="top" width="50%" headers="mcps1.2.3.1.1 "><p id="p16151430143016"><a name="p16151430143016"></a><a name="p16151430143016"></a>网卡</p>
</td>
<td class="cellrowborder" valign="top" width="50%" headers="mcps1.2.3.1.2 "><p id="p561513020308"><a name="p561513020308"></a><a name="p561513020308"></a>25GE网卡*2</p>
</td>
</tr>
</tbody>
</table>

**操作系统和软件要求<a name="section1214719227301"></a>**

如[表2](#_table127mcpsimp)所示。

**表 2**  操作系统和软件要求

<a name="_table127mcpsimp"></a>
<table><thead align="left"><tr id="row139mcpsimp"><th class="cellrowborder" valign="top" width="25.27%" id="mcps1.2.4.1.1"><p id="p141mcpsimp"><a name="p141mcpsimp"></a><a name="p141mcpsimp"></a>项目</p>
</th>
<th class="cellrowborder" valign="top" width="44.72%" id="mcps1.2.4.1.2"><p id="p143mcpsimp"><a name="p143mcpsimp"></a><a name="p143mcpsimp"></a>名称</p>
</th>
<th class="cellrowborder" valign="top" width="30.009999999999998%" id="mcps1.2.4.1.3"><p id="p147mcpsimp"><a name="p147mcpsimp"></a><a name="p147mcpsimp"></a>获取地址</p>
</th>
</tr>
</thead>
<tbody><tr id="row149mcpsimp"><td class="cellrowborder" valign="top" width="25.27%" headers="mcps1.2.4.1.1 "><p id="p151mcpsimp"><a name="p151mcpsimp"></a><a name="p151mcpsimp"></a>操作系统</p>
</td>
<td class="cellrowborder" valign="top" width="44.72%" headers="mcps1.2.4.1.2 "><p id="p153mcpsimp"><a name="p153mcpsimp"></a><a name="p153mcpsimp"></a>openEuler 22.03 LTS SP4</p>
</td>
<td class="cellrowborder" valign="top" width="30.009999999999998%" headers="mcps1.2.4.1.3 "><p id="p157mcpsimp"><a name="p157mcpsimp"></a><a name="p157mcpsimp"></a><a href="https://www.openeuler.org/zh/download/archive/detail/?version=openEuler%252022.03%2520LTS%2520SP4" target="_blank" rel="noopener noreferrer">获取链接</a></p>
</td>
</tr>
<tr id="row19654155105513"><td class="cellrowborder" valign="top" width="25.27%" headers="mcps1.2.4.1.1 "><p id="p665565115518"><a name="p665565115518"></a><a name="p665565115518"></a>容器</p>
</td>
<td class="cellrowborder" valign="top" width="44.72%" headers="mcps1.2.4.1.2 "><p id="p56551958552"><a name="p56551958552"></a><a name="p56551958552"></a>openEuler-docker.aarch64.tar.xz</p>
</td>
<td class="cellrowborder" valign="top" width="30.009999999999998%" headers="mcps1.2.4.1.3 "><p id="p197761153105510"><a name="p197761153105510"></a><a name="p197761153105510"></a><a href="https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP4/docker_img/aarch64/openEuler-docker.aarch64.tar.xz" target="_blank" rel="noopener noreferrer">获取链接</a></p>
</td>
</tr>
<tr id="row16402023163714"><td class="cellrowborder" valign="top" width="25.27%" headers="mcps1.2.4.1.1 "><p id="p180mcpsimp"><a name="p180mcpsimp"></a><a name="p180mcpsimp"></a>KRAIO亲和内核</p>
</td>
<td class="cellrowborder" valign="top" width="44.72%" headers="mcps1.2.4.1.2 "><p id="p73112158235"><a name="p73112158235"></a><a name="p73112158235"></a>kernel-5.10.0-275.0.0.178.oe2203sp4.aarch64.rpm</p>
</td>
<td class="cellrowborder" valign="top" width="30.009999999999998%" headers="mcps1.2.4.1.3 "><p id="p2099816274"><a name="p2099816274"></a><a name="p2099816274"></a><a href="https://repo.openeuler.org/openEuler-22.03-LTS-SP4/update/aarch64/Packages/kernel-5.10.0-275.0.0.178.oe2203sp4.aarch64.rpm" target="_blank" rel="noopener noreferrer">获取链接</a></p>
</td>
</tr>
</tbody>
</table>

# 快速上手<a name="ZH-CN_TOPIC_0000002477057013"></a>

**源码编译<a name="section1296918319382"></a>**

此处以7.0.15版本为例进行说明。

```
cd kraio
make -j 4
cp ./libkraio.so /usr/lib64 
cp ./include/kraio.h /usr/include 
cd redis-7.0.15 
cp path/Redis/redis-7.0.15-adapt-iouring.patch .
patch -p1 < redis-7.0.15-adapt-iouring.patch 
make distclean & make -j #从这里开始参考Redis编译  
```

**测试功能（单机模式）<a name="section33042032153820"></a>**

1.  在Server端环境分别进入4个Docker容器，每个Docker容器上启动一个网络异步优化的redis-server实例，共启动4个网络异步优化后的redis-sever实例。

    ```
    
    docker exec -it {容器名} bash
    ```

2.  在Client端环境上进入Redis目录，准备压力压测脚本，可参考以下脚本内容并按实际情况修改相应参数。 说明：Client端可以Server端在同机器，但性能会受影响；建议远端压测，在远端机器安装标准版Redis7.0.15进行测试。

    以下参数请按实际情况进行修改：

    -   REDIS\_SERVER\_IP\_PREFIX为IP网段。
    -   redis\_server\_ip\_suffix为起始ip后缀。
    -   instances=4。
    -   client为-c参数，设为最优并发数。
    -   size为-d参数，默认3字节，也可改为256字节或其他。

    ```
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
    mkdir -p $DATA_LOG  rm -rf ${DATA_LOG}/*    
    
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

3.  执行压测脚本同时对四个实例进行redis-benchmark压测。性能结果会记录在规定路径DATA\_LOG下，用**cat\***命令查看，取四个实例的平均值为四实例性能。

# 贡献指南<a name="ZH-CN_TOPIC_0000002443776962"></a>

如果使用过程中有任何问题，或者需要反馈特性需求和bug报告，可以提交issues联系我们，具体贡献方法可参考[这里](https://gitcode.com/boostkit/community/blob/master/docs/contributor/contributing.md)。

# 免责声明<a name="ZH-CN_TOPIC_0000002476976829"></a>

此代码仓计划参与redis软件开源，仅作Redis网络异步化IO性能提升，编码风格遵照原生开源软件，继承原生开源软件安全设计，不破坏原生开源软件设计及编码风格和方式，软件的任何漏洞与安全问题，均由相应的上游社区根据其漏洞和安全响应机制解决。请密切关注上游社区发布的通知和版本更新。鲲鹏计算社区对软件的漏洞及安全问题不承担任何责任。

# 许可证书<a name="ZH-CN_TOPIC_0000002443617074"></a>

参考Redis的license。

通过下载并使用此源码及其附带的软件，您即同意遵守软件许可协议中的条款和条件。

# 参考文档<a name="ZH-CN_TOPIC_0000002443784086"></a>

The dependent library libkraio.so is accessible via a link as :https://gitcode.com/BoostKit/kraio

The dependent redis-7.0.15 source code is accessible via a link as :https://download.redio.io/releases/redis-7.0.15.tar.gz

The dependent redis-6.0.20 source code is accessible via a link as :https://download.redio.io/releases/redis-6.0.20.tar.gz

