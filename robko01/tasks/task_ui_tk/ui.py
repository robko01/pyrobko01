#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

Robko 01 - Python ControlSoftware

Copyright (C) [2020] [Orlin Dimitrov]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import queue

from tkinter import BOTTOM, RAISED, SUNKEN, W, X, BooleanVar, Button, Checkbutton, Frame, IntVar, Label, LabelFrame, Listbox, Menu, PhotoImage, Scale, Text, Tk, messagebox
from tkinter.messagebox import askyesno
from tkinter.ttk import Notebook

from robko01.tasks.task_ui_tk.led import LedStatus
from robko01.tasks.task_ui_tk.led import LedShape
from robko01.tasks.task_ui_tk.led import LED

from robko01.utils.logger import get_logger
from robko01.utils.thread_timer import ThreadTimer
from robko01.utils.timer import Timer
from robko01.utils.utils import scale
from robko01.utils.axis_action_controller import AxisActionController
from robko01.utils.actions import Actions

from robko01.kinematics.data.steppers_coefficients import SteppersCoefficients
from robko01.kinematics.kinematics import Kinematics

from robko01.joystick.joystick import JoystickController

import serial

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, Orlin Dimitrov"
"""Copyright holder"""

__credits__ = []
"""Credits"""

__license__ = "GPLv3"
"""License
@see http://www.gnu.org/licenses/"""

__version__ = "1.0.0"
"""Version of the file."""

__maintainer__ = "Orlin Dimitrov"
"""Name of the maintainer."""

__email__ = "robko01@8bitclub.com"
"""E-mail of the author."""

__class_name__ = "GUI"
"""Task name."""

#endregion

class GUI():

#region Attributes

    __logger = None
    """Logger module.
    """

    __master = None
    """Form master object.
    """

    __frm_tab_man = None
    """Form tab manual.
    """

    __frm_tab_auto = None
    """Forma tab auto.
    """

    __frm_port_a_input_leds = []
    """Port A input LEDs.
    """

    __frm_port_a_output_chk = []
    """Port A outputs Checks.
    """

    __frm_axis_labels = []
    """Axis labels.
    """

    __frm_axis_control_leds = []
    """Axis control LEDs.
    """

    __frm_axis_controllers = []
    """Axis controllers.
    """

    __actions_queue = None
    """Actions queue.
    """

    __controller = None
    """Robot controller.
    """

    __current_speed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    """Axis speeds.
    """

    __current_position = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    """Current end-efector position.
    """

    __axis_states = 0
    """Axis action states.
    """

    __port_a_inputs = 0
    """Port A inputs.
    """

    __port_a_outputs = 0
    """Port A outputs.
    """

    __bit_weight = [128, 64, 32, 16, 8, 4, 2, 1]

    __dead_zone = 0.2
    """Joystick analogs dead zone.
    """

    __jsax_to_rbtax = {0:0, 1:1, 2:4, 3:2, 4:5}
    """Joystick controller map to robot axis.
    """

    __jsbtn_to_rbtoc = {0:6}
    """Joystick controller map to robot axis.
    """

    __jsc = None
    """Joiystick controller.
    """

    __kb_key_state = ""
    """Keyboard key state.
    """

    __block_grasping = False
    """Block grasping action flag.
    """

#endregion

#region Constructor

    def __init__(self, **kwargs):

        if "controller" in kwargs:
            self.__controller = kwargs["controller"]

        if self.__logger is None:
            self.__logger = get_logger(__name__)

        self.__actions_queue = queue.Queue()

        self.__action_update_timer = ThreadTimer()
        self.__action_update_timer.update_rate = 0.01
        self.__action_update_timer.set_cb(self.__action_timer_cb)

        self.__frm_update_timer = Timer()
        self.__frm_update_timer.update_rate = 0.05
        self.__frm_update_timer.set_cb(self.__frm_update)

        # Key controllers.
        self.__frm_axis_controllers.append(AxisActionController(callback=self.__axis_0))
        self.__frm_axis_controllers.append(AxisActionController(callback=self.__axis_1))
        self.__frm_axis_controllers.append(AxisActionController(callback=self.__axis_2))
        self.__frm_axis_controllers.append(AxisActionController(callback=self.__axis_3))
        self.__frm_axis_controllers.append(AxisActionController(callback=self.__axis_4))
        self.__frm_axis_controllers.append(AxisActionController(callback=self.__axis_5))

        # Kinematics
        self.__kin = Kinematics()
        self.__sc = SteppersCoefficients()

