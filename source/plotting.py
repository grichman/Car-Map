import math
import matplotlib.pyplot as plt

class Arc:
	def __init__(self, arc_length, direction, turn_speed, time):
		self.arc_length = arc_length
		self.direction = direction
		self.turn_speed = turn_speed
		self.time = time

	def __repr__(self):
		return '(' + str(self.arc_length) + ", " + str(self.direction) + ", " + str(self.turn_speed) + ", " + str(self.time) + ")"

	def calc_radius(self):
		circumference = self.arc_length * self.get_angle() / 360
		return circumference / (2 * math.pi)

	def get_angle(self):
		return self.turn_speed * self.time

def main():
	data = parseFile()
	print(data)
	#plt.plot([1,1.1,1.2,1/3],[1,4,9,16], 'ro')
	#x_points, y_points = map(lambda x,y: x + y,  getArcPairs(90, 0, 0, data[0])
	x_points = [0]
	y_points = [0]
	prev_angle = 90	
	x_offset = 0
	y_offset = 0
	for segment in data:
		new_x_points,new_y_points = getArcPairs(prev_angle,x_offset,y_offset,segment)
		x_points += new_x_points
		y_points += new_y_points
		prev_angle += segment.get_angle()
		x_offset = x_points[-1]
		y_offset = y_points[-1]

	plt.plot(x_points, y_points)
	plt.axis([-5,5,-5,5])
	plt.show()
	
# this method draws an arc by drawing a series of straight lines, with an incrementing angle
def getArcPairs(prev_angle, x_offset, y_offset, arc, theta_resolution = 1.0):
	print("Args:", prev_angle, x_offset, y_offset, arc)
	x_points = []
	y_points = []
	if arc.get_angle() == 0:
		x_points = [ x_offset + arc.arc_length * math.cos(math.radians(prev_angle)) ]
		y_points = [ y_offset + arc.arc_length * math.sin(math.radians(prev_angle)) ]
		return x_points, y_points
	for _ in range(abs(int(arc.get_angle()/theta_resolution))):
		#     /| 				sin(t) = y/l
		#  l / | 				cos(t) = x/l
		#   /  | y
		#  /t__|
		#     x
		length = arc.arc_length * theta_resolution / abs(arc.get_angle())
		y_offset += length * math.sin(math.radians(prev_angle))
		x_offset += length * math.cos(math.radians(prev_angle))
		prev_angle += theta_resolution * (-1 if arc.get_angle() < 0 else 1)
		x_points.append(x_offset)
		y_points.append(y_offset)
	return (x_points, y_points)
	

# prompts the user for a filename and tries to open it
#   if it fails it continues prompting until it gets a valid one
#   parses the file and returns a list of Arcs
def parseFile():
	while True:
		fname = raw_input('type in the arduino output file: ')
		try:
			log_file = open(fname, 'r')
			break
		except:
			print('Please provide a valid filename')
	arcs = []
	for line in log_file:
		data = [int(info) for info in line.strip().split(",")]
		new_arc = Arc(int(data[0]), int(data[1]), int(data[2]), int(data[3]))
		arcs.append(new_arc)
	return arcs
main()