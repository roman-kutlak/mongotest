import os

from mongoengine import Document, StringField, connect, EmbeddedDocument, EmbeddedDocumentField


class Address(EmbeddedDocument):
    street1 = StringField()
    street2 = StringField()
    town = StringField()
    postcode = StringField()


class Person(Document):
    name = StringField(max_length=256, regex=r'^[A-Za-z].+')
    address = EmbeddedDocumentField(Address)

    def __repr__(self):
        return f'<Person ({self.id}): {self.name}>'


def main(connection_str):
    connect('test', host=connection_str)
    print(Person.objects.all())
    roman = Person(name='Roman', address=Address(town='Oxford'))
    roman.save()
    print(roman.id)
    print(Person.objects.filter(address__town='Oxford'))
    roman.delete()


if __name__ == '__main__':
    host = os.environ['MONGO_HOST']
    username = os.environ['MONGO_USERNAME']
    password = os.environ['MONGO_PASSWORD']
    main(f'mongodb+srv://{username}:{password}@{host}/?retryWrites=true')
