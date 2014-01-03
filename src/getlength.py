# PyDia Simple Scale
# Copyright (c) 2003, Hans Breuer <hans@breuer.org>
#
# Experimental scaleing (selected) Objects via property api
#
# Known Issues:
#  - HANDLE_NON_MOVEABLE ?
#  - bezier control points
#  - unsizeable objects (or sizeable via multiple text size changing, e.g. UML Class)
#

#  This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import dia
import string
import math

#data = dia.active_display().diagram

class CLengthDialog :
  def __init__(self, d, data) :
    import pygtk
    pygtk.require("2.0")
    import gtk
    win = gtk.Window()
    win.connect("delete_event", self.on_delete)
    win.set_title("Line Length")

    self.diagram = d
    self.data = data
    self.win = win

    box1 = gtk.VBox()
    win.add(box1)
    box1.show()

    box2 = gtk.VBox(spacing=10)
    box2.set_border_width(10)
    box1.pack_start(box2)
    box2.show()

    self.entry = gtk.Entry()
    self.entry.set_text(get_selected_line_length(self.data))
    box2.pack_start(self.entry)
    self.entry.show()

    separator = gtk.HSeparator()
    box1.pack_start(separator, expand=0)
    separator.show()

    box2 = gtk.VBox(spacing=10)
    box2.set_border_width(10)
    box1.pack_start(box2, expand=0)
    box2.show()

    button = gtk.Button("OK")
    button.connect("clicked", self.on_delete)
    box2.pack_start(button)
    button.set_flags(gtk.CAN_DEFAULT)
    button.grab_default()
    button.show()
    win.show()
  
  def on_delete (self, *args) :
    self.win.destroy ()
    
def dump_o(name,o,depth):
  s_str=""
  for a in dir(o) :
    if hasattr(o,a) :
      s_str += name+".%s = %s\n" % (a,getattr(o,a))
      if depth != 0:
        s_str += dump_o(name+"."+a,getattr(o,a),depth-1)
  return s_str

def get_selected_line_length(data) :
  s_str = ""
  objs = data.get_sorted_selected()
  if len(objs) == 0:
    return "No line selected"
  if len(objs) > 1:
    return "Only select 1 please"
  for o in objs :
    if hasattr(o,"properties") :
      if o.properties.has_key ('start_point') and o.properties.has_key ('end_point') :
        break
      return "Object is not a line"
    else :
      return "Object does not have properties"
    
  for o in objs :
    x1 = o.properties['start_point'].value[0]
    x2 = o.properties['end_point'].value[0]
    
    y1 = o.properties['start_point'].value[1]
    y2 = o.properties['end_point'].value[1]
    
    x_len = math.fabs(x1 - x2)
    y_len = math.fabs(y1 - y2)
        
    if x_len == 0 or y_len == 0 :
      llen = x_len + y_len
      s_str += "%s" % llen
    else :
      s_str += "%s" % math.sqrt(math.pow(y_len,2) + math.pow(x_len,2))

    return s_str

def GetSelectedLineLength(data, flags) :
  dlg = CLengthDialog(dia.active_display().diagram,data)
  
dia.register_action ("GetSelectLineLength", "Get Select Line Length","/DisplayMenu/Objects/GetSelectLineLength",GetSelectedLineLength)
