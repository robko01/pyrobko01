
#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

Robko 01 - Python Control Software

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

import sys
import os
import traceback

from robko01.tasks.task_ui_qt.editor.code_editor import CodeEditor
from robko01.tasks.task_ui_qt.utils.stream_redirector import StreamRedirector
from robko01.tasks.task_ui_qt.utils.worker import Worker

from robko01.kinematics.data.steppers_coefficients import SteppersCoefficients
from robko01.kinematics.kinematics import Kinematics
from robko01.kinematics.utils.utils import xy2lr
from robko01.utils.action_controller import ActionController
from robko01.utils.thread_timer import ThreadTimer
from robko01.utils.logger import get_logger
from robko01.utils.axis_action_controller import AxisActionController
from robko01.utils.actions import Actions
from robko01.utils.utils import scale
from robko01.joystick.joystick import JoystickController

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog
from PySide6.QtCore import QEvent, QObject, Qt, Signal, Slot, QThread, Qt
from PySide6.QtGui import QAction, QTextCursor

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

#endregion

class GUI(QApplication):
    """GUI
    """

#region Attributes

#endregion

#region Constructor

    def __init__(self, **kwargs):
        """Constructor

        Raises:
            ReferenceError: Invalid controller instance.
        """

        super().__init__([])

        self.__logger = get_logger(__name__)
        """Logger module.
        """

        self.__controller = None
        """Robot controller.
        """
        if "controller" in kwargs:
            self.__controller = kwargs["controller"]

        if self.__controller is None:
            raise ReferenceError("Invalid controller instance.")

        # Kinematics
        self.__kin = Kinematics()
        """Kinematics model.
        """        

        self.__sc = SteppersCoefficients()
        """Steppers coefficients.
        """        

        self.__window = None
        """Main window.
        """

        self.__current_speed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        """Axis speeds.
        """

        self.__current_position = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        """Current end-effector position.
        """

        self.__target_position = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        """Target end-effector position.
        """

        self.__axis_states = 0
        """Axis action states.
        """

        self.__axis_states_prev = 0
        """Axis action previous states.
        """

        self.__port_a_inputs = 0
        """Port A inputs.
        """

        self.__port_a_outputs = 0
        """Port A outputs.
        """

        self.__max_speed = 100
        """Maximum speed.
        """

        self.__jsc = None
        """Joystick controller.
        """

        self.__dead_zone = 0.2
        """Joystick analogs dead zone.
        """

        self.__jsax_to_rbtax = {0:0, 1:1, 3:2, 4:5}
        """Joystick controller map to robot axis.
        """

        self.__jsbtn_temp = None
        """Temporary joystick buttons data.
        """

        self.__block_grasping = False
        """Software grasping lock.
        """

        self.__init_update_timer()

        self.__init_axises_controllers()

        self.__init_action_controller()

#endregion

