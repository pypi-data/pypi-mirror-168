import tkinter as tk
from tkinter import messagebox
import fdtd
from tkinter.ttk import *
# import os
# import numpy as np
from PIL import Image

fdtd.set_backend('numpy')

list_of_waveguide = []
list_of_source = []
list_of_detector = []

simfolder = 'f'

grid = 1

grid_x = 200  # get()函数返回str
grid_y = 200
grid_z = 200
PML_width = 10
grid_spacing = 0.1


def Resize(img, i):
    """更改图像尺寸"""
    img_new = img.resize((int(screenwidth * 2 / 5), int(screenheight * 2 / 5)), Image.ANTIALIAS)
    img_new.save('%s/file000%d.png' % (simfolder, i))


def Button_set_object_command():
    """设置元件按钮"""

    def Button_del_object_command():
        """删除物体按钮
           删除选中的物体
            """

        i = Listbox_object.curselection()
        if i != ():
            Listbox_object.delete(i)
            del list_of_waveguide[int(i[0]) * 7:int(i[0]) * 7 + 7]

        InitializeGrid(grid_x, grid_y, grid_z, grid_spacing, PML_width)
        Plot(grid, 0, simfolder)

    def Button_add_object_command():
        """添加波导按钮，按下后开启一个新窗口,在其中设置波导的类别与属性"""

        def Button_confirm_object_command():
            """确认添加波导按钮，按下后将新的波导数据添加到grid中"""
            try:
                global list_of_waveguide
                list_of_waveguide.extend(
                    [int(Text_x_waveguide.get()), int(Text_y_waveguide.get()), int(Text_z_waveguide.get()),
                     int(Text_x0_waveguide.get()), int(Text_y0_waveguide.get()), int(Text_z0_waveguide.get()),
                     float(Text_per_waveguide.get())])
            except:
                tk.messagebox.showerror('error', '长、宽、坐标必须是正整数！')

            Listbox_object.insert(Listbox_object.size(), Text_name_waveguide.get())

            Plot(grid, 0, simfolder)

            window_add_object.destroy()

        window_add_object = tk.Toplevel(window_set_object)
        window_add_object.geometry('500x500')
        window_add_object.title('添加元件')
        tk.Label(window_add_object, text='波导x方向长度').place(x=25, y=80)
        tk.Label(window_add_object, text='波导y方向长度').place(x=25, y=120)
        tk.Label(window_add_object, text='波导z方向长度').place(x=25, y=160)
        tk.Label(window_add_object, text='坐标').place(x=25, y=200)
        tk.Label(window_add_object, text='介电常数').place(x=25, y=240)
        tk.Label(window_add_object, text='名称').place(x=25, y=280)

        var_x_waveguide = tk.IntVar(value=60)
        var_y_waveguide = tk.IntVar(value=10)
        var_z_waveguide = tk.IntVar(value=10)
        var_x0_waveguide = tk.IntVar(value=50)
        var_y0_waveguide = tk.IntVar(value=50)
        var_z0_waveguide = tk.IntVar(value=50)
        var_per_waveguide = tk.DoubleVar(value=pow(1.7, 1 / 2))  # 介电常数
        var_name_waveguide = tk.StringVar(value='物体')

        Text_x_waveguide = tk.Entry(window_add_object, textvariable=var_x_waveguide)
        Text_x_waveguide.place(x=250, y=80)
        Text_y_waveguide = tk.Entry(window_add_object, textvariable=var_y_waveguide)
        Text_y_waveguide.place(x=250, y=120)
        Text_z_waveguide = tk.Entry(window_add_object, textvariable=var_z_waveguide)
        Text_z_waveguide.place(x=250, y=160)
        Text_x0_waveguide = tk.Entry(window_add_object, textvariable=var_x0_waveguide, width=20)
        Text_x0_waveguide.place(x=250, y=200)
        Text_y0_waveguide = tk.Entry(window_add_object, textvariable=var_y0_waveguide, width=20)
        Text_y0_waveguide.place(x=330, y=200)
        Text_z0_waveguide = tk.Entry(window_add_object, textvariable=var_z0_waveguide, width=20)
        Text_z0_waveguide.place(x=410, y=200)
        Text_per_waveguide = tk.Entry(window_add_object, textvariable=var_per_waveguide, width=20)
        Text_per_waveguide.place(x=250, y=240)
        Text_name_waveguide = tk.Entry(window_add_object, textvariable=var_name_waveguide, width=20)
        Text_name_waveguide.place(x=250, y=280)

        Button_confirm_object = tk.Button(window_add_object, text='确认', width=15, height=2,
                                          command=Button_confirm_object_command)
        Button_confirm_object.place(x=250, y=15)

    window_set_object = tk.Toplevel(window)
    window_set_object.geometry('800x300')
    window_set_object.title('元件设置')

    tk.Label(window_set_object, text='元件类型').place(x=25, y=30)
    Listbox_object = tk.Listbox(window_set_object, width=50, height=5)
    Listbox_object.place(x=25, y=130)

    Button_add_object = tk.Button(window_set_object, text='添加', width=15, height=2, command=Button_add_object_command)
    Button_add_object.place(x=400, y=30)

    # 删除物体按钮
    Button_del_object = tk.Button(window_set_object, text='删除', width=15, height=2, command=Button_del_object_command)
    Button_del_object.place(x=500, y=130)

    Button_del_object = tk.Button(window_set_object, text='修改', width=15, height=2, command=Button_del_object_command)
    Button_del_object.place(x=500, y=180)

    var = tk.StringVar()
    combobox_choose_waveguide = Combobox(window_set_object, textvariable=var,
                                         values=['矩形波导', 'S波导', 'Y型波导', '方向耦合器'])
    combobox_choose_waveguide.place(x=125, y=30)
    combobox_choose_waveguide.current(0)


