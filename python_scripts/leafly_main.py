import json
import pandas as pd
from os.path import exists
import pickle

#####################
### The Weed Shop ###
#####################

def df_to_html(df):
    """Convert dataframe to HTML table string. Display directly on webpage."""
    return df.to_html()

### FILE READ/WRITE FUNCTIONS ###

def read_file(file_path, columns=None, file_type='csv'):
	
	try:
		if file_type == 'csv':
			df = pd.read_csv(file_path)
		elif file_type == 'pkl':
			df = pd.read_csv(file_path)
		elif file_type == 'json':
			df = pd.read_csv(file_path)
		else:
			print("Specified file format not supported. Choose 'csv', 'pkl' or 'json'")
	except FileNotFoundError:
		print('Specified file or directory not found.')
	else:
		if columns is not None:
			return df.filter(items=columns, axis=1)
		else:
			return df

def write_file(df, file_name, file_type):

	if file_type == 'csv':
		df.to_csv(file_name)
	elif file_type == 'pkl':
		df.to_pickle(file_name)
	elif file_type == 'json':
		df.to_csv(file_name)
	else:
		print("Specified file format not supported. Choose 'csv', 'pkl' or 'json'")
		return False
	print(f'{file_type} file successfully written.')
	return True

def get_dicts(df):
	"""Convert dataframe to dictionaries."""
	return df.to_dict('records')

# database already created, don't need to read file again
# leafly_df, leafly_dicts = read_file('leafly_no_null.pkl')

### CREATE FUNCTIONS ###

def make_new_strain(name, type_, thc_level, description, img_url):
	"""Return a list of values for a new database row."""

	if type_.title() not in ['Sativa', 'Indica', 'Hybrid']:
		raise Exception('type_ must be Sativa, Indica or Hybrid')
	if type(thc_level) != int:
		raise Exception('thc_level must be an integer value.')

	return [name, type_, thc_level, description, img_url]

### EDIT DATA FUNCTIONS ###

def percents_to_ints(df, col_name):
	"""Edit the dataframe col_name values if they are object percent values."""

	try:
		col_values = df[col_name]
	except KeyError: 
		print(f'{col_name} is not a valid column name in the supplied dataframe.')
	else:
		try:
			df[col_name] = df[col_name].str.rstrip('%').astype('int')
		except ValueError:
			print("'Column values must be percentages i.e. '1%' or '20'.")
		else:
			return df

def remove_non_alpha(dicts, col_name):
	"""Remove all non-alphanumeric characters from the specified column strings."""

	new_dicts = dicts.copy()
	for i in new_dicts:
		i[col_name] = ''.join([x for x in i[col_name] if x.isalpha() == True or x in [',', '-', ' ', '(', ')']])
	
	return new_dicts

def replace_chars(df, col_name, **chars):
	"""Remove all specified characters from the text in the column name."""

	# pass in dictionary with existing char as key and replacement char as value
	new_df = df.copy()
	values = df[col_name]
	# loop over chars dict and replace characters
	pass

### SEARCH FUNCTIONS ###

def searchData(df, col_name, value):
	"""Return new dataframe containing only those strains where the column has the specified value."""

	if col_name not in df.keys():
		raise Exception(f'Not a valid column name. Choose from {", ",join(df.keys)}.')
	elif col_name == 'type' and value not in ['Sativa', 'Indica', 'Hybrid']:
		raise Exception('strain type must be Sativa, Indica or Hybrid. Did you forget to capitalise?')
	else:
		if value not in df[col_name]:
			raise Exception("{col_name} of '{value}' not found in the database.")
		else:
			new_df = df.loc[df[col_name] == value]
			print(new_df.info())
			
			return new_df

def searchThcLevels(df, min_thc, max_thc):
	"""Return new dataframe containing only those strains with a thc_level between specified values."""
	
	if type(min_thc) != int or type(max_thc) != int:
		raise Exception('Minimum and maximum THC levels must be integer values.') 
	
	return df.loc[(df['thc_level'] >= min_thc) & (df['thc_level'] <= max_thc)]