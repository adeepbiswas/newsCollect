from bs4 import BeautifulSoup
import requests
import re
import csv

pages= set()
datepages= set()
newspages= set()
slno=1

def getMonthLinks(pageUrl):
    global pages
    try:
        r = requests.get(pageUrl)
        bsobj = BeautifulSoup(r.text, "lxml")
        x=bsobj.select("div.archiveBorder > ul > li > a")
        #x = bsobj.find(class_="archiveBorder").find_all("ul").find_all("li").find_all("a", href=re.compile("^(http://www.thehindu.com/archive/print/)"))
    except requests.exceptions.RequestException as e:
        print("Error occurred 1\n"+str(e))
    except AttributeError as e:
        print("Something is missing 1\n"+str(e))
    else:
        #for link in bsobj.find(class_="archiveBorder").find_all("ul").find_all("li").find_all("a", href=re.compile("^(http://www.thehindu.com/archive/print/)")):
        for link in x:
            if 'href' in link.attrs:
                if link.get('href') not in pages:
                    newpage = link.get('href')
                    yearstr=newpage[38:42]
                    ust = newpage[43:45]
                    year=int(yearstr)
                    u=int(ust)
                    if year >= 2014 and u >= 8:
                        print(newpage)
                        pages.add(newpage)
                        getDateLinks(newpage)

def getDateLinks(datepageUrl):
    global datepages
    try:
        r = requests.get(datepageUrl)
        bsobj = BeautifulSoup(r.text, "lxml")
        x=bsobj.select(".archiveTable > tbody > tr > td > a")
        #x = bsobj.find(class_="archiveTable").find("tbody").findAll("tr").findAll("td").findAll("a", href=re.compile("^(http://www.thehindu.com/thehindu/)"))
    except requests.exceptions.RequestException as e:
        print("Error occurred 2\n"+str(e))
    except AttributeError as e:
        print("Something is missing 2\n"+str(e))
    else:
        for link in x:
            if 'href' in link.attrs:
                if link.get('href') not in pages:
                    newpage = link.get('href')
                    print(newpage)
                    datepages.add(newpage)
                    check = newpage.find("print")
                    if check == -1:
                        continue
                        #getOldNewsLinks(newpage)
                    else:
                        getNewNewsLinks(newpage)

def getOldNewsLinks(newspageUrl):
    global newspages
    categories=set()
    try:
        r = requests.get(newspageUrl)
        bsobj = BeautifulSoup(r.text, "lxml")
        x=bsobj.select("font > a")
        #x = bsobj.findAll("table")[1].find("tbody").findAll("tr").findAll("td")[0].findAll("p")[0].findAll("a")
        #y = bsobj.findAll("table")[1].find("tbody").findAll("tr").findAll("td")[1].findAll("a")
    except requests.exceptions.RequestException as e:
        print("Error occurred 3\n"+str(e))
    except AttributeError as e:
        print("Something is missing 3\n"+str(e))
    else:
        for link in x:
            if 'href' in link.attrs:
                fl = link.get('href').find("hdline")
                if fl != -1:
                    if link.get('href') not in categories:
                        newpage = newspageUrl+link.get('href')
                        print(newpage)
                        categories.add(newpage)

        for i in categories:
            s = requests.get(i)
            bsobj1 = BeautifulSoup(r.text, "lxml")
            y = bsobj1.select("a")
            for link in y:
                if 'href' in link.attrs:
                    if link.get('href').find("stories") != -1:
                        title=link.get_text().lower()
                        if title.find("rape")!=-1 or title.find("raping")!=-1 or title.find("molest")!=-1 or title.find("abuse")!=-1 or title.find("murder")!=-1 or title.find("assault")!=-1:
                            if newspageUrl+link.get('href') not in newspages:
                                newpage = newspageUrl+link.get('href')
                                print(newpage)
                                newspages.add(newpage)
                                getOldData(title, newpage)

def getNewNewsLinks(newspageUrl):
    global newspages
    try:
        r = requests.get(newspageUrl)
        bsobj = BeautifulSoup(r.text, "lxml")
        x=bsobj.select("div.section-container > div > div > div > ul.archive-list > li > a")
        #x = bsobj.find(class_="container-main").findAll("section")[0].findAll("div").findAll("div").findAll(
            #"div").findAll("div").findAll("section").findAll(class_="section-container").findAll("a", href=re.compile(
            #"^(http://www.thehindu.com/todays-paper/)"))

    except requests.exceptions.RequestException as e:
        print("Error occurred 4\n"+str(e))
    except AttributeError as e:
        print("Something is missing 4\n"+str(e))
    else:
        for link in x:
            if 'href' in link.attrs:
                title = link.get_text().lower()
                if title.find("rape") != -1 or title.find("raping") != -1 or title.find("molest") != -1 or title.find("abuse") != -1 or title.find("murder") != -1 or title.find("assault")!=-1:
                    if link.get('href') not in pages:
                        newpage = link.get('href')
                        print(newpage)
                        newspages.add(newpage)
                        getNewData(title, newpage)

def getOldData(arctitle, locationUrl):

    try:
        date = ""
        location = ""
        r = requests.get(locationUrl)
        bsobj = BeautifulSoup(r.text, "lxml")
        para=bsobj.select("location")
        #path=bsobj.findAll("table")[1].find("tbody").findAll("tr")
        for i in para:
            location=i.get_text()
        dateobj = bsobj.select("center > font")
        for i in dateobj:
            date = i.get_text()
        #dateobj=bsobj.select("table[0] > tbody > tr[0] > td[0] > font[1]")
        #dateobj=bsobj.findAll("table")[0].findAll("tbody").findAll("tr")[0].findAll("td")[0].findAll("font")[1]
        #date=dateobj.get_text()
        addData(date, location, arctitle, locationUrl)
    except requests.exceptions.RequestException as e:
        print("Error occurred 5\n"+str(e))
    except AttributeError as e:
        print("Something is missing 5\n"+str(e))

def getNewData(arctitle, locationUrl):

    r = requests.get(locationUrl)
    details = []
    i = 0
    date=""
    location=""
    bsobj = BeautifulSoup(r.text, "lxml")
    rt=bsobj.select("div.ut-container > span")
    for elements in rt:
        details.append(elements.get_text())
        i=i+1
    #rt = bsobj.findAll("div", class_="ut-container").findAll("span")
    rtlen = len(rt)
    try:
        if rtlen == 1:
            date = details[0]
            locationx = bsobj.select("div.article > div > p")
            for para in locationx:
                ps = para.get_text().split(" ")
                for word in ps:
                    if word.find(":") != -1 and word[0].isupper():
                        location = word
                        break
        else:
            date = details[1]
            location = details[0]
        addData(date, location, arctitle, locationUrl)
    except AttributeError as e:
        print("Something is missing 6\n"+str(e))
    except IndexError as e:
        print("Index error 6\n"+str(e))


def addData(date,location,name,url):
    global slno
    row = [slno, date, location, name, url]
    slno=slno+1
    with open('newsdata.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    #csvFile.close()

heading = ['Serial No', 'Date', 'Location', 'Title', 'Link']
#with open('newsdata.csv', 'w') as csvFile:
#    writer = csv.writer(csvFile)
#    writer.writerow(heading)
getMonthLinks("http://www.thehindu.com/archive/print/")

#csvFile.close()