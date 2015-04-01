#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from string import Template

from .parser import MARCXMLParser


# Classes =====================================================================
class MARCXMLSerializer(MARCXMLParser):
    """
    Class which holds all the data from parser, but contains also XML
    serialization methods.
    """
    def __init__(self, xml=None, resort=True):
        super(MARCXMLSerializer, self).__init__(xml, resort)

    def _serialize_ctl_fields(self):
        template = '<$TAGNAME $FIELD_NAME="$FIELD_ID">$CONTENT</$TAGNAME>\n'
        tagname = "controlfield" if not self.oai_marc else "fixfield"
        field_name = "tag" if not self.oai_marc else "id"

        output = ""
        for field_id in self.resorted(self.controlfields):
            # some control fields are specific for oai
            # if not self.oai_marc and field_id in ["LDR", "FMT"]:
            if not self.oai_marc and not field_id.isdigit():
                continue

            output += Template(template).substitute(
                TAGNAME=tagname,
                FIELD_NAME=field_name,
                FIELD_ID=field_id,
                CONTENT=self.controlfields[field_id]
            )

        return output

    def _serialize_data_subfields(self, subfields):
        template = '\n<$TAGNAME $FIELD_NAME="$FIELD_ID">$CONTENT</$TAGNAME>'

        tagname = "subfield"
        field_name = "code" if not self.oai_marc else "label"

        output = ""
        for field_id in self.resorted(subfields):
            for subfield in subfields[field_id]:
                output += Template(template).substitute(
                    TAGNAME=tagname,
                    FIELD_NAME=field_name,
                    FIELD_ID=field_id,
                    CONTENT=subfield
                )

        return output

    def _serialize_data_fields(self):
        template = '<$TAGNAME $FIELD_NAME="$FIELD_ID" $I1_NAME="$I1_VAL" '
        template += '$I2_NAME="$I2_VAL">'
        template += '$CONTENT\n'
        template += '</$TAGNAME>\n'

        tagname = "datafield" if not self.oai_marc else "varfield"
        field_name = "tag" if not self.oai_marc else "id"

        output = ""
        for field_id in self.resorted(self.datafields):
            # unpac dicts from array
            for dict_field in self.datafields[field_id]:
                # this allows to convert between OAI and XML formats simply
                # by switching .oai_marc property
                oai = not self.oai_marc
                real_i1_name = self.i1_name if self.i1_name in dict_field \
                                            else self.get_i_name(1, oai)
                real_i2_name = self.i2_name if self.i2_name in dict_field \
                                            else self.get_i_name(2, oai)

                i1_val = dict_field[real_i1_name]
                i2_val = dict_field[real_i2_name]

                # temporarily remove i1/i2 from dict
                del dict_field[real_i1_name]
                del dict_field[real_i2_name]

                output += Template(template).substitute(
                    TAGNAME=tagname,
                    FIELD_NAME=field_name,
                    FIELD_ID=field_id,
                    I1_NAME=self.i1_name,
                    I2_NAME=self.i2_name,
                    I1_VAL=i1_val,
                    I2_VAL=i2_val,
                    CONTENT=self._serialize_data_subfields(dict_field)
                )

                # put back temporarily removed i1/i2
                dict_field[real_i1_name] = i1_val
                dict_field[real_i2_name] = i2_val

        return output

    def to_XML(self):
        """
        Serialize object back to XML string.

        Returns:
            str: String which should be same as original input, if everything\
                 works as expected.
        """
        marcxml_template = """<record xmlns="http://www.loc.gov/MARC21/slim/"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.loc.gov/MARC21/slim
http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">
$LEADER
$CONTROL_FIELDS
$DATA_FIELDS
</record>
"""

        oai_template = """<record>
<metadata>
<oai_marc>
$LEADER$CONTROL_FIELDS
$DATA_FIELDS
</oai_marc>
</metadata>
</record>
"""

        # serialize leader, if it is present and record is marc xml
        leader = self.leader if self.leader is not None else ""
        if leader:  # print only visible leaders
            leader = "<leader>" + leader + "</leader>"

        # discard leader for oai
        if self.oai_marc:
            leader = ""

        # serialize
        xml_template = oai_template if self.oai_marc else marcxml_template
        xml_output = Template(xml_template).substitute(
            LEADER=leader.strip(),
            CONTROL_FIELDS=self._serialize_ctl_fields().strip(),
            DATA_FIELDS=self._serialize_data_fields().strip()
        )

        return xml_output

    def __str__(self):
        """
        Alias for :meth:`to_XML`.
        """
        return self.to_XML()

    def __repr__(self):
        return str(self.__dict__)
