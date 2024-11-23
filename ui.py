import tkinter as tk
import subprocess

# 回调函数，调用 plot.py 并传递参数
def call_plot(timeframe):
    try:
        # 调用 plot.py，并传递时间范围作为参数
        subprocess.run(['./Scripts/python', 'plot.py', timeframe], check=True)
    except Exception as e:
        print(f"Error occurred: {e}")


# 创建一个用于显示选择的菜单（初始隐藏）
def show_options(root):
    # 创建【近七日】【今年】【全量】选项按钮
    option_frame = tk.Frame(root)
    option_frame.pack(side="left", padx=20, pady=20)

    btn_recent_seven_days = tk.Button(option_frame, text="近七日", width=15, height=2,
                                      command=lambda: call_plot("7days"))
    btn_recent_seven_days.grid(row=0, column=0, pady=5)

    btn_recent_a_month = tk.Button(option_frame, text="近一月", width=15, height=2,
                                      command=lambda: call_plot("this_month"))
    btn_recent_a_month.grid(row=1, column=0, pady=5)

    btn_this_year = tk.Button(option_frame, text="今年", width=15, height=2,
                              command=lambda: call_plot("this_year"))
    btn_this_year.grid(row=2, column=0, pady=5)

    btn_all_time = tk.Button(option_frame, text="全量", width=15, height=2,
                             command=lambda: call_plot("all_time"))
    btn_all_time.grid(row=3, column=0, pady=5)

def main():
    # 创建主窗口
    root = tk.Tk()
    root.title("kachikahi")

    # 设置窗口大小
    root.geometry("300x300")

    # 创建左侧面板，显示【总览】按钮
    frame_left = tk.Frame(root)
    frame_left.pack(side="left", padx=20, pady=20)
    # 创建【总览】按钮
    btn_overview = tk.Button(frame_left, text="总览", width=15, height=2, command=lambda: show_options(root))
    btn_overview.grid(row=0, column=0)

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()
