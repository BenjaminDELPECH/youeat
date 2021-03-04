# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

import time
import urllib3
import base64
from PIL import Image

import requests as req

import re
import codecs
import json
from io import BytesIO
import unidecode
from shutil import copyfile

import re


class RecipeNotFound(Exception):
	pass


class MarmitonCustom(object):

	def __init__(self):
		self.first_measure_words = ['cuillère', 'g', 'mg', 'cl', 'g',  'mg', 'cl', 'tasse', 'once', 'tranche', 'sachet','gousse','bâton',
							   'pincée', 'brin', "gousse",'goutte','branche', 'rondelle','zeste', 'feuille', 'boîte', 'paquet', "boule", "verre", "grosse poignée", "cube"]
		self.prepositions = ['de', 'à']
		self.second_measure_words = ['soupe', 'café', 'extrait']

		plurals = []
		for first_measure_word in self.first_measure_words:
			plural = first_measure_word + 's'
			plurals.append(plural)
		self.first_measure_words += plurals

		self.first_measure_words_complete = []
		for e in self.first_measure_words:
			for e2 in self.prepositions:
				self.first_measure_words_complete.append(e+' '+e2)

	@staticmethod
	def search(query_dict):
		"""
		Search recipes parsing the returned html data.
		Options:
		'aqt': string of keywords separated by a white space  (query seamerch)
		Optional options :
		'dt': "entree" | "platprincipal" | "accompagnement" | "amusegueule" | "sauce"  (plate type)
		'exp': 1 | 2 | 3  (plate expense 1: cheap, 3: expensive)
		'dif': 1 | 2 | 3 | 4  (recipe difficultie 1: easy, 4: advanced)
		'veg': 0 | 1  (vegetarien only: 1)
		'rct': 0 | 1  (without cook: 1)
		'sort': "markdesc" (rate) | "popularitydesc" (popularity) | "" (empty for relevance)
		"""
		base_url = "http://www.marmiton.org/recettes/recherche.aspx?"
		query_url = urllib.parse.urlencode(query_dict)

		url = base_url + query_url

		html_content = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(html_content, 'html.parser')

		search_data = []

		articles = soup.findAll("div", {"class": "recipe-card"})

		iterarticles = iter(articles)
		for article in iterarticles:
			data = {}
			try:
				data["name"] = article.find("h4", {"class": "recipe-card__title"}).get_text().strip(' \t\n\r')
				data["description"] = article.find("div", {"class": "recipe-card__description"}).get_text().strip(' \t\n\r')
				data["url"] = article.find("a", {"class": "recipe-card-link"})['href']
				data["rate"] = article.find("span", {"class": "recipe-card__rating__value"}).text.strip(' \t\n\r')
				try:
					data["image"] = article.find('img')['src']
				except Exception as e1:
					pass
			except Exception as e2:
				pass
			if data:
				search_data.append(data)

		return search_data

	@staticmethod
	def __clean_text(element):
		return element.text.replace("\n", "").strip()


	def get(self, url,nb_person):
		"""
		'url' from 'search' method.
		 ex. "/recettes/recette_wraps-de-poulet-et-sauce-au-curry_337319.aspx"
		"""
		data = {}

	

		soup = MarmitonCustom.getSoupByUrl("https://www.marmiton.org/recettes/recette_roti-de-porc-a-la-moutarde-et-au-miel_17178.aspx")

		containerImgUrl = soup.find("div", {"id": "recipe-media-viewer-thumbnail-container-0"})
		img = containerImgUrl.find("img")
		meal_img_url = img.attrs['data-src']

		main_data = soup.find("div", {"class": "m_content_recette_main"})
		meal_name = ""
		try:
			meal_name = soup.find("h1", {"class", "main-title "}).get_text().strip(' \t\n\r')
		except:
			meal_name = soup.find("h1", {"class", "main-title"}).get_text().strip(' \t\n\r')


		meal_name_bytes = str.encode(unidecode.unidecode(meal_name))
		meal_id = int(int(meal_name_bytes.hex(), 16) %911231244)

		ingredients = []
		for item in soup.find_all("li", {"class": "recipe-ingredients__list__item"}):
			try:
				quantity = None
				ingredient=None
				measure_name = None

				ingredients.append(item)
				quantity = item.find("span", {"class":"recipe-ingredient-qt"}).text
				ingredient = item.find("span", {"class": "ingredient"}).text
				ingredient_complement = item.find("span", {"class":"recipe-ingredient__complement"}).text
				ingredient += ingredient_complement

				try:
					measure_name = self.getMeasureName(ingredient)
					if measure_name:
						ingredient_splitted = ingredient.split(measure_name)
						ingredient = ''.join([ elem+' ' for elem in ingredient_splitted[0:] ])
						for prep in self.prepositions:
							prep = ' ' + prep + ' '
							if prep in ingredient:
								ingredient_splitted2 = ingredient.split(prep)
								ingredient = ''.join([ elem+' ' for elem in ingredient_splitted2[0:] ])
								break

					print(ingredient)
				except Exception:
					print('')

				if measure_name is None:
					isNumber = re.search("^[-+]?[0-9]+$", ingredient)
					if '(' in ingredient and isNumber:

						ingredient_splitted = ingredient.split('(')
						measure_and_quantity = ingredient.split('(')[1].replace(")", "")
						measure_and_quantity_splitted = measure_and_quantity.split(" ")
						quantity = measure_and_quantity_splitted[0]
						measure_name = measure_and_quantity_splitted[1]

						ingredient = ingredient_splitted[0]




				quantity2 = self.getQuantity(nb_person, quantity)

				print("quantity"+str(quantity2))
				print("personNb:"+str(nb_person))
				sendPostMutation(createLMFQuery, {
					"foodText": ingredient,
					"mealId": meal_id,
					"mealName": meal_name,
					"measureName": measure_name,
					"quantity": float(quantity),
					"mealImgUrl":meal_img_url
				})






			except Exception:
				print(Exception)

		return






		# try:
		# 	tags = list(set([item.text.replace("\n", "").strip() for item in soup.find('ul', {"class": "mrtn-tags-list"}).find_all('li', {"class": "mrtn-tag"})]))
		# except:
		# 	tags = []
		#
		# recipe_elements = [
		# 	{"name": "author", "query": soup.find('span', {"class": "recipe-author__name"})},
		# 	{"name": "rate","query": soup.find("span", {"class": "recipe-reviews-list__review__head__infos__rating__value"})},
		# 	{"name": "difficulty", "query": soup.find("div", {"class": "recipe-infos__level"})},
		# 	{"name": "budget", "query": soup.find("div", {"class": "recipe-infos__budget"})},
		# 	{"name": "prep_time", "query": soup.find("span", {"class": "recipe-infos__timmings__value"})},
		# 	{"name": "total_time", "query": soup.find("span", {"class": "title-2 recipe-infos__total-time__value"})},
		# 	{"name": "people_quantity", "query": soup.find("span", {"class": "title-2 recipe-infos__quantity__value"})},
		# 	{"name": "author_tip", "query": soup.find("div", {"class": "recipe-chief-tip mrtn-recipe-bloc "}).find("p", {"class": "mrtn-recipe-bloc__content"}) if soup.find("div", {"class": "recipe-chief-tip mrtn-recipe-bloc "}) else "" },
		# ]
		# for recipe_element in recipe_elements:
		# 	try:
		# 		data[recipe_element['name']] = MarmitonCustom.__clean_text(recipe_element['query'])
		# 	except:
		# 		data[recipe_element['name']] = ""
		#
		# try:
		# 	cook_time = MarmitonCustom.__clean_text(soup.find("div", {"class": "recipe-infos__timmings__cooking"}).find("span"))
		# except:
		# 	cook_time = "0"
		#
		# try:
		# 	nb_comments = MarmitonCustom.__clean_text(soup.find("span", {"class": "recipe-infos-users__value mrtn-hide-on-print"})).split(" ")[0]
		# except:
		# 	nb_comments = ""
		#
		# steps = []
		# soup_steps = soup.find_all("li", {"class": "recipe-preparation__list__item"})
		# for soup_step in soup_steps:
		# 	steps.append(MarmitonCustom.__clean_text(soup_step))
		#
		# image = soup.find("img", {"id": "af-diapo-desktop-0_img"})['src'] if soup.find("img", {"id": "af-diapo-desktop-0_img"}) else ""
		#
		# data.update({
		# 	"ingredients": ingredients,
		# 	"steps": steps,
		# 	"name": name,
		# 	"tags": tags,
		# 	"image": image if image else "",
		# 	"nb_comments": nb_comments,
		# 	"cook_time": cook_time
		# })

		return data

	def getQuantity(self, nb_person,quantity):
		if quantity:
			if '/' in quantity:
				quantity_splitted = quantity.split('/')
				quantity = int(quantity_splitted[0]) / int(quantity_splitted[1])

			quantity = float(quantity) / int(nb_person)
		return quantity

	def getMeasureName(self, ingredient):
		ingredient = ingredient
		measure_name = None

		for first_measure_word in self.first_measure_words_complete:
			if first_measure_word in ingredient:
				measure_name = first_measure_word
				is_second_measure_word = False
				for second_measure_word in self.second_measure_words:
					if second_measure_word in ingredient:
						measure_name += ' '+ second_measure_word
						is_second_measure_word = True
						break

				if not is_second_measure_word:
					for elem in self.prepositions:
						if elem in measure_name:
							measure_name = measure_name.split(elem)[0]

				break

		return measure_name

	@staticmethod
	def getSoupByUrl(url):
		try:
			html_content = urllib.request.urlopen(url).read()
		except urllib.error.HTTPError as e:
			raise RecipeNotFound if e.code == 404 else e
		soup = BeautifulSoup(html_content, 'html.parser')
		return soup


