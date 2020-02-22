#! /usr/bin/env python

from __future__ import print_function

#  ROS imports
import rospy
from geometry_msgs.msg import Pose
from std_msgs.msg import (String, Bool)

import os
import json

#  Graphics imports
import Tkinter as tk  # Works on 2.7
import ttk
from custom_notebook import CustomNotebook
from custom_container_tab import RosContainerTab

#  Helper class imports
from intera_examples.msg import SortableObjectMessage as SortableObjectMsg
from sortable_object_class import SortableObject
from object_position_updating_service import LiveViewFrame
import xml.etree.ElementTree as ET

from Tkinter import *
from ttk import *



##  This class will detail how the application window will be constructed
class Application(Frame):

    def __init__(self, master=None):
        #  ros initialization
        rospy.init_node("main_gui_node")
        self.publisher = rospy.Publisher('move_to_dest/goal', SortableObjectMsg, queue_size=10)
        self.shutdown_ik_pub = rospy.Publisher('rsdk_flex_ik_service_client/shudown', Bool, queue_size=10)
        rospy.Rate(10)

        #  Graphics initialization
        Frame.__init__(self, master)

        #  Create Notebook 
        self.notebook = CustomNotebook()
        
        #  Create Tabs and add 
        self.create_tab(self.notebook)
        self.notebook.pack(expand=1, fill="both")

        self.pack()
        self.createWidgets()

        master.title('ROS TEST UI')



    ##  This method will send a SortableObjectMsg to the ik solver
    def send_object_pos(self):
        if self.notebook.m_all_open_tabs_dict.values() <= 0:
            error_name = "No Containers!"
            error_msg = "There are no containers! Try adding some with the <Add Container> button"
            self.error_popup_msg(error_name, error_msg)
            return

        #  For every tab, get m_selected_objects_dict
        for tab in self.notebook.m_all_open_tabs_dict.values():

            for item in tab.m_selected_objects_dict.values():  # Get all selected SortableObjects
                msg = item.to_sortableObjectMessage()
                self.publisher.publish(msg)
                
        self.top_lvl_window = tk.Toplevel(self.master)
        self.top_lvl_window.title("Live View")
        self.top_lvl_window.minsize(150,100)
        self.top_lvl_window.maxsize(450, 400)
        self.live_sort_window = LiveViewFrame(self.top_lvl_window, i_all_containers=self.notebook.m_all_open_tabs_dict.keys(), i_selected_objects=self.get_selected_objects())



    ##  Create widgets which are not specific to tabs
    ##  TODO: Replace the QUIT button with a RUN button, talks to ik solver
    def createWidgets(self):

        style = ttk.Style()  # Create style for buttons
        style.configure("WR.TButton", foreground="white", background="red", width=20, height=20)

        self.run = ttk.Button(self, text="RUN", style="WR.TButton", command= lambda: self.send_object_pos())
        self.run.pack(side='left', ipadx=10, padx=30)
        
        self.add_container_button = ttk.Button(self, text="Add Container", command= lambda: self.create_tab(self.notebook))
        self.add_container_button.pack(side='right', ipadx=10, padx=30)



    ##  This method will be used to add tabs to the notebook
    def create_tab(self, note):

        tab = note.add_tab(parent_note=note)

        if tab != None:
            #  Create a grid with dimensions 10x10
            for i in range(10):
                tab.rowconfigure(i, weight=1)
                tab.columnconfigure(i, weight=1)



    ##  This method returns a list of all selected object names
    def get_selected_objects(self):
        selected_obj_list = []
        
        for container in self.notebook.m_all_open_tabs_dict.values():
            for item in container.m_selected_objects_dict.keys():
                selected_obj_list.append(item)
        return selected_obj_list


    ##  This method will create a popup if some error occures
    def error_popup_msg(self, error_name, error_msg):
        title = "Error: " + str(error_name)
        tkMessageBox.showerror(title, error_msg)

    
    ##  This method will shutdown the current and the ik_solver node
    def shutdown_nodes(self):
        signal = Bool(True)
        self.shutdown_ik_pub.publish(signal)
        rospy.signal_shutdown("User closed main ui window")





root = Tk()  # The window which will contain all components
root.geometry('750x500')  # Default size of window 

app = Application(master=root)


def handle_close():
    app.shutdown_nodes()
    root.destroy()


root.protocol('WM_DELETE_WINDOW', handle_close)
app.mainloop()