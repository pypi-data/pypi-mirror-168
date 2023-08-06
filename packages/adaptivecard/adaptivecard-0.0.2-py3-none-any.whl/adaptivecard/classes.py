from entities.mixin import Mixin
from typing import Union, List


class Content:
    """Content é o elemento que recebe o AdaptiveCard e é adicionado à lista atachments, atributo de Message"""
    def __init__(self, content: "AdaptiveCard"):
        self.contentType = "application/vnd.microsoft.card.adaptive"
        self.content = content

class Message(Mixin):
    """"Estrutura final do card tal como se requer para envio a um canal do Teams"""
    def __init__(self, attachments: Union[None, List["Content"]] = None):
        self.type = "message"
        if attachments == None:
            attachments = []
        self.attachments = attachments

    def attach(self, content):
        self.attachments.append(content)

#-------------------------Cards-------------------------#

class AdaptiveCard(Mixin):
    """O template principal do card"""  # Essas descrições hão de ficar mais detalhadas à medida que eu desenvolver a lib e sua documentação
    def __init__(self, type: str = "AdaptiveCard", version = "1.2", schema: str = "http://adaptivecards.io/schemas/adaptive-card.json", body: Union[None, List[Union["ColumnSet", "Container", "TextBlock", "Image"]]] = None, falbackText: Union[None, str] = None, backgroundImage = None, minHeight = None, rtl = None, speak = None, lang = None, verticalContentAlignment = None):
        self.type = type
        self.version = version
        super().set_version(self.version)
        self.schema = schema

        if body == None:
            body = []

        self.body = body
        super().create_fields(locals())

    def add_to_body(self, card_element):
        self.body.append(card_element)

#---------------------Containers-------------------------#

class Container(Mixin):
    """Um contâiner é um agrupamento de elementos"""
    def __init__(self, items = None, style: Union[None, str] = None, verticalContentAlignment: Union[None, str] = None, bleed: Union[None, bool] = None, minHeight: Union[None, str] = None, rtl: Union[None, bool] = None):
        self.type = "Container"

        if items == None:
            items = []
        self.items = items

        super().create_fields(locals())

    def add_to_items(self, card_element):
        self.items.append(card_element)

class ColumnSet(Mixin):
    """ColumnSet define um grupo de colunas"""
    def __init__(self, columns: Union[None, List["Column"]] = None, style: Union[None, str] = None, bleed: Union[None, bool] = None,
                 minHeight: Union[None, str] = None, horizontalAlignment: Union[None, str] = None):
        self.type = "ColumnSet"
        if columns is None:
            columns = []
        self.columns = columns

        super().create_fields(locals())

    def add_to_columns(self, column_element):
        self.columns.append(column_element)

class Column(Mixin):
    """O contâiner Column define um elemento de coluna, que é parte de um ColumnSet."""
    def __init__(self, items: Union[None, List[Union["Image", "TextBlock"]]] = None, backgroundImage = None, bleed: Union[None, bool] = None, fallback = None,
                 minHeight: Union[None, str] = None, rtl: Union[None, bool] = None, separator: Union[None, bool] = None,
                 spacing: Union[None, str, int] = None, style: Union[None, str] = None, verticalContentAlignment: Union[None, str] = None,
                 width: Union[None, str, int] = None, id: Union[None, str] = None, isVisible: Union[None, bool] = None):
        self.type = "Column"
        if items is None:
            items = []

        super().create_fields(locals())

    def add_to_items(self, card_element):
        self.items.append(card_element)

class Table(Mixin):
    def __init__(self, columns: Union[None, List[dict]], rows: Union[None, List[dict]], firstRowAsHeader: Union[None, bool], showGridLines: Union[None, bool],
    gridStyle: Union[None, str], horizontalCellContentAlignment = Union[None, str], verticalCellContentAlignment: Union[None, str] = None,
    fallback: Union[None, "ColumnSet", "Container", "Image", "Table"] = None, height: Union[None, str] = None, separator: Union[None, bool] = None,
    spacing: Union[None, str] = None, id: Union[None, str] = None, isVisible = Union[None, bool]):
        self.type = "Table"

class TableCell(Mixin):
    def __init__(self, items: Union[None, "ColumnSet", "Container", "Image", "Table"] = None, selectAction: None = None, style: Union[None, str] = None,
    verticalContentAlignment: Union[None, str] = None, bleed: Union[None, bool] = None, backgroundImage: Union[None, str] = None,
    minHeight: Union[None, str] = None, rtl: Union[None, bool] = None):
        pass
#-------------------------Card Elements---------------------------#

class TextBlock(Mixin):
    """Elemento de texto"""
    def __init__(self, text: str = "", color: Union[None, str] = None, fontType: Union[None, str] = None, horizontalAlignment: Union[None, str] = None,
                isSubtle: Union[None, bool] = None, maxLines: Union[None, int] = None, size: Union[None, str] = None, weight: Union[None, str] = None,
                wrap: Union[None, bool] = None, style: Union[None, str] = None, fallback: Union[None, str, ColumnSet, "Container", "TextBlock"] = None, height: Union[None, str] = None,
                separator: Union[None, bool] = None, spacing: Union[None, str] = None, id: Union[None, str] = None, isVisible: Union[None, bool] = None):
        self.type = "TextBlock"
        self.text = text
        super().create_fields(locals())
    def update_text(self, text):
        self.text = text

class Image(Mixin):
    def __init__(self, url: str, altText: Union[None, str] = None, backgroundColor: Union[None, str] = None, height: Union[None, str] = None, horizontalAlignment: Union[None, str] = None, selectAction: Union[None, str] = None):
        self.type = "Image"
        super().create_fields(locals())
    