#endregion

#region Private Methods (Autmaton)

    def __init_automation(self):

        pass

    def __update_automation(self):

        # Stop the gripper if it is closed enough.
        if (1 & self.__port_a_inputs):
            if self.__frm_axis_controllers[5].direction == -1:
                self.__frm_axis_controllers[5].stop()
        
        # if (2 & self.__port_a_inputs):
        #     if self.__frm_axis_controllers[5].direction == -1:
        #         self.__frm_axis_controllers[5].stop()

#endregion

#region Private Methods (Action Control)

    def __put_action(self, action):

        self.__actions_queue.put(action)

    def __do_action(self, action):

        if action == Actions.NONE:
            pass

        if action == Actions.UpdateSpeeds:
            self.__controller.move_speed(self.__current_speed)

        elif action == Actions.UpdateOutputs:
            self.__controller.set_outputs(self.__port_a_outputs)

        elif action == Actions.ClearController:
            self.__controller.clear()

        elif action == Actions.ResetController:
            pass

        elif action == Actions.DoTest1:
            # self.__controller.move_absolute([200, 100, 200, 100, 200, 100, 0, 0, 0, 0, 0, 0])
            pass

        elif action == Actions.DoTest2:
            # self.__controller.move_absolute([0, 100, 0, 100, 0, 100, 0, 0, 0, 0, 0, 0])
            pass

    def __action_timer_cb(self):

        try:
            self.__axis_states = self.__controller.is_moving()
            self.__port_a_inputs = self.__controller.get_inputs()
            self.__current_position = self.__controller.current_position()

            if not self.__actions_queue.empty():
                action = self.__actions_queue.get()
                self.__do_action(action)

        except serial.serialutil.SerialException as e:
            self.__logger.info(e)

        except Exception as e:
            self.__logger.info(e)

#endregion

#region Private Methods (Axices CB)

    def __axis_0(self, speed):

        self.__current_speed[1] = speed * -1

        self.__put_action(Actions.UpdateSpeeds)

    def __axis_1(self, speed):

        self.__current_speed[3] = speed * -1

        self.__put_action(Actions.UpdateSpeeds)

    def __axis_2(self, speed):

        self.__current_speed[5] = speed
        self.__current_speed[11] = speed * -1

        self.__put_action(Actions.UpdateSpeeds)

    def __axis_3(self, speed):

        self.__current_speed[7] = speed * -1
        self.__current_speed[9] = speed

        self.__put_action(Actions.UpdateSpeeds)

    def __axis_4(self, speed):

        self.__current_speed[7] = speed
        self.__current_speed[9] = speed

        self.__put_action(Actions.UpdateSpeeds)

    def __axis_5(self, speed):

        self.__current_speed[11] = speed

        self.__put_action(Actions.UpdateSpeeds)

#endregion

#region Private Methods (Keyboard Events)

    def __kbc_key_release(self, event):
        self.__kb_key_state = "UP({})".format(event.char)

    def __kbc_key_press(self, event):

        char = event.char

        self.__kb_key_state = "DN({})".format(char)

        if char == " ":
            for key_controller in self.__frm_axis_controllers:
                key_controller.stop()

        elif char == "1":
            self.__frm_axis_controllers[0].set_cw()

        elif char == "q":
            self.__frm_axis_controllers[0].set_ccw()

        elif char == "2":
            self.__frm_axis_controllers[1].set_cw()

        elif char == "w":
            self.__frm_axis_controllers[1].set_ccw()

        elif char == "3":
            self.__frm_axis_controllers[2].set_cw()

        elif char == "e":
            self.__frm_axis_controllers[2].set_ccw()

        elif char == "4":
            self.__frm_axis_controllers[3].set_cw()

        elif char == "r":
            self.__frm_axis_controllers[3].set_ccw()

        elif char == "5":
            self.__frm_axis_controllers[4].set_cw()

        elif char == "t":
            self.__frm_axis_controllers[4].set_ccw()

        elif char == "6":
            self.__frm_axis_controllers[5].set_cw()

        elif char == "y":
            self.__frm_axis_controllers[5].set_ccw()

    def __kbc_enable(self, value):
        if value:
            # Bind keys.
            self.__bid_press = self.__master.bind_all("<KeyPress>", self.__kbc_key_press)
            self.__bid_release = self.__master.bind_all("<KeyRelease>", self.__kbc_key_release)

            self.__led_kb_state.turnon()

        else:
            # Unbind keys.
            self.__master.unbind("<KeyPress>", self.__bid_press)
            self.__master.unbind("<KeyRelease>", self.__bid_release)

            self.__led_kb_state.turnoff()

