# 树莓派
## 开发环境
1. node v8.12.0
2. vue cli 3 ( npm install @vue/cli -g)
3. python 3.6
4. flask
5. PyCharm 用于Python 开发 
6. VS Code 用于前端开发

## 项目结构
### 1 pc_server 作为上位机，用于图像识别
pc_server 是 PC 端部分，分为`BackEnd`和`FrontEnd`两部分

1. FrontEnd 由 vuejs + vuetify 编写。 在`pc_server/FrontEnd` 目录下执行`npm install` 可以初始化开发环境， 之后使用`npm start serve` 可以开始调试运行
2. BackEnd 由Python + Flask 编写， `pc_server/BackEnd/module`为Python部分根目录，启动脚本是`manager.py`

### 2. rasp_server 作为rasp 远程控制工具，用于raspberry pi 远程控制

1.  FrontEnd 前端界面
2.  BackEnd  后端代码`pc_server/BackEnd/`为Python部分根目录，启动脚本是`web/main.py`, 后端代码依赖Raspberry Pi 特有的库，需要在Raspberry Pi 运行