def scrappeMeal(url, nb_person):
	marmittonCustom = MarmitonCustom()
	# url = "https://www.marmiton.org/recettes/recette_tarte-salee-au-chevre-et-aux-pruneaux_22973.aspx"
	detailed_recipe = marmittonCustom.get(url, nb_person)  # Get the details of the first returned recipe (most relevant in our case)
	# Display result :
	# print("## %s\n" % detailed_recipe['name'])  # Name of the recipe
	# print("Recette par '%s'" % (detailed_recipe['author']))
	# print("Noté %s/5 par %s personnes." % (detailed_recipe['rate'], detailed_recipe['nb_comments']))
	# print("Temps de cuisson : %s / Temps de préparation : %s / Temps total : %s." % (
	# detailed_recipe['cook_time'] if detailed_recipe['cook_time'] else 'N/A', detailed_recipe['prep_time'],
	# detailed_recipe['total_time']))
	# print("Tags : %s" % (", ".join(detailed_recipe['tags'])))
	# print("Difficulté : '%s'" % detailed_recipe['difficulty'])
	# print("Budget : '%s'" % detailed_recipe['budget'])
	# print("\nRecette pour %s personne(s) :\n" % detailed_recipe['people_quantity'])
	# for ingredient in detailed_recipe['ingredients']:  # List of ingredients
	# 	print("- %s" % ingredient)
	# print("")
	# for step in detailed_recipe['steps']:  # List of cooking steps
	# 	print("# %s" % step)
	# if detailed_recipe['author_tip']:
	# 	print("\nNote de l'auteur :\n%s" % detailed_recipe['author_tip'])

