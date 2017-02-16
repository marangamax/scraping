import statistic_modules as sm
import pandas as pd

class One_dimensional_analysis():

	def __init__(self, one_dimensional_data):
		self.series = one_dimensional_data
		self.n = len(self.series)
		self.mean = sm.mean(self.series)
		self.min = min(self.series)
		self.max = max(self.series)
		self.median = sm.median(self.series)
		self.mode = sm.mode(self.series)
		self.stdev = sm.standard_deviation(self.series)

	def get_quantile(self, pth_value):
		return sm.quantile(self.series, pth_value)

	def get_innerquantile_range(self, p=0.1):
		return sm.innerquantile_range(self, p)

	def summarize(self):
		summary = vars(self).copy()
		summary.pop('series', None)
		return summary

	def plot_histogram(self, x_axis=None, bucket_size=1, tittle=''):
		return sm.plot_histogram(self.series, x_axis, bucket_size, tittle)

class Multi_dimensional_analysis():
	# takes a pd.df a make analysis on single dimension and in between them
    def __init__(self, dataframe):
    	self.df = dataframe
        self.columns = self.df.columns.tolist()
        # transpose df to have a simgle list per row
        self.data = [sm.get_column(self.df.values.tolist(), n) for n in range(len(self.columns))]
        self.class_list = [One_dimensional_analysis(i) for i in self.data]
        
    def summarize_dimension(self):
    	# return a pd.df with the the summary of each dimension
        summaries = [i.summarize() for i in self.class_list]
        summary = pd.DataFrame(summaries, index=self.columns)
        summary_column_order = ['n', 'mean', 'min', 'max', 'stdev' , 'median', 'mode']
        summary = summary[summary_column_order]
        return summary

    def correlation_matrix(self):
    	# returns the num_columns x num_columns matrix whose (i,j)th entry 
    	# is the correlation between the columns i and j of the data

    	num_rows, _ = sm.shape(self.data)

    	def matrix_entry(i, j):
    		return sm.correlation(sm.get_row(self.data, i-1), sm.get_row(self.data, j-1))

    	correlations = sm.make_matrix(num_rows, num_rows, matrix_entry)

    	return pd.DataFrame(correlations, columns=self.columns, index=self.columns)

    def make_scatterplot_matrix(self):
    	# make a matrix of scatterplots from different variable
    	# no more than 4 variables if not it does not look to good

    	_, num_columns = sm.shape(self.data)
    	fig, ax = plt.subplots(num_columns, num_columns)

    	for i in range(num_columns):
    		for j in range(num_columns):
    			# scatter column_j on the x-axis vs column_i on the y-axis
    			if i != j: 
    				ax[i][j].scatter(sm.get_column(self.data, i), sm.get_column(self.data, j))
    			#  unless i == j, in which case show the series name
    			else: 
    				ax[i][j].annotate(self.columns[i], (0.5, 0.5), xycoords='axes fraction', ha='center', va='center')
				# then hide axis labels except left and bottom charts
				if i < num_columns - 1: ax[i][j].xaxis.set_visible(False)
				if j < 0: ax[i][j].yaxis.set_visible(False)

		# fix the bottom right and top left axis labels, which are wrong because
		# their charts only have text in them
		ax[-1][-1].set_xlim(ax[0][-1].get_xlim())
		ax[0][0].set_ylim(ax[0][1].get_ylim())
