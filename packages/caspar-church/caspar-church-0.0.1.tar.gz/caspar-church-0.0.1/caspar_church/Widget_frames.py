#Copyright (C) <2020>  <Jeffrey Rydell>
import tkinter as tk
from tkinter import ttk
from tkinter import *

def Sort_Widget_start(event):
    Widget = event.widget
    Widget.changed_position = False
    Source_index = Widget.index
    Master = Widget.Container_index
    widget_info = Master[Source_index].place_info()
    if Master[Source_index].orientation == "Vertical":
        Widget.start_Y = int(widget_info.get('y'))
    # print(Widget.orientation)
    if Master[Source_index].orientation == "Horizontal":
        Widget.start_X = int(widget_info.get('x'))

def Sort_Widget_motion(event):
    Widget = event.widget
    Master = Widget.Container_index# gets the widget frame array of the widget's parent frame 

    Source_index = Widget.index 

    widget_info = Master[Source_index].place_info()
    widget_index = Master[Source_index].Position_index

    widget_x = int(widget_info.get('x'))
    widget_y = int(widget_info.get('y'))
    if Widget.orientation == "Vertical":
        # print("working1")
        Dest_index = round((widget_y-10) / 160)
    if Widget.orientation == "Horizontal":
        Dest_index = round((widget_x-10) / 160)
    if Dest_index <= 0:
        Dest_index = 0
    if Dest_index >= len(Master):
        Dest_index = len(Master)
    NEW_x =  widget_x  + event.x
    NEW_y = widget_y  + event.y
    Widget.end_x = NEW_x
    if Dest_index != widget_index:
        cnt = 0
        for item in Master:
            if item.Position_index == Dest_index:
                item.Position_index = widget_index
                item_place_info = item.place_info()

                if Master[Source_index].orientation == "Vertical":
                    Widget.new_dest_y = int(item_place_info.get('y'))
                    item.place(y=Widget.start_Y)
                    Widget.start_Y = int(item_place_info.get('y'))

                if Master[Source_index].orientation == "Horizontal":
                    Widget.new_dest_x = int(item_place_info.get('x'))
                    item.place(x=Widget.start_X)
                    Widget.start_X = int(item_place_info.get('x'))
            cnt += 1
            
        Master[Source_index].Position_index = Dest_index
        Master[Source_index].place(x=NEW_x,y=NEW_y)
        Widget.changed_position = True
    else:
        Master[Source_index].place(x=NEW_x,y=NEW_y)

def Sort_Widget_end(event):
    Widget = event.widget
    Source_index = Widget.index 
    Master = Widget.Container_index
    if Widget.changed_position == True:
        if Master[Source_index].orientation == "Vertical":
            Master[Source_index].place(x=0, y=Widget.new_dest_y)

        if Master[Source_index].orientation == "Horizontal":
            Master[Source_index].place(x=Widget.new_dest_x ,y=20)
            

def delete_widget_frame(WidgetIndex, index, grid, canvas, x_y, offset):# global widget delete function to eliminate excess code
    WidgetIndex[index].state = False
    WidgetIndex[index].destroy()
    WidgetIndex[index].Position_index = -1
    widget_place = 0
    NewPindex = 0
    for x in range(len(WidgetIndex)):
        for ItemFrame in WidgetIndex:
            if ItemFrame.state == True:
                if ItemFrame.Position_index == x:
                    ItemFrame.Position_index = NewPindex
                    if x_y == "y":
                        ItemFrame.place(y=widget_place)
                        widget_place += offset
                    if x_y == "x":    
                        ItemFrame.place(x=widget_place)
                        widget_place += offset
                    NewPindex +=1
    if x_y == "y":
        grid_height = grid.cget('height')
        grid.configure(height=int(grid_height) - offset)
    if x_y == "x":
        grid_width = grid.cget('width')
        grid.configure(width=int(grid_width) - offset)

    canvas.configure(scrollregion=canvas.bbox("all")) # updates the scrollbar
    return widget_place, NewPindex

def add_widget_frame(frame_index, Index, PosIndex, widgetPosition, orientation, grid, canvas, Width, Height,X,Y):
    WidgetFrame = tk.LabelFrame(grid)

    if orientation == "Vertical":
        WidgetFrame.place(y=(widgetPosition), x=X, width=Width,height=Height)
        WidgetFrame.orientation = "Vertical"
        grid_height = grid.cget('height')
        grid.configure(height=int(grid_height) + Height)
        widgetPosition += Height

    if orientation == "Horizontal":
        WidgetFrame.place(y=Y, x=(widgetPosition), width=Width,height=Height)
        WidgetFrame.orientation = "Horizontal"
        grid_width = grid.cget('width')
        grid.configure(width=int(grid_width) + Width)
        widgetPosition += Width

    frame_index.append(WidgetFrame)

    WidgetFrame.state = True
    WidgetFrame.Position_index = PosIndex
    WidgetFrame.index = Index
    WidgetFrame.Container_index = frame_index
    WidgetFrame.Canvas = canvas # for mousewheel
    WidgetFrame.bind('<Button-1>', Sort_Widget_start)
    WidgetFrame.bind('<B1-Motion>', Sort_Widget_motion)
    WidgetFrame.bind('<ButtonRelease-1>', Sort_Widget_end)
    canvas.configure(scrollregion=canvas.bbox("all"))

    PosIndex += 1

    return WidgetFrame, widgetPosition, PosIndex

def add_scrollable_canvas(Frame ,XY, Application,Height=None, Width=None, G_Width=None, G_Height=None, ):

        if XY == "X":
            SC_Canvas = Canvas(Frame, height=Height, width=Width) # width=1300, height=900
            SC_Canvas.pack(side=TOP, fill=X, expand=1)

            scrollbar = ttk.Scrollbar(Frame, orient=HORIZONTAL,command=SC_Canvas.xview)
            scrollbar.pack(side=BOTTOM, fill=X)
            SC_Canvas.configure(xscrollcommand=scrollbar.set)


        if XY == "Y":
            SC_Canvas = Canvas(Frame, height=Height, width=Width) # width=1300, height=900
            SC_Canvas.pack(side=LEFT, fill=BOTH, expand=1)

            scrollbar = ttk.Scrollbar(Frame, orient=VERTICAL,command=SC_Canvas.yview)
            scrollbar.pack(side=RIGHT, fill=Y)
            SC_Canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.Canvas = SC_Canvas # for mousewheel

        SC_Canvas.XY = XY
        SC_Canvas.bind('<Configure>', lambda e: SC_Canvas.configure(scrollregion = SC_Canvas.bbox("all")))
        Frame.Canvas = SC_Canvas # for mousewheel

        SC_grid = tk.Frame(SC_Canvas, width=G_Width, height=G_Height) 
        SC_Canvas.create_window((0,0),window=SC_grid, anchor="nw")

        SC_grid.Canvas = SC_Canvas # for mousewheel
        SC_grid.bind('<Enter>', Application._bound_to_mousewheel)
        SC_grid.bind('<Leave>', Application._unbound_to_mousewheel)
        return SC_Canvas, SC_grid
############################# End of widget sorting functions