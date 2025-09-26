
# redis use kbiao feature
# 1.Select a Mode run
## 1.1 Library preloading mode
The preloading library mode can quickly adapt to various scenarios, but the return value of reids cannot be obtained, which may be unreliable.
```shell
cd kraio
LD_PRELOAD=./libkraio.so redis-origin/src/redis-server redis-origin/redis.conf
```
## 1.2 Callback mode
In the callback mode, the Redis is modified in a few ways. The callback return value is more reliable, but the adaptation is complex
### 1.2.1 for redis 7.0.15
```shell
cd kraio
cp ./libkraio.so /usr/lib64
cp ./include/kraio.h /usr/include
cd redis-7.0.15
cp path/Redis/redis-7.0.15-adapt-iouring.patch .
patch -p1 < redis-7.0.15-adapt-iouring.patch
make distclean & make -j
```

Enable the callback parameter in the configuration file /etc/kraio/iouring.conf file and set send_callback to 1.
```shell
./src/redis-server ./redis.conf
```
The dependent library libkraio.so is accessible via a link as :https://gitcode.com/BoostKit/kraio  
The dependent redis-7.0.15 source code is accessible via a link as :https://download.redio.io/releases/redis-7.0.15.tar.gz