#region Private Methods (Update Timer)

    def __update_displays_animation(self):

        # Update if it si different to prevent flicking.
        if self.__axis_states == self.__axis_states_prev:
            return
        self.__axis_states = self.__axis_states_prev

        # Axis 1
        if 1 & self.__axis_states:
            self.__window.lcdP0.setStyleSheet("""QLCDNumber {
                                                 background-color: yellow; 
                                                 color: black;}""")
            self.__window.lcdV0.setStyleSheet("""QLCDNumber {
                                                 background-color: yellow; 
                                                 color: black;}""")
        else:
            self.__window.lcdP0.setStyleSheet("""QLCDNumber {
                                                 background-color: green; 
                                                 color: yellow;}""")
            self.__window.lcdV0.setStyleSheet("""QLCDNumber {
                                                 background-color: green; 
                                                 color: yellow;}""")

        if 2 & self.__axis_states:
            self.__window.lcdP1.setStyleSheet("""QLCDNumber {
                                                 background-color: yellow; 
                                                 color: black;}""")
            self.__window.lcdV1.setStyleSheet("""QLCDNumber {
                                                 background-color: yellow; 
                                                 color: black;}""")
        else:
            self.__window.lcdP1.setStyleSheet("""QLCDNumber {
                                                 background-color: green; 
                                                 color: yellow;}""")
            self.__window.lcdV1.setStyleSheet("""QLCDNumber {
                                                 background-color: green; 
                                                 color: yellow;}""")

        if 4 & self.__axis_states:
            self.__window.lcdP2.setStyleSheet("""QLCDNumber {
                                                 background-color: yellow; 
                                                 color: black;}""")
            self.__window.lcdV2.setStyleSheet("""QLCDNumber {
                                                 background-color: yellow; 
                                                 color: black;}""")
        else:
            self.__window.lcdP2.setStyleSheet("""QLCDNumber {
                                                 background-color: green; 
                                                 color: yellow;}""")
            self.__window.lcdV2.setStyleSheet("""QLCDNumber {
                                                 background-color: green; 
                                                 color: yellow;}""")

        if 8 & self.__axis_states:
            self.__window.lcdP3.setStyleSheet("""QLCDNumber {
                                                 background-color: yellow; 
                                                 color: black;}""")
            self.__window.lcdV3.setStyleSheet("""QLCDNumber {
                                                 background-color: yellow; 
                                                 color: black;}""")
        else:
            self.__window.lcdP3.setStyleSheet("""QLCDNumber {
                                                 background-color: green; 
                                                 color: yellow;}""")
            self.__window.lcdV3.setStyleSheet("""QLCDNumber {
                                                 background-color: green; 
                                                 color: yellow;}""")

        if 16 & self.__axis_states:
            self.__window.lcdP4.setStyleSheet("""QLCDNumber {
                                                 background-color: yellow; 
                                                 color: black;}""")
            self.__window.lcdV4.setStyleSheet("""QLCDNumber {
                                                 background-color: yellow; 
                                                 color: black;}""")
        else:
            self.__window.lcdP4.setStyleSheet("""QLCDNumber {
                                                 background-color: green; 
                                                 color: yellow;}""")
            self.__window.lcdV4.setStyleSheet("""QLCDNumber {
                                                 background-color: green; 
                                                 color: yellow;}""")

        if 32 & self.__axis_states:
            self.__window.lcdP5.setStyleSheet("""QLCDNumber {
                                                 background-color: yellow; 
                                                 color: black;}""")
            self.__window.lcdV5.setStyleSheet("""QLCDNumber {
                                                 background-color: yellow; 
                                                 color: black;}""")
        else:
            self.__window.lcdP5.setStyleSheet("""QLCDNumber {
                                                 background-color: green; 
                                                 color: yellow;}""")
            self.__window.lcdV5.setStyleSheet("""QLCDNumber {
                                                 background-color: green; 
                                                 color: yellow;}""")

    def __update_cartesian_pos(self):

        j1 = self.__current_position[0] / self.__sc.t1_const
        j2 = self.__current_position[2] / self.__sc.t2_const
        j3 = self.__current_position[4] / self.__sc.t3_const
        j4 = self.__current_position[6] / self.__sc.t4_const
        j5 = self.__current_position[8] / self.__sc.t5_const

        d_pos = self.__kin.forward_from_scale(j1, j2, j3, j4, j5)

        self.__window.lcdX.display(d_pos[0])
        self.__window.lcdY.display(d_pos[1])
        self.__window.lcdZ.display(d_pos[2])
        self.__window.lcdP.display(d_pos[3])
        self.__window.lcdR.display(d_pos[4])

    def __update_joint_pos(self):

        self.__window.lcdP0.display(self.__current_position[0])
        self.__window.lcdV0.display(self.__current_position[1])

        self.__window.lcdP1.display(self.__current_position[2])
        self.__window.lcdV1.display(self.__current_position[3])

        self.__window.lcdP2.display(self.__current_position[4])
        self.__window.lcdV2.display(self.__current_position[5])

        self.__window.lcdP3.display(self.__current_position[6])
        self.__window.lcdV3.display(self.__current_position[7])

        self.__window.lcdP4.display(self.__current_position[8])
        self.__window.lcdV4.display(self.__current_position[9])

        self.__window.lcdP5.display(self.__current_position[10])
        self.__window.lcdV5.display(self.__current_position[11])

    def __update_port_a_inputs(self):

        self.__window.cbIn0.setChecked(not bool(1 & self.__port_a_inputs))
        self.__window.cbIn1.setChecked(not bool(2 & self.__port_a_inputs))
        self.__window.cbIn2.setChecked(not bool(4 & self.__port_a_inputs))
        self.__window.cbIn3.setChecked(not bool(8 & self.__port_a_inputs))
        self.__window.cbIn4.setChecked(not bool(16 & self.__port_a_inputs))
        self.__window.cbIn5.setChecked(not bool(32 & self.__port_a_inputs))
        self.__window.cbIn6.setChecked(not bool(64 & self.__port_a_inputs))
        self.__window.cbIn7.setChecked(not bool(128 & self.__port_a_inputs))

    def __update_port_a_outputs(self):

        self.__port_a_outputs = 0

        self.__port_a_outputs += self.__window.cbOut0.isChecked() * 1
        self.__port_a_outputs += self.__window.cbOut1.isChecked() * 2
        self.__port_a_outputs += self.__window.cbOut2.isChecked() * 4
        self.__port_a_outputs += self.__window.cbOut3.isChecked() * 8
        self.__port_a_outputs += self.__window.cbOut4.isChecked() * 16
        self.__port_a_outputs += self.__window.cbOut5.isChecked() * 32
        self.__port_a_outputs += self.__window.cbOut6.isChecked() * 64
        self.__port_a_outputs += self.__window.cbOut7.isChecked() * 128

        self.__action_controller.add_action({
                "action": Actions.UpdateOutputs,
                "data": self.__port_a_outputs
                })

    def __update_time_cb(self):

        try:
            if self.__jsc is not None:
                self.__jsc.update()

            self.__axis_states = self.__controller.is_moving()
            self.__current_position = self.__controller.current_position()
            self.__port_a_inputs = self.__controller.get_inputs()

            self.__update_displays_animation()
            self.__update_joint_pos()
            self.__update_cartesian_pos()
            self.__update_port_a_inputs()

            # Stop the gripper if it is closed enough.
            if 1 & self.__port_a_inputs:
                if self.__axis_controllers[5].direction == -1:
                    self.__axis_controllers[5].stop()

            # if (2 & self.__port_a_inputs):
            #     if self.__axis_controllers[5].direction == -1:
            #         self.__axis_controllers[5].stop()

        except serial.serialutil.SerialException as exc:
            self.__logger.error(exc)

        except Exception as exc:
            self.__logger.error(traceback.format_exc())

    def __init_update_timer(self):
        self.__update_timer = ThreadTimer()
        """Update timer.
        """
        self.__update_timer.update_rate = 0.1 # Update time!
        self.__update_timer.set_cb(self.__update_time_cb)

