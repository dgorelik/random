from pylab import imshow, show, get_cmap
import numpy as np
import urllib2
import wave
import random, struct

def random_ints(n):
	""" Return n random ints 0-255 using random.org library"""

	req = urllib2.Request(
		"https://www.random.org/integers/?num=16&min=1&max=256&col=1&base=10&format=plain&rnd=new")
	response = urllib2.urlopen(req)
	the_page = response.read()

	print response.code
	data = [int(n) for n in the_page.split("\n")[:-1]]

	return data

def show_pic(data):
	data = np.array(data).reshape(4, 4)
	imshow(data, cmap=get_cmap("Spectral"), interpolation='nearest')
	show()

def generate_sound(data):
	# wav generation inspired by:
	# https://soledadpenades.com/2009/10/29/fastest-way-to-generate-wav-files-in-python-using-the-wave-module/

	noise_output = wave.open('noise.wav', 'w')
	noise_output.setparams((2, 2, 4410, 0, 'NONE', 'not compressed'))

	SAMPLE_LEN = 13230 # 3 seconds

	for i in range(0, SAMPLE_LEN):
			# scale from (0, 255) to (-32767, 32767)
			value = (random.randint(0, 255) - 128) * 256 

			packed_value = struct.pack('h', value)
			noise_output.writeframes(packed_value)
			noise_output.writeframes(packed_value)

	noise_output.close()