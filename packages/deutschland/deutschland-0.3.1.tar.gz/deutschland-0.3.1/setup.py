# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['deutschland',
 'deutschland.bundesanzeiger',
 'deutschland.bundesnetzagentur',
 'deutschland.bundeswahlleiter',
 'deutschland.destatis',
 'deutschland.destatis.api',
 'deutschland.destatis.apis',
 'deutschland.destatis.model',
 'deutschland.destatis.models',
 'deutschland.handelsregister',
 'deutschland.lebensmittelwarnung',
 'deutschland.presseportal',
 'deutschland.verena']

package_data = \
{'': ['*'], 'deutschland.bundesanzeiger': ['assets/*']}

install_requires = \
['Pillow>=8.3.1,<9.0.0',
 'Shapely>=1.8.0,<2.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'boto3>=1.18.9,<2.0.0',
 'dateparser>=1.0.0,<2.0.0',
 'de-autobahn>=1.0.4,<2.0.0',
 'de-bundesrat>=0.1.0,<0.2.0',
 'de-bundestag>=0.1.0,<0.2.0',
 'de-dwd>=1.0.1,<2.0.0',
 'de-interpol>=0.1.0,<0.2.0',
 'de-jobsuche>=0.1.0,<0.2.0',
 'de-ladestationen>=1.0.5,<2.0.0',
 'de-mudab>=0.1.0,<0.2.0',
 'de-nina>=1.0.1,<2.0.0',
 'de-polizei-brandenburg>=0.1.0,<0.2.0',
 'de-risikogebiete>=0.1.0,<0.2.0',
 'de-smard>=0.1.0,<0.2.0',
 'de-strahlenschutz>=1.0.0,<2.0.0',
 'de-travelwarning>=0.1.0,<0.2.0',
 'de-zoll>=0.1.0,<0.2.0',
 'gql>=2.0.0,<3.0.0',
 'lxml>=4.6.3,<5.0.0',
 'mapbox-vector-tile>=1.2.1,<2.0.0',
 'more-itertools>=8.10.0,<9.0.0',
 'numpy>=1.19.0,<2.0.0',
 'onnxruntime>=1.10.0,<2.0.0',
 'pandas>=1.1.5,<2.0.0',
 'protobuf>=3.0,<4.0',
 'pypresseportal>=0.1,<0.2',
 'requests>=2.26.0,<3.0.0',
 'slugify>=0.0.1,<0.0.2']

extras_require = \
{'abfallnavi': ['de-abfallnavi>=0.1.0,<0.2.0'],
 'all': ['de-ausbildungssuche>=0.1.0,<0.2.0',
         'de-berufssprachkurssuche>=0.1.0,<0.2.0',
         'de-bundestag-lobbyregister>=0.1.0,<0.2.0',
         'de-coachingangebote>=0.1.0,<0.2.0',
         'de-dip-bundestag>=0.1.0,<0.2.0',
         'de-dip-bundestag>=0.1.0,<0.2.0',
         'de-entgeltatlas>=0.1.0,<0.2.0',
         'de-hochwasserzentralen>=0.1.0,<0.2.0',
         'de-pegel-online>=0.1.0,<0.2.0',
         'de-pflanzenschutzmittelzulassung>=0.1.0,<0.2.0',
         'de-studiensuche>=0.1.0,<0.2.0',
         'de-tagesschau>=0.1.0,<0.2.0',
         'de-weiterbildungssuche>=0.1.0,<0.2.0',
         'de-feiertage>=1.0.1,<2.0.0',
         'de-marktstammdaten>=0.1.0,<0.2.0',
         'de-vag>=0.1.0,<0.2.0',
         'de-abfallnavi>=0.1.0,<0.2.0',
         'de-bundeshaushalt>=1.0.0,<2.0.0',
         'de-ecovisio>=0.1.0,<0.2.0',
         'de-dashboarddeutschland>=0.1.0,<0.2.0'],
 'ausbildungssuche': ['de-ausbildungssuche>=0.1.0,<0.2.0'],
 'berufssprachkurssuche': ['de-berufssprachkurssuche>=0.1.0,<0.2.0'],
 'bundeshaushalt': ['de-bundeshaushalt>=1.0.0,<2.0.0'],
 'bundestag_lobbyregister': ['de-bundestag-lobbyregister>=0.1.0,<0.2.0'],
 'coachingangebote': ['de-coachingangebote>=0.1.0,<0.2.0'],
 'dashboarddeutschland': ['de-dashboarddeutschland>=0.1.0,<0.2.0'],
 'dip_bundestag': ['de-dip-bundestag>=0.1.0,<0.2.0'],
 'ecovisio': ['de-ecovisio>=0.1.0,<0.2.0'],
 'entgeltatlas': ['de-entgeltatlas>=0.1.0,<0.2.0'],
 'feiertage': ['de-feiertage>=1.0.1,<2.0.0'],
 'hochwasserzentralen': ['de-hochwasserzentralen>=0.1.0,<0.2.0'],
 'marktstammdaten': ['de-marktstammdaten>=0.1.0,<0.2.0'],
 'pegel_online': ['de-pegel-online>=0.1.0,<0.2.0'],
 'pflanzenschutzmittelzulassung': ['de-pflanzenschutzmittelzulassung>=0.1.0,<0.2.0'],
 'studiensuche': ['de-studiensuche>=0.1.0,<0.2.0'],
 'tagesschau': ['de-tagesschau>=0.1.0,<0.2.0'],
 'vag': ['de-vag>=0.1.0,<0.2.0'],
 'weiterbildungssuche': ['de-weiterbildungssuche>=0.1.0,<0.2.0']}