#endregion

#region Private Methods (Action Controller)

    def __action_controller_cb(self, payload):

        action = payload["action"]

        if action == Actions.NONE:
            pass

        if action == Actions.UpdateAbsolutePositions:
            self.__controller.move_absolute(payload["data"])

        elif action == Actions.UpdateSpeeds:
            self.__controller.move_speed(self.__current_speed)

        elif action == Actions.UpdateOutputs:
            self.__controller.set_outputs(self.__port_a_outputs)

        elif action == Actions.ClearController:
            self.__controller.clear()

        elif action == Actions.ResetController:
            pass

    def __set_position(self):

        def calc_speeds(steps, speed):
            speeds = steps
            max_pos = max(steps)

            if max_pos <= 0:
                max_pos = 1

            for index, step in enumerate(steps):
                speeds[index] = (steps[index] * speed) / max_pos
                speeds[index] = abs(speeds[index])
                speeds[index] = int(speeds[index])
            return speeds

        ax0 = self.__window.sbBasePos.value()
        ax1 = self.__window.sbShoulderPos.value()
        ax2 = self.__window.sbElbowPos.value()
        ax3 = self.__window.sbPPos.value()
        ax4 = self.__window.sbRPos.value()
        ax5 = self.__window.sbGripperPos.value()

        steps = [ax0, ax1, ax2, ax3, ax4, ax5]

        # Differentials inverse model.
        q4 = steps[4] + steps[3]
        q5 = steps[4] - steps[3]
        steps[3] = q4
        steps[4] = q5

        # Gripper compensation.
        # In steps is essayer because
        # ration between elbow and gripper is 1:1.
        steps[5] = steps[5] - steps[2]
        
        # speeds = calc_speeds(steps, self.__max_speed)

        self.__target_position[0:12:2] = steps
        self.__target_position[1:12:2] = [self.__max_speed]*6 # speeds

        self.__action_controller.add_action({
                "action": Actions.UpdateAbsolutePositions,
                "data": self.__target_position
                })

    def __move_j(self, a1,a2,a3,a4,a5,a6,speed=-1):
        if speed == -1:
            speed = self.__max_speed
        self.__target_position[0:12:2] = [a1,a2,a3,a4,a5,a6]
        self.__target_position[1:12:2] = [speed]*6

        self.__action_controller.add_action({
                "action": Actions.UpdateAbsolutePositions,
                "data": self.__target_position
                })

        while self.__axis_states != 0:
            pass

    def __init_action_controller(self):
        self.__action_controller = ActionController()
        """Action controller.
        """
        self.__action_controller.set_action_cb(self.__action_controller_cb)

#endregion

