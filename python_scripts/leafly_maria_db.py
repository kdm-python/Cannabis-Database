import mariadb
import pandas as pd
import sys
import json

# access files or use pandas functions
# hidden from user
import leafly_main as leafly

def maria_connect(user, password, host, port, database):
	"""Create and return mariadb connection object."""

	try:
		con = mariadb.connect(
		user=user,
		password=password,
		host=host,
		port=port,
		database=database
		)

	except mariadb.Error as e:
		print(f"Error connecting to MariaDB Platform: {e}")
		sys.exit(1)

	else:
		print('Connection successful.')
		return con

def insert_data(cursor, table, ld):
	"""Insert data from a list of dictionaries into the specified table. """

	for ind in range(len(ld)):
		try: 
			cursor.execute(f"INSERT INTO {table} (name, type, thc_level, description, img_url) VALUES (?, ?, ?, ?, ?)", 
					(ld[ind]['name'], ld[ind]['type'], ld[ind]['thc_level'], ld[ind]['description'], ld[ind]['img_url'])) 

		except mariadb.Error as e: 
			print(f"Error: {e}")

def delete_data(cursor, table, strain_id):
	"""Delete selected row from database with matching ID."""

	try: 
		cursor.execute(f"DELETE FROM {table} WHERE id=?", (strain_id,))

	except mariadb.Error as e: 
		print(f"Error: {e}")

	# if delete successful, return True, if not found, return False

def get_strain_data(cursor, table, col_name, value):
	"""Retrieve all data for specified strain matching the chosen column name.
	Return list of the column values to Flask function."""

	### ADD *col_names and *values to look for multipls columns and/or values
	### check col_names and values are same length
	### print msg if col_name wrong or value not found
	keys = ['name', 'type', 'thc_level', 'description', 'img_url']

	try: 
		cursor.execute(f"SELECT name, type, thc_level, description, img_url FROM {table} WHERE {col_name}=?", (value,)) 
		d = dict(zip(keys, list(cursor)[0]))
		# j = json.dumps(list(cursor)[0])
		json_data = json.dumps(d)
		return json_data

	except mariadb.Error as e: 
		print(f"Error: {e}")

def get_all_names(cursor, table='weed_strains'):

	try: 
		cursor.execute(f"SELECT name FROM {table}") 
		names = sorted([x[0] for x in list(cursor)])
		return json.dumps(names)
		
	except mariadb.Error as e: 
		print(f"Error: {e}")	

user_="kyle"
password_="blackmore"
host_="192.168.0.130"
port_=3306
database_="kyle"

def connect_get(strain_name, col_name, table='weed_strains'):
	"""Create connection and retrive data with specified strain name."""

	conn = maria_connect(user_, password_, host_, port_, database_)
	cur = conn.cursor()
	result = get_strain_data(cur, table, col_name, strain_name)
	conn.close()
	
	return result

def connect_all_names(table='weed_strains'):
	"""Create connection and return a list of all the strain names."""

	conn = maria_connect(user_, password_, host_, port_, database_)
	cur = conn.cursor()
	result = json.dumps(get_all_names(cur, table)).replace('\\', '')

	return result

def connect_insert(table, ld):
	"""Create connection and run the insert function."""

	conn = maria_connect(user_, password_, host_, port_, database_)
	cur = conn.cursor()
	result = insert_data(cur, table, ld)
	conn.commit()
	conn.close()
	
	return result

### DELETE ROW ID 1-102 in leafly_no_null database 

def connect_delete(table, *strain_ids):
	"""Create connection and delete row with corresponding ID."""

	conn = maria_connect(user_, password_, host_, port_, database_)
	cur = conn.cursor()
	for id_no in strain_ids:
		delete_data(cur, table, id_no)
	# print(f'Row(s) with ID {", ".join(map(lambda x: str(x), deleted))} successfully deleted from the database')
	conn.commit()
	conn.close()