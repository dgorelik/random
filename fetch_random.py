from pylab import imshow, show, get_cmap
import numpy, urllib, urllib2, wave, struct

MAX_REQUEST_SIZE = 10000
IMAGE_HEIGHT = 128
IMAGE_WIDTH = 128
SOUND_SAMPLING_RATE = 4410
SAMPLE_LEN = SOUND_SAMPLING_RATE * 3 # 3 seconds

def random_ints(n):
	""" Return n random ints 0-255 using random.org library"""
	
	# Make multiple requests if n > MAX_REQUEST_SIZE
	data = []
	while len(data) != n:
		increase_by = min(MAX_REQUEST_SIZE, n - len(data))
		data += random_int_request(increase_by)

	return data

def random_int_request(n):
	""" Return n (where n < MAX_REQUEST_SIZE) random ints 
		0-255 using random.org library"""

	params = {
		"num"    : str(n),
		"min"    : "0",
		"max"    : "255",
		"col"    : "1",
		"base"   : "10",
		"format" : "plain",
		"rnd"    : "new",
	}
	encoded_params = urllib.urlencode(params)
	req = urllib2.Request(
		"https://www.random.org/integers/?" + encoded_params)
	response = urllib2.urlopen(req)
	the_page = response.read()
	print "Debug -- HTML response code:", response.code

	# Each line is number except last line, which is empty
	data = [int(n) for n in the_page.split("\n")[:-1]]

	return data

def show_pic(data):
	""" Show a picture with height IMAGE_HEIGHT and width IMAGE_WIDTH """

	data = numpy.array(data).reshape(IMAGE_HEIGHT, IMAGE_WIDTH)
	imshow(data, cmap=get_cmap("Spectral"), interpolation='nearest')
	show()

def generate_sound(data):
	""" Ouput wav file based on inpute data with sampling rate
	SOUND_SAMPLING_RATE. This function assumes input data is in range 0-255 and
	scales accordingly."""

	# wav generation inspired by:
	# https://soledadpenades.com/2009/10/29/fastest-way-to-generate-wav-files-in-python-using-the-wave-module/

	noise_output = wave.open('noise.wav', 'w')
	noise_output.setparams((2, 2, SOUND_SAMPLING_RATE, 0,
							'NONE', 'not compressed'))

	for i in range(0, len(data)):
			# scale from (0, 255) to (-32767, 32767)
			value = (data[i] - 128) * 256 
			packed_value = struct.pack('h', value)
			noise_output.writeframes(packed_value)
			noise_output.writeframes(packed_value)

	noise_output.close()

show_pic(random_ints(IMAGE_WIDTH*IMAGE_HEIGHT))
generate_sound(random_ints(SAMPLE_LEN))