#region Private Methods (Automatic Control)

    @Slot()
    def __load_program(self):
        path, _ = QFileDialog.getOpenFileName(self.__window, "Load Python Script", "", "Python Files (*.py)")
        if not path:
            return
        self.__worker.script_path = path
        with open(path, "r", encoding="utf-8") as f:
            self.__window.pteProgramEditor.setPlainText(f.read())
        self.__window.teConsole.append(f"Loaded script: {path}\n")
        self.__window.actionSaveProgram.setEnabled(True)
        self.__window.pbRunProgram.setEnabled(True)

    @Slot()
    def __save_program(self):
        pass

    @Slot()
    def __run_program(self):
        if self.__worker is not None:
            if not self.__worker.isRunning():

                # ensure the latest edits are saved before execution
                if self.__window.actionSaveProgram.isEnabled():
                    self.__save_program()

                # reset controls
                self.__worker.continue_()
                self.__worker._stepping = False
                self.__worker._stop_requested = False
                self.__worker.start()

                # Lock the UI.
                self.__window.pbRunProgram.setEnabled(False)
                for a in (self.__window.pbStopProgram, 
                        self.__window.pbPauseProgram,
                        self.__window.pbContinueProgram,
                        self.__window.pbStepProgram):
                    a.setEnabled(True)

    @Slot()
    def __stop_program(self):
        if self.__worker is not None:
            self.__worker.stop()

    @Slot()
    def __pause_program(self):
        if self.__worker is not None:
            self.__worker.pause()
            # Lock UI.
            self.__window.pbPauseProgram.setEnabled(False)
            self.__window.pbContinueProgram.setEnabled(True)
            self.__window.pbStepProgram.setEnabled(True)

    @Slot()
    def __continue_program(self):
        if self.__worker is not None:
            self.__worker.continue_()
            # Lock UI.
            self.__window.pbPauseProgram.setEnabled(True)
            self.__window.pbContinueProgram.setEnabled(False)

    @Slot()
    def __step_program(self):
        if self.__worker is not None:
            self.__worker.step_once()
            # Lock UI.
            self.__window.pbPauseProgram.setEnabled(False)
            self.__window.pbContinueProgram.setEnabled(True)

    @Slot()
    def __on_script_started(self):
        self.__window.teConsole.append("Script started...\n")

        # Redirect STDOUT
        self.__original_stdout = sys.stdout
        sys.stdout = StreamRedirector(self.__window.teConsole)

    @Slot()
    def __on_script_finished(self):
        self.__window.teConsole.append("Script finished.\n")

        self.__window.pbStopProgram.setEnabled(False)
        self.__window.pbPauseProgram.setEnabled(False)
        self.__window.pbContinueProgram.setEnabled(False)
        self.__window.pbStepProgram.setEnabled(False)
        self.__window.pbRunProgram.setEnabled(True)

        # Redirect STDOUT
        sys.stdout = self.__original_stdout

    @Slot(int, str)
    def __on_dbg_line(self, lineno: int, src: str):
        # show current line and bring it into view
        self.__window.statusBar().showMessage(f"Line {lineno}: {src}")
        # print(f"Line {lineno}: {src}")
        cursor = self.__window.pteProgramEditor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, max(0, lineno - 1))
        self.__window.pteProgramEditor.setTextCursor(cursor)
        self.__window.pteProgramEditor.ensureCursorVisible()

    def __init_automatic(self):

        # self.__window.pteProgramEditor = CodeEditor()
        self.__worker = Worker()
        """Script executor.
        """
        self.__worker.output.connect(self.__window.teConsole.append)
        self.__worker.started.connect(self.__on_script_started)
        self.__worker.finished.connect(self.__on_script_finished)
        self.__worker.dbg_line.connect(self.__on_dbg_line)
        self.__worker.add_api({"move_j": self.__move_j})

#endregion

#region Private Methods (Axises Controllers)

    def __axis_0(self, speed):

        self.__current_speed[1] = speed * -1

        self.__action_controller.add_action({
                "action": Actions.UpdateSpeeds,
                "data": self.__current_speed
                })

    def __axis_1(self, speed):

        self.__current_speed[3] = speed * -1

        self.__action_controller.add_action({
                "action": Actions.UpdateSpeeds,
                "data": self.__current_speed
                })

    def __axis_2(self, speed):

        self.__current_speed[5] = speed
        self.__current_speed[11] = speed * -1

        self.__action_controller.add_action({
                "action": Actions.UpdateSpeeds,
                "data": self.__current_speed
                })

    def __axis_3(self, speed):

        self.__current_speed[7] = speed

        self.__action_controller.add_action({
                "action": Actions.UpdateSpeeds,
                "data": self.__current_speed
                })

    def __axis_4(self, speed):

        self.__current_speed[9] = speed

        self.__action_controller.add_action({
                "action": Actions.UpdateSpeeds,
                "data": self.__current_speed
                })

    def __axis_5(self, speed):

        self.__current_speed[11] = speed

        self.__action_controller.add_action({
                "action": Actions.UpdateSpeeds,
                "data": self.__current_speed
                })

    def __init_axises_controllers(self):
        self.__axis_controllers = []
        """Axis controllers.
        """
        # Key controllers.
        self.__axis_controllers.append(AxisActionController(callback=self.__axis_0))
        self.__axis_controllers.append(AxisActionController(callback=self.__axis_1))
        self.__axis_controllers.append(AxisActionController(callback=self.__axis_2))
        self.__axis_controllers.append(AxisActionController(callback=self.__axis_3))
        self.__axis_controllers.append(AxisActionController(callback=self.__axis_4))
        self.__axis_controllers.append(AxisActionController(callback=self.__axis_5))

