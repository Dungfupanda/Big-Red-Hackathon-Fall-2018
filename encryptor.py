from PIL import Image, ImageChops
import numpy as np
import sys, hashlib, binascii
import hash_image as hi
import hashlib
import decryptor as d  #For now




def get_binary_message(message):
	message_to_base10 = list()
	for character in message:
		message_to_base10.append(ord(character))
	out_str = ""
	for i in range(len(message_to_base10)):
		out_str += '{0:08b}'.format(message_to_base10[i])

	return out_str




def alter_picture(picture, indices, message_bin):
	altered_picture_list = picture.copy()
	message_bin = list(message_bin)  #Convert to a list to use pop()
	if (len(message_bin) / 2 != len(indices)):
		raise RuntimeError("The message converted to binary should be exactly twice as long as the number of indices")
	for i in range(len(indices)):
		first_bit = message_bin.pop(0)
		second_bit = message_bin.pop(0)
		r = indices[i][0]
		c = indices[i][1]
		which_rgb = 0
		original_bin = np.binary_repr(altered_picture_list[r][c][which_rgb], 8)
		altered_bin = original_bin[:-2] + first_bit + second_bit
		altered_picture_list[r][c][which_rgb] = int(altered_bin, 2)


	return Image.fromarray(altered_picture_list, 'RGB')




if __name__ == "__main__":
	h = hashlib.sha256()
	message = sys.argv[1]
	username = sys.argv[2]
	password = sys.argv[3]   #This is the seed for the random number generator
	h.update(password.encode('utf-8'))
	original_im = Image.open("sleepie.jpeg")
	



	# This gets a 3 dimensional array of RBG data.
	# First inner array is a row of pixels
	# Each array in that row represent a pixel in RBG format	
	rgb_array = np.asarray(original_im)

	#Now lets work on the random number generator to get the indices of the picture to change
	#Lets also convert our message and password.
	seed = d.key_to_int(h.digest())
	message_bin = get_binary_message(message)

	#How many random numbers do we need?
	#We need the number of bits of the message divided by 2.
	num_pixels_change = int(len(message_bin)/2)  

	#Now lets generate that many random numbers
	#Need total number of pixels
	width, height = original_im.size
	total_num_pixels = width * height

	#Alright now we can get the indices of the pixels to change
	indices = hi.get_indices(seed, num_pixels_change, width, height)



	altered_im = alter_picture(rgb_array, indices, message_bin)


	altered_im.save("sleepie_altered.png")
	altered_im.show()

	print("result:", d.decrypt("sleepie_altered.png", password, num_pixels_change))

	#difference.show()
	#Alright so maybe implement the difference function. Maybe make this a website? Or maybe
	#make a crude website and post it on github for free? Basically I just want to make this more user
	#friendly. Easier access and more intuitive design with some more features ultimately