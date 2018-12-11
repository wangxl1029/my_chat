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
