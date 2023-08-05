# -*- coding: utf-8 -*-
import array
import operator
from base64 import b64decode

import qrcode
from reportlab.lib.units import toLength


DEFAULT_PARAMS = {
	'size': '5cm',
	'padding': '2.5',
	'fg': '#000000',
	'bg': None,
	'version': None,
	'error_correction': 'L',
}
GENERATOR_PARAMS = {'size', 'padding', 'fg', 'bg'}
QR_PARAMS = {'version', 'error_correction'}
QR_ERROR_CORRECTIONS = {
	'L': qrcode.ERROR_CORRECT_L,
	'M': qrcode.ERROR_CORRECT_M,
	'Q': qrcode.ERROR_CORRECT_Q,
	'H': qrcode.ERROR_CORRECT_H,
}
DIRECTION = (
	( 1,  0), # right
	( 0,  1), # down
	(-1,  0), # left
	( 0, -1), # up
)
# left, direct, right
DIRECTION_TURNS_CHECKS = (
	(( 0, -1), ( 0,  0), (-1,  0)), # right
	(( 0,  0), (-1,  0), (-1, -1)), # down
	((-1,  0), (-1, -1), ( 0, -1)), # left
	((-1, -1), ( 0, -1), ( 0,  0)), # up
)


class Vector(tuple):
	def __add__(self, other):
		return self.__class__(map(operator.add, self, other))


