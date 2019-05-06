import http.server
import socketserver
import termcolor
import http.client
import json

socketserver.TCPServer.allow_reuse_address = True

# Define the Server's port
PORT = 8000

# -- API information
HOSTNAME = 'rest.ensembl.org'
ENDPOINT_1 = '/info/species'
FORMAT_1 = '?content-type=application/json'
ENDPOINT_2 = '/info/assembly/'
FORMAT_2 = '?expand=1;'
ENDPOINT_3 = '/lookup/symbol/homo_sapiens/'
FORMAT_3 = '?feature=gene;'
ENDPOINT_4 = '/sequence/id/'
ENDPOINT_5 = '/overlap/region/human/'
METHOD = 'GET'


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # -- Parser the path
        list_resource = self.path.split('?')
        print(list_resource, '!')
        resource = list_resource[0]

        if resource == "/":
            f = open("index.html", 'r')
            code = 200
            # Read the file
            contents = f.read()

            content_type = 'text/html'

        elif resource == "/listSpecies":

            try:
                number_species = list_resource[1][list_resource[1].find("limit=") + 6:]

                if number_species == "0":
                    number_species = 199

                elif "-" in number_species:
                    number_species = "error"

                if not number_species:
                    number_species = 199

            except IndexError:

                number_species = 199

            try:

                json_species = json.loads(get_ensembl_species(ENDPOINT_1))

                info_species = information_species(json_species)

                species = ""

                for k, v in info_species.items():
                    if k < int(number_species):
                        species = species + str(k+1) + ': ' + v + "</br>"
                    else:
                        break
                contents1 = """ <head>
                        <meta charset="utf-8">
                        <title>listSpecies</title>
                      </head>
                      <body> """

                contents2 = """    <a href="/" >MAIN PAGE</a>
                      </body>
                    </html>"""
                contents = contents1 + species + contents2

                code = 200
                content_type = 'text/html'

            except ValueError:

                f = open("error.html", 'r')
                code = 404
                contents = f.read()
                content_type = 'text/html'

        elif resource == "/karyotype":

            try:

                species_name = list_resource[1][list_resource[1].find("specie=") + 7:].replace("+", "_")

                json_karyotypes = json.loads(get_ensembl_karyotypes(species_name))

                info_karyotype = information_karyotypes(json_karyotypes)

                karyotype = ""

                for k, v in info_karyotype.items():
                    karyotype = karyotype + "-   " + v + "." + "<br>"

                contents1 = """ <head>
                                <meta charset="utf-8">
                                <title>karyotype</title>
                              </head>
                              <body> """

                contents2 = """    <a href="/" >MAIN PAGE</a>
                              </body>
                            </html>"""

                contents = contents1 + karyotype + contents2
                code = 200
                content_type = 'text/html'

            except (KeyError, IndexError, UnboundLocalError) as error:

                e = "ERROR: "
                print(e, error)
                f = open("error.html", 'r')
                code = 404
                contents = f.read()
                content_type = 'text/html'

        elif resource == "/chromosomeLength":

            try:

                parameters = list_resource[1].split("&")
                print(parameters)

                for i in parameters:
                    if "specie" in i:

                        species_name = i[i.find("specie=") + 7:].replace("+", "_")

                    else:

                        number_chromosome = i[i.find("chromo=") + 7:]

                json_chromosomes = json.loads(get_ensembl_chromosomes(species_name, number_chromosome))

                length_chromosome = json_chromosomes['length']

                inf = "The chromosome " + number_chromosome + " of the species " + species_name + " has a length of: "
                chromosome = "<br>" + str(length_chromosome) + "<br>"

                contents1 = """ <head>
                                                <meta charset="utf-8">
                                                <title>chromosomeLength</title>
                                              </head>
                                              <body> """

                contents2 = """    <a href="/" >MAIN PAGE</a>
                                              </body>
                                            </html>"""

                contents = contents1 + inf + chromosome + contents2
                code = 200
                content_type = 'text/html'

            except (KeyError, IndexError, UnboundLocalError) as error:

                e = "ERROR: "
                print(e, error)
                f = open("error.html", 'r')
                code = 404
                contents = f.read()
                content_type = 'text/html'

        elif resource == "/geneSeq":

            try:

                gene = list_resource[1][list_resource[1].find("gene=") + 5:]

                json_gene = json.loads(get_ensembl_gene(gene))

                json_genesequence = json.loads(get_ensembl_genesequence(json_gene))

                genesequence = "<p style=\"word-break:break-all\"> " + str(json_genesequence['seq']) + "</p>" + "<br>"

                contents1 = """ <head>
                                                                <meta charset="utf-8">
                                                                <title>geneSeq</title>
                                                              </head>
                                                              <body> """

                contents2 = """    <a href="/" >MAIN PAGE</a>
                                                              </body>
                                                            </html>"""

                contents = contents1 + genesequence + contents2
                code = 200
                content_type = 'text/html'

            except (KeyError, IndexError, UnboundLocalError) as error:

                e = "ERROR: "
                print(e, error)
                f = open("error.html", 'r')
                code = 404
                contents = f.read()
                content_type = 'text/html'

        elif resource == "/geneInfo":

            try:

                gene = list_resource[1][list_resource[1].find("gene=") + 5:]

                json_gene = json.loads(get_ensembl_gene(gene))

                json_genesequence = json.loads(get_ensembl_genesequence(json_gene))

                info_g1 = "<br>" + "The start of the sequence: " + str(json_gene['start']) + "<br>"
                info_g2 = "<br>" + "The end of the sequence: " + str(json_gene['end']) + "<br>"
                info_g3 = "<br>" + "The length of the sequence: " + str(len(json_genesequence['seq'])) + "<br>"
                info_g4 = "<br>" + "The id of the sequence: " + str(json_gene['id']) + "<br>"
                info_g5 = "<br>" + "The chromosome of the sequence: " + str(json_gene['seq_region_name']) + "<br>"

                contents1 = """ <head>
                                                                                <meta charset="utf-8">
                                                                                <title>geneSeq</title>
                                                                              </head>
                                                                              <body> """

                contents2 = """    <a href="/" >MAIN PAGE</a>
                                                                              </body>
                                                                            </html>"""

                contents = contents1 + info_g1 + info_g2 + info_g3 + info_g4 + info_g5 + contents2
                code = 200
                content_type = 'text/html'

            except (KeyError, IndexError, UnboundLocalError) as error:

                e = "ERROR: "
                print(e, error)
                f = open("error.html", 'r')
                code = 404
                contents = f.read()
                content_type = 'text/html'

        elif resource == "/geneCalc":

            try:

                gene = list_resource[1][list_resource[1].find("gene=") + 5:]

                json_gene = json.loads(get_ensembl_gene(gene))

                json_genesequence = json.loads(get_ensembl_genesequence(json_gene))

                info_gene = information_gene(json_genesequence)

                calc = ""

                for k, v in info_gene.items():

                    contents_txt = "The " + k + " of the gene " + gene + " is: "
                    calc = calc + contents_txt + v + "<br>"

                contents1 = """ <head>
                                                                                            <meta charset="utf-8">
                                                                                            <title>geneSeq</title>
                                                                                          </head>
                                                                                          <body> """

                contents2 = """    <a href="/" >MAIN PAGE</a>
                                                                                          </body>
                                                                                        </html>"""

                contents = contents1 + calc + contents2
                code = 200
                content_type = 'text/html'

            except (KeyError, IndexError, UnboundLocalError) as error:

                e = "ERROR: "
                print(e, error)
                f = open("error.html", 'r')
                code = 404
                contents = f.read()
                content_type = 'text/html'

        elif resource == "/geneList":

            try:

                parameters = list_resource[1].split("&")

                for i in parameters:
                    if "chromo" in i:

                        chromo_name = i[i.find("chromo=") + 7:]

                    elif "start" in i:

                        start_chromo = i[i.find("start=") + 6:]

                    else:

                        end_chromo = i[i.find("end=") + 4:]

                json_genelist = json.loads(get_ensembl_genelist(chromo_name, start_chromo, end_chromo))

                info_genelist = information_genelist(json_genelist)

                genelist = ""

                for k, v in info_genelist.items():
                    print(v)
                    contents_txt = "The gene " + k + " is from in the position: " + str(v[0]) + " to " + str(v[1])

                    genelist = genelist + contents_txt + "<br>"

                contents1 = """ <head>
                                                                         <meta charset="utf-8">
                                                                         <title>geneList</title>
                                                                         </head>
                                                                                                          <body> """

                contents2 = """    <a href="/" >MAIN PAGE</a>
                                                                                                          </body>
                                                                                                        </html>"""

                contents = contents1 + genelist + contents2
                code = 200
                content_type = 'text/html'

            except (KeyError, IndexError, UnboundLocalError) as error:

                e = "ERROR: "

                print(e, error)

                f = open("error.html", 'r')

                code = 404

                contents = f.read()

                content_type = 'text/html'

        else:
            f = open("error.html", 'r')
            code = 404
            # Read the file
            contents = f.read()
            content_type = 'text/html'

        # Generating the response message
        self.send_response(code)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - FUNCTIONS