#endregion

#region Private Methods (Joystick Events)

    def __jsc_update_cb(self, button_data, axis_data, hat_data):

        if not self.__jsbtn_temp == button_data:

            # Save last state.
            self.__jsbtn_temp = button_data.copy()

            # # Print the new state.
            # for index in button_data:
            #     value = button_data[index]
            #     if value:
            #         print(index, value)
            # print(button_data)

            # Activate output 6 to enable external equipment.
            if button_data[0]:
                self.__window.cbOut0.setChecked(True)
            else:
                self.__window.cbOut0.setChecked(False)

            # Stop all axises!
            if button_data[15]:
                for key_controller in self.__axis_controllers:
                    if key_controller.is_stopped:
                        key_controller.stop()

        def update_axis(index):
            # Does the axis exists?
            # Does the axis is out of the dead zone?
            if (index in axis_data) and (abs(axis_data[index]) >= self.__dead_zone):
                pos = axis_data[index]

                # Scale the speed.
                self.__axis_controllers[self.__jsax_to_rbtax[index]].speed\
                     = int(abs(scale(pos, -1.0, 1.0, -self.__max_speed, self.__max_speed)))

                # Determine the direction.
                if pos < 0:
                    self.__axis_controllers[self.__jsax_to_rbtax[index]].set_ccw()
                elif pos > 0:
                    self.__axis_controllers[self.__jsax_to_rbtax[index]].set_cw()
                else:
                    self.__axis_controllers[self.__jsax_to_rbtax[index]].stop()

                # Block grasping when moving elbow.
                self.__block_grasping = ((index == 3) and\
                    (not self.__axis_controllers[self.__jsax_to_rbtax[index]].is_stopped))

            else:
                if not self.__axis_controllers[self.__jsax_to_rbtax[index]].is_stopped:
                    self.__axis_controllers[self.__jsax_to_rbtax[index]].stop()

        update_axis(0)
        update_axis(1)

        # If this flag is true, then use right analog to run differential joint.
        if button_data[10]:

            # Convert XY to LR differential.
            left, right = xy2lr(axis_data[3], axis_data[2])
            # print(f"Left: {left:.2f}; Right: {right:.2f}")

            # Scale the speed.
            left_speed = int(abs(scale(left, -1.0, 1.0, -self.__max_speed, self.__max_speed)))

            # # Set the speed
            self.__axis_controllers[3].speed = left_speed

            # # Determine the direction.
            if left < -self.__dead_zone:
                self.__axis_controllers[3].set_cw()
            elif left > self.__dead_zone:
                self.__axis_controllers[3].set_ccw()
            else:
                self.__axis_controllers[3].stop()

            # Scale the speed.
            right_speed = int(abs(scale(right, -1.0, 1.0, -self.__max_speed, self.__max_speed)))

            # # Set the speed
            self.__axis_controllers[4].speed = right_speed

            # Determine the direction.
            if right < -self.__dead_zone:
                self.__axis_controllers[4].set_ccw()
            elif right > self.__dead_zone:
                self.__axis_controllers[4].set_cw()
            else:
                self.__axis_controllers[4].stop()

        # Stop if the button is released.
        else:
            self.__axis_controllers[3].stop()
            self.__axis_controllers[4].stop()
            update_axis(3)


        index = 4
        # Does the axis exists?
        if (index in axis_data) and (not self.__block_grasping):
            pos = axis_data[index]
            # Does the axis is out of the dead zone?
            if abs(pos) >= self.__dead_zone:
                self.__axis_controllers[self.__jsax_to_rbtax[index]].speed\
                     = int(abs(scale(pos, -1.0, 1.0, 0, self.__max_speed)))
                if button_data[9]:
                    self.__axis_controllers[self.__jsax_to_rbtax[index]].set_cw()
                else:
                    self.__axis_controllers[self.__jsax_to_rbtax[index]].set_ccw()
            else:
                if not self.__axis_controllers[self.__jsax_to_rbtax[index]].is_stopped:
                    self.__axis_controllers[self.__jsax_to_rbtax[index]].stop()

    def __jsc_enable(self, value):

        try:
            if value and self.__jsc is None:
                self.__jsc = JoystickController()
                self.__jsc.update_cb(self.__jsc_update_cb)

                # self.__led_js_state.turnon()

            elif not value and self.__jsc is not None:
                del self.__jsc
                self.__jsc = None

                # self.__led_js_state.turnoff()

        except Exception as exc:

            msg_box = QMessageBox()
            msg_box.setWindowTitle("Joystick Error")
            msg_box.setText(str(exc))
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setDefaultButton(QMessageBox.Ok)
            msg_box.exec() # Returns keys answer.