class ReportlabImageBase(qrcode.image.base.BaseImage):
	size = None
	padding = None
	bg = None
	fg = None
	rects = []
	bitmap = None

	def __init__(self, *args, **kwargs):
		self.rects = []
		super().__init__(*args, **kwargs)
		self.bitmap = array.array('B', [0] * self.width * self.width)
		self.size = toLength(self.size)
		if '%' in self.padding:
			self.padding = float(self.padding[:-1]) * self.size / 100
		else:
			try:
				self.padding = float(self.padding)
				self.padding = (self.size / (self.width + self.padding * 2)) * self.padding
			except ValueError:
				self.padding = toLength(self.padding)

	def drawrect(self, row, col):
		self.bitmap_set((col, row), 1)

	def save(self, stream, kind=None):
		stream.saveState()

		try:
			# Draw background
			if self.bg is not None:
				stream.setFillColor(self.bg)
				stream.rect(0, 0, self.size, self.size, fill=1, stroke=0)

			# Draw code
			stream.setFillColor(self.fg)
			p = stream.beginPath()
			segment = self.consume_segment()
			while segment:
				coords = segment[0]
				coords = (coords[0], self.width - coords[1])
				coords = self.bitmap_position_to_length(coords)
				p.moveTo(*coords)
				for coords in segment[1:-1]:
					coords = (coords[0], self.width - coords[1])
					coords = self.bitmap_position_to_length(coords)
					p.lineTo(*coords)
				p.close()
				segment = self.consume_segment()
			stream.drawPath(p, stroke=0, fill=1)
		finally:
			stream.restoreState()

	def addr(self, coords):
		"""
		Get index to bitmap
		"""
		col, row = coords
		if row < 0 or col < 0 or row >= self.width or col >= self.width:
			return None
		return row * self.width + col

	def coord(self, addr):
		"""
		Returns bitmap coordinates from address
		"""
		return Vector((addr % self.width, addr // self.width))

	def bitmap_get(self, coords):
		"""
		Returns pixel value of bitmap
		"""
		addr = self.addr(coords)
		return 0 if addr is None else self.bitmap[addr]

	def bitmap_set(self, coords, value):
		"""
		Set pixel value of bitmap
		"""
		addr = self.addr(coords)
		self.bitmap[addr] = value

	def bitmap_invert(self, coords):
		"""
		Invert value of pixel
		"""
		addr = self.addr(coords)
		self.bitmap[addr] = 0 if self.bitmap[addr] else 1

	def consume_segment(self):
		"""
		Returns segment of qr image as path (pairs of x, y coordinates)
		"""

		# Accumulated path
		path = []

		line_intersections = [[] for __ in range(self.width)]

		# Find coordinate of first non empty pixel
		coords = None
		for addr, val in enumerate(self.bitmap):
			if val == 1:
				coords = self.coord(addr)
				break
		else:
			return path

		# Begin of line
		path.append(tuple(coords))
		# Default direction to right
		direction = 0

		def move():
			nonlocal coords
			step = DIRECTION[direction]

			# Record intersection
			if step[1]: # Vertical move
				line = coords[1]
				if step[1] == -1:
					line -= 1
				line_intersections[line].append(coords[0])

			# Step
			coords += step

		# Move to right
		move()

		# From shape begin to end
		while coords != path[0]:
			# Trun left
			val = self.bitmap_get(coords + DIRECTION_TURNS_CHECKS[direction][0])
			if val:
				path.append(tuple(coords))
				direction = (direction - 1) % 4
				move()
				continue

			# Straight
			val = self.bitmap_get(coords + DIRECTION_TURNS_CHECKS[direction][1])
			if val:
				move()
				continue

			# Trun right
			path.append(tuple(coords))
			direction = (direction + 1) % 4
			move()

		path.append(tuple(coords))

		# Remove shape from bitmap
		for row, line in enumerate(line_intersections):
			line = sorted(line)
			for start, end in zip(line[::2], line[1::2]):
				for col in range(start, end):
					self.bitmap_invert((col, row))

		return path

	def bitmap_position_to_length(self, coords):
		return tuple(c * (self.size - 2 * self.padding) / self.width + self.padding for c in coords)



def reportlab_image_factory(**kwargs):
	"""
	Returns ReportlabImage class for qrcode image_factory
	"""
	return type('ReportlabImage', (ReportlabImageBase,), kwargs)


def parse_graphic_params(params):
	"""
	Parses params string in form:

	key=value,key2=value2;(text|base64);content

	For example:

	size=5cm,fg=#ff0000,bg=#ffffff,version=1,error_correction=M,padding=5%;text;text to encode
	"""
	try:
		parsed_params, fmt, text = params.split(';', 2)
	except ValueError:
		raise ValueError("Wrong format, expected parametrs;format;content")
	if fmt not in ('text', 'base64'):
		raise ValueError("Unknown format '%s', supprted are text or base64" % fmt)

	params = DEFAULT_PARAMS.copy()
	if parsed_params:
		try:
			params.update(dict(item.split("=") for item in parsed_params.split(",")))
		except ValueError:
			raise ValueError("Wrong format of parameters '%s', expected key=value pairs delimited by ',' character" % parsed_params)

	for key, __ in params.items():
		if key not in GENERATOR_PARAMS and key not in QR_PARAMS:
			raise ValueError("Unknown attribute '%s'" % key)

	if params['version'] is not None:
		try:
			params['version'] = int(params['version'])
		except ValueError:
			raise ValueError("Version '%s' is not a number" % params['version'])

	if params['error_correction'] in QR_ERROR_CORRECTIONS:
		params['error_correction'] = QR_ERROR_CORRECTIONS[params['error_correction']]
	else:
		raise ValueError("Unknown error correction '%s', expected one of %s" % (params['error_correction'], ', '.join(QR_ERROR_CORRECTIONS.keys())))

	text = text.encode('utf-8')
	if fmt == 'base64':
		try:
			text = b64decode(text)
		except Exception as e:
			raise ValueError("Wrong base64 '%s': %s" % (text.decode('utf-8'), e))

	return params, text


def qr_factory(params):
	params, text = parse_graphic_params(params)
	factory_kwargs = {key: value for key, value in params.items() if key in GENERATOR_PARAMS}
	qr_kwargs = {key: value for key, value in params.items() if key in QR_PARAMS}
	return qrcode.make(text, image_factory=reportlab_image_factory(**factory_kwargs), border=0, **qr_kwargs)


def qr(canvas, params):
	"""
	Generate QR code using plugInGraphic or plugInFlowable

	Example RML code:

	<illustration height="5cm" width="5cm" align="center">
		<plugInGraphic module="reportlab_qrcode" function="qr">size=5cm;text;Simple text</plugInGraphic>
	</illustration>
	"""
	qr_factory(params).save(canvas)
