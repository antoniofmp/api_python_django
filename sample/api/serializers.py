from rest_framework import serializers
from . models import DNASequence

class DNASerializerSequence(serializers.HyperlinkedModelSerializer):
    """Class that defines a serializer for the model DNASequence.
    This serializer exposes the 'sequence' field.
    """

    class Meta:
        model = DNASequence
        fields = ['sequence']

class DNASerializerId(serializers.HyperlinkedModelSerializer):
    """Class that defines a serializer for the model DNASequence.
    This serializer exposes the 'id' field.
    """
    
    class Meta:
        model = DNASequence
        fields = ['id']