setup_kwargs = {
    'name': 'deutschland',
    'version': '0.3.1',
    'description': '',
    'long_description': '[![PyPI version deutschland](https://badge.fury.io/py/deutschland.svg)](https://pypi.python.org/pypi/deutschland/)\n[![GitHub license](https://img.shields.io/github/license/bundesAPI/deutschland.svg)](https://github.com/bundesAPI/deutschland/blob/main/LICENSE)\n\n[![Lint](https://github.com/bundesAPI/deutschland/actions/workflows/black.yml/badge.svg?branch=main)](https://github.com/bundesAPI/deutschland/actions/workflows/black.yml)\n[![Publish Python 🐍 distributions 📦 to PyPI and TestPyPI](https://github.com/bundesAPI/deutschland/actions/workflows/publish.yml/badge.svg?branch=main)](https://github.com/bundesAPI/deutschland/actions/workflows/publish.yml)\n[![Run Python 🐍 tests](https://github.com/bundesAPI/deutschland/actions/workflows/runtests.yml/badge.svg?branch=main)](https://github.com/bundesAPI/deutschland/actions/workflows/runtests.yml)\n\n# Deutschland\nA python package that gives you easy access to the most valuable datasets of Germany.\n\n## Installation\n```bash\npip install deutschland\n```\n\n### Development\nFor development poetry version `>=1.2.0` is required.\n\n## Geographic data\nFetch information about streets, house numbers, building outlines, …\n\n```python\nfrom deutschland.geo import Geo\ngeo = Geo()\n# top_right and bottom_left coordinates\ndata = geo.fetch([52.530116236589244, 13.426532801586827],\n                 [52.50876180448243, 13.359631043007212])\nprint(data.keys())\n# dict_keys([\'Adresse\', \'Barrierenlinie\', \'Bauwerksflaeche\', \'Bauwerkslinie\', \'Bauwerkspunkt\', \'Besondere_Flaeche\', \'Besondere_Linie\', \'Besonderer_Punkt\', \'Gebaeudeflaeche\', \'Gebaeudepunkt\', \'Gewaesserflaeche\', \'Gewaesserlinie\', \'Grenze_Linie\', \'Historischer_Punkt\', \'Siedlungsflaeche\', \'Vegetationslinie\', \'Verkehrsflaeche\', \'Verkehrslinie\', \'Verkehrspunkt\', \'Hintergrund\'])\n\nprint(data["Adresse"][0])\n# {\'geometry\': {\'type\': \'Point\', \'coordinates\': (13.422642946243286, 52.51500157651358)}, \'properties\': {\'postleitzahl\': \'10179\', \'ort\': \'Berlin\', \'ortsteil\': \'Mitte\', \'strasse\': \'Holzmarktstraße\', \'hausnummer\': \'55\'}, \'id\': 0, \'type\': \'Feature\'}\n```\nThe data is provided by the [AdV SmartMapping](https://adv-smart.de/index_en.html). The team consists of participants from the German state surveying offices, the Federal Agency for Cartography and Geodesy (BKG), the German Federal Armed Forces (Bundeswehr ZGeoBW) and third parties from research and education.\n\n\n\n## Company Data\n\n### Bundesanzeiger\nGet financial reports for all german companies that are reporting to Bundesanzeiger.\n\n```python\nfrom deutschland.bundesanzeiger import Bundesanzeiger\nba = Bundesanzeiger()\n# search term\ndata = ba.get_reports("Deutsche Bahn AG")\n# returns a dictionary with all reports found as fulltext reports\nprint(data.keys())\n# dict_keys([\'Jahresabschluss zum Geschäftsjahr vom 01.01.2020 bis zum 31.12.2020\', \'Konzernabschluss zum Geschäftsjahr vom 01.01.2020 bis zum 31.12.2020\\nErgänzung der Veröffentlichung vom 04.06.2021\',\n```\n*Big thanks to Nico Duldhardt and Friedrich Schöne, who [supported this implementation with their machine learning model](https://av.tib.eu/media/52366).*\n\n### Handelsregister\nFetch general company information about any company in the Handelsregister.\n\n```python\nfrom deutschland.handelsregister import Handelsregister\nhr = Handelsregister()\n# search by keywords, see documentation for all available params\nhr.search(keywords="Deutsche Bahn Aktiengesellschaft")\nprint(hr)\n```\n\n\n## Consumer Protection Data\n\n### Lebensmittelwarnung\nGet current product warnings provided by the german federal portal lebensmittelwarnung.de.\n\n```python\nfrom deutschland.lebensmittelwarnung import Lebensmittelwarnung\nlw = Lebensmittelwarnung()\n# search by content type and region, see documetation for all available params\ndata = lw.get("lebensmittel", "berlin")\nprint(data)\n# [{\'id\': 19601, \'guid\': \'https://www.lebensmittelwarnung.de/bvl-lmw-de/detail/lebensmittel/19601\', \'pubDate\': \'Fri, 10 Feb 2017 12:28:45 +0000\', \'imgSrc\': \'https://www.lebensmittelwarnung.de/bvl-lmw-de/opensaga/attachment/979f8cd3-969e-4a6c-9a8e-4bdd61586cd4/data.jpg\', \'title\': \'Sidroga Bio Säuglings- und Kindertee\', \'manufacturer\': \'Lebensmittel\', \'warning\': \'Pyrrolizidinalkaloide\', \'affectedStates\': [\'Baden-Württemberg\', \'...\']}]\n```\n\n## Federal Job Openings\n\n### NRW\n\n#### VERENA\nGet open substitute teaching positions in NRW from https://www.schulministerium.nrw.de/BiPo/Verena/angebote\n```python\nfrom deutschland.verena import Verena\nv = Verena()\ndata = v.get()\nprint(data)\n# a full example data can be found at deutschland/verena/example.md\n# [{ "school_id": "99999", "desc": "Eine Schule\\nSchule der Sekundarstufe II\\ndes Landkreis Schuling\\n9999 Schulingen", "replacement_job_title": "Lehrkraft", "subjects": [ "Fach 1", "Fach 2" ], "comments": "Bemerkung zur Stelle: Testbemerkung", "duration": "01.01.2021 - 01.01.2022", ...} ...]\n```\n\n## Autobahn\n\nGet data from the Autobahn.\n\n```python\nfrom deutschland import autobahn\nfrom deutschland.autobahn.api import default_api\n\nfrom pprint import pprint\n\nautobahn_api_instance = default_api.DefaultApi()\n\ntry:\n    # Auflistung aller Autobahnen\n    api_response = autobahn_api_instance.list_autobahnen()\n    pprint(api_response)\n\n    # Details zu einer Ladestation\n    station_id = "RUxFQ1RSSUNfQ0hBUkdJTkdfU1RBVElPTl9fMTczMzM="  # str |\n    api_response = autobahn_api_instance.get_charging_station(station_id)\n    pprint(api_response)\n\nexcept autobahn.ApiException as e:\n    print("Exception when calling DefaultApi->get_charging_station: %s\\n" % e)\n```\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/autobahn/README.md)\n\n\n## Presseportal\n\nFor further information see: https://github.com/tcmetzger/pypresseportal\n\n```python\nfrom deutschland.presseportal import PresseportalApi\n\npresseportal = PresseportalApi("YOUR_KEY_HERE")\n\nstories = presseportal.get_stories()\n```\n\n## Auto-Generated API-Clients\n\n### bundesrat\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/bundesrat/README.md)\n### bundestag\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/bundestag/README.md)\n### destatis\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/destatis/README.md)\n### dwd\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/dwd/README.md)\n### interpol\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/interpol/README.md)\n### jobsuche\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/jobsuche/README.md)\n### ladestationen\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/ladestationen/README.md)\n### mudab\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/mudab/README.md)\n### nina\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/nina/README.md)\n### polizei_brandenburg\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/polizei_brandenburg/README.md)\n### risikogebiete\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/risikogebiete/README.md)\n### smard\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/smard/README.md)\n### strahlenschutz\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/strahlenschutz/README.md)\n### travelwarning\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/travelwarning/README.md)\n### zoll\nFor the detailed documentation of this API see [here](https://github.com/bundesAPI/deutschland/blob/main/docs/zoll/README.md)\n',
    'author': 'Lilith Wittmann',
    'author_email': 'mail@lilithwittmann.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bundesAPI/deutschland',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
