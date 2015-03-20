#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import dhtmlparser


# Variables ===================================================================
XML = """
    <datafield tag="015" ind1=" " ind2=" ">
    <subfield code="a">cnb001492461</subfield>
    </datafield>
    <datafield tag="020" ind1=" " ind2=" ">
    <subfield code="a">80-251-0225-4 (brož.) :</subfield>
    <subfield code="c">Kč 590,00</subfield>
    </datafield>
    <datafield tag="035" ind1=" " ind2=" ">
    <subfield code="a">(OCoLC)85131856</subfield>
    </datafield>
    <datafield tag="040" ind1=" " ind2=" ">
    <subfield code="a">BOA001</subfield>
    <subfield code="b">cze</subfield>
    <subfield code="d">ABA001</subfield>
    </datafield>
    <datafield tag="041" ind1="1" ind2=" ">
    <subfield code="a">cze</subfield>
    <subfield code="h">eng</subfield>
    </datafield>
    <datafield tag="072" ind1=" " ind2="7">
    <subfield code="a">004.4/.6</subfield>
    <subfield code="x">Programování. Software</subfield>
    <subfield code="2">Konspekt</subfield>
    <subfield code="9">23</subfield>
    </datafield>
    <datafield tag="080" ind1=" " ind2=" ">
    <subfield code="a">004.451.9Unix</subfield>
    <subfield code="2">MRF</subfield>
    </datafield>
    <datafield tag="080" ind1=" " ind2=" ">
    <subfield code="a">004.451</subfield>
    <subfield code="2">MRF</subfield>
    </datafield>
    <datafield tag="080" ind1=" " ind2=" ">
    <subfield code="a">004.42</subfield>
    <subfield code="2">MRF</subfield>
    </datafield>
    <datafield tag="080" ind1=" " ind2=" ">
    <subfield code="a">(035)</subfield>
    <subfield code="2">MRF</subfield>
    </datafield>
    <datafield tag="100" ind1="1" ind2=" ">
    <subfield code="a">Raymond, Eric S.</subfield>
    <subfield code="7">jn20020721375</subfield>
    <subfield code="4">aut</subfield>
    </datafield>
    <datafield tag="245" ind1="1" ind2="0">
    <subfield code="a">Umění programování v UNIXu /</subfield>
    <subfield code="c">Eric S. Raymond</subfield>
    </datafield>
    <datafield tag="250" ind1=" " ind2=" ">
    <subfield code="a">Vyd. 1.</subfield>
    </datafield>
    <datafield tag="260" ind1=" " ind2=" ">
    <subfield code="a">Brno :</subfield>
    <subfield code="b">Computer Press,</subfield>
    <subfield code="c">2004</subfield>
    </datafield>
    <datafield tag="300" ind1=" " ind2=" ">
    <subfield code="a">509 s. :</subfield>
    <subfield code="b">il. ;</subfield>
    <subfield code="c">23 cm</subfield>
    </datafield>
    <datafield tag="500" ind1=" " ind2=" ">
    <subfield code="a">Glosář</subfield>
    </datafield>
    <datafield tag="504" ind1=" " ind2=" ">
    <subfield code="a">Obsahuje bibliografii, bibliografické odkazy a rejstřík</subfield>
    </datafield>
    <datafield tag="546" ind1=" " ind2=" ">
    <subfield code="a">Přeloženo z angličtiny</subfield>
    </datafield>
    <datafield tag="650" ind1="0" ind2="7">
    <subfield code="a">UNIX</subfield>
    <subfield code="7">ph117153</subfield>
    <subfield code="2">czenas</subfield>
    </datafield>
    <datafield tag="650" ind1="0" ind2="7">
    <subfield code="a">operační systémy</subfield>
    <subfield code="7">ph115593</subfield>
    <subfield code="2">czenas</subfield>
    </datafield>
    <datafield tag="650" ind1="0" ind2="7">
    <subfield code="a">programování</subfield>
    <subfield code="7">ph115891</subfield>
    <subfield code="2">czenas</subfield>
    </datafield>
    <datafield tag="650" ind1="0" ind2="9">
    <subfield code="a">UNIX</subfield>
    <subfield code="2">eczenas</subfield>
    </datafield>
    <datafield tag="650" ind1="0" ind2="9">
    <subfield code="a">operating systems</subfield>
    <subfield code="2">eczenas</subfield>
    </datafield>
    <datafield tag="650" ind1="0" ind2="9">
    <subfield code="a">programming</subfield>
    <subfield code="2">eczenas</subfield>
    </datafield>
    <datafield tag="655" ind1=" " ind2="7">
    <subfield code="a">příručky</subfield>
    <subfield code="7">fd133209</subfield>
    <subfield code="2">czenas</subfield>
    </datafield>
    <datafield tag="655" ind1=" " ind2="9">
    <subfield code="a">handbooks, manuals, etc.</subfield>
    <subfield code="2">eczenas</subfield>
    </datafield>
    <datafield tag="765" ind1="0" ind2=" ">
    <subfield code="t">Art of UNIX programming</subfield>
    <subfield code="9">Česky</subfield>
    </datafield>
    <datafield tag="901" ind1=" " ind2=" ">
    <subfield code="b">9788025102251</subfield>
    <subfield code="f">1. vyd.</subfield>
    <subfield code="o">20050217</subfield>
    </datafield>
    <datafield tag="910" ind1="1" ind2=" ">
    <subfield code="a">ABA001</subfield>
    </datafield>
"""


# Functions & classes =========================================================
def process_datafield(datafield):
    out = ""

    num = datafield.params["tag"]
    ind1 = datafield.params["ind1"]
    ind2 = datafield.params["ind2"]

    last = None
    last_code = None
    for tag in datafield.find("subfield"):
        code = tag.params["code"]
        content = tag.getContent()

        out += 'assert record.getDataRecords("%s", "%s")[0] == "%s"\n' % (
            num,
            code,
            content
        )
        last = tag
        last_code = code

    out += 'ind_test = record.getDataRecords("%s", "%s")[-1]\n' % (
        num,
        last_code
    )
    out += 'assert ind_test.getI1() == "%s"\n' % ind1
    out += 'assert ind_test.getI2() == "%s"\n' % ind2
    out += "\n"

    return out


def process_datafields(datafiled_tags):
    out = ""

    for field_tag in datafiled_tags:
        out += process_datafield(field_tag)

    return out


# Main program ================================================================
if __name__ == '__main__':
    dom = dhtmlparser.parseString(XML)

    print process_datafields(dom.find("datafield"))