def Button_set_source_command():
    def Button_del_source_command():
        """删除物体按钮
           删除选中的物体
            """
        i = Listbox_source.curselection()
        if i != ():
            Listbox_source.delete(i)
            del list_of_source[i[0] * 6:i[0] * 6 + 6]

        InitializeGrid(grid_x, grid_y, grid_z, grid_spacing, PML_width)
        Plot(grid, 0, simfolder)

    def Button_add_source_command():
        """添加波导按钮，按下后开启一个新窗口,在其中设置波导的类别与属性"""

        def Button_confirm_source_command():
            """确认添加波导按钮，按下后将新的波导数据添加到grid中"""
            try:
                global list_of_source
                list_of_source.extend([int(Text_x_source.get()), int(Text_y_source.get()), int(Text_z_source.get()),
                                       int(Text_x0_source.get()), int(Text_y0_source.get()), int(Text_z0_source.get())])
            except:
                tk.messagebox.showerror('error', '长、宽、坐标必须是正整数！')

            Listbox_source.insert(Listbox_source.size(), Text_name_source.get())
            Plot(grid, 0, simfolder)
            window_add_source.destroy()

        window_add_source = tk.Toplevel(window_set_source)
        window_add_source.geometry('500x500')
        window_add_source.title('添加光源')
        var = tk.StringVar()

        tk.Label(window_add_source, text='线光源x方向长度').place(x=25, y=80)
        tk.Label(window_add_source, text='线光源y方向长度').place(x=25, y=120)
        tk.Label(window_add_source, text='线光源z方向长度').place(x=25, y=160)
        tk.Label(window_add_source, text='坐标').place(x=25, y=200)
        tk.Label(window_add_source, text='名称').place(x=25, y=240)

        var_x_source = tk.IntVar(value=1)
        var_y_source = tk.IntVar(value=30)
        var_z_source = tk.IntVar(value=1)
        var_x0_source = tk.IntVar(value=40)
        var_y0_source = tk.IntVar(value=40)
        var_z0_source = tk.IntVar(value=40)
        var_name_source = tk.StringVar(value='光源')

        Text_x_source = tk.Entry(window_add_source, textvariable=var_x_source)
        Text_x_source.place(x=250, y=80)
        Text_y_source = tk.Entry(window_add_source, textvariable=var_y_source)
        Text_y_source.place(x=250, y=120)
        Text_z_source = tk.Entry(window_add_source, textvariable=var_z_source)
        Text_z_source.place(x=250, y=160)
        Text_x0_source = tk.Entry(window_add_source, textvariable=var_x0_source, width=20)
        Text_x0_source.place(x=250, y=200)
        Text_y0_source = tk.Entry(window_add_source, textvariable=var_y0_source, width=20)
        Text_y0_source.place(x=330, y=200)
        Text_z0_source = tk.Entry(window_add_source, textvariable=var_z0_source, width=20)
        Text_z0_source.place(x=410, y=200)
        Text_name_source = tk.Entry(window_add_source, textvariable=var_name_source, width=20)
        Text_name_source.place(x=250, y=240)

        Button_confirm_source = tk.Button(window_add_source, text='确认', width=15, height=2,
                                          command=Button_confirm_source_command)
        Button_confirm_source.place(x=250, y=15)

    window_set_source = tk.Toplevel(window)
    window_set_source.geometry('800x300')
    window_set_source.title('光源设置')

    tk.Label(window_set_source, text='光源类型').place(x=25, y=30)
    Listbox_source = tk.Listbox(window_set_source, width=50, height=5)
    Listbox_source.place(x=25, y=130)

    Button_add_object = tk.Button(window_set_source, text='添加', width=15, height=2, command=Button_add_source_command)
    Button_add_object.place(x=400, y=30)

    # 删除物体按钮
    Button_del_object = tk.Button(window_set_source, text='删除', width=15, height=2, command=Button_del_source_command)
    Button_del_object.place(x=500, y=130)

    var = tk.StringVar()
    combobox_choose_source = Combobox(window_set_source, textvariable=var, values=['线光源', '点光源', '面光源'])
    combobox_choose_source.place(x=125, y=30)
    combobox_choose_source.current(0)


