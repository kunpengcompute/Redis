
# redis use kbiao feature
# 1.Select a Mode run
## 1.1 Library preloading mode
The preloading library mode can quickly adapt to various scenarios, but the return value of reids cannot be obtained, which may be unreliable.
```shell
cd kraio
LD_PRELOAD=./libkbaio.so redis-origin/src/redis-server redis-origin/redis.conf
```
## 1.2 Callback mode
In the callback mode, the Redis is modified in a few ways. The callback return value is more reliable, but the adaptation is complex
### 1.2.1 for redis 6.0.20
```shell
cd kraio
cp ./libkbaio.so /usr/lib64
cp ./include/kbaio.h /usr/include

cd redis-6.0.20
cp path/Redis/redis-6.0.20-adapt-iouring.patch .
patch -p1 < redis-6.0.20-adapt-iouring.patch
make distclean & make -j
```
### 1.2.2 for redis 7.0.15
```shell
cd kraio
cp ./libkbaio.so /usr/lib64
cp ./include/kbaio.h /usr/include
cd redis-7.0.15
cp path/Redis/redis-7.0.20-adapt-iouring.patch .
patch -p1 < redis-7.0.15-adapt-iouring.patch
make distclean & make -j
```

Enable the callback parameter in the configuration file /etc/kbaio2/iouring.conf file and set send_callback to 1.
```shell
./src/redis-server ./redis.conf
```
The dependent library libkbaio2.so is accessible via a link as :https://gitcode.com/BoostKit/kraio  
The dependent redis-7.0.15 source code is accessible via a link as :https://download.redio.io/releases/redis-7.0.15.tar.gz
The dependent redis-6.0.20 source code is accessible via a link as :https://download.redio.io/releases/redis-6.0.20.tar.gz