# Example: python graph_photon_frequency.py "9-15-18 0325pm.txt"

# Takes an input file of photon-statistics data as argv[1].
# Reads the input file line by line and determines the probability
# of each integer N, which represents the probability of N photons
# being detected in a single division (here each division is 
# temporal, from 5ms to 500ms).

import sys
import numpy as np
import matplotlib.pyplot as pypl

def main():
	input_filename = get_file()
	div, length, max = get_metadata(input_filename)
	mean, std_dev = calc_stats(input_filename, length)
	frequency = create_frequency_array(input_filename, max)
	create_distribution_graph(frequency, length, div, mean, std_dev)
	
# reads file name from args and returns file,
# making necessary checks
def get_file():
	if len(sys.argv) > 1:
		return sys.argv[1]
	else:
		print("No filename supplied. Exiting...")
		exit()
	
# reads file contents and determines the length of the file
# in lines, the maximum value held within the file, and the
# length of the time division used (in milliseconds)
def get_metadata(input_filename):
	div, length, max = 0, 0, 0
	with open(input_filename, 'r') as ifile:
		length_and_div = ifile.readlines()[1].split(",")
		length, div = int(length_and_div[0]), int(length_and_div[1])
		ifile.seek(0)
		for line in ifile:
			if is_num(line) and int(line) > max:
				max = int(line)
	return div, length, max

# reads input file and counts the number of times each 
# number of occurrences was measured in a single time
# division. The value of the array at index I will measure
# the number of times I photons were detected in a time division.
def create_frequency_array(input_filename, max):
	frequency = np.zeros(max+1, dtype=np.int16)
	with open(input_filename, 'r') as ifile:
		for line in ifile:
			if is_num(line):
				photon_count = int(line)
				frequency[photon_count] = frequency[photon_count]+1
	return frequency
	
# TODO
# given an array of frequencies of photon events, visualize
# the statistical distribution of these photon events by
# graphing the data. X axis is number of photons measured in
# a single divison. Y axis is how many times that number of 
# photons was measured within a single division.
def create_distribution_graph(frequency, total_measurements, div, mean, std_dev):
	photons_per_div = list(range(len(frequency)))
	probabilities = get_normalized_frequency(frequency, total_measurements)
	pypl.bar(photons_per_div, probabilities, width=0.9)
	pypl.xlabel("Photons per {0}ms".format(div))
	pypl.ylabel("Probability of occurrence")
	pypl.text(
		12, 0.1, "{0} measurements taken\n{1:0.2f} mean photons per div\n{2:0.2f} standard deviation".format(
		total_measurements, mean, std_dev))
	pypl.title("Photon probability distribution", fontsize=16)
	pypl.show()
	
# checks if a given string can properly represent a number-
# specifically, an integer. Used to verify that the current 
# line of the input file is not a comment or metadata.
def is_num(num_str):
	try:
		int(num_str)
		return True
	except ValueError:
		return False
	
# converts frequency values from number of occurrences to fractions
# of total number of measurements (i.e. to probabilities).
def get_normalized_frequency(frequency, total_measurements):
	probabilities = np.zeros(len(frequency), dtype=np.float32)
	for i in range(len(frequency)):
		probabilities[i] = frequency[i] / total_measurements
	return probabilities
	
# calculates and returns the mean value of the array corresponding
# to all measurements taken.
def calc_stats(input_filename, length):
	raw_data = np.zeros(length, dtype=np.int16)
	mean = 0
	std_dev = 0
	with open(input_filename, 'r') as ifile:
		file_lines = ifile.readlines()[2:]
		for i in range(length):
			raw_data[i] = np.int16(file_lines[i])
	mean = np.mean(raw_data)
	std_dev = np.std(raw_data)
	return mean, std_dev
	
if __name__ == "__main__":
	main()