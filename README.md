Myc Hat
=======
A python chatting program.

development version »
- python 3.6.4
- pyqt5 5.11

Key Qt Class »
- QTextEdit : <http://doc.qt.io/qt-5/qtextedit.html>


Features
--------

最简的chatting界面，如下。

![image](https://s1.ax1x.com/2018/12/04/FQk0RH.png)


### Development Log

#### Week 49th, 2018

##### Dec 6, 2018. Tue, Sunny

###### key points

+ Derive the class of OutputEdit from QTextEdit.
   - define the slot of message to output message.
   - every message take a line in output and the upper is newer.
      * 参考链接：[pyqt5 QTextEdit 追加分行](https://www.cnblogs.com/topshooter/p/5576c4b13acc73812b0f0ac7902237b9.html)
+ InputEdit defines the signal of input.
   - the input signal connects to output message.


##### Dec 5, 2018. Wed, Sunny 


###### key points

+ Override the key keyPressEvent() method from the super class of QTextEdit.
   - Key code : Qt.Enter, Qt.Return
   - 一定要调用父类的keyPressEvent(),否则event会乱套。
      * 参见：<https://blog.csdn.net/akyamaaa/article/details/83788429> 
+ Focus policy
   - Focus policy : 这个也要注意。
      * 参见：<https://blog.csdn.net/yexiangcsdn/article/details/80337491>
      * 参见：<https://blog.csdn.net/qq_24185239/article/details/83750474>

###### IDE PyCharm

+ print statement »
   - 会在Run的窗口里看到print语句的output，
   - 但在Debug状态下好像是看不到print的output。
+ break points »
   - Run的状态下不能设定断点。
   - Debug状态下可以设定断点。

