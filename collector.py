# Collects all the votings from the Camara's website and exports the data to two
# csv files. The first one contains all the propositions:
#
# id, type, number, year, keywords, abstract
#
# The second one contains the votes of entities:
#
# name [(proposition id, session id, vote)]
#
# Where name is the name of a politician or party and only presential votes are
# collected (non-attendance is ignored).

import urllib
import xml.etree.ElementTree as ET

# If the candidate is not present, no vote is recorded.
# Possible votes:
#  yes = 1
#  no = 2
#  neutral = 3
#  obstruct = 4 # when the candidate refuses to vote to obey superior orders (chicken :P)

class Proposition:
  ptype = ""
  pid = -1
  number = -1
  year = -1
  keywords = ""
  abstract = ""

def collect():
  base_url = "http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/"

  print "========> Starting data collection"

  # Get all ids of propositions which were voted from 1990 until 2014
  prop_ids = []
  service_url = "ListarProposicoesVotadasEmPlenario?"
  # TODO: change 1992 to 2015. Leaving for quick testing
  for i in range(1991, 1992):
    query = "ano=" + str(i) + "&tipo="
    url = base_url + service_url + query
    response = urllib.urlopen(url)
    if response.getcode() == 200:
      root = ET.fromstring(response.read())
      for cod_prop in root.iter('codProposicao'):
	prop_ids.append(int(cod_prop.text))
    else:
      print "ERROR: could not get data for " + url
      print response.read()
    response.close()
  
  print "========> Collected all propositions' ids"

  # Get the information for each proposition
  # TODO: export to a csv file
  propositions = []
  service_url = "ObterProposicaoPorID?"
  for prop_id in prop_ids:
    query = "IdProp=" + str(prop_id)
    url = base_url + service_url + query
    response = urllib.urlopen(url)
    if response.getcode() == 200:
      root = ET.fromstring(response.read())
      prop = Proposition()
      prop.ptype = root.attrib['tipo'] 
      prop.pid = prop_id
      prop.number = root.attrib['numero']
      prop.year = root.attrib['ano']
      prop.keywords = root.find('tema').text # Use 'Indexacao' perhaps... 
      prop.abstract = root.find('Ementa').text
      propositions.append(prop)
    else:
      print "ERROR: could not get data for proposition " + str(prop_id)
      print response.read()
  
  print "========> Collected all propositions' information"

  # For each proposition, get the voting sessions
  voters = dict() # holds persons and parties
  service_url = "ObterVotacaoProposicao?"
  for prop in propositions:
    query = "tipo=" + prop.ptype + "&numero=" + prop.number + "&ano=" + prop.year
    url = base_url + service_url + query
    response = urllib.urlopen(url)
    if response.getcode() == 200:
       root = ET.fromstring(response.read())
       for voting in root.iter('Votacao'):
	  # TODO: process voting
    else:
      print "ERROR: could not get voting for proposition " + str(prop.pid)
      print response.read()


collect()
