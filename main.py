import shutil
import imdb
import os
from fpdf import FPDF
import urllib.request
from PIL import Image
ia = imdb.IMDb()

def run():
    print("1: Top 100 movies \n2: Popular movies right now \n3: Top 100 TV series \n4: Actor movies \n5: Bottom 100 movies \n6: Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        top100movies()
    elif choice == "2":
        popular100movies()
    elif choice == "3":
        top100tv()
    elif choice == "4":
        actor = input("Enter the actor name: ")
        ActorMovies(actor)
    elif choice == "5":
        bottom100movies()
    elif choice == "6":
        exit()

def top100movies():
    list = ia.get_top250_movies()
    print("Downloading 100 movie posters from the slowest package, please wait a couple of minutes")
    create_csv(list)
    heading = 'T o p  1 0 0   M o v i e s   b u c k e t   l i s t '
    heading2 = ' --- The highest rated IMDb favorites --- '
    create_pdf(heading, heading2)

def bottom100movies():
    list = ia.get_bottom100_movies()
    print("Downloading 100 movie posters from the slowest package, please wait a couple of minutes")
    create_csv(list)
    heading = 'B o t t o m  1 0 0   M o v i e s   b u c k e t   l i s t '
    heading2 = ' --- The lowest rated IMDb favorites --- '
    create_pdf(heading, heading2)

def top100tv():
    list = ia.get_top250_tv()
    print("Downloading 100 series posters from the slowest package, please wait a couple of minutes")
    create_csv(list)
    heading = 'T o p  1 0 0   S e r i e s   b u c k e t   l i s t '
    heading2 = ' --- The highest rated IMDb favorites --- '
    create_pdf(heading, heading2)

def popular100movies():
    list = ia.get_popular100_movies()
    print("Downloading 100 popular movies posters from the slowest package, please wait a couple of minutes")
    create_csv(list)
    heading = '1 0 0   P o p u l a r   M o v i e s   b u c k e t   l i s t '
    heading2 = ' --- Popular IMDb favorites --- '
    create_pdf(heading, heading2)

def ActorMovies(actor):
    people = ia.search_person(actor)
    people = ia.get_person(people[0].personID)
    if "actor" in people['filmography']:
        list = people['filmography']['actor']
        heading2 = ' --- Actor favorites --- '
    else:
        list = people['filmography']['actress']
        heading2 = ' --- Actress favorites --- '
    list = list[::-1]
    print("Downloading " + str(len(list)) + " movie posters from the slowest package, please wait a couple of minute")
    create_csv(list)
    heading = str(people) + '   b u c k e t   l i s t '

    create_pdf(heading, heading2)

def create_csv(list):
    x = 0
    if os.path.isfile("movierecords.csv"):
        os.remove("movierecords.csv")
    for movie in list:
        with open('movierecords.csv', 'a') as f:
            f.write(str(movie.movieID) + ',' + movie.get('title') + ',' + str(movie.get('year')) + ',' + str(movie.get('rating')) + '\n')
            fullfilename = os.path.join("movie_posters/", str(movie.movieID)+".jpg")
            if not os.path.isfile(fullfilename):
                #print(ia.get_movie(movie.movieID).get('cover url'))
                try:
                    urllib.request.urlretrieve(ia.get_movie(movie.movieID).get('cover url'), fullfilename)
                except:
                    shutil.copy("unknown.jpg",fullfilename)
            x = x + 1
            if x == 100:
                break

def create_pdf(heading, heading2):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.add_font('Bebas', '', r"BebasNeue-Regular.ttf", uni=True)
    pdf.add_font('Bebas-L', '', r"BebasNeue-Light.ttf", uni=True)

    img = Image.new('RGB', (210, 297), "#262123")
    img.save('gray.png')
    pdf.image('gray.png', x=0, y=0, w=210, h=297, type='', link='')

    pdf.set_font('Bebas-L', '', 25)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 5, heading, 0, 1, 'C')
    pdf.set_font('Bebas', '', 12)
    pdf.cell(0, 10, heading2, 0, 1, 'C')

    pdf.set_font('Helvetica', 'B', 5)
    x = 0
    y = 0
    offsety = 30
    offsetx = 17
    with open('movierecords.csv', 'r') as f:
        for line in f:
            line = line.split(',')
            pdf.image('movie_posters/'+line[0]+'.jpg', (x * 18 + offsetx), (y + offsety), 13, 18)
            wordlist = line[1].split()
            if len(wordlist) > 2 and len(wordlist) < 6:
                pdf.text((x * 18 + offsetx), (y + offsety + 20), ' '.join(wordlist[0:2]))
                pdf.text((x * 18 + offsetx), (y + offsety + 22), ' '.join(wordlist[2:]))
            elif len(wordlist) > 5:
                pdf.text((x * 18 + offsetx), (y + offsety + 20), ' '.join(wordlist[0:2]))
            else:
                pdf.text((x * 18 + offsetx), (y + offsety + 20), line[1])
            x = x + 1
            if x == 10:
                pdf.multi_cell(0, 5, '\n')
                y =  y + 25
                x = 0
    pdf.output('poster.pdf', 'F')

if __name__ == '__main__':
    run()