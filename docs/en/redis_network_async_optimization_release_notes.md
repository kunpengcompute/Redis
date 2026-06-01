# Redis Network Asynchronization Release Notes

## Version Mapping<a name="EN-US_TOPIC_0000002518399596"></a>

### Product Version Information<a name="EN-US_TOPIC_0000002518239676"></a>

<a name="table227mcpsimp"></a>
<table><tbody><tr id="row232mcpsimp"><th class="firstcol" valign="top" width="28.000000000000004%" id="mcps1.1.3.1.1"><p id="p234mcpsimp"><a name="p234mcpsimp"></a><a name="p234mcpsimp"></a>Product Name</p>
</th>
<td class="cellrowborder" valign="top" width="72%" headers="mcps1.1.3.1.1 "><p id="p236mcpsimp"><a name="p236mcpsimp"></a><a name="p236mcpsimp"></a>Kunpeng BoostKit</p>
</td>
</tr>
<tr id="row237mcpsimp"><th class="firstcol" valign="top" width="28.000000000000004%" id="mcps1.1.3.2.1"><p id="p239mcpsimp"><a name="p239mcpsimp"></a><a name="p239mcpsimp"></a>Product Version</p>
</th>
<td class="cellrowborder" valign="top" width="72%" headers="mcps1.1.3.2.1 "><p id="p241mcpsimp"><a name="p241mcpsimp"></a><a name="p241mcpsimp"></a>25.3.0</p>
</td>
</tr>
<tr id="row242mcpsimp"><th class="firstcol" valign="top" width="28.000000000000004%" id="mcps1.1.3.3.1"><p id="p244mcpsimp"><a name="p244mcpsimp"></a><a name="p244mcpsimp"></a>Feature Name</p>
</th>
<td class="cellrowborder" valign="top" width="72%" headers="mcps1.1.3.3.1 "><p id="p246mcpsimp"><a name="p246mcpsimp"></a><a name="p246mcpsimp"></a>Redis network asynchronization</p>
</td>
</tr>
</tbody>
</table>


### Software Version Mapping<a name="EN-US_TOPIC_0000002549759431"></a>

|Type|Version|
|--|--|
|OS|openEuler 22.03 LTS SP4|
|Redis|Redis 6.0.20 or Redis 7.0.15|
|Network asynchronization affinity kernel|kernel-5.10.0-275.0.0.178.oe2203sp4.aarch64.rpm|



### Hardware Version Mapping<a name="EN-US_TOPIC_0000002518239672"></a>

|Item|Requirement|
|--|--|
|Processor|New Kunpeng 920 processor model or Kunpeng 950 processor|



### Virus Scan Results<a name="EN-US_TOPIC_0000002518399598"></a>

Virus scanning is not involved because no software package is released.



## v25.3.0<a name="EN-US_TOPIC_0000002549759435"></a>

### Change Description<a name="EN-US_TOPIC_0000002518399600"></a>

Enhanced the quality of Redis network asynchronization to ensure that all open-source test cases provided by Redis can pass. Added the iouring switch, which allows users to enable the network asynchronization feature as required.


### Resolved Issues<a name="EN-US_TOPIC_0000002518399604"></a>

None


### Known Issues<a name="EN-US_TOPIC_0000002518239678"></a>

None



## v25.2.RC1<a name="EN-US_TOPIC_0000002518239674"></a>

### Change Description<a name="EN-US_TOPIC_0000002549879441"></a>

Added network asynchronization for Redis 7.0.15.


### Resolved Issues<a name="EN-US_TOPIC_0000002549879435"></a>

None


### Known Issues<a name="EN-US_TOPIC_0000002518399602"></a>

None



## v25.1.RC1<a name="EN-US_TOPIC_0000002549879437"></a>

### Change Description<a name="EN-US_TOPIC_0000002549759437"></a>

Kunpeng Redis Asynchronous I/O (KRAIO) is a batch asynchronous I/O algorithm developed by Kunpeng. The Redis network asynchronization feature enhances performance by offloading network I/O operations to KRAIO for asynchronous batch processing. This reduces system calls and context switching, enabling non-blocking Redis operations and significantly improving throughput. When the submission queue polling (sqpoll) mode is enabled, KRAIO utilizes a dedicated kernel thread to automatically handle network I/O events, eliminating the need for system calls during I/O operations.


### Resolved Issues<a name="EN-US_TOPIC_0000002549879439"></a>

None


### Known Issues<a name="EN-US_TOPIC_0000002549759433"></a>

None



## Related Documentation<a name="EN-US_TOPIC_0000002549759439"></a>

### Documentation<a name="EN-US_TOPIC_0000002518239670"></a>

|Document|Description|Delivery Method|
|--|--|--|
|*Kunpeng BoostKit 25.3.0 Redis Network Asynchronization Release Notes*|Describes the version release and mapping information of the Redis network asynchronization feature.|[Open-source repository](https://gitcode.com/boostkit/Redis/tree/master/docs/en)|
|*Kunpeng BoostKit 25.3.0 Redis Network Asynchronization Feature Guide*|Describes the environment requirements and provides guidance on enabling the Redis network asynchronization feature.|[Open-source repository](https://gitcode.com/boostkit/Redis/tree/tree/master/docs/en)|



### Obtaining Documentation<a name="EN-US_TOPIC_0000002549759441"></a>

Visit the [open-source repository](https://gitcode.com/boostkit/Redis/tree/master/docs/en) to view or download required documents.