def Button_set_detector_command():
    def Button_del_detector_command():
        """删除物体按钮
           删除选中的物体
            """
        i = Listbox_detector.curselection()
        if i != ():
            Listbox_detector.delete(i)
            del list_of_detector[i[0] * 4:i[0] * 4 + 4]

        InitializeGrid(grid_x, grid_y, grid_z, grid_spacing, PML_width)
        Plot(grid, 0, simfolder)

    def Button_add_detector_command():
        """添加波导按钮，按下后开启一个新窗口,在其中设置波导的类别与属性"""

        def Button_confirm_detector_command():
            """确认添加波导按钮，按下后将新的波导数据添加到grid中"""
            try:
                global list_of_detector
                list_of_detector.extend(
                    [int(Text_x_detector.get()), int(Text_y_detector.get()), int(Text_z_detector.get()),
                     int(Text_x0_detector.get()), int(Text_y0_detector.get()), int(Text_z0_detector.get())])
            except:
                tk.messagebox.showerror('error', '长、宽、坐标必须是正整数！')

            Listbox_detector.insert(Listbox_detector.size(), Text_name_detector.get())
            Plot(grid, 0, simfolder)
            window_add_detector.destroy()

        window_add_detector = tk.Toplevel(window_set_detector)
        window_add_detector.geometry('500x500')
        window_add_detector.title('添加监视器')

        tk.Label(window_add_detector, text='监视器x方向长度').place(x=25, y=80)
        tk.Label(window_add_detector, text='监视器y方向长度').place(x=25, y=120)
        tk.Label(window_add_detector, text='监视器z方向长度').place(x=25, y=160)
        tk.Label(window_add_detector, text='坐标').place(x=25, y=200)
        tk.Label(window_add_detector, text='名称').place(x=25, y=240)

        var_x_detector = tk.IntVar(value=1)
        var_y_detector = tk.IntVar(value=30)
        var_z_detector = tk.IntVar(value=1)
        var_x0_detector = tk.IntVar(value=120)
        var_y0_detector = tk.IntVar(value=40)
        var_z0_detector = tk.IntVar(value=40)
        var_name_detector = tk.StringVar(value='监视器')

        Text_x_detector = tk.Entry(window_add_detector, textvariable=var_x_detector)
        Text_x_detector.place(x=250, y=80)
        Text_y_detector = tk.Entry(window_add_detector, textvariable=var_y_detector)
        Text_y_detector.place(x=250, y=120)
        Text_z_detector = tk.Entry(window_add_detector, textvariable=var_y_detector)
        Text_z_detector.place(x=250, y=160)
        Text_x0_detector = tk.Entry(window_add_detector, textvariable=var_x0_detector, width=20)
        Text_x0_detector.place(x=250, y=200)
        Text_y0_detector = tk.Entry(window_add_detector, textvariable=var_y0_detector, width=20)
        Text_y0_detector.place(x=330, y=200)
        Text_z0_detector = tk.Entry(window_add_detector, textvariable=var_y0_detector, width=20)
        Text_z0_detector.place(x=410, y=200)
        Text_name_detector = tk.Entry(window_add_detector, textvariable=var_name_detector, width=20)
        Text_name_detector.place(x=250, y=240)

        Button_confirm_source = tk.Button(window_add_detector, text='确认', width=15, height=2,
                                          command=Button_confirm_detector_command())
        Button_confirm_source.place(x=250, y=15)

    window_set_detector = tk.Toplevel(window)
    window_set_detector.geometry('800x300')
    window_set_detector.title('监视器设置')

    tk.Label(window_set_detector, text='监视器类型').place(x=25, y=30)
    Listbox_detector = tk.Listbox(window_set_detector, width=50, height=5)
    Listbox_detector.place(x=25, y=130)

    Button_add_detector = tk.Button(window_set_detector, text='添加', width=15, height=2,
                                    command=Button_add_detector_command)
    Button_add_detector.place(x=400, y=30)

    # 删除物体按钮
    Button_del_detector = tk.Button(window_set_detector, text='删除', width=15, height=2,
                                    command=Button_del_detector_command())
    Button_del_detector.place(x=500, y=130)

    var = tk.StringVar()
    combobox_choose_detector = Combobox(window_set_detector, textvariable=var, values=['矩形监视器', '面监视器'])
    combobox_choose_detector.place(x=125, y=30)
    combobox_choose_detector.current(0)


