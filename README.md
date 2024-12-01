# Kachikachi

一个简单的时间统计工具.  
a simple time tracker.

# Usage

以 python 脚本运行：  
run as python script:
~~~python
python main.py
~~~

![image](https://github.com/user-attachments/assets/612c1680-b4eb-436b-8158-1593e867c100)

`Status` 显示当前记录状态。  
`Status` shows currnet record status.  

点击 `Stop record` 或 `Continue record` 以停止或继续记录。  
click `Stop record` or `Continue record` to stop/continue record.  

点击 `Plot` 显示统计结果。  
click `plot` to show statistic result.  

![image](https://github.com/user-attachments/assets/ab7720f5-c756-4541-b551-d083737b4ee6)

点击 `Exit` 以退出程序.  
click `Exit` to exit the program.

# Statistic logic

每分钟获取当前活动窗口，则认为过去的一分钟使用的是该程序。  
retrieve the currently active window once per minute, and consider the past minute as being spent using that program.

# UML

~~~mermaid
classDiagram
    note for Tray "Singleton"
    class Tray{
      - icon : pystray.Icon
      + on_stop()
      + on_continue()
      + on_plot()
      + on_exit()
      + run()
    }
    note for ShutdownListener "Singleton"
    class ShutdownListener{
        - regiter_name: string
        - hwnd ：HWND
        - callback : list
        + addCallback()
        + run()
    }
    note for ThreadManager "Singleton"
    class ThreadManager{
        + record_event : threading.Event()
        + exit_event : threading.Event()
        - threads : list
        + start_thread()
        + join_all()
    }
    note for DbManager "Not Singleton"
    class DbManager{
        - conn : Connection
        - cursor : Cursor
        + get_process_tbl() : list
        + get_activity_tbl() : list
        + insert_process_tbl()
        + insert_activity_tbl()
        + commit()
        + disconnect()
    }
~~~

# File dependency diagram

~~~mermaid
graph BT;
    main-->tray;
    tray-->plot;
    plot-->db_manager;
    main-->kachikachi;
    kachikachi-->db_manager;
    kachikachi-->thread_manager;
    tray-->thread_manager;
    main-->thread_manager;
    main-->shutdown_listener;
~~~
