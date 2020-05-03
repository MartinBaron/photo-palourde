#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import os
import unidecode
import string
import shutil
import imghdr
import csv
from distutils.dir_util import copy_tree
from datetime import datetime

try:
    from PIL import Image
    import hitherdither
    enabled = True
except:
    logging.warning("Unable to load PIL or hitherdither, disabling thumbnailer")
    enabled = False

DEFAULT_DITHER_PALETTE = [(25,25,25), (75,75,75),(125,125,125),(175,175,175),(225,225,225),(250,250,250)] # 6 tone palette\
DEFAULT_THRESHOLD = [96, 96, 96]
DEFAULT_MAX_SIZE = (500,500)
DEFAULT_MAX_SIZE_ORIGINAL = (300,300)

def create_folders(album_name):
	cur = os.getcwd()
	if not os.path.exists("./output/albums/" + album_name + '/'):
		os.makedirs("./output/albums/" + album_name + '/')
	if not os.path.exists("./output/albums/" + album_name + '/photo/'):
		os.makedirs("./output/albums/" + album_name + '/photo/')
	if not os.path.exists("./output/albums/" + album_name + '/photo_page/'):
		os.makedirs("./output/albums/" + album_name + '/photo_page/')
	if not os.path.exists("./output/albums/" + album_name + '/photo_vignette/'):
		os.makedirs("./output/albums/" + album_name + '/photo_vignette/')



def rename_photos(input, album_name):
	dst = os.getcwd() + '/output/albums/' + album_name + '/photo/'
	photos = os.listdir(input)
	photos = sorted(photos)
	photo_counter = 1
	for p in photos :
		if p=='.DS_Store':
			continue
		if photo_counter < 10 :
			new_name = '0' + str(photo_counter) + '.jpg'
		else:
			new_name = str(photo_counter) + '.jpg'
		print("La photo "+ p + " a été importée et renommée en " +new_name)
		#os.rename(os.getcwd() + '/input/'+p, os.getcwd() + '/output/albums/'+ album_name + '/photo/'+ new_name)
		shutil.copy2(os.getcwd() + '/input/'+p,dst)
		os.rename(dst + p, dst + new_name)
		photo_counter = photo_counter + 1




def dither_photos(album_name):
	featured_photo = input("Quel est le numéro de la photo qui sera la couverture de l'album ? (ex : 01, 11, 24) /!\\ merci de choisir une photo en paysage. \n")
	if not os.path.exists("./output/albums/" + album_name + '/'):
		print("La création du dossier initiale a échoué...\n")
		return
	else:
		print("Compression de la featured photo en cours...\n")
		filename = featured_photo+'.jpg'
		fn= os.path.join("./output/albums/"+album_name+'/photo/',filename)
		of = os.path.join("./output/albums/"+album_name+"/featured_dithered.png")
		of2 = os.path.join("./output/albums/"+album_name+"/featured.jpg")
		img= Image.open(fn).convert('RGB')
		image_size =DEFAULT_MAX_SIZE
		img.thumbnail(image_size, Image.LANCZOS)
		palette = hitherdither.palette.Palette(DEFAULT_DITHER_PALETTE)            
		threshold = DEFAULT_THRESHOLD   
		img_dithered = hitherdither.ordered.bayer.bayer_dithering(img, palette, threshold, order=8) #see hither dither documentation for different dithering algos
		img_dithered.save(of, optimize=True)
		shutil.copy2(fn,of2)




def resize_photos(album_name):
	indirname =  "./output/albums/" + album_name + '/photo/'
	outdirname = "./output/albums/" + album_name + '/photo_vignette/'
	if not os.path.exists(indirname) or not os.path.exists(outdirname):
		print("La création du dossier initiale a échoué...\n")
		return
	else:
		print("Création des vignettes en cours...\n")
		for p in os.listdir(indirname):
			img= Image.open(os.path.join(indirname,p)).convert('RGB')
			image_size =DEFAULT_MAX_SIZE_ORIGINAL
			img.thumbnail(image_size, Image.LANCZOS)
			img.save(os.path.join(outdirname,p.replace('.jpg','_vignette.png')), optimize=True)