#endregion

#region Private Methods (Joiystick Events)

    def __jsc_update_cb(self, button_data, axis_data, hat_data):

        # for index in button_data:
        #     value = button_data[index]
        #     if value == True:
        #         print(index, value)

        # print(axis_data)

        # return

        # Key map to OC/DO.
        # Go trought button map.
        for button, bit in self.__jsbtn_to_rbtoc.items():

            # Read button state.
            act_bit_state = button_data[button]

            # Check bit state.
            prev_bit_state = self.__frm_port_a_output_chk[bit].get() > 0

            # Comapare the bit states.
            update_flag = prev_bit_state != act_bit_state

            # If it is time to update.
            if update_flag:

                # Apply actual bit state.
                if act_bit_state:
                    self.__frm_port_a_output_chk[bit].set(self.__bit_weight[bit])
                else:
                    self.__frm_port_a_output_chk[bit].set(0)

        self.__block_grasping = False

        # Stop all axices!
        if button_data[15] == True:
            for key_controller in self.__frm_axis_controllers:
                if key_controller.is_stopped:
                    key_controller.stop()

        # Switch right analog function.
        if button_data[10] == True:
            self.__jsax_to_rbtax[3] = 3
        else:
            self.__jsax_to_rbtax[3] = 2

        # Go trought analogs functions and axices.
        for index in range(4):
            # Does the axis exists?
            if index in axis_data:
                pos = axis_data[index]
                # Does the axis is out of the dead zone?
                if abs(pos) >= self.__dead_zone:
                    self.__frm_axis_controllers[self.__jsax_to_rbtax[index]].speed = int(abs(scale(pos, -1.0, 1.0, -self.__max_speed, self.__max_speed)))
                    if pos < 0:
                        self.__frm_axis_controllers[self.__jsax_to_rbtax[index]].set_ccw()
                    elif pos > 0:
                        self.__frm_axis_controllers[self.__jsax_to_rbtax[index]].set_cw()
                    else:
                        self.__frm_axis_controllers[self.__jsax_to_rbtax[index]].stop()

                    # Block grasping when moving elbow.
                    self.__block_grasping = ((index == 3) and (self.__frm_axis_controllers[self.__jsax_to_rbtax[index]].is_stopped == False))

                else:
                    if not self.__frm_axis_controllers[self.__jsax_to_rbtax[index]].is_stopped:
                        self.__frm_axis_controllers[self.__jsax_to_rbtax[index]].stop()

        index = 4
        # Does the axis exists?
        if (index in axis_data) and (self.__block_grasping == False):
            pos = axis_data[index]
            # Does the axis is out of the dead zone?
            if abs(pos) >= self.__dead_zone:
                self.__frm_axis_controllers[self.__jsax_to_rbtax[index]].speed = int(abs(scale(pos, -1.0, 1.0, 0, self.__max_speed)))
                if button_data[9] == True:
                    self.__frm_axis_controllers[self.__jsax_to_rbtax[index]].set_cw()
                else:
                    self.__frm_axis_controllers[self.__jsax_to_rbtax[index]].set_ccw()
            else:
                if not self.__frm_axis_controllers[self.__jsax_to_rbtax[index]].is_stopped:
                    self.__frm_axis_controllers[self.__jsax_to_rbtax[index]].stop()

    def __jsc_enable(self, value):

        try:
            if value:
                if self.__jsc == None:
                    self.__jsc = JoystickController()
                    self.__jsc.update_cb(self.__jsc_update_cb)

                    self.__led_js_state.turnon()

            else:
                if self.__jsc is not None:
                    del self.__jsc
                    self.__jsc = None

                    self.__led_js_state.turnoff()

        except Exception as e:
            messagebox.showerror("error", e)
            self.__bv_enable_jsc.set(False)

            self.__led_js_state.turnoff()

#endregion

