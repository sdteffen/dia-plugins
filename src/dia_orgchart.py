# PyDia CSV Organization Chart Import
#
# Copyright (c) 2010 Steffen Macke <sdteffen@sdteffen.de>
#
# First column should contain the box content
# Second column should contain a reference (name) to the parent box
# If the second column is empty, there is no parent
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA

import string, math, os
	
class OrgchartImporter :
	def __init__(self) :
		self.errors = {}
		self.objects = []

	def Parse(self, sFile) :
		import csv, codecs
		csvReader = csv.reader(open(sFile, 'rb'), delimiter=';')
		table = []
		y = 0
		ready = []
		for row in csvReader:
			table.append((unicode(row[1], 'ISO-8859-14').encode('utf-8'),unicode(row[0], 'ISO-8859-14').encode('utf-8')))
		edges = []
		left = {}
		right = {}
		table.sort() # comment this out if you want the order from the CSV
		while len(table) > 0 :
			row = []
			for t in table :
				if t[0] not in [l[1] for l in table]:
					row.append(t)
			x = -len(row)*5
			for t in row:
				o, h1, h2 = dia.get_object_type('Flowchart - Box').create (1, 1)
				o.properties['text'] = t[1]					
				o.move(x, y)
				left[t[1]] = x
				right[t[1]] = x
				for p in self.objects:
					if p.properties['text'].value.text == t[0] :
						left[t[0]] = min(left[t[0]], x)
						right[t[0]] = max(right[t[0]], x)
						edgeType = dia.get_object_type('Standard - ZigZagLine')
						con, h1, h2 = edgeType.create(x,y)
						h = con.handles[0]
						pos = o.connections[2].pos
						con.move_handle(h, pos, 0, 0)
						h.connect(o.connections[2])
						h = con.handles[1]
						pos = p.connections[13].pos
						con.move_handle(h, pos, 0, 0)
						h.connect (p.connections[13])
						edges.append(con)
				self.objects.append(o)
				x = x + 20
				table.remove(t)
			y = y + 10
		for edge in edges:
			self.objects.append(edge)
		# center parents over children
		for o in self.objects:
			if 'text' in o.properties.keys() and o.properties['text'].value.text in right:
				y = (o.bounding_box.bottom + o.bounding_box.top)/2
				x = (right[o.properties['text'].value.text] + left[o.properties['text'].value.text])/2
				o.move(x,y)
		# update connecting lines
		for l in self.objects:
			if l.type.name == 'Standard - ZigZagLine':
				h = l.handles[0]
				pos = h.connected_to.object.connections[2].pos
				l.move_handle(h, pos, 0, 0)
				h = l.handles[1]
				pos = h.connected_to.object.connections[13].pos
				l.move_handle(h, pos, 0, 0)

	def Render(self,data) :
		layer = data.active_layer
		for o in self.objects :
			layer.add_object(o)
		data.update_extents ()
			
def import_csv(sFile, diagramData) :
	imp = OrgchartImporter()
	f = open(sFile)
	imp.Parse(sFile)
	return imp.Render(diagramData)

import dia
dia.register_import("CSV Organization Chart", "csv", import_csv);

