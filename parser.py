__author__ = 'mmozaffari'

from bs4 import BeautifulSoup
import requests
import eduworkParser
import re
import json
import glob
import os

dir_path = os.path.join("fb")  # will return 'feed/address'
if not os.path.exists(dir_path):
    os.mkdir(dir_path)

def parse(htmlfile):
    f = open(htmlfile,'r')
    content = f.read()
    soup = BeautifulSoup(content)

    '''
    div = soup.select("div#pagelet_timeline_medley_info")
    for v in div:
    '''

    '''
    head = soup.find('div',attrs={"id":"pagelet_timeline_medley_info"})
    about = soup.find("div",attrs={"id":"pagelet_timeline_medley_info"})
    print(about)
    '''


    fbProfileName = soup.find('div',attrs={'id':'fbProfileCover'}).find('h2').get_text()

    #### Education and work : work, graduate school, college, high school, skills

    data = dict()
    dataKey = ""
    dataValue = dict()
    # "dataKey" : "dataValue"

    eduwork = soup.find('div',attrs={'id':'eduwork'})
    eduworkHeader = eduwork.find('h4',attrs={'class':'uiHeaderTitle'}).get_text()
    dataKey = eduworkHeader
    #print eduworkHeader

    table = eduwork.find('table').find_all('tbody',recursive=False)
    for tbody in table :
        rows = tbody.find_all('tr',recursive=False)
        for row in rows :
            if row.get('class') is None:
                rowHeader = row.th.get_text()  ## header
                key = rowHeader
                print "   "+rowHeader
                value = list()

                for item in row.td.find_all('li'):
                    experience = item.find('div',attrs={'class':'experienceTitle'})
                    s = ""
                    if experience is not None:
                        s = s + experience.get_text()
                        print("      "+experience.get_text())
                    desc = item.find_all('div',attrs={'class':'experienceBody'})
                    if desc is not None:
                        for d in desc:
                            s = s + " " + d.get_text()
                            print("        "+d.get_text())
                    if s != "":
                        value.append(s)
                dataValue[str(key)] = value

            elif row.get('class') == [u'mvl']:    # in class ro nemifahme ke hamune!!
                header = row.td.div.div.get_text()
                print "   "+header
                key = header
                value = list()
                skills = row.find_all('a') # inam emtehan kon ke age unchizi ke be onvane skill vared mikoni nadashte bashe kodesh ham tagesh a mishe ya na!
                for skill in skills:
                    value.append(skill.get_text())
                    print "      "+skill.get_text()
                dataValue[key] = value



    data[dataKey] = dataValue
    #print data


    print('#######################Relationships#########################')
    # relationships

    relationships = soup.find('div',attrs={'id':'relationships'})
    if relationships is not None:
        header = relationships.find('h4',attrs={'class':'uiHeaderTitle'})
        k = header.get_text()
        v = ""
        print(header.get_text())
        rels = relationships.find('table').find_all('tbody') # chanta tbody mitune dashte bshe va har tbody chanta tr
        for rel in rels :
            t = rel.find('div',attrs={'class':'fsl fwb fcb'})
            person = t.find('a')
            about = rel.find('div',attrs={'class':'aboutSubtitle'})
            if person is not None:
                v = person.get_text()
                print("   "+person.get_text())
                print("   "+person.get('href'))
            else:
                v = t.get_text()
                print("   "+t.get_text())
            if about is not None :
                v = v + ", " + about.get_text()
                print ("    "+about.get_text())
        data[str(k)] = v

    # print data

    print('#########################Family#########################')
    # Family
    family = soup.find('div',attrs={'id':'family'})
    if family is not None:
        familyHeader = family.find('h4').get_text()
        print(familyHeader)
        k = familyHeader
        v= list()

        table = family.find('table').find('tbody').find('tr').find('td')
        # OR table = family.find('div',attrs={'id':'family-relationships-pagelet'})
        items = table.find('ul').children
        if items is not None: # lazeme ya na!
            for item in items :
                t = item.find('div',attrs={'class':'fsl fwb fcb'})  # age ax nadashte bashe ham tagesh a e?
                person = t.find('a')

                rel = item.find('div',attrs={'class':'aboutSubtitle'})
                if person is not None:
                    personName = person.get_text()
                    listItem = personName
                    print "    "+personName
                    link = person.get('href')
                    print "    "+link
                else:
                    listItem = t.get_text()
                    print "    "+t.get_text()
                if rel is not None:
                    listItem = listItem +", " + rel.get_text()
                    print "    "+rel.get_text()
                v.append(listItem)
            data[str(k)] = v
    #print data

    print('#####################Places Lived#########################')
    # places lived

    places = soup.find('div',attrs={'id':'pagelet_hometown'})
    if len(places.contents) != 0:
        header = places.find('h4',attrs={'class':'uiHeaderTitle'})
        print header.get_text()
        k = header.get_text()
        v = list()

        table = places.find('table').find_all('tbody',recursive=False)
        for item in table:
            rows = item.find_all('tr',recursive=False)
            for r in rows:
                city = r.find('div',attrs={'class':'fsl fwb fcb'})
                about = r.find('div',attrs={'class':'aboutSubtitle'})

                if city is not None:
                    s = city.get_text()
                    print "      "+ city.get_text()
                    if about is not None:
                        s = s +", " + about.get_text()
                        print "        "+about.get_text()
                v.append(s)
        data[str(k)] = v
    #print data


    print('########################About#############################')
    # Bio
    Bio = soup.find('div',attrs={'id':'pagelet_bio'})

    if len(Bio.contents) != 0:
        header = Bio.find('h4',attrs={'class':'uiHeaderTitle'})
        print header.get_text()
        about = Bio.find('div',attrs={'class':'profileText'})
        print "   "+about.get_text()
        data[str(header.get_text())] = about.get_text()

    # print data

    print('##################Favorite Quotations#####################')

    # favorite quotations
    quotes = soup.find('div',attrs={'id':'pagelet_quotes'})
    isNone = quotes.contents
    if len(quotes.contents) != 0:
        header = quotes.find('h4',attrs={'class':'uiHeaderTitle'})
        print header.get_text()
        favQuot = quotes.find('div',attrs={'class':'profileText'})
        print "   "+favQuot.get_text()
        data[str(header.get_text())] = favQuot.get_text()
    # print data


    print('###################Basic Information######################')
    '''
    hometown = soup.find('div',attrs={'id':'pagelet_hometown'})
    if hometown is not None:
        header = hometown.find('div',attrs={'class':'uiHeader'}).get_text()
        print header
        table = hometown.find('table').find('tbody').find_all('tr')
        for row in table:
            currentCity = row.find('div',attrs={'id':'current_city'})
            if currentCity is not None :
                print "Current City : " + currentCity

                '''
    # Basic information

    basic = soup.find('div',attrs={'id':'pagelet_basic'})
    if basic is not None:
        header = basic.find('h4',attrs={'class':'uiHeaderTitle'})
        print header.get_text()
        table = basic.find_all('tbody')
        k = header.get_text()
        v = dict()
        for part in table:
            items = part.children
            for item in items:
                v[item.th.get_text()] = item.td.get_text()
                print("   " + item.th.get_text() + " : " + item.td.get_text())
        data[str(k)] = v
   # print data


    print('###################contact information####################')
    # Contact information

    contactInfo = soup.find('div',attrs={'id':'pagelet_contact'})
    if contactInfo is not None:
        header = contactInfo.find('h4',attrs={'class':'uiHeaderTitle'})
        print header.get_text()
        k = header.get_text()
        v = dict()

        table = contactInfo.find('table').find_all('tbody',recursive=False)

        for part in table:
            items = part.find_all('tr',recursive=False)
            for item in items:
                text = item.th.get_text()
                print("   " +text)

                isList = item.td.find('ul')
                if isList is not None:
                    ll =  list()
                    lis = item.find_all('li')
                    for l in lis:
                        ll.append(l.get_text())
                        print("      "+l.get_text())
                    v[str(text)] = ll

                else:
                    t = str(item.td.get_text())
                    if not t.startswith("Ask for"):
                        print("      "+t)
                        v[str(text)] = t
        data[str(k)] = v
    #print data
    #######################################################

    events = soup.find('div',attrs={'id':'pagelet_yearly'})
    print events
    if len(events.contents) != 0:
        header = events.find('h4',attrs={'class':'uiHeaderTitle'})
        if header is not None :
            header = header.get_text()

        k = header
        v = dict()
        print(header)

        items = events.find('ul').find_all('li',recursive=False)
        for item in items:
            if item.get('class') != [u'showAll']:
                year = item.find('ul').find('li',attrs={'class':'_5mj_'})
                evs = item.find('ul').find('li',attrs={'class':'_5mk0'})
                temp = evs.find_all('li')
                if len(temp) >1:
                    templ = list()
                    for e in temp:
                        t = e.get_text()
                        templ.append(t)
                    print templ
                elif len(temp) == 1:
                    templ = temp[0].get_text()
                    print templ

                if year.get_text() == "":
                    year = "-"
                else:
                    year = year.get_text()
                v[year] = templ

        data[k] = v

    ## writing json data to file

    json_encoded = json.dumps(data)

    fileName = fbProfileName + ".txt"
    with open(os.path.join(dir_path, fileName), 'wb') as outfile:
      json.dump(data, outfile,sort_keys=True,indent=4)


files = glob.glob("./*.txt")
for personsFile in files:
    parse(personsFile)