#endregion

#region private Methods (Keyboard Events)

    def eventFilter(self, obj, event):

        if event.type() == QEvent.KeyPress:
            btn = event.key()

            if btn == Qt.Key_1:
                self.__axis_controllers[0].set_cw()

            elif btn == Qt.Key_Q:
                self.__axis_controllers[0].set_ccw()

            if btn == Qt.Key_2:
                self.__axis_controllers[1].set_cw()

            elif btn == Qt.Key_W:
                self.__axis_controllers[1].set_ccw()

            if btn == Qt.Key_3:
                self.__axis_controllers[2].set_cw()

            elif btn == Qt.Key_E:
                self.__axis_controllers[2].set_ccw()

            if btn == Qt.Key_4:
                self.__axis_controllers[3].set_cw()
                self.__axis_controllers[4].set_ccw()

            elif btn == Qt.Key_R:
                self.__axis_controllers[3].set_ccw()
                self.__axis_controllers[4].set_cw()

            if btn == Qt.Key_5:
                self.__axis_controllers[3].set_cw()
                self.__axis_controllers[4].set_cw()

            elif btn == Qt.Key_T:
                self.__axis_controllers[3].set_ccw()
                self.__axis_controllers[4].set_ccw()

            elif btn == Qt.Key_6:
                self.__axis_controllers[5].set_cw()

            elif btn == Qt.Key_Y:
                self.__axis_controllers[5].set_ccw()

            elif btn == Qt.Key_Space:
                for controller in self.__axis_controllers:
                    controller.stop()

            return True

        if event.type() == QEvent.KeyRelease:
            btn = event.key()

            if btn == Qt.Key_1:
                self.__axis_controllers[0].stop()

            elif btn == Qt.Key_Q:
                self.__axis_controllers[0].stop()

            if btn == Qt.Key_2:
                self.__axis_controllers[1].stop()

            elif btn == Qt.Key_W:
                self.__axis_controllers[1].stop()

            if btn == Qt.Key_3:
                self.__axis_controllers[2].stop()

            elif btn == Qt.Key_E:
                self.__axis_controllers[2].stop()

            if btn == Qt.Key_4:
                self.__axis_controllers[3].stop()
                self.__axis_controllers[4].stop()

            elif btn == Qt.Key_R:
                self.__axis_controllers[3].stop()
                self.__axis_controllers[4].stop()

            if btn == Qt.Key_5:
                self.__axis_controllers[4].stop()
                self.__axis_controllers[3].stop()

            elif btn == Qt.Key_T:
                self.__axis_controllers[4].stop()
                self.__axis_controllers[3].stop()

            if btn == Qt.Key_6:
                self.__axis_controllers[5].stop()

            elif btn == Qt.Key_Y:
                self.__axis_controllers[5].stop()

            return True

        return QObject.event(obj, event)

#endregion

#region Private Methods (Buttons)

    def __diff_stop(self):
        self.__axis_controllers[3].stop()
        self.__axis_controllers[4].stop()

    def __btnPUp_pressed(self):
        self.__axis_controllers[3].set_ccw()
        self.__axis_controllers[4].set_cw()

    def __btnPDown_pressed(self):
        self.__axis_controllers[3].set_cw()
        self.__axis_controllers[4].set_ccw()

    def __btnRCW_pressed(self):
        self.__axis_controllers[3].set_cw()
        self.__axis_controllers[4].set_cw()

    def __btnRCCW_pressed(self):
        self.__axis_controllers[3].set_ccw()
        self.__axis_controllers[4].set_ccw()

#endregion

#region Private Methods (Slider)

    def __sldSpeed_valueChanged(self, value):

        self.__max_speed = value

        self.__window.lcdSpeed.display(self.__max_speed)

        # If the Joystick is active, do not update speed controllers by hand from he slider.
        if self.__jsc is not None:
            return

        for index in range(0, 6):
            self.__axis_controllers[index].speed = self.__max_speed

