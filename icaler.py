# coding: utf8
#Those are the modules that i used, they are python files with already coded functions
import csv
from ics import Calendar, Event
from os import walk,SEEK_SET,SEEK_END
import datetime
from pytz import timezone
import os
from shutil import rmtree

#######################################################################################################################################################################################################

############################################################         VARIABLES TO CHANGE FOR THE WELL BEING OF THE PROGRAM          #####################################################################

#######################################################################################################################################################################################################

#here i set up the timezone, i work with Paris, change that to where you work/live
paris = timezone('Europe/Paris')

#######################################################################################################################################################################################################

#if you get undesired strings in table, at the end your parsing (weirdly named file etc...) add them their 
undesiredBeginningStrings = ["ï»¿SEMAINE", "\ufeffSEMAINE", "SEMAINE", 'SEMAINE']

#######################################################################################################################################################################################################

#same but in the cells ( stuff you don't need like if the persons is on a break the whole day, you might not want to put it in the file, just saying)
inCellsUndesiredStrings = [" REPOS "]

#######################################################################################################################################################################################################

separator = ';' #VERY IMPORTANT : ON SOME OS, CSV FILE GENERATED ISNT ',' BUT ';', here your chance to change it 

#######################################################################################################################################################################################################




#######################################################################################################################################################################################################

##########################################################                      FUNCTIONS                                           ##################################################################

#######################################################################################################################################################################################################

