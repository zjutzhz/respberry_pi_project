# 模块

# 识别
## 安装Protobuf

```angular2html

# Make sure you grab the latest version
curl -OL https://github.com/google/protobuf/releases/download/v3.2.0/protoc-3.2.0-linux-x86_64.zip

# Unzip
unzip protoc-3.2.0-linux-x86_64.zip -d protoc3

# Move protoc to /usr/local/bin/
sudo mv protoc3/bin/* /usr/local/bin/

# Move protoc3/include to /usr/local/include/
sudo mv protoc3/include/* /usr/local/include/

# Optional: change owner
sudo chwon [user] /usr/local/bin/protoc
sudo chwon -R [user] /usr/local/include/google


# https://gist.github.com/sofyanhadia/37787e5ed098c97919b8c593f0ec44d8
```