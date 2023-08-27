from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    ListField,
    DateTimeField,
    CASCADE,
    EmbeddedDocument,
    EmbeddedDocumentField,
)


class Authors(Document):
    fullname = StringField(required=True, max_length=255, unique=True)
    born_date = DateTimeField()
    born_location = StringField(max_length=255)
    biography = StringField()


class Tag(EmbeddedDocument):
    name = StringField()


class Quotes(Document):
    tags = ListField(EmbeddedDocumentField(Tag))
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    quote = StringField(min_length=3)
