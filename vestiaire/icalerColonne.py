import csv
from ics import Calendar, Event

def line_gatherer():
    with open('juilAout.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        line_count = 0
        jours =  []
        noms= []
        
        
        print("Generating the Days and the Names in the file...  \n \n")
        for row in csv_reader:
            if row[0] == "ï»¿SEMAINE" or row[0] == 'SEMAINE':
                for jour in row:
                    if len(jour) > 2 and jour != 'ï»¿SEMAINE' and jour !='SEMAINE':
                        jours.append(jour)
            elif len(row[0]) > 2 and row[0] not in noms:
                noms.append(row[0])
        csv_file.seek(0)
        
        line_decrem = 0
        print(f"les jours {jours}")
        print(f"\n et les noms : {noms}")
        for nom in noms:
            creneau = [None,None,None]
            planning = {}
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
                        #print(f"la case : {row[case]}")
                        #print(f" la case : {case}, la case%3 :  {case%3}")
                        
                        if case%3==1:
##                            print(f"case%3==1")
                            creneau[0]=row[case]
                            alt = case//3
                            if alt<7:
                                #print(alt*(1+(rowInt//19)))
                                creneau[2]=jours[alt+(7*(rowInt//19))]
                        elif case%3==2:
                            creneau[1]= row[case]
                            
                            if creneau[0] != " REPOS " and len(creneau[0])>0 and len(creneau[1])>0:
                                
                                planning['creneau'].append((creneau[0],creneau[1],creneau[2]))
                                print (creneau)
                                
                            creneau = [None,None,None]
                
                    
            print(planning, "\n \n")
            for creneau in planning["creneau"]:
                #print(creneau)
                heureamodifier = ['7:45','8:00','8:30','9:00']
                if creneau[0] in heureamodifier:
                    correctedcreneau = '0'+creneau[0]
                    creneauStr = (creneau[2]+ " "+ correctedcreneau,creneau[2]+ " "+ creneau[1])
                else :
                    #print(f"not in heureamodifier : {creneau[0]}")
                    creneauStr = (creneau[2]+ " "+ creneau[0],creneau[2]+ " "+ creneau[1])
                c = Calendar()
                e = Event()
                e.name = 'piscine ' + planning["nom"]
                e.begin = creneauStr[0]
                e.end = creneauStr[1]
                c.events.add(e)
                c.events
                with open(planning["nom"]+'.ics', 'a') as my_file:
                    my_file.writelines(c)
                
            planning['nom']= None
            planning['creneau']= []
            csv_file.seek(0)
##            if line_count == 0 and len(row)>3:
##                print(f'Column names are {", ".join(row)}')
##                line_count += 1
##            else:
##                print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
##                line_count += 1
##        print(f'Processed {line_count} lines.')
line_gatherer()
