# Dependencies.
import csv
import time
import sys

# Our path to the municipality address file.
# If using own CSV file, make sure to put it in the same file directory or define the full path.
# This data originates in our case from: https://www.lounaistieto.fi/turun-kaupungin-osoitedata/
path = "adrs.csv"

# This serves as our output CSV file where our finished parsed addresses will be stored in.
# We assume the first row in our output CSV file contains: kaupunki,katunimi,osoitenumero,n,e,gatan
# The first row should be retained if we are to continue with the importers.
outputpath = "mycsv.csv"

is_user_done = False

while is_user_done == False:

    fin_muni = input("Write the Finnish municipality name: ")
    sv_muni = input("Write the corresponding Swedish municipality name. Press enter if no Swedish name: ")

    def preprocess(finnish_municipality_name, swedish_corresponding_municipality_name):

        print("Started processing. . .")
        print(finnish_municipality_name, swedish_corresponding_municipality_name)

        with open(path, 'r', newline='', encoding="iso-8859-1") as csv_file:
            csv_reader = csv.reader(csv_file)
            print(csv_reader)

            # We are mapping our CSV file objects row by row, getting rid of the delimiter ";"
            # and joining each row objects together into the array variable c.
            # Please notice that the city geo location inside c is made into an array with both the north and east coordinates.
            # We then return c and make a list of the entire CSV file known as k.
            # a, b variables are a list comprehension where our array variable a goes through our Finnish municipalities
            # and b finds the corresponding Swedish municipality name IF that can/was be found/defined.
            def map_to_obj(x):
                o = "".join(x).split(';')
                c = [o[0],o[1],o[2],[o[3], o[4]]]
                return c
            k = list(filter(lambda t: t is not None, map(map_to_obj, csv_reader)))
            a, b = [ k[i] for i in range(len(k)) if k[i][0] == finnish_municipality_name ] , [ k[i] for i in range(len(k)) if k[i][0] == swedish_corresponding_municipality_name ]
            #ab = [[ a[x][0], a[x][1], a[x][2], a[x][3][0], a[x][3][1], b[z][1] ] for x in range(len(a)) for z in range(len(b)) if a[x][3] in b[z]]


        #Dependency variables for parsing & finished formatted array.
        returned = False
        ab = []
        newarr = []

        # This section here loops through the Finnish municipality city data and finds
        # the corresponding Swedish municipality city based on the geo coordinate data.
        # We append the Swedish city name on the very last column in our combined array "ab".
        # In case we DON'T find a corresponding Swedish city name, we simply append the Finnish
        # city name on the last column.
        for x in range(len(a)):
            for z in range(len(b)):
                if a[x][3] in b[z]:
                    returned = True
                    a[x].append(b[z][1])
                    break
                returned = False
            if returned == True:
                #print(str(x)+" PROCESSING: FI SV Compatible: "+str(a[x]))
                ab.append(a[x])
            else:
                #print(str(x)+" PROCESSING: Didn't find Swedish name of: "+str(a[x]))
                temp_a = []
                temp_a = a[x]
                temp_a.append(a[x][1])
                ab.append(temp_a)

        print("Formatting . . .")

        # Since our combined ab array at this point still has our geo location data in an array,
        # we can't simply put that data into a CSV file without formattin it accordingly.
        # We iterate through the ab array and see if our current index value is an array and if that is the case,
        # we iterate through that one as well (which will be our geo location data) and append it
        # to our finished "newarr" array with the other ab data as well which will be fully CSV compatible.
        for xa in range(len(ab)):
            tempnewarr = []
            for b in ab[xa]:
                if isinstance(b, list):
                    for ll in b:
                        tempnewarr.append(ll)
                else:
                    tempnewarr.append(b)
            newarr.append(tempnewarr)

        print("Writing to CSV. . . ")

        # At this point we are ready to start writing our "newarr" data to our CSV output file.
        def writing(abc):
            with open('mycsv.csv', 'a', newline='') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(abc)

        for idx, arrobjidx in enumerate(newarr):
            writing(arrobjidx)

    preprocess(fin_muni, sv_muni)

    # When our file has been written, we ask the user if they want to add more municipality data
    # into the output CSV file from our source address CSV file.
    # However, please note you can only add existing data from the source address CSV file.
    isreadyloop = True
    while isreadyloop == True:
        isready = input("Would you like to continue adding more municipalities? [Y,N]: ")
        if isready.lower() == "y":
            isreadyloop = False
        elif isready.lower() == "n":
            sys.exit()
        else:
            print("Please choose either Y or N to continue?")