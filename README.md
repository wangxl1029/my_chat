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

#### Category

+ python native
    - random module
        * [random choice](#J8908), etc.@CSDN
    - name enumerate module
+ PyQt5



#### Week 51th, 2018

##### Dec 17, 2018. Mon, Sunny

###### queue get

Official online help :  
» <https://docs.python.org/3/library/queue.html#queue.Queue.get>

Alive memory会用到queue的get方法的timeout，timeout的单位是秒。

###### random choice

<html><span id="J8908">&#9875;</span>
CSDN online help :
</html>

- <https://www.cnblogs.com/duking1991/p/6121300.html>


这篇网文还不错，例说明了：
+ random.random
+ random.choice
+ random.uniform
+ random.int
+ random.sample
+ random.shuffle

会发现在random module里，期待的**随机机**能都有。

#### Week 50th, 2018

##### Dec 13, 2018. Thu, Sunny

###### os walk

Official online helper : <https://docs.python.org/3/library/os.html#os.walk>

上面链接里对os walk的说明比较清楚了，这里简要总结下：

`os.walk(top, topdown=True, onerror=None, followlinks=False)`

的返回值是是一个`(dirpath, dirnames, filenames)`元组的产生式，即，yield。
Os walk会访问top顶目录和其下的所有目录，每访问一个目录就会yield上述的三元组。
三元组中的`dirpath`就是访问的当前目录，`dirnames`是当前目录下的所有目录名的list，
`filenames`是当前目录下所有文件名（不包含文件链接）的list。

###### 类方法 

即，python的类里的方法冠以`@classmethod`修饰符的方法，即，所谓的类方法。
类方法为该类的所有实例所共有，听起来好像类的静态方法，即，冠以`@staticmethod`的文法。
但类方法与静态方法的区别是，类方法能在第一个参数传入类名，参考如下online help。

- CSND online help : <https://blog.csdn.net/dyh4201/article/details/78336529>
    * 评论：笔者认为此文还没有说到本质。
    * 类方法的本质：在于，父类要调用派生类的方法时就一定要知道当前类名，
    比较如下代码`create()`方法，体味类方法的优势。

```python
import threading
class AliveThread(threading.Thread):
    @classmethod
    def create(cls, start_flag=True):
        t = cls()
        t.daemon = True
        if start_flag:
            t.start()
        return t


class FilesystemSensor(AliveThread):
    # @staticmethod
    # def create(start_flag=True):
    #     t = FilesystemSensor()
    #     t.daemon = True
    #     if start_flag:
    #         t.start()
    #     return t

    def __init__(self):
        super().__init__()
        
class AliveMessager(threading.Thread):
    @staticmethod
    def create(start_flag=True):
        t = AliveMessager()
        t.daemon = True
        if start_flag:
            t.start()
        return t

    def __init__(self):
        super().__init__()
 ```

##### Dec 11, 2018. Tue, Sunny

###### names
+ anonym  ['ænəˌnɪm] 
   - noun.假名;无名氏; 笔名; 作者不明的出版物
+ pseudonym 英 [ˈsu:dənɪm] 美 [ˈsudn:ˌɪm]
   - noun.假名，化名，（尤指）笔名
+ nom
   - abbr.nominal 名义上的，有名无实的;Nominative 主格的

###### The Matrix, 1999 film

Wikipedia : <https://en.wikipedia.org/wiki/The_Matrix>

Computer programmer Thomas Anderson, living a double life as the hacker "**Neo"**, feels something is wrong with the world and is puzzled by repeated online encounters with the cryptic phrase "the Matrix".

###### drag/drop file

**Official Doc Helper**
- QDragEnterEvent Class : <http://doc.qt.io/qt-5/qdragenterevent.html>
- QMimeData Class : <http://doc.qt.io/qt-5/qmimedata.html>
   * 文档包含`hasFormat()`等方法说明。
   * 我们关注`hasUrls()`方法。

**Web Code Helper**
- CSDN : <https://blog.csdn.net/rl529014/article/details/53057577>
   * 标题：Qt: QDropEvent拖拽事件，拖拽打开文件
   * 文章的代码实现了拖拽文本文件到窗口，并在窗口显示文本文件的内容。
   * 参考这里的代码，成功实现拖拽文件到QTextEdit，并在QTextEdit中显示文件的路径，
   代码如下。

```python
from PyQt5.QtWidgets import QTextEdit
class SomeTextEdit(QTextEdit):
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        urls = e.mimeData().urls()
        filename = urls[0].toLocalFile()
        self.insertPlainText(filename)
```

如上代码省略了构造函数等其它的细节，通过以上两个drag/drop函数完成了期望功能。

###### QColor

CSDN Helper
+ QT的[text edit](https://blog.csdn.net/spy_h/article/details/80502201?utm_source=blogxgwz7)设成QColor，如下。
   - 设置背景颜色
   - 设置背景图
   - 设置文字背景颜色

如下代码设text edit的背景色是很浅的绿。

```python
output_edit = OutputEdit(self)
output_edit_bg_col = QColor(240, 250, 240)
output_edit.setStyleSheet(f'background:{output_edit_bg_col.name()}')
```

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
