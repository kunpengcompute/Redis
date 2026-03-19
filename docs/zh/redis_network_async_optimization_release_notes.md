# Redis网络异步优化 版本说明书<a name="ZH-CN_TOPIC_0000002521254772"></a>

## 版本配套说明<a name="ZH-CN_TOPIC_0000002518399596"></a>

### 产品版本信息<a name="ZH-CN_TOPIC_0000002518239676"></a>

<a name="table227mcpsimp"></a>
<table><tbody><tr id="row232mcpsimp"><th class="firstcol" valign="top" width="28.000000000000004%" id="mcps1.1.3.1.1"><p id="p234mcpsimp"><a name="p234mcpsimp"></a><a name="p234mcpsimp"></a>产品名称</p>
</th>
<td class="cellrowborder" valign="top" width="72%" headers="mcps1.1.3.1.1 "><p id="p236mcpsimp"><a name="p236mcpsimp"></a><a name="p236mcpsimp"></a>Kunpeng BoostKit</p>
</td>
</tr>
<tr id="row237mcpsimp"><th class="firstcol" valign="top" width="28.000000000000004%" id="mcps1.1.3.2.1"><p id="p239mcpsimp"><a name="p239mcpsimp"></a><a name="p239mcpsimp"></a>产品版本</p>
</th>
<td class="cellrowborder" valign="top" width="72%" headers="mcps1.1.3.2.1 "><p id="p241mcpsimp"><a name="p241mcpsimp"></a><a name="p241mcpsimp"></a>25.3.0</p>
</td>
</tr>
<tr id="row242mcpsimp"><th class="firstcol" valign="top" width="28.000000000000004%" id="mcps1.1.3.3.1"><p id="p244mcpsimp"><a name="p244mcpsimp"></a><a name="p244mcpsimp"></a>特性名称</p>
</th>
<td class="cellrowborder" valign="top" width="72%" headers="mcps1.1.3.3.1 "><p id="p246mcpsimp"><a name="p246mcpsimp"></a><a name="p246mcpsimp"></a>Redis网络异步优化</p>
</td>
</tr>
</tbody>
</table>


### 软件版本配套说明<a name="ZH-CN_TOPIC_0000002549759431"></a>

|软件类型|版本|
|--|--|
|OS|openEuler 22.03 LTS SP4|
|Redis|Redis 6.0.20、Redis 7.0.15|
|网络异步优化亲和内核|kernel-5.10.0-275.0.0.178.oe2203sp4.aarch64.rpm|



### 硬件版本配套说明<a name="ZH-CN_TOPIC_0000002518239672"></a>

|项目|要求|
|--|--|
|处理器|鲲鹏920新型号处理器、鲲鹏950处理器|



### 病毒扫描结果<a name="ZH-CN_TOPIC_0000002518399598"></a>

不涉及软件包发布，不涉及病毒扫描。



## v25.3.0<a name="ZH-CN_TOPIC_0000002549759435"></a>

### 更新说明<a name="ZH-CN_TOPIC_0000002518399600"></a>

针对Redis网络异步优化进行质量加固，确保Redis自身提供的开源测试用例能够全部通过。同时增加iouring使能开关，用户可以根据需要决定是否使能网络异步优化特性。


### 已解决的问题<a name="ZH-CN_TOPIC_0000002518399604"></a>

无。


### 遗留问题<a name="ZH-CN_TOPIC_0000002518239678"></a>

无。



## v25.2.RC1<a name="ZH-CN_TOPIC_0000002518239674"></a>

### 更新说明<a name="ZH-CN_TOPIC_0000002549879441"></a>

新增支持Redis 7.0.15版本使能网络异步优化特性。


### 已解决的问题<a name="ZH-CN_TOPIC_0000002549879435"></a>

无。


### 遗留问题<a name="ZH-CN_TOPIC_0000002518399602"></a>

无。



## v25.1.RC1<a name="ZH-CN_TOPIC_0000002549879437"></a>

### 更新说明<a name="ZH-CN_TOPIC_0000002549759437"></a>

KRAIO（Kunpeng Redis Asynchronous I/O）是鲲鹏自研的批量异步IO算法，Redis数据库网络异步化通过将Redis中网络IO操作交由KRAIO异步批量执行，减少系统调用和上下文切换，实现Redis业务无阻塞执行，从而提高Redis吞吐量。通过配置sqpoll模式，KRAIO启用一个内核线程，自动消费网络IO事件，实现无需系统调用完成IO操作。


### 已解决的问题<a name="ZH-CN_TOPIC_0000002549879439"></a>

无。


### 遗留问题<a name="ZH-CN_TOPIC_0000002549759433"></a>

无。



## 版本配套文档<a name="ZH-CN_TOPIC_0000002549759439"></a>

### 版本配套文档<a name="ZH-CN_TOPIC_0000002518239670"></a>

|文档名称|内容简介|交付形式|
|--|--|--|
|《Kunpeng BoostKit 25.3.0 Redis-Network-Async-Optimization-Release-Notes》|本文档提供Redis网络异步优化的版本发布及其配套信息。|[开源仓](https://gitcode.com/boostkit/Redis/tree/master/docs/zh)|
|《Kunpeng BoostKit 25.3.0 Redis-Network-Async-Optimization-Feature-Guide》|本文档提供Redis使能网络异步优化算法的环境要求、特性使能指导。|[开源仓](https://gitcode.com/boostkit/Redis/tree/tree/master/docs/zh)|



### 获取文档的方法<a name="ZH-CN_TOPIC_0000002549759441"></a>

您可以通过访问[[开源仓](https://gitcode.com/boostkit/Redis/tree/master/docs/zh)]浏览和获取相关文档。



