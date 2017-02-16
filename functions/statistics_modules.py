import math
from collections import Counter
from matplotlib import pyplot as plt
from decimal import Decimal, getcontext

getcontext().prec = 20

#  VECTORS CALCULATIONS
	# simple computation of collections of numbers
def vector_add(x, y):
	# adds corresponding elements
	return [x_i + y_i for x_i, y_i in zip(x,y)]

def vector_substract(x, y):
	# substract corresponding elements
	return [x_i - y_i for x_i, y_i in zip(x,y)]

def vector_sum(vectors):
	# sums all corresponding elements
	return reduce(vector_add, vectors)

def scalar_multiply(v, c):
	# c in a number, v is a vector
	return [v_i * c for v_i in v]

def vector_mean(vectors):
	""" compute the vector whose ith element in the mean 
	of ith elements of the input vectors"""
	n = len(vectors)
	return scalar_multiply(vector_sum(vectors), 1/n)

def dot(x,y):
	# x_1 * y_1 + x_2 * y_2 .... x_n * y_n
	return sum(x_i * y_i for x_i, y_i in zip (x,y))

def sum_squares(v):
	# x_1 ** 2 + x_2 ** 2 .... x_n ** 2
	return dot(v,v)

def magnitude(v):
	return math.sqrt(sum_squares(v))

def distance(v, w):
	return magnitude(vector_substract(v,w))

# MATRICES
	# to create matrices

def shape(a):
	num_rows = len(a)
	num_cols = len(a[0]) if a else 0
	return num_rows, num_cols

def get_row(a, i):
	return a[i]

def get_column(a, n):
	return [a_i[n] for a_i in a]

def make_matrix(k, n, entry_fn):
	# return a matrix k * n following entry_fn function
	return [[entry_fn(k_i, n_i) for n_i in range(n)] for k_i in range(k)]

def is_diagonal(i, j):
	# 1's if its on the diagonal else 0
	return 1 if i == j else 0

# STATISTICS
	# calculate main statistics figures of collections

def mean(x):
	return sum(x) / float(len(x))

def median(x):
	# return the central value of the collection
	N = len(x)
	collection = sorted(x)
	mid_point = N// 2

	# if N is uneven return mid_point of collection
	if N % 2 == 1:
		return collection[mid_point]

	# if is even return mean of of the middle values
	else:
		return mean([collection[mid_point - 1], collection[mid_point]])

def quantile(x, p):
	# return the pth percentile in x
	p_index = int(p * len(x))
	return sorted(x)[p_index]

def mode(x):
	# return the most common values of the collection
	counts = Counter(x)
	highest_counts = max(counts.values())
	return [x_i for x_i, count in counts.iteritems() if count == highest_counts]

def error_mean(x):
	#returns a list of the different between the element n and the mean(x)
	x_mean = mean(x)
	return [x_i - x_mean for x_i in x]

def variance(x):
	n = len(x)
	if n == 0:
		return None
	elif n == 1:
		return 0
	else:
		deviations = error_mean(x)
		return sum_squares(deviations)/float((n - 1))

def standard_deviation(x):
	return math.sqrt(variance(x))

def innerquantile_range(x, p=0.1):
	return quantile(x, 1 - p) - quantile(x, p)

def covariance(x, y):
	n = len(x)
	return dot(error_mean(x), error_mean(y)) / float((n - 1))

def correlation(x, y):
	stdex_x = standard_deviation(x)
	stdex_y = standard_deviation(y)
	if Decimal(stdex_x) > Decimal(0) and Decimal(stdex_y) > Decimal(0):
		return covariance(x, y) / float(stdex_x) / float(stdex_y)
	else:
		return 0 # if no variance, correlation is 0

# ONE DIMENSIONAL ANALYSIS
# Create histogram
def bucketize(point, bucket_size=1):
	# floor the point to the next lower multiple of bucket_size
	return bucket_size * math.floor(point/bucket_size)

def count_points(points, bucket_size):
	# buckets the points and counts how many in each bucket
	return Counter(bucketize(point / bucket_size) for point in points)

def plot_histogram(values, x_axis=None, bucket_size=1, title=''):
	# if dict is passed as value dict_keys will be taken as x-axis
	if type(values) == 'dict':
		axis = values.keys()
		points = values.values()
	else:
		# if list of values and list of axis given use them
		if x_axis:
			axis = x_axis
			points = values
		else:
			# if list of values given but not x-axis use counter 
			histogram = count_points(values, bucket_size)
			axis = histogram.keys()
			points = histogram.values()

	plt.bar(axis, points, width=bucket_size)
	plt.title(title)
	plt.show()