#region Private Methods (Menu)

    def __mnu_clear_controller(self):

        answer = askyesno(title="Clear axis positions",
            message="Are you sure you want to clear the axis positions?")
        
        if answer:
            self.__put_action(Actions.ClearController)

    def __mnu_reset_controller(self):

        answer = askyesno(title="Reset robot controller",
            message="Are you sure you want to reset the robot controller?")
        
        if answer:
            self.__put_action(Actions.ResetController)

    def __mnu_enable_kbc(self):

        value = self.__bv_enable_kbc.get()

        self.__kbc_enable(value)

    def __mnu_enable_jsc(self):

        value = self.__bv_enable_jsc.get()

        self.__jsc_enable(value)

    def __mnu__do_test_1(self):

        self.__put_action(Actions.DoTest1)

    def __mnu__do_test_2(self):

        self.__put_action(Actions.DoTest2)

    def __create_menu_bar(self):

        donothing = None

        # Menu bar.
        menu_bar = Menu(self.__master)

        # First menu block.
        filemenu = Menu(menu_bar, tearoff=0)
        filemenu.add_command(label="New", command=donothing)
        filemenu.add_command(label="Open", command=donothing)
        filemenu.add_command(label="Save", command=donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.__frm_on_closing)
        menu_bar.add_cascade(label="File", menu=filemenu)

        # Second menu block.
        controller_menu = Menu(menu_bar, tearoff=0)
        controller_menu.add_command(label="Clear", command=self.__mnu_clear_controller)
        controller_menu.add_command(label="Reset", command=self.__mnu_reset_controller)
        
        self.__bv_enable_kbc = BooleanVar()
        self.__bv_enable_kbc.set(False)
        controller_menu.add_checkbutton(
            label="Enable Keyboard Control",
            onvalue=1,
            offvalue=0,
            variable=self.__bv_enable_kbc,
            command=self.__mnu_enable_kbc)

        self.__bv_enable_jsc = BooleanVar()
        self.__bv_enable_jsc.set(False)
        controller_menu.add_checkbutton(
            label="Enable Joystick Control",
            onvalue=1,
            offvalue=0,
            variable=self.__bv_enable_jsc,
            command=self.__mnu_enable_jsc)

        # controller_menu.add_command(label="Do Test 1", command=self.__mnu__do_test_1)

        # controller_menu.add_command(label="Do Test 2", command=self.__mnu__do_test_2)

        menu_bar.add_cascade(label="Controller", menu=controller_menu)

        # Third menu block.
        helpmenu = Menu(menu_bar, tearoff=0)
        helpmenu.add_command(label="About", command=donothing)
        menu_bar.add_cascade(label="Help", menu=helpmenu)

        # Add the menu.
        self.__master.config(menu=menu_bar)

#endregion

#region Private Methods (Tabs)

    def __create_tabs(self):

        self.notebook = Notebook(self.__master)

        self.__frm_tab_man = Frame(self.notebook)
        self.notebook.add(self.__frm_tab_man, text="Manual")

        self.__frm_tab_auto = Frame(self.notebook)
        self.notebook.add(self.__frm_tab_auto, text="Auto")        

        self.notebook.pack(expand=1, fill ="both")

#endregion