#endregion

#region Private Methods (Menu)

    def __actionExit_triggered(self):
        print("HOI")
        pass

    def __actionClear_triggered(self):

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Controller")
        msg_box.setText("Are you sure you want to reset the robot controller?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        answer = msg_box.exec()

        if answer == 16384:
            self.__action_controller.add_action({
                    "action": Actions.ClearController,
                    "data": None
                    })

    def __actionReset_triggered(self):

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Controller")
        msg_box.setText("Are you sure you want to reset the robot controller?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        answer = msg_box.exec()

        if answer == 16384:
            self.__action_controller.add_action({
                    "action": Actions.ResetController,
                    "data": None
                    })

    def __actionEnable_Keyboard_Control_triggered(self):

        # Stop Joystick
        self.__window.actionEnable_Joystick_Control.setChecked(False)
        self.__jsc_enable(False)

        if self.__window.actionEnable_Keyboard_Control.isChecked():
            self.__window.installEventFilter(self)

        else:
            self.__window.removeEventFilter(self)

        for controller in self.__axis_controllers:
            controller.stop()

    def __actionEnable_Joystick_Control_triggered(self):

        # Stop keyboard.
        self.__window.actionEnable_Keyboard_Control.setChecked(False)
        self.__window.removeEventFilter(self)
        self.__jsc_enable(self.__window.actionEnable_Joystick_Control.isChecked())

    def __actionAbout_triggered(self):

        msg_box = QMessageBox()
        msg_box.setWindowTitle("About")
        msg_box.setText("Robko 01 Software")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDefaultButton(QMessageBox.Ok)
        msg_box.exec() # Returns keys answer.

#endregion

#region Private Methods (Form)

    def __init_form(self):

        # Form the path to the UI file.
        target_file = "main.ui"
        file_name = os.path.abspath(__file__)
        file_name = os.path.dirname(file_name)
        file_name = os.path.join(file_name, "ui", target_file)

        # Load UI
        loader = QUiLoader()
        self.__window = loader.load(file_name)

        # Menu
        self.__window.actionExit.triggered.connect(self.__actionExit_triggered)
        self.__window.actionClear.triggered.connect(self.__actionClear_triggered)
        self.__window.actionReset.triggered.connect(self.__actionReset_triggered)
        self.__window.actionEnable_Keyboard_Control.triggered.connect(\
            self.__actionEnable_Keyboard_Control_triggered)
        self.__window.actionEnable_Joystick_Control.triggered.connect(\
            self.__actionEnable_Joystick_Control_triggered)
        self.__window.actionAbout.triggered.connect(self.__actionAbout_triggered)

        # Buttons Manual
        self.__window.btnBaseCW.pressed.connect(self.__axis_controllers[0].set_cw)
        self.__window.btnBaseCW.released.connect(self.__axis_controllers[0].stop)
        self.__window.btnBaseCCW.pressed.connect(self.__axis_controllers[0].set_ccw)
        self.__window.btnBaseCCW.released.connect(self.__axis_controllers[0].stop)

        self.__window.btnShoulderUp.pressed.connect(self.__axis_controllers[1].set_cw)
        self.__window.btnShoulderUp.released.connect(self.__axis_controllers[1].stop)
        self.__window.btnShoulderDown.pressed.connect(self.__axis_controllers[1].set_ccw)
        self.__window.btnShoulderDown.released.connect(self.__axis_controllers[1].stop)

        self.__window.btnElbowUp.pressed.connect(self.__axis_controllers[2].set_ccw)
        self.__window.btnElbowUp.released.connect(self.__axis_controllers[2].stop)
        self.__window.btnElbowDown.pressed.connect(self.__axis_controllers[2].set_cw)
        self.__window.btnElbowDown.released.connect(self.__axis_controllers[2].stop)

        self.__window.btnPUp.pressed.connect(self.__btnPUp_pressed)
        self.__window.btnPUp.released.connect(self.__diff_stop)
        self.__window.btnPDown.pressed.connect(self.__btnPDown_pressed)
        self.__window.btnPDown.released.connect(self.__diff_stop)

        self.__window.btnRCW.pressed.connect(self.__btnRCW_pressed)
        self.__window.btnRCW.released.connect(self.__diff_stop)
        self.__window.btnRCCW.pressed.connect(self.__btnRCCW_pressed)
        self.__window.btnRCCW.released.connect(self.__diff_stop)

        self.__window.btnGripperOpen.pressed.connect(self.__axis_controllers[5].set_ccw)
        self.__window.btnGripperOpen.released.connect(self.__axis_controllers[5].stop)
        self.__window.btnGripperClose.pressed.connect(self.__axis_controllers[5].set_cw)
        self.__window.btnGripperClose.released.connect(self.__axis_controllers[5].stop)

        # Manual Positioning Control
        self.__window.btnBasePos.clicked.connect(self.__set_position)
        self.__window.btnShoulderPos.clicked.connect(self.__set_position)
        self.__window.btnElbowPos.clicked.connect(self.__set_position)
        self.__window.btnPPos.clicked.connect(self.__set_position)
        self.__window.btnRPos.clicked.connect(self.__set_position)
        self.__window.btnGripperPos.clicked.connect(self.__set_position)

        # Hold buttons for PORT A
        self.__window.btnOut0.pressed.connect(lambda: self.__window.cbOut0.setChecked(True))
        self.__window.btnOut0.released.connect(lambda: self.__window.cbOut0.setChecked(False))
        self.__window.btnOut1.pressed.connect(lambda: self.__window.cbOut1.setChecked(True))
        self.__window.btnOut1.released.connect(lambda: self.__window.cbOut1.setChecked(False))
        self.__window.btnOut2.pressed.connect(lambda: self.__window.cbOut2.setChecked(True))
        self.__window.btnOut2.released.connect(lambda: self.__window.cbOut2.setChecked(False))
        self.__window.btnOut3.pressed.connect(lambda: self.__window.cbOut3.setChecked(True))
        self.__window.btnOut3.released.connect(lambda: self.__window.cbOut3.setChecked(False))
        self.__window.btnOut4.pressed.connect(lambda: self.__window.cbOut4.setChecked(True))
        self.__window.btnOut4.released.connect(lambda: self.__window.cbOut4.setChecked(False))
        self.__window.btnOut5.pressed.connect(lambda: self.__window.cbOut5.setChecked(True))
        self.__window.btnOut5.released.connect(lambda: self.__window.cbOut5.setChecked(False))
        self.__window.btnOut6.pressed.connect(lambda: self.__window.cbOut6.setChecked(True))
        self.__window.btnOut6.released.connect(lambda: self.__window.cbOut6.setChecked(False))
        self.__window.btnOut7.pressed.connect(lambda: self.__window.cbOut7.setChecked(True))
        self.__window.btnOut7.released.connect(lambda: self.__window.cbOut7.setChecked(False))

        # Check buttons for PORT A
        self.__window.cbOut0.toggled.connect(self.__update_port_a_outputs)
        self.__window.cbOut1.toggled.connect(self.__update_port_a_outputs)
        self.__window.cbOut2.toggled.connect(self.__update_port_a_outputs)
        self.__window.cbOut3.toggled.connect(self.__update_port_a_outputs)
        self.__window.cbOut4.toggled.connect(self.__update_port_a_outputs)
        self.__window.cbOut5.toggled.connect(self.__update_port_a_outputs)
        self.__window.cbOut6.toggled.connect(self.__update_port_a_outputs)
        self.__window.cbOut7.toggled.connect(self.__update_port_a_outputs)

        # Speed slider
        self.__window.sldSpeed.valueChanged.connect(self.__sldSpeed_valueChanged)

        # Automatic
        self.__window.teConsole.setReadOnly(True)

        self.__window.actionNewProgram.triggered.connect(lambda: print("Not Implemented"))
        self.__window.actionLoadProgram.triggered.connect(self.__load_program)
        self.__window.actionSaveProgram.triggered.connect(self.__save_program)
        self.__window.actionSaveAsProgram.triggered.connect(lambda: print("Not Implemented"))
        
        self.__window.actionRunProgram.triggered.connect(self.__run_program)
        self.__window.actionStopProgram.triggered.connect(self.__stop_program)

        self.__window.pbRunProgram.clicked.connect(self.__run_program)
        self.__window.pbStopProgram.clicked.connect(self.__stop_program)
        self.__window.pbPauseProgram.clicked.connect(self.__pause_program)
        self.__window.pbContinueProgram.clicked.connect(self.__continue_program)
        self.__window.pbStepProgram.clicked.connect(self.__step_program)

        # Lock the UI.
        self.__window.pbRunProgram.setEnabled(True)
        for a in (self.__window.pbStopProgram, 
                self.__window.pbPauseProgram,
                self.__window.pbContinueProgram,
                self.__window.pbStepProgram):
            a.setEnabled(False)

        # Show the UI.
        self.__window.show()

#endregion

#region Public Methods

    def start(self):
        """Start
        """

        self.__init_form()

        self.__init_automatic()

        self.__update_timer.start()

        self.__action_controller.start()

    def stop(self):
        """Stop
        """

        self.__update_timer.stop()

        self.__action_controller.stop()

#endregion