def gen_index(album_liste, album_vignette):
	hin = open("template_html/index.html", "rt")
	hout = open("output/index.html", "wt")
	for line in hin:
		hout.write(line.replace('#ALBUM_LISTE', album_liste).replace('#ALBUM_VIGNETTE', album_vignette))
	hin.close()
	hout.close()

def gen_a_propos(album_liste):
	hin = open("template_html/a_propos.html", "rt")
	hout = open("output/a_propos.html", "wt")
	for line in hin:
		hout.write(line.replace('#ALBUM_LISTE', album_liste))
	hin.close()
	hout.close()

def gen_overview(album_name,album_date, album_name_display, album_liste, album_overview):
	hin = open("template_html/overview.html", "rt")
	hout = open("output/albums/" + album_name + "/overview.html", "wt")
	for line in hin:
		hout.write(line.replace('#ALBUM_LISTE', album_liste).replace('#ALBUM_OVERVIEW', album_overview).replace('#ALBUM_DATE',album_date).replace('#ALBUM_NAME_DISPLAY', album_name_display ))
	hin.close()
	hout.close()	


def gen_overview_part(album_name):
	print("generating overview for album " + album_name)
	album_overview = ""
	indirname =  "./output/albums/" + album_name + '/photo/'
	for p in sorted(os.listdir(indirname)):
		page_name = p.replace(".jpg","")
		album_overview = album_overview +'<li><a href="photo_page/' + page_name + '.html"><img src="photo_vignette/' + page_name + '_vignette.png", alt="vignette_' + page_name + '"/></a></li>\n'
	return album_overview

def gen_page(current,album_name, album_name_display, last_page):
	hin = open("template_html/page.html", "rt")
	hout = open("output/albums/" + album_name + "/photo_page/"+current+".html", "wt")
	#checking if first page
	if current == "01":
		photo_previous = '<img src="../../../images/left_palourde.png", alt="previous" style="opacity:0;"/>'
	else:
		previous_number = int(current)-1
		if previous_number < 10:
			previous_number = "0" + str(previous_number)
		else:
			previous_number = str(previous_number)
		photo_previous = '<a href="'+previous_number+'.html"><img src="../../../images/left_palourde.png", alt="previous"/></a>'
	#checking if last page
	if last_page:
		photo_next = '<img src="../../../images/right_palourde.png", alt="next" style="opacity:0;"/>'
	else:
		next_number = int(current)+1
		if next_number < 10:
			next_number = "0" + str(next_number)
		else:
			next_number = str(next_number)
		photo_next = '<a href="'+next_number+'.html"><img src="../../../images/right_palourde.png", alt="next"/></a>'
	#other variables
	photo_current = '<img src="../photo/'+current+'.jpg", alt="album-photo"/>'
	photo_bottom = '<a href="../overview.html">← '+ album_name_display + '</a> // Photo ' + current
	#writing page
	for line in hin:
		hout.write(line.replace('#PHOTO_NEXT', photo_next).replace('#PHOTO_PREVIOUS', photo_previous).replace('#PHOTO_CURRENT',photo_current).replace('#PHOTO_BOTTOM',photo_bottom))
	hin.close()
	hout.close()

    #PHOTO_PREVIOUS
    #<a href="09.html"><img src="../../../images/left_palourde.png", alt="previous"/></a>
    #PHOTO_NEXT
    #<a href="09.html"><img src="../../../images/right_palourde.png", alt="next"/></a>
    #PHOTO_CURRENT
    #<img src="../photo/09.jpg", alt="album-photo"/>
    #PHOTO_BOTTOM
    #<a href="../overview.html">< Début d'hiver</a> - 03


def gen_album_pages(album_name, album_name_display):
	print("generating pages for album " + album_name)
	indirname =  "./output/albums/" + album_name + '/photo/'
	counter = 0
	for p in sorted(os.listdir(indirname)):
		page_name = p.replace(".jpg","")
		if counter == len(os.listdir(indirname))-1:
			gen_page(page_name,album_name, album_name_display,True)
		else:
			gen_page(page_name,album_name, album_name_display,False)
		counter = counter+1