# def Button0_command():
#     "按下确认按钮后，运行模拟，绘制模拟图像，给出结果"
#
#     try:
#         length = int(Text_x1.get())  # get()函数返回str
#         width = int(Text_y1.get())
#         PML = int(PML_width.get())
#     except:
#         tk.messagebox.showerror('error', '长、宽、坐标必须是正整数！')
#
#     data = [length, width, PML]
#
#     for datas in data:
#         if datas == 0:
#             tk.messagebox.showerror('error', '请输入正确数据！')
#             break
#
#     grid = fdtd.Grid(shape=(int(length), int(width), 1), )  # 设置区域
#     #加载设置好的波导
#
#     for i in range (0,101,5):
#         try:
#             grid[list_of_waveguide[i+2]:list_of_waveguide[i+2]+list_of_waveguide[i],
#             list_of_waveguide[i+3]:list_of_waveguide[i+3]+list_of_waveguide[i+1], 0] = fdtd.Object(permittivity=list_of_waveguide[i+4], name="object%d"% (i/5))
#         except:
#             break
#
#     for i in range (0,101,4):
#         try:
#             grid[list_of_source[i+2]:list_of_source[i+2]+list_of_source[i],
#             list_of_source[i+3]:list_of_source[i+3]+list_of_source[i+1], 0] = fdtd.LineSource(period = 1550e-9 / (3e8), name="source%d"% (i/4))
#         except:
#             break
#
#     for i in range (0,101,4):
#         try:
#             grid[list_of_detector[i+2]:list_of_detector[i+2]+list_of_detector[i],
#             list_of_detector[i+3]:list_of_detector[i+3]+list_of_detector[i+1], 0] = fdtd.LineDetector(name="detector%d"% (i/4))
#         except:
#             break
#
#     grid[0:int(PML), :, :] = fdtd.PML(name="pml_xlow")
#     grid[-int(PML):, :, :] = fdtd.PML(name="pml_xhigh")
#     grid[:, 0:int(PML), :] = fdtd.PML(name="pml_ylow")
#     grid[:, -int(PML):, :] = fdtd.PML(name="pml_yhigh")
#     print(grid)
#     grid.run(total_time=100)
#     grid.visualize(z=0, show=True)
#
#     simfolder = grid.save_simulation("GRIN")
#     grid.visualize(z=0, animate=True, save=True, folder=simfolder)
#     grid.save_data()  # saving detector readings
#
#     with open(os.path.join("./fdtd_output", grid.folder, "grid.txt"), "w") as f:
#         f.write(str(grid))
#         wavelength = 3e8 / grid.source0.frequency
#         wavelengthUnits = wavelength / grid.grid_spacing
#         GD = np.array([grid.x, grid.y, grid.z])
#         gridRange = [np.arange(x / grid.grid_spacing) for x in GD]
#         objectRange = np.array([[gridRange[0][x.x], gridRange[1][x.y], gridRange[2][x.z]] for x in grid.objects],
#                                dtype=object).T
#         f.write("\n\nGrid details (in wavelength scale):")
#         f.write("\n\tGrid dimensions: ")
#         f.write(str(GD / wavelength))
#         f.write("\n\tSource dimensions: ")
#         f.write(str(np.array([grid.source0.x[-1] - grid.source0.x[0] + 1, grid.source0.y[-1] - grid.source0.y[0] + 1,
#                               grid.source0.z[-1] - grid.source0.z[0] + 1]) / wavelengthUnits))
#         f.write("\n\tObject dimensions: ")
#         f.write(str([(max(map(max, x)) - min(map(min, x)) + 1) / wavelengthUnits for x in objectRange]))
#
#     dic = np.load(os.path.join(simfolder, "detector_readings.npz"))
#     import warnings;
#     warnings.filterwarnings("ignore")  # TODO: fix plot_detection to prevent warnings
#     fdtd.plot_detection(dic)

