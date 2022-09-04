from bs4 import BeautifulSoup
import json
import requests
from datetime import datetime
from time import sleep

from purelogic_parse import collect_purelogic
from daxtroine_parse import collect_darxtron
from cnc_tehn_parse import collect_cnc
from x_3ddiy_parse import collect_3ddiy
from duxe_parse import collect_duxe


if __name__ == '__main__':
    collect_3ddiy()
    collect_cnc()
    collect_darxtron()
    collect_purelogic()
    collect_duxe()
