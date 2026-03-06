"""
GUI工具函数模块
提取app.py中的重复代码
"""
import tkinter
from tkinter import Canvas


def create_button(canvas, x, y, width, height, text, radius=5, 
                 outline='white', fill='white', font=('楷体', 24, 'bold')):
    """
    创建标准化的按钮（双矩形+文本）
    
    Args:
        canvas: Canvas对象
        x, y: 按钮左上角坐标
        width, height: 按钮宽高
        text: 按钮文本
        radius: 内矩形边距
        outline: 边框颜色
        fill: 文本颜色
        font: 字体
    
    Returns:
        (rectangle_1, rectangle_2, text_item): 三个canvas对象的ID
    """
    rect1 = canvas.create_rectangle(x, y, x + width, y + height,
                                    width=2.5, outline=outline)
    rect2 = canvas.create_rectangle(x + radius, y + radius,
                                    x + width - radius, y + height - radius,
                                    width=2.5, outline=outline)
    text_item = canvas.create_text(x + 0.5 * width, y + 0.5 * height,
                                   text=text, font=font, fill=fill)
    return rect1, rect2, text_item


def bind_button_hover(canvas, rect1, rect2, text_item, 
                     hover_outline='black', hover_fill='black',
                     normal_outline='white', normal_fill='white'):
    """
    绑定按钮悬停效果
    
    Args:
        canvas: Canvas对象
        rect1, rect2, text_item: 按钮的三个canvas对象ID
        hover_outline, hover_fill: 悬停时的边框和文本颜色
        normal_outline, normal_fill: 正常状态的边框和文本颜色
    """
    def on_enter(event):
        canvas.itemconfigure(rect1, outline=hover_outline)
        canvas.itemconfigure(rect2, outline=hover_outline)
        canvas.itemconfigure(text_item, fill=hover_fill)
        canvas.configure(cursor='hand2')
    
    def on_leave(event):
        canvas.itemconfigure(rect1, outline=normal_outline)
        canvas.itemconfigure(rect2, outline=normal_outline)
        canvas.itemconfigure(text_item, fill=normal_fill)
        canvas.configure(cursor='arrow')
    
    # 注意：实际绑定需要在调用处使用canvas.bind
    return on_enter, on_leave


def create_label(window, text, x, y, width=None, height=None,
                fg='black', bg='white', font=('华文新魏', 18),
                anchor='w'):
    """
    创建标准化的标签
    
    Args:
        window: 窗口对象
        text: 标签文本
        x, y: 位置（使用relx/rely或x/y）
        width, height: 大小（使用relwidth/relheight或width/height）
        fg, bg: 前景色和背景色
        font: 字体
        anchor: 对齐方式
    """
    label = tkinter.Label(window, text=text, fg=fg, bg=bg, font=font, anchor=anchor)
    if width and height:
        if isinstance(x, float):  # 使用相对位置
            label.place(relx=x, rely=y, relwidth=width, relheight=height)
        else:  # 使用绝对位置
            label.place(x=x, y=y, width=width, height=height)
    else:
        label.place(x=x, y=y)
    return label


def create_text_widget(window, x, y, width=None, height=None,
                      fg='black', bg='white', font=('华文新魏', 12),
                      relief=tkinter.RAISED):
    """
    创建标准化的文本控件
    
    Args:
        window: 窗口对象
        x, y: 位置
        width, height: 大小
        fg, bg: 前景色和背景色
        font: 字体
        relief: 边框样式
    """
    text_widget = tkinter.Text(window, fg=fg, bg=bg, font=font, relief=relief)
    if width and height:
        if isinstance(x, float):  # 使用相对位置
            text_widget.place(relx=x, rely=y, relwidth=width, relheight=height)
        else:  # 使用绝对位置
            text_widget.place(x=x, y=y, width=width, height=height)
    else:
        text_widget.place(x=x, y=y)
    return text_widget


def check_button_click(event, button_x, button_y, button_width, button_height):
    """
    检查鼠标点击是否在按钮区域内
    
    Args:
        event: 鼠标事件
        button_x, button_y: 按钮左上角坐标
        button_width, button_height: 按钮宽高
    
    Returns:
        bool: 是否点击在按钮内
    """
    return (button_x <= event.x <= button_x + button_width and
            button_y <= event.y <= button_y + button_height)

