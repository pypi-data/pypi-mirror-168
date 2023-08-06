#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# A module to access data from the DFG-funded SPP Computational Literary Studies
#
# Usage:
#   import dracor
#   dracor.plays("shake")
#
# Author: rja
#
# Changes:
# 2022-09-20 (rja)
# - changed scene naming
# 2022-09-14 (rja)
# - initial version

from urllib import request
import json
import xml.etree.ElementTree as ET

DRACOR_API = "https://dracor.org/api"                # API endpoint for DraCor
NS = {"tei" : "http://www.tei-c.org/ns/1.0"}         # TEI/XML namespace


def corpora():
    """Download list of corpora."""
    url = DRACOR_API + "/corpora"                    # base URL
    with request.urlopen(url) as req:                # download data
        data = json.loads(req.read().decode())       # parse data
        return [d["name"] for d in data]             # extract corpora


def plays(corpus):
    """Download list of plays for corpus."""
    url = DRACOR_API + "/corpora/" + corpus          # base URL
    with request.urlopen(url) as req:                # download data
        plays = json.loads(req.read().decode())      # parse data
        return [d["name"] for d in plays["dramas"]]  # extract plays


def play(corpus, play):
    """Download play as TEI/XML and return xml object."""
    url = DRACOR_API + "/corpora/" + corpus          # base URL
    url = url + "/play/" + play + "/tei"             # URL for play data
    with request.urlopen(url) as req:                # download data
        return ET.fromstring(req.read().decode())    # extract play data


def _speakers(scene):
    """Return all speakers from the given scene."""
    return set([sp.attrib["who"] for sp in scene.findall("tei:sp", NS)])


def scenes(play):
    """Return all scenes of the play with their speakers."""
    scenes = dict()
    for actid, act in enumerate(play.find("tei:text", NS).find("tei:body", NS)):    # loop acts
        if act.attrib["type"] == "act":
            for sceneid, scene in enumerate(act.findall("tei:div", NS)):            # loop scenes
                if scene.attrib["type"] == "scene":
                    scenes[str(actid) + "/" + str(sceneid)] = _speakers(scene)
    return scenes


if __name__ == '__main__':
    pass