def date_translator(album_date):
	album_date = album_date.strftime('%b %Y')
	a = album_date.split(" ")[0]
	if a == "Jan":
		mois = "Janvier"
	elif a == "Feb":
		mois = "Février"
	elif a == "Mar":
		mois = "Mars"
	elif a == "Apr":
		mois = "Avril"
	elif a == "May":
		mois = "Mai"
	elif a == "Jun":
		mois = "Juin"
	elif a == "Jul":
		mois = "Juillet"
	elif a == "Aug":
		mois = "Août"
	elif a == "Sep":
		mois = "Septembre"
	elif a == "Oct":
		mois = "Octobre"
	elif a == "Nov":
		mois = "Novembre"
	elif a == "Dec":
		mois = "Décembre"
	return str(mois + " " + album_date.split(" ")[1])

def create_htmls(album_name = "", album_date = "",album_name_display = ""):
	#updating album.csv
	if album_name != "" and album_date != "" and album_name_display != "":	
		with open('albums.csv','a', newline='\n') as csvfile:
			csvwriter = csv.writer(csvfile,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,lineterminator='\n')
			csvwriter.writerow([album_name, album_date.strftime('%m/%Y'), album_name_display])
	
	#generating album liste and album vignette html parts
	with open('albums.csv','r') as csvfile:
		csvreader = csv.reader(csvfile,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		album_liste = ""
		album_liste_home = ""
		album_vignette = ""
		print(csvreader)
		for line in sorted(csvreader,key=lambda r:  datetime.strptime(r[1], '%m/%Y'),reverse=True):
			print(line)

			album_liste = album_liste +'<li><a href="../' + line[0] + '/overview.html">' + line[2] + '</a></li>\n'
			album_liste_home = album_liste_home + '<li><a href="albums/' + line[0] + '/overview.html">' + line[2] + '</a></li>\n'
			album_vignette = album_vignette + '<li><a href="albums/' + line[0] + '/photo_page/01.html"><img src="albums/' + line[0] + '/featured_dithered.png", alt="cover-'+line[0]+'"/></a><div class="thumb"><h2>'+line[2]+'</h2><time>'+date_translator(datetime.strptime(line[1],'%m/%Y'))+'</time></div></li>\n'
			
		###print(album_liste)
		###print(album_vignette)
	#generating home page
	gen_index(album_liste_home,album_vignette)
	print("generating index")
	#generating a_propos page
	gen_a_propos(album_liste_home)
	print("generating about")

	#generating overview.html and pages for all albums
	with open('albums.csv','r') as csvfile:
		csvreader = csv.reader(csvfile,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for line in csvreader:
			album_overview = gen_overview_part(line[0])
			gen_overview(line[0],date_translator(datetime.strptime(line[1],'%m/%Y')),line[2],album_liste.replace(line[2],"<em>&nbsp " + line[2] + "</em>"), album_overview)
			gen_album_pages(line[0], line[2])
			




	#ALBUM_LIST
	#<li><a href="albums/debut_d_hiver/debut_d_hiver.html">Début d'hiver</a></li>
    #<li><a href="#">States</a></li>
    #<li><a href="#">Vin et Cidre</a></li>

	#ALBUM_VIGNETTE
    #<li><a href="#"><img src="dithering/dithers/03.png", alt="cover-debuts-d-hiver"/></a><div class="thumb"><h2>Débuts d'hiver</h2><time>Décembre 2019</time></div></li>
    #<li><a href="#"><img src="dithering/dithers/03.png", alt="cover-strates"/></a><div class="thumb"><h2>Strates</h2><time>Décembre 2019</time></div></li>
    #<li><a href="#"><img src="dithering/dithers/22.png", alt="cover-vin-et-cidre"/></a><div class="thumb"><h2>Vin et Cidre</h2><time>Décembre 2019</time></div></li>
    #<li><a href="#"><img src="dithering/dithers/18.png", alt="cover-debuts-d-hiver"/></a><div class="thumb"><h2>Débuts d'hiver</h2><time>Décembre 2019</time></div></li>
    #<li><a href="#"><img src="dithering/dithers/17.png", alt="cover-strates"/></a><div class="thumb"><h2>Strates</h2><time>Décembre 2019</time></div></li>
    #<li><a href="#"><img src="dithering/dithers/29.png", alt="cover-vin-et-cidre"/></a><div class="thumb"><h2>Vin et Cidre</h2><time>Décembre 2019</time></div></li>


	#ALBUMOVERVIEW
					#<li><a href="photo_page/03.html"><img src="photo_vignette/03_vignette.png", alt="vignette_03"/></a></li>
					#<li><a href="photo_page/09.html"><img src="photo_vignette/09_vignette.png", alt="vignette_09"/></a></li>
        			#<li><a href="photo_page/10.html"><img src="photo_vignette/10_vignette.png", alt="vignette_10"/></a></li>
                    #<li><a href="photo_page/13.html"><img src="photo_vignette/13_vignette.png", alt="vignette_13"/></a></li>
                    #<li><a href="photo_page/17.html"><img src="photo_vignette/17_vignette.png", alt="vignette_17"/></a></li>
                    #<li><a href="photo_page/18.html"><img src="photo_vignette/18_vignette.png", alt="vignette_18"/></a></li>
                    #<li><a href="photo_page/22.html"><img src="photo_vignette/22_vignette.png", alt="vignette_22"/></a></li>
                    #<li><a href="photo_page/24.html"><img src="photo_vignette/24_vignette.png", alt="vignette_24"/></a></li>
                    #<li><a href="photo_page/26.html"><img src="photo_vignette/26_vignette.png", alt="vignette_26"/></a></li>
                    #<li><a href="photo_page/27.html"><img src="photo_vignette/27_vignette.png", alt="vignette_27"/></a></li>
                    #<li><a href="photo_page/28.html"><img src="photo_vignette/28_vignette.png", alt="vignette_28"/></a></li>
                    #<li><a href="photo_page/29.html"><img src="photo_vignette/29_vignette.png", alt="vignette_29"/></a></li>
                    #<li><a href="photo_page/33.html"><img src="photo_vignette/33_vignette.png", alt="vignette_33"/></a></li>

def backup():
	# copy subdirectory example
	fromDirectory = "./output"
	toDirectory = "./output-backup"
	copy_tree(fromDirectory, toDirectory)


def main():
	print("*P*H*O*T*O*P*A*L*O*U*R*D*E*","\n")
	rep1 = ""
	while rep1 not in ["o","n"]:
		rep1 = input("Bonjour ! Souhaitez-vous importer un nouvel album ? o/n")
		print(rep1)
	if rep1 == "n" :
		print("Nous allons donc simplement mettre à jour le code avec les albums existant !")
		create_htmls()
		print("************************\n")
		print("Le code a été mis à jour !")
	elif rep1 == "o":
		print("Importons un nouvel album !")
		print("************************\n")
		album_name_display = input("Comment s'appelle ce nouvel album ? \n")
		album_date_input = input("Quelle est la date de cet album ? (MM/AAAA, commme 03/2020 par exemple) \n")
		album_date_split = album_date_input.split("/")
		album_date = datetime(int(album_date_split[1]), int(album_date_split[0]),1)
		print(album_date.strftime('%b %Y'))
		d = date_translator(album_date)
		print(d)
		#create the folder name
		album_name = unidecode.unidecode(album_name_display.replace(" ", "_").lower().translate(str.maketrans('', '', string.punctuation)))
		###print(album_date)
		###print(album_name_display)
		print("Le dossier sera appelé " + album_name)
		backup()
		create_folders(album_name)
		rename_photos("input/", album_name)
		dither_photos(album_name)
		resize_photos(album_name)
		create_htmls(album_name, album_date,album_name_display)
		print("************************\n")
		print("L'import est terminé. Ouvrez output/index.html pour admirer le résultat :) \n")

exc = main()

