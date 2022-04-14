# DIP-assignment
 DIP gui

### Requirements：
pyqt5
opencv-python

### Run：
```
python main.py
```
### Development

* 需要实现的功能在 ./function/目录下，实现相应功能的函数，函数的输入为两个参数，第一个是图像，第二个是额外的参数列表，返回值为处理后的图像

* 需要配置的函数在：./gui/config.py中，格式看注释。

* 右上角的的“例子”按钮是一个简单流程的样例，可以先执行一下看看结果。

### BUG

* 路径中不能有中文（懒得改了

* 直方图绘制很卡，不用建议关掉

* 灰度图增强好像没有用