def goToRandomMarmittonPage(driver):
	random_button = driver.find_element_by_id('random-recipe')
	random_button.click()
	time.sleep(1)
	return driver.current_url

createLMFQuery = """
mutation($foodText: String!, $mealId:Int!, $measureName:String, $quantity: Float!, $mealImgUrl: String!, $mealName:String!){
  createLinkMealFoodScrapping(foodText:$foodText, mealId:$mealId, measureName: $measureName, quantity: $quantity, mealImgUrl: $mealImgUrl, mealName: $mealName){
    linkMealFood{
      id
    }
  }
}
"""


def sendPostMutation(mutation, payload):
	url = 'http://127.0.0.1:8888/graphql/'
	r = req.post(url, json={'query': mutation, 'variables': payload})
	print(r.status_code)




from selenium import webdriver



DRIVER_PATH = 'C:/dev/runtime/chromedriver_win32_chrome_87/chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
try:



	start_page = 1
	end_page = 2
	index = start_page

	while(index<=end_page):
		try:
			main_url = 'https://www.marmiton.org/recettes/recherche.aspx?aqt=&dt=platprincipal&page=' + str(index)
			driver.get(main_url)

			time.sleep(0.1)
			try:
				button_agree = driver.find_element_by_id("didomi-notice-agree-button")
				if button_agree:
					button_agree.click()
			except Exception:
				print("hello")

			button_agree = driver.find_elements_by_class_name("af-popin-btn-close")
			if button_agree:
				button_agree[0].click()

			cards = driver.find_elements_by_class_name("recipe-card")
			index+=1

			for i in range(0, len(cards)):
				try:
					time.sleep(0.1)
					cards = driver.find_elements_by_class_name("recipe-card")
					cards[i].click()
					time.sleep(0.35)
					url = goToRandomMarmittonPage(driver)
					nb_person = driver.find_elements_by_class_name("recipe-ingredients__qt-counter__value")[0].get_attribute("value")
					time.sleep(0.35)


					scrappeMeal(url, nb_person)
					break
					driver.get(main_url)

				except Exception:
					print("error")
		except Exception:
			print("error")
except Exception:
	print('time out')





