#region Private Methods (Status Bar)

    def __update_port_a_inputs(self):

        if len(self.__frm_port_a_input_leds) == 8:
            led_index = 7
            for index in range(0, 8):
                if (2**index) & self.__port_a_inputs:
                    self.__frm_port_a_input_leds[led_index].turnoff()
                else:
                    self.__frm_port_a_input_leds[led_index].turnon()
                led_index -= 1

    def __create_port_a_inputs(self):

        # Create the frame.
        lbl_frame = LabelFrame(self.__frm_status_frame, text="DI on port A")
        lbl_frame.place(x=300, y=0)

        led_w = 20
        led_h = 20

        for index in range(0, 8):

            led = LED(lbl_frame, shape=LedShape.ROUND, status=LedStatus.OFF,
                width=led_w, height=led_h, appearance=RAISED,
                blink=0, bd=1, outline="")
            led.frame.grid(row=0, column=index)

            self.__frm_port_a_input_leds.append(led)


    def __update_axis_control_leds(self):

        if len(self.__frm_axis_control_leds) == 6:
            for index in range(0, 6):
                if (2**index) & self.__axis_states:
                    self.__frm_axis_control_leds[index].turnon()
                else:
                    self.__frm_axis_control_leds[index].turnoff()

    def __create_axis_control_leds(self):

        # Create the frame.
        lbl_frame = LabelFrame(self.__frm_status_frame, text="Axis control LEDs")
        lbl_frame.place(x=160, y=0)

        led_w = 20
        led_h = 20

        for index in range(0, 6):

            led = LED(lbl_frame, shape=LedShape.ROUND, status=LedStatus.OFF,
                width=led_w, height=led_h, appearance=RAISED,
                blink=0, bd=1, outline="")
            led.frame.grid(row=0, column=index)

            self.__frm_axis_control_leds.append(led)


    def __update_cartesian_pos_lbl(self):

        j1 = self.__current_position[0] / self.__sc.t1_const
        j2 = self.__current_position[2] / self.__sc.t2_const
        j3 = self.__current_position[4] / self.__sc.t3_const
        j4 = self.__current_position[6] / self.__sc.t4_const
        j5 = self.__current_position[8] / self.__sc.t5_const
        d_pos = self.__kin.forward_from_scale(j1, j2, j3, j4, j5)
        x = d_pos[0]
        y = d_pos[1]
        z = d_pos[2]
        p = d_pos[3]
        r = d_pos[4]
        message = "X: {0:4.2f} P: {3:4.2f}\nY: {1:4.2f} R: {3:4.2f}\nZ: {2:4.2f}".format(x, y, z, p, r)
        self.__lbl_pos.config(text=message)
    
    def __create_cartesian_pos_lbl(self):
        text_pos = "-------------------"
        self.__lbl_pos = Label(self.__frm_status_frame, text=text_pos, width=len(text_pos))
        self.__lbl_pos.place(x=500, y=0) # , width= 400, height= 300)


    def __craete_kb_status_led(self):

        kb_status_frame = LabelFrame(self.__frm_status_frame, text="Keyboard")
        kb_status_frame.place(x=30, y=0)

        self.__led_kb_state = LED(kb_status_frame, shape=LedShape.ROUND, status=LedStatus.OFF,
                width=20, height=20, appearance=RAISED,
                blink=0, bd=1, outline="")
        self.__led_kb_state.frame.grid(row=0, column=0)

        self.__lbl_kb_status = Label(kb_status_frame)
        self.__lbl_kb_status.place(x=23, y=0)

    def __craete_js_status_led(self):

        js_status_frame = LabelFrame(self.__frm_status_frame, text="Joystick")
        js_status_frame.place(x=100, y=0)

        self.__led_js_state = LED(js_status_frame, shape=LedShape.ROUND, status=LedStatus.OFF,
                width=20, height=20, appearance=RAISED,
                blink=0, bd=1, outline="")
        self.__led_js_state.frame.grid(row=0, column=1)


    def __update_status_bar(self):

        self.__update_axis_control_leds()

        self.__update_port_a_inputs()

        self.__update_cartesian_pos_lbl()

        self.__lbl_kb_status.config(text="{}".format(self.__kb_key_state))

    def __create_status_bar(self):

        self.__frm_status_frame = Frame(self.__master, bd=1, relief=SUNKEN, height=50)
        self.__frm_status_frame.pack(side=BOTTOM, fill=X)

        self.__craete_kb_status_led()

        self.__craete_js_status_led()

        self.__create_axis_control_leds()

        self.__create_port_a_inputs()

        self.__create_cartesian_pos_lbl()

#endregion

