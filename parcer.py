import requests
from bs4 import BeautifulSoup as bs
import csv


def url_code(url):
	response = requests.get(url)
	return response.status_code

def get_html(url):
	try:
		r = requests.get(url)
	except:
		print('unable to reach page ' + url)
		return None
	return r.text

def write_csv(data):
	with open('salads.csv', mode='a', 
		# newline='',
		encoding='utf-16'
		) as f:
		#newline - to avoid blank rows after each record
		#encoding utf-16 - we are in russia, thats all
		writer = csv.writer(f, delimiter=';')
		writer.writerow(data)
write_csv(['name', 'ingred']) # adding header



for number in range(1, 2):  # there are 103 pages
	url = 'https://www.russianfood.com/recipes/bytype/?fid=35&page={}'.format(number)
	print('\n', url, '\n', 'returns code: ', url_code(url), '\n')

	try:
		soup = bs(get_html(url), 'lxml')
		salads = soup.find_all('div', {'class': 'recipe_list_new'})[0].\
		find_all('div', {'class': 'title_o'})
		salads_urls = soup.find_all('div', {'class': 'recipe_list_new'})[0].\
		find_all('div', {'class': 'title'})

		for salad_url in salads_urls:
			salad_url = 'https://www.russianfood.com' + salad_url.find('a')['href']
			# print(salad_url)

			salat_soup = bs(get_html(salad_url), 'lxml')

			# temp = l.find('table', {'class': 'ingr'})
			name = salat_soup.find('h1', {'class': 'title'}).get_text(strip=True).replace('"', "'")
			ingreds = salat_soup.find('table', {'class': 'ingr'}).\
			find_all('tr')[1:]

			print(name)

			for i in ingreds:
				ingred = i.find('span').get_text(strip=True).lower().replace('"', "'")
				print(ingred)
				write_csv([name, ingred])

	except:
		pass

# 
