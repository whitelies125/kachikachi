# kachikachi

一个简单的时间统计工具.  
a simple time tracker.

# usage

以 python 脚本运行：  
run as python script:
~~~python
python main.py
~~~

![image](https://github.com/user-attachments/assets/612c1680-b4eb-436b-8158-1593e867c100)

点击 `plot` 显示统计结果.  
click `plot` to show statistic result.

![image](https://github.com/user-attachments/assets/ab7720f5-c756-4541-b551-d083737b4ee6)


# statistic logic

每分钟获取当前活动窗口，则认为过去的一分钟使用的是该程序。  
retrieve the currently active window once per minute, and consider the past minute as being spent using that program.
