import folium
import geopy


def create_dict(input_year, file, permission1):	
	f = open(file,'r',encoding = 'utf-8', errors = 'ignore')
	final_dict = dict()
	film_white_list = set()
	for i in range(14):
		f.readline()
	for line in f:
		if not line[:3] == '---':	
			if line[-2] == ')':
				site_ind_end = line.rindex('\t')
				site_ind_start = line.rindex('\t',0,site_ind_end)
				site = line[site_ind_start+1:site_ind_end]
			else:
				try:
					site_ind_start = line.rindex('\t')
				except:
					print(line)
				site = line[site_ind_start+1:-1]
			if site.count(',') > 1:
				start = site.rindex(',',0,site.rindex(','))
				site = site[start+2:]
			name_ind_end = line.index('(')
			name = line[:name_ind_end-1]
			try:
				if name[0] == '"':
					name = name[1:len(name)-1]
			except:
				pass
			year_ind_start = line.index('(')
			year = line[year_ind_start+1:year_ind_start+5]
			if not name in film_white_list:
				if permission1:
					film_white_list.add(name)
				if year == input_year:
					try:
						if not name in final_dict[site]:
							final_dict[site].append(name)
					except:
						final_dict[site] = [name]
	return final_dict


def create_films_layer(final_dict, permission2, map):
	create_geocoder = geopy.geocoders.Bing('Av7RE8z6Aw7I7yPq_0\
	yUv26n7uCxcfwVz1gfl0RvHWmEoYk0U8l_3FFf0mEKmgoA')
	fg_films = folium.FeatureGroup(name="Films")
	for el in final_dict:
		try:
			create_cords = create_geocoder.geocode(el)
			try:
				if 1 <= len(final_dict[el]) < 3:
					color = 'orange'
				elif 3 <= len(final_dict[el]) < 25:
					color = 'red'
				else:
					color = 'darkblue'
				fg_films.add_child(folium.Marker(location=[create_cords.latitude,\
				 create_cords.longitude], popup=' | '.join(final_dict[el]),\
				  icon=folium.Icon(color=color, icon='info-sign')))
			except:
				if permission2:
					print('Site cords error: ' + el)
				pass
		except:
			if permission2:
				print('Server error. Site: ' + el + ", list of films that\
 woulnd't be showed: " + str(final_dict[el]))
			pass
	map.add_child(fg_films)
	return map


def add_population_layer(map, world_file):
	fg_pp = folium.FeatureGroup(name="Population")
	fg_pp.add_child(folium.GeoJson(data=open(world_file, 'r',
	 encoding='utf-8-sig').read(),
	 style_function=lambda x: {'fillColor':'green'
	 if x['properties']['POP2005'] < 10000000
	 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
	 else 'red'}))
	map.add_child(fg_pp)
	return map


def main():
	map_name = input('Type tha map file name(without extension): ') 
	map = folium.Map()
	layers = input("Type layers' types(films or/and population)\
(example: films, population): ").split(', ')
	for el_ind in range(len(layers)):
		layers[el_ind] = layers[el_ind].lower()
	if 'films' in layers:
		file = input('Type the location.list file adress: ')
		input_year = input('Year: ')
		permission1 = input('Should we show every place where the\
 film was filmed or just one?(type yes or no): ').lower()
		if permission1 == 'yes':
			permission1 = True
		else:
			permission1 == False
		permission2 = input('Should we print all the errors that could occure?\
(type yes or no): ').lower()
		if permission2 == 'yes':
			permission2 = True
		else:
			permission2 == False
		final_dict = create_dict(input_year, file, permission1)
		map = create_films_layer(final_dict, permission2, map)
	if 'population' in layers:
		world_file = input('Type the world.json file adress: ')
		map = add_population_layer(map, world_file)
	map.add_child(folium.LayerControl())
	map.save(map_name + '.html')
main()