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

from enum import Enum

from tkinter import *

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

__class_name__ = "TaskGUI"
"""Task name."""

#endregion

class LedShape(Enum):
    SQUARE      = 1
    ROUND       = 2
    ARROW       = 3

class LedPoint(Enum):
    DOWN  = 0
    UP    = 1
    RIGHT = 2
    LEFT  = 3

class LedStatus(Enum):
    OFF   = 1
    ON    = 2
    WARN  = 3
    ALARM = 4
    SET   = 5

class LedColor:
    PANEL     = '#545454'
    OFF       = '#656565'
    ON        = '#00FF33'
    WARN      = '#ffcc00'
    ALARM     = '#ff4422'

class LED:

#region Constructor

    def __init__(self, master=None, width=25, height=25, 
                 appearance=FLAT,
                 status=LedStatus.ON, bd=1, 
                 bg=None, 
                 shape=LedShape.SQUARE, outline="",
                 blink=0, blinkrate=1,
                 orient=LedPoint.UP,
                 takefocus=0):

        # preserve attributes
        self.master       = master
        self.shape        = shape
        self.onColor      = LedColor.ON
        self.offColor     = LedColor.OFF
        self.alarmColor   = LedColor.ALARM
        self.warningColor = LedColor.WARN
        self.specialColor = '#00ffdd'
        self.status       = status
        self.blink        = blink
        self.blinkrate    = int(blinkrate)
        self.on           = 0
        self.onState      = None

        if not bg:
            bg = LedColor.PANEL

        ## Base frame to contain light
        self.frame=Frame(master, relief=appearance, bg=bg, bd=bd, 
                         takefocus=takefocus)

        basesize = width
        d = center = int(basesize/2)

        if self.shape == LedShape.SQUARE:
            self.canvas=Canvas(self.frame, height=height, width=width, 
                               bg=bg, bd=0, highlightthickness=0)

            self.light=self.canvas.create_rectangle(0, 0, width, height,
                                                    fill=LedColor.ON)
        elif self.shape == LedShape.ROUND:
            r = int((basesize-2)/2)
            self.canvas=Canvas(self.frame, width=width, height=width, 
                               highlightthickness=0, bg=bg, bd=0)
            if bd > 0:
                self.border=self.canvas.create_oval(center-r, center-r, 
                                                    center+r, center+r)
                r = r - bd
            self.light=self.canvas.create_oval(center-r-1, center-r-1, 
                               center+r, center+r, fill=LedColor.ON,
                               outline=outline)
        else:  # Default is an ARROW
            self.canvas=Canvas(self.frame, width=width, height=width,
                               highlightthickness=0, bg=bg, bd=0)
            x = d
            y = d
            if orient == LedPoint.DOWN:
                self.light=self.canvas.create_polygon(x-d,y-d, x,y+d,
                               x+d,y-d, x-d,y-d, outline=outline)
            elif orient == LedPoint.UP:
                self.light=self.canvas.create_polygon(x,y-d, x-d,y+d,
                               x+d,y+d, x,y-d, outline=outline)
            elif orient == LedPoint.RIGHT:
                self.light=self.canvas.create_polygon(x-d,y-d, x+d,y,
                               x-d,y+d, x-d,y-d, outline=outline)
            elif orient == LedPoint.LEFT:
                self.light=self.canvas.create_polygon(x-d,y, x+d,y+d,
                               x+d,y-d, x-d,y, outline=outline)

        self.canvas.pack(side=TOP, fill=X, expand=NO)
        self.update()

#endregion

#region Public Methods

    def turnon(self):
        self.status = LedStatus.ON
        if not self.blink: self.update()

    def turnoff(self):
        self.status = LedStatus.OFF
        if not self.blink: self.update()

    def alarm(self):
        self.status = LedStatus.ALARM
        if not self.blink: self.update()

    def warn(self):
        self.status = LedStatus.WARN
        if not self.blink: self.update()

    def set(self, color):
        self.status       = LedStatus.SET
        self.specialColor = color
        self.update()

    def blinkon(self):
        if not self.blink:
            self.blink   = 1
            self.onState = self.status
            self.update()

    def blinkoff(self):
        if self.blink:
            self.blink   = 0
            self.status  = self.onState
            self.onState = None
            self.on      = 0
            self.update()

    def blinkstate(self, blinkstate):
        if blinkstate:
            self.blinkon()
        else:
            self.blinkoff()

    def update(self):
        # First do the blink, if set to blink
        if self.blink:
            if self.on:
                if not self.onState:
                    self.onState = self.status
                self.status  = LedStatus.OFF
                self.on = 0                            
            else:
                if self.onState:
                    self.status = self.onState     # Current ON color
                self.on = 1

        if self.status == LedStatus.ON:
            self.canvas.itemconfig(self.light, fill=self.onColor)
        elif self.status == LedStatus.OFF:
            self.canvas.itemconfig(self.light, fill=self.offColor)
        elif self.status == LedStatus.WARN:
            self.canvas.itemconfig(self.light, fill=self.warningColor)
        elif self.status == LedStatus.SET:
            self.canvas.itemconfig(self.light, fill=self.specialColor)
        else:
            self.canvas.itemconfig(self.light, fill=self.alarmColor)

        self.canvas.update_idletasks()

        if self.blink:
            self.frame.after(self.blinkrate * 1000, self.update)

#endregion