def InitializeGrid(grid_x, grid_y, grid_z, grid_spacing, PML_width):
    global grid

    grid = fdtd.Grid(shape=(grid_x, grid_y, grid_z),
                     grid_spacing=grid_spacing)

    grid[0:PML_width, :, :] = fdtd.PML(name="pml_xlow")
    grid[-PML_width:, :, :] = fdtd.PML(name="pml_xhigh")
    grid[:, 0:PML_width, :] = fdtd.PML(name="pml_ylow")
    grid[:, -PML_width:, :] = fdtd.PML(name="pml_yhigh")
    grid[:, :, 0:PML_width] = fdtd.PML(name="pml_zlow")
    grid[:, :, -PML_width:] = fdtd.PML(name="pml_zhigh")


def Plot(grid, time, simfolder):
    """fdtd计算以及绘图"""
    print(list_of_waveguide)
    print(grid)
    for i in range(0, 119, 7):
        try:
            grid[list_of_waveguide[i + 3]:list_of_waveguide[i + 3] + list_of_waveguide[i],
            list_of_waveguide[i + 4]:list_of_waveguide[i + 4] + list_of_waveguide[i + 1],
            list_of_waveguide[i + 5]:list_of_waveguide[i + 5] + list_of_waveguide[i + 2]] = fdtd.Object(
                permittivity=list_of_waveguide[i + 6], name="object%d" % (i / 7))
        except:
            break

    for i in range(0, 102, 6):
        try:
            grid[list_of_source[i + 3]:list_of_source[i + 3] + list_of_source[i],
            list_of_source[i + 4]:list_of_source[i + 4] + list_of_source[i + 1],
            list_of_source[i + 5]:list_of_source[i + 5] + list_of_source[i + 2]] = fdtd.LineSource(
                period=1550e-9 / (3e8), name="source%d" % (i / 6))
        except:
            break

    for i in range(0, 102, 6):
        try:
            grid[list_of_detector[i + 3]:list_of_detector[i + 3] + list_of_detector[i],
            list_of_detector[i + 4]:list_of_detector[i + 4] + list_of_detector[i + 1],
            list_of_detector[i + 5]:list_of_detector[i + 5] + list_of_detector[i + 2]] = fdtd.LineDetector(
                name="detector%d" % (i / 6))
        except:
            break

    grid.run(total_time=time)
    grid.visualize(z=0, animate=True, save=True, index=0, folder=simfolder, show=False)
    grid.visualize(y=0, animate=True, save=True, index=1, folder=simfolder, show=False)
    grid.visualize(x=0, animate=True, save=True, index=2, folder=simfolder, show=False)

    imgxy_0 = Image.open('%s/file0000.png' % simfolder)
    imgxz_0 = Image.open('%s/file0001.png' % simfolder)
    imgyz_0 = Image.open('%s/file0002.png' % simfolder)

    Resize(imgxy_0, 0)
    Resize(imgxz_0, 1)
    Resize(imgyz_0, 2)

    # 将图像显示在画布上
    imgxy = tk.PhotoImage(file='%s/file0000.png' % simfolder)
    imgxz = tk.PhotoImage(file='%s/file0001.png' % simfolder)
    imgyz = tk.PhotoImage(file='%s/file0002.png' % simfolder)
    canvas.create_image(screenwidth * 2 / 5, 0, image=imgxy, anchor='ne')
    canvas.create_image(screenwidth * 4 / 5, 0, image=imgxz, anchor='ne')
    canvas.create_image(screenwidth * 2 / 5, screenheight * 2 / 5, image=imgyz, anchor='ne')
    canvas.pack()
    window.mainloop()


