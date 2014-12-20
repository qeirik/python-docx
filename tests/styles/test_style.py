# encoding: utf-8

"""
Test suite for the docx.styles.style module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.enum.style import WD_STYLE_TYPE
from docx.styles.style import (
    BaseStyle, _CharacterStyle, _ParagraphStyle, _NumberingStyle,
    StyleFactory, _TableStyle
)

from ..unitutil.cxml import element, xml
from ..unitutil.mock import class_mock, instance_mock


class DescribeStyleFactory(object):

    def it_constructs_the_right_type_of_style(self, factory_fixture):
        style_elm, StyleCls_, style_ = factory_fixture
        style = StyleFactory(style_elm)
        StyleCls_.assert_called_once_with(style_elm)
        assert style is style_

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=['paragraph', 'character', 'table', 'numbering'])
    def factory_fixture(
            self, request, paragraph_style_, _ParagraphStyle_,
            character_style_, _CharacterStyle_, table_style_, _TableStyle_,
            numbering_style_, _NumberingStyle_):
        type_attr_val = request.param
        StyleCls_, style_mock = {
            'paragraph': (_ParagraphStyle_, paragraph_style_),
            'character': (_CharacterStyle_, character_style_),
            'table':     (_TableStyle_,     table_style_),
            'numbering': (_NumberingStyle_, numbering_style_),
        }[request.param]
        style_cxml = 'w:style{w:type=%s}' % type_attr_val
        style_elm = element(style_cxml)
        return style_elm, StyleCls_, style_mock

    # fixture components -----------------------------------

    @pytest.fixture
    def _ParagraphStyle_(self, request, paragraph_style_):
        return class_mock(
            request, 'docx.styles.style._ParagraphStyle',
            return_value=paragraph_style_
        )

    @pytest.fixture
    def paragraph_style_(self, request):
        return instance_mock(request, _ParagraphStyle)

    @pytest.fixture
    def _CharacterStyle_(self, request, character_style_):
        return class_mock(
            request, 'docx.styles.style._CharacterStyle',
            return_value=character_style_
        )

    @pytest.fixture
    def character_style_(self, request):
        return instance_mock(request, _CharacterStyle)

    @pytest.fixture
    def _TableStyle_(self, request, table_style_):
        return class_mock(
            request, 'docx.styles.style._TableStyle',
            return_value=table_style_
        )

    @pytest.fixture
    def table_style_(self, request):
        return instance_mock(request, _TableStyle)

    @pytest.fixture
    def _NumberingStyle_(self, request, numbering_style_):
        return class_mock(
            request, 'docx.styles.style._NumberingStyle',
            return_value=numbering_style_
        )

    @pytest.fixture
    def numbering_style_(self, request):
        return instance_mock(request, _NumberingStyle)


class DescribeBaseStyle(object):

    def it_knows_its_style_id(self, id_get_fixture):
        style, expected_value = id_get_fixture
        assert style.style_id == expected_value

    def it_can_change_its_style_id(self, id_set_fixture):
        style, new_value, expected_xml = id_set_fixture
        style.style_id = new_value
        assert style._element.xml == expected_xml

    def it_knows_its_type(self, type_get_fixture):
        style, expected_value = type_get_fixture
        assert style.type == expected_value

    def it_knows_its_name(self, name_get_fixture):
        style, expected_value = name_get_fixture
        assert style.name == expected_value

    # fixture --------------------------------------------------------

    @pytest.fixture(params=[
        ('w:style',                   None),
        ('w:style{w:styleId=Foobar}', 'Foobar'),
    ])
    def id_get_fixture(self, request):
        style_cxml, expected_value = request.param
        style = BaseStyle(element(style_cxml))
        return style, expected_value

    @pytest.fixture(params=[
        ('w:style',                'Foo', 'w:style{w:styleId=Foo}'),
        ('w:style{w:styleId=Foo}', 'Bar', 'w:style{w:styleId=Bar}'),
        ('w:style{w:styleId=Bar}', None,  'w:style'),
        ('w:style',                None,  'w:style'),
    ])
    def id_set_fixture(self, request):
        style_cxml, new_value, expected_style_cxml = request.param
        style = BaseStyle(element(style_cxml))
        expected_xml = xml(expected_style_cxml)
        return style, new_value, expected_xml

    @pytest.fixture(params=[
        ('w:style{w:type=table}',                      None),
        ('w:style{w:type=table}/w:name{w:val=Boofar}', 'Boofar'),
    ])
    def name_get_fixture(self, request):
        style_cxml, expected_value = request.param
        style = BaseStyle(element(style_cxml))
        return style, expected_value

    @pytest.fixture(params=[
        ('w:style',                   WD_STYLE_TYPE.PARAGRAPH),
        ('w:style{w:type=paragraph}', WD_STYLE_TYPE.PARAGRAPH),
        ('w:style{w:type=character}', WD_STYLE_TYPE.CHARACTER),
        ('w:style{w:type=numbering}', WD_STYLE_TYPE.LIST),
    ])
    def type_get_fixture(self, request):
        style_cxml, expected_value = request.param
        style = BaseStyle(element(style_cxml))
        return style, expected_value