# ------------------------

# -- Here we can define special headers if needed
headers = {'User-Agent': 'http-client'}


# A FUNCTION TO GET THE LIST OF ALL SPECIES
def get_ensembl_species(ENDPOINT_1):

    conn = http.client.HTTPSConnection(HOSTNAME)

    # -- Send the request. No body (None)
    # -- Use the defined headers
    conn.request(METHOD, ENDPOINT_1 + FORMAT_1, None, headers)

    # -- Wait for the server's response
    r1 = conn.getresponse()

    # -- Print the status
    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)

    # -- Read the response's body and close
    # -- the connection
    text_json_1 = r1.read().decode("utf-8")
    conn.close()

    return text_json_1


# A function to unpack the species' information
def information_species(json_species):

    dict_species = dict()

    for index in range(len(json_species['species'])):
        dict_species[index] = json_species['species'][index]['common_name']

    return dict_species


# A function to get the karyotype of the given specie.
def get_ensembl_karyotypes(species_name):

    conn = http.client.HTTPSConnection(HOSTNAME)

    # -- Send the request. No body (None)
    # -- Use the defined headers
    conn.request(METHOD, ENDPOINT_2 + species_name + FORMAT_1, None, headers)
    print(ENDPOINT_2 + species_name + FORMAT_1)

    # -- Wait for the server's response
    r2 = conn.getresponse()

    # -- Print the status
    print()
    print("Response received: ", end='')
    print(r2.status, r2.reason)

    # -- Read the response's body and close
    # -- the connection
    text_json_2 = r2.read().decode("utf-8")
    conn.close()

    return text_json_2