def window_set_grid():
    """点击新建首先弹出设置模拟区域的窗口"""  # TODO:感觉这样设置很笨拙

    def confirm_grid():
        global grid_x
        global grid_y
        global grid_z
        global PML_width
        global grid_spacing

        grid_x = int(Text_x1.get())  # get()函数返回str
        grid_y = int(Text_y1.get())
        grid_z = int(Text_z1.get())
        PML_width = int(pml.get())
        grid_spacing = float(Text_grid_spacing.get())

        global simfolder

        InitializeGrid(grid_x, grid_y, grid_z, grid_spacing, PML_width)
        simfolder = grid.save_simulation("GRIN")

        Plot(grid, 0, simfolder)
        window_set_grid.destroy()

    window_set_grid = tk.Toplevel(window)
    window_set_grid.title('设置模拟区域')
    window_set_grid.geometry('500x500')
    # 指定模拟区域(规格，空间步长，pml宽度）
    tk.Label(window_set_grid, text='x').place(x=25, y=30)
    tk.Label(window_set_grid, text='y').place(x=25, y=80)
    tk.Label(window_set_grid, text='z').place(x=25, y=130)
    tk.Label(window_set_grid, text='空间步长,单位um').place(x=25, y=180)
    tk.Label(window_set_grid, text='PML边界宽度').place(x=25, y=230)

    var_x1 = tk.IntVar(value=200)
    var_grid_spacing = tk.IntVar(value=0.1)
    var_pml = tk.IntVar(value=10)

    Text_x1 = tk.Entry(window_set_grid, textvariable=var_x1)
    Text_x1.place(x=300, y=30)
    Text_y1 = tk.Entry(window_set_grid, textvariable=var_x1)
    Text_y1.place(x=300, y=80)
    Text_z1 = tk.Entry(window_set_grid, textvariable=var_x1)
    Text_z1.place(x=300, y=130)
    Text_grid_spacing = tk.Entry(window_set_grid, textvariable=var_grid_spacing)
    Text_grid_spacing.place(x=300, y=180)
    pml = tk.Entry(window_set_grid, textvariable=var_pml)
    pml.place(x=300, y=230)

    Button_confirm0 = tk.Button(window_set_grid, text='确认', width=15, height=2,
                                command=confirm_grid)
    Button_confirm0.place(x=300, y=280)


if __name__ == '__main__':
    window = tk.Tk()
    window.title('fdtd')

    # 获取屏幕尺寸
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    size_geo = '%dx%d' % (screenwidth, screenheight)
    window.geometry(size_geo)

    canvas = tk.Canvas(window,
                       bg='#CDC9A5',
                       height=screenheight * 4 / 5,
                       width=screenwidth * 4 / 5)
    canvas.pack()
    line1 = canvas.create_line([(0, screenheight * 2 / 5), (screenwidth * 4 / 5, screenheight * 2 / 5)], fill="black",
                               dash=(1, 1), width=2)
    line2 = canvas.create_line([(screenwidth * 2 / 5, 0), (screenwidth * 2 / 5, screenheight * 4 / 5)], fill="black",
                               dash=(1, 1), width=2)

    main_menu = tk.Menu(window)

    filemenu = tk.Menu(main_menu, tearoff=False)

    filemenu.add_command(label="新建", accelerator="Ctrl+N", command=window_set_grid)
    filemenu.add_command(label="打开", accelerator="Ctrl+O")
    filemenu.add_command(label="保存", accelerator="Ctrl+S")
    filemenu.add_separator()
    filemenu.add_command(label="退出", command=window.quit)
    # 在主目录菜单上新增"文件"选项，并通过menu参数与下拉菜单绑定
    main_menu.add_cascade(label="文件", menu=filemenu)

    # filemenu = tk.Menu(main_menu, tearoff=False)

    component_set_menu = tk.Menu(main_menu, tearoff=False)
    component_set_menu.add_command(label='元件设置', command=Button_set_object_command)
    component_set_menu.add_command(label='光源设置', command=Button_set_source_command)
    component_set_menu.add_command(label='传感器设置', command=Button_set_detector_command)
    component_set_menu.add_command(label='FDTD模拟')
    component_set_menu.add_command(label='帮助')
    main_menu.add_cascade(label='器件设置', menu=component_set_menu)

    window.config(menu=main_menu)

    window.mainloop()