def calGeter():
    if os.path.exists('fichiersSortie'):
        rmtree('fichiersSortie')
    os.chdir(r'fichiersAtraiter')
    
    files = [f for f in os.listdir('.') if f.endswith('.csv')]
    for file in files:
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=separator)

            line_count = 0
            jours =  []
            noms= []
            rows = 0
             
            #print("Generating the Days and the Names in the file...  \n \n")
            for row in csv_reader:

                rows += 1
                if row[0] in undesiredBeginningStrings :
                    for jour in row:
                        if len(jour) > 2 and jour != 'ï»¿' and jour !='SEMAINE'and jour != 'ï»¿SEMAINE' and jour !='\ufeffSEMAINE' and jour !='\ufeff' :
                            jours.append(jour)
                elif len(row[0]) > 2 and row[0] not in noms:
                    noms.append(row[0])
            csv_file.seek(0)
            planning = {}
 
            
            if rows > 45: #if the structure is a column structure (ok this isn't great a way to proceed, but that has to work for my way of doing things anyway) 
                line_decrem = 0

                for nom in noms:
                    creneau = [None,None,None]
                    planning["creneau"]=[]
                    planning['nom']=nom
                    print(f"Generating the planning for : {nom} ... \n \n")
                    rowInt = 0
                    for row in csv_reader:
                        rowInt += 1
                        if row[0] == nom or line_decrem > 0:
                           
                            #print(f" la row[0] : {row[0]}")
                            if line_decrem > 0:
                                line_decrem -= 1
                            else:
                                line_decrem += 1 
                            for case in range(len(row)):
                                if case%3==1:
                                    creneau[0]=row[case]
                                    alt = case//3
                                    if alt<7:
                                        #print(alt*(1+(rowInt//19)))
                                        creneau[2]=jours[alt+(7*(rowInt//19))]
                                elif case%3==2:
                                    creneau[1]= row[case]
                                
                                    if creneau[0] not in inCellsUndesiredStrings and len(creneau[0])>0 and len(creneau[1])>0:
                                        
                                        planning['creneau'].append((creneau[0],creneau[1],creneau[2]))
                                        
                                    creneau = [None,None,None]
                            
                    printerToCalendar(planning,csv_file)
            else :
                line_decrem = 0
                for nom in noms:
                    creneau = [None,None,None]
                    planning["creneau"]=[]
                    planning['nom']=nom
                    print(f"Generating the planning for : {nom} ... \n \n")
                    for row in csv_reader:
                        if row[0] == nom or line_decrem > 0:
                            #print(f" la row[0] : {row[0]}")
                            if line_decrem > 0:
                                line_decrem -= 1
                            else:
                                line_decrem += 1
                            for case in range(len(row)):
                                #print(f"la case : {row[case]}")
                                #print(f" la case : {case}, la case%3 :  {case%3}")

                                if case%3==1:
        ##                            print(f"case%3==1")
                                    creneau[0]=row[case]
                                    alt = case//3
                                    if alt<63:
                                        creneau[2]=jours[alt]
                                elif case%3==2:
                                    creneau[1]= row[case]
                                    if creneau[0] != " REPOS " and len(creneau[0])>0 and len(creneau[1])>0:

                                        planning['creneau'].append((creneau[0],creneau[1],creneau[2]))

                                    creneau = [None,None,None]

                        

                    printerToCalendar(planning,csv_file)
    toCalendarFormatter()
    


#######################################################################################################################################################################################################



    
def printerToCalendar(planning,csv_file):
    for creneau in planning["creneau"]:
        c = Calendar()
        e = Event()
        e.name = 'piscine ' + planning['nom']
        heureCreneau = list(creneau[0])
        for elem in heureCreneau:
            if elem == ':':
                heureCreneau = heureCreneau[:heureCreneau.index(elem)]
                pass
        heureCreneau = ''.join(str(elem) for elem in heureCreneau)
        heureCreneauend = list(creneau[1])
        for elem in heureCreneauend:
            if elem == ':':
                heureCreneauend = heureCreneauend[:heureCreneauend.index(elem)]
                pass
        heureCreneauend = ''.join(str(elem) for elem in heureCreneauend)
        minute = ''.join(str(elem) for elem in creneau[0][-2:])
        minuteEnd = ''.join(str(elem) for elem in creneau[1][-2:])
        #print(f"heure : {heureCreneau}  et la minute : {minute}, creneau : {creneau[1]}")
        date = creneau[2].split(' ')
        # print(f" la date : {date}")
        datetime_object = datetime.datetime.strptime(date[2], "%B")
        date[2] = datetime_object.month
        

        e.begin = datetime.datetime(int(date[3]), int(date[2]), int(date[1]),int(heureCreneau), int(minute), 0, tzinfo=paris)
        # e.begin = creneauStr[0]
        # e.end = creneauStr[1]
        #print(date,heureCreneauend+':'+minute)
        e.end = datetime.datetime(int(date[3]), int(date[2]), int(date[1]),
                                  int(heureCreneauend), int(minuteEnd), 0, tzinfo=paris)

        # e.begin = creneauStr[0]
        # e.end = creneauStr[1]
        c.events.add(e)
        c.events
        os.chdir(r'../')
        if not os.path.exists('tmp'):
            os.mkdir('tmp')
        os.chdir('tmp')
        #planning['nom'] = nom
        with open(planning["nom"] + '.ics', 'a') as my_file:
            my_file.writelines(c)
        os.chdir('../fichiersAtraiter')
    planning['nom'] = None
    planning['creneau'] = []
    csv_file.seek(0)

#######################################################################################################################################################################################################


def toCalendarFormatter():
    '''
        This function is intended to correct the file, as the ICS modules allows only one event at a time
        (or at least, couldn't find any information that would go against this, i changed the file myself, after learning the ics files' configuration)
        this function take the files that were previously generated and change them into a diggestable file for any calendar (Mac, outlook, google were tested)
    '''
    os.chdir('../tmp')
    f = []
    e = []
    for (dirpath, dirnames, filenames) in walk("./"):
        f.extend(filenames)
        break
    for name in f:
        if 'ics' in name:
            e.append(name)
    
    for infile in e:
        
        
        outfile=infile
        delete_list = ["BEGIN:VCALENDAR","END:VCALENDAR", "VERSION:2.0", "PRODID:ics.py - http://git.io/lLljaA"]
        fin = open(infile)
        os.chdir(r'../')
        if not os.path.exists('fichiersSortie'):
            os.mkdir('fichiersSortie')
        os.chdir('fichiersSortie')
        fout = open(outfile, "w+")
        
        for line in fin:
            for word in delete_list:
               line = line.replace(word, "")
            fout.write(line)
        fin.close()
        fout.close()
        fout = open(outfile, "r+")
        lines = fout.readlines()
        fout.seek(0, SEEK_SET)
        fout.write(delete_list[0])
        fout.write("\n")
        fout.write(delete_list[2])
        fout.write("\n")
        fout.write(delete_list[3])
        fout.write("\n")
        fout.write("\n")
        for line in lines: 
            fout.write(line)

        fout.write("\n")
        fout.write(delete_list[1])
        
        fout.close()
        os.chdir(r'../tmp')
    os.chdir('../')
    if os.path.exists('tmp/'):
        rmtree('tmp/')
    

#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################


if __name__ == '__main__':
    calGeter()