# A function to unpack the species' karyotype.
def information_karyotypes(json_karyotypes):

    dict_karyotypes = dict()

    for index in range(len(json_karyotypes['karyotype'])):
        dict_karyotypes[index] = json_karyotypes['karyotype'][index]

    return dict_karyotypes


# A function to get all the chromosomes.
def get_ensembl_chromosomes(species_name, number_chromosome):

    conn = http.client.HTTPSConnection(HOSTNAME)

    # -- Send the request. No body (None)
    # -- Use the defined headers
    conn.request(METHOD, ENDPOINT_2 + species_name + "/" + number_chromosome + FORMAT_1, None, headers)
    print(ENDPOINT_2 + species_name + "/" + number_chromosome + FORMAT_1)
    # -- Wait for the server's response
    r3 = conn.getresponse()

    # -- Print the status
    print()
    print("Response received: ", end='')
    print(r3.status, r3.reason)

    # -- Read the response's body and close
    # -- the connection
    text_json_3 = r3.read().decode("utf-8")
    conn.close()

    return text_json_3


# A function to get the info about the gene.
def get_ensembl_gene(gene):

    conn = http.client.HTTPSConnection(HOSTNAME)

    # -- Send the request. No body (None)
    # -- Use the defined headers
    conn.request(METHOD, ENDPOINT_3 + gene + FORMAT_2 + FORMAT_1[1:], None, headers)
    print(ENDPOINT_3 + gene + FORMAT_2 + FORMAT_1[1:])

    # -- Wait for the server's response
    r4 = conn.getresponse()

    # -- Print the status
    print()
    print("Response received: ", end='')
    print(r4.status, r4.reason)

    # -- Read the response's body and close
    # -- the connection
    text_json_4 = r4.read().decode("utf-8")
    conn.close()

    return text_json_4


# A function to get the info about the gene's sequence.
def get_ensembl_genesequence(json_gene):

    id_gene = json_gene['id']

    conn = http.client.HTTPSConnection(HOSTNAME)

    # -- Send the request. No body (None)
    # -- Use the defined headers

    conn.request(METHOD, ENDPOINT_4 + id_gene + FORMAT_1, None, headers)
    print(ENDPOINT_4 + id_gene + FORMAT_1)

    # -- Wait for the server's response
    r5 = conn.getresponse()

    # -- Print the status
    print()
    print("Response received: ", end='')
    print(r5.status, r5.reason)

    # -- Read the response's body and close
    # -- the connection
    text_json_5 = r5.read().decode("utf-8")

    conn.close()

    return text_json_5


# A function to unpack the info about the gene.
def information_gene(json_genesequence):

    dict_infogene = dict()

    total_length = len(json_genesequence['seq'])

    aminoacids = "ACTG"

    for aa in aminoacids:

        percentage = float(json_genesequence['seq'].count(aa)/total_length) * 100

        key = "percentage of " + aa

        dict_infogene[key] = str(round(percentage, 2)) + "%"

    dict_infogene['length'] = str(total_length)

    return dict_infogene


# A function to get the list of the genes in the chromosome.
def get_ensembl_genelist(chromo_name, start_chromo, end_chromo):

    conn = http.client.HTTPSConnection(HOSTNAME)

    # -- Send the request. No body (None)
    # -- Use the defined headers
    info_endpoint = chromo_name + ':' + start_chromo + '-' + end_chromo
    conn.request(METHOD, ENDPOINT_5 + info_endpoint + FORMAT_3 + FORMAT_1[1:], None, headers)
    print(ENDPOINT_5 + info_endpoint + FORMAT_3 + FORMAT_1[1:])

    # -- Wait for the server's response
    r6 = conn.getresponse()

    # -- Print the status
    print()
    print("Response received: ", end='')
    print(r6.status, r6.reason)

    # -- Read the response's body and close
    # -- the connection
    text_json_6 = r6.read().decode("utf-8")
    conn.close()

    return text_json_6


# A function to unpack the info about the gene.
def information_genelist(json_genelist):

    dict_genelist = dict()

    print(json_genelist, "!!")
    for i in range(len(json_genelist)):
        print(json_genelist[i]['end'])
        if json_genelist[i]['feature_type'] == 'gene':
            dict_genelist[json_genelist[i]['external_name']] = [json_genelist[i]['start'], json_genelist[i]['end']]

    # print(dict_genelist)
    return dict_genelist


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler


Handler = TestHandler


# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- client, the handler is called.
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()

print("")
print("Server Stopped")