#region Private Methods (Tab Manual)

    def __update_port_a_outputs(self):

        value = 0

        for index in range(0, 8):
            value += self.__frm_port_a_output_chk[index].get()

        if value != self.__port_a_outputs:
            self.__port_a_outputs = value
            self.__put_action(Actions.UpdateOutputs)

    def __create_port_a_outputs(self):

        fields = [
                {
                    "text": "7",
                    "press": lambda event: self.__frm_port_a_output_chk[0].set(self.__bit_weight[0]),
                    "release": lambda event: self.__frm_port_a_output_chk[0].set(0)
                },
                {
                    "text": "6",
                    "press": lambda event: self.__frm_port_a_output_chk[1].set(self.__bit_weight[1]),
                    "release": lambda event: self.__frm_port_a_output_chk[1].set(0)
                },
                {
                    "text": "5",
                    "press": lambda event: self.__frm_port_a_output_chk[2].set(self.__bit_weight[2]),
                    "release": lambda event: self.__frm_port_a_output_chk[2].set(0)
                },
                {
                    "text": "4",
                    "press": lambda event: self.__frm_port_a_output_chk[3].set(self.__bit_weight[3]),
                    "release": lambda event: self.__frm_port_a_output_chk[3].set(0)
                },
                {
                    "text": "3",
                    "press": lambda event: self.__frm_port_a_output_chk[4].set(self.__bit_weight[4]),
                    "release": lambda event: self.__frm_port_a_output_chk[4].set(0)
                },
                {
                    "text": "2",
                    "press": lambda event: self.__frm_port_a_output_chk[5].set(self.__bit_weight[5]),
                    "release": lambda event: self.__frm_port_a_output_chk[5].set(0)
                },
                {
                    "text": "1",
                    "press": lambda event: self.__frm_port_a_output_chk[6].set(self.__bit_weight[6]),
                    "release": lambda event: self.__frm_port_a_output_chk[6].set(0)
                },
                {
                    "text": "0",
                    "press": lambda event: self.__frm_port_a_output_chk[7].set(self.__bit_weight[7]),
                    "release": lambda event: self.__frm_port_a_output_chk[7].set(0)
                },
            ]

        # Create the frame.
        lbl_frame = LabelFrame(self.__frm_tab_man, text="DO on port A")

        # Create the check boxes.
        for index in range(0, 8):

            # Create the check box.
            var = IntVar()
            var.trace_add("write", lambda name, nz, operation: self.__update_port_a_outputs())
            self.__frm_port_a_output_chk.append(var)

            check = Checkbutton(lbl_frame, variable=var, offvalue=0, onvalue=self.__bit_weight[index])
            check.grid(row=0, column=index)

            button = Button(lbl_frame, text="{}".format(fields[index]["text"]), padx=5, pady=2)
            button.bind("<ButtonPress>", fields[index]["press"])
            button.bind("<ButtonRelease>", fields[index]["release"])
            button.grid(row=1, column=index)

        # Place the frame.
        lbl_frame.place(x=300, y=200)


    def __update_axis_speed(self, event):

        self.__max_speed = self.__sldr_speed.get()

        # If the Joystick is active, do not update speed controllers by hand from he slider.
        if self.__jsc is not None:
            return

        for index in range(0, 6):
            self.__frm_axis_controllers[index].speed = self.__max_speed

    def __create_axis_speed(self):

        lbl_frame = LabelFrame(self.__frm_tab_man, text="Axises speed")

        self.__sldr_speed = Scale(lbl_frame, from_=20, to=150, orient="horizontal", command=self.__update_axis_speed)
        self.__sldr_speed.grid(row=0, column=0, sticky="ew")
        self.__sldr_speed.set(100)

        lbl_frame.place(x=33, y=200) # , width= 400, height= 300)


    def __update_axis_controls(self):

        for index in range(0, 6):
            text = "P: {}\nV: {}".format(self.__current_position[index*2], self.__current_position[index*2 + 1])
            self.__frm_axis_labels[index].config(text=text)

    def __create_axis_controls(self):

        w_size = 10
        h_size = 10

        # Create the frame.
        frame = Frame(self.__frm_tab_man)

        empty_text = "P: {}\nV: {}".format(0, 0)

        fields = {
            "cw":[
                {
                    "text": "Base CW",
                    "press": lambda event: self.__frm_axis_controllers[0].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[0].stop()
                },
                {
                    "text": "Shoulder UP",
                    "press": lambda event: self.__frm_axis_controllers[1].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[1].stop()
                },
                {
                    "text": "Elbow UP",
                    "press": lambda event: self.__frm_axis_controllers[2].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[2].stop()
                },
                {
                    "text": "P UP",
                    "press": lambda event: self.__frm_axis_controllers[3].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[3].stop()
                },
                {
                    "text": "R CW",
                    "press": lambda event: self.__frm_axis_controllers[4].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[4].stop()
                },
                {
                    "text": "Gripper OPEN",
                    "press": lambda event: self.__frm_axis_controllers[5].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[5].stop()
                },
            ],
            "ccw":[
                {
                    "text": "Base CCW",
                    "press": lambda event: self.__frm_axis_controllers[0].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[0].stop()
                },
                {
                    "text": "Shoulder DOWN",
                    "press": lambda event: self.__frm_axis_controllers[1].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[1].stop()
                },
                {
                    "text": "Elbow DOWN",
                    "press": lambda event: self.__frm_axis_controllers[2].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[2].stop()
                },
                {
                    "text": "P DOWN",
                    "press": lambda event: self.__frm_axis_controllers[3].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[3].stop()
                },
                {
                    "text": "R CCW",
                    "press": lambda event: self.__frm_axis_controllers[4].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[4].stop()
                },
                {
                    "text": "Gripper CLOSE",
                    "press": lambda event: self.__frm_axis_controllers[5].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[5].stop()
                }
            ]
        }

        buttons_cw = []
        buttons_ccw = []

        for index in range(0, 6):

            self.__frm_axis_labels.append(Label(frame, text=empty_text))
            self.__frm_axis_labels[index].grid(row=0, column=index, ipadx=h_size, ipady=w_size, sticky="ew")

            buttons_cw.append(Button(frame, text=fields["cw"][index]["text"]))
            buttons_cw[index].bind("<ButtonPress-1>", fields["cw"][index]["press"])
            buttons_cw[index].bind("<ButtonRelease-1>", fields["cw"][index]["release"])
            buttons_cw[index].grid(row=1, column=index, ipadx=h_size, ipady=w_size, sticky="ew")

            buttons_ccw.append(Button(frame, text=fields["ccw"][index]["text"]))
            buttons_ccw[index].bind("<ButtonPress-1>", fields["ccw"][index]["press"])
            buttons_ccw[index].bind("<ButtonRelease-1>", fields["ccw"][index]["release"])
            buttons_ccw[index].grid(row=2, column=index, ipadx=h_size, ipady=w_size, sticky="ew")

        # Place the frame.
        frame.place(x=33, y=33)

#endregion

#region Private Methods (Tab Auto)

    def resizeImage(self, img, newWidth, newHeight):

        oldWidth = img.width()
        oldHeight = img.height()
        newPhotoImage = PhotoImage(width=newWidth, height=newHeight)

        for x in range(newWidth):
            for y in range(newHeight):
                xOld = int(x*oldWidth/newWidth)
                yOld = int(y*oldHeight/newHeight)
                rgb = '#%02x%02x%02x' % img.get(xOld, yOld)
                newPhotoImage.put(rgb, (x, y))

        return newPhotoImage

    def __create_list_view(self):

        listbox = Listbox(self.__frm_tab_auto)
        listbox.insert(1,"India")
        listbox.insert(2, "USA")
        listbox.insert(3, "Japan")
        listbox.insert(4, "Austrelia")
        listbox.place(x=20, y=20, w=300, h=200)

        cmd_input = Text(self.__frm_tab_auto)
        cmd_input.place(x=20, y=200, w=300, h=20)

        # cwf = os.path.dirname(os.path.abspath(__file__))
        # file_name = os.path.join(cwf, "resources", "images", "arrow-up.png")
        # image = PhotoImage(file=file_name)
        # img = self.resizeImage(image, 15, 110)
        # btn_up = Button(self.__frm_tab_auto, text="UP", image=img, compound="left")
        btn_up = Button(self.__frm_tab_auto, text="UP")
        btn_up.place(x=320, y=20, w=50, h=30)

        btn_up = Button(self.__frm_tab_auto, text="DOWN")
        btn_up.place(x=320, y=50, w=50, h=30)

        btn_up = Button(self.__frm_tab_auto, text="RUN")
        btn_up.place(x=320, y=80, w=50, h=30)

        btn_up = Button(self.__frm_tab_auto, text="STOP")
        btn_up.place(x=320, y=110, w=50, h=30)

#endregion

#region Private Methods (Form)

    def __frm_update(self):

        self.__update_status_bar()

        self.__update_axis_controls()

        if self.__jsc is not None:
            self.__jsc.update()

        self.__update_automation()

    def __frm_on_closing(self):

        self.__is_runing = False

    def __frm_create(self):

        self.__init_automation()

        self.__master = Tk()
        self.__master.geometry("700x400")
        self.__master.title("Robko 01")
        self.__master.protocol("WM_DELETE_WINDOW", self.__frm_on_closing)

        self.__create_menu_bar()

        self.__create_status_bar()

        self.__create_tabs()

        self.__create_axis_controls()

        self.__create_port_a_outputs()

        self.__create_axis_speed()

        self.__create_list_view()

 #endregion

#region Public Methods

    def start(self):

        self.__action_update_timer.start()

        self.__frm_create()
        self.__frm_update_timer.start()

        self.__is_runing = True
        while self.__is_runing:
            self.__master.update()
            self.__frm_update_timer.update()

        self.__master.quit()

    def stop(self):

        self.__is_runing = False

        self.__action_update_timer.stop()

#endregion
