from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from . models import DNASequence
from . serializers import DNASerializerSequence
from . serializers import DNASerializerId
from django.http import JsonResponse
import re

class SequenceDb:
    """Class used to define the methods of a DNA sequence: 'insert', 'get', 'find' and 'overlap'.
    Each method returns a JSON that gives the detailed information expected.

    Attributes:
        BAD_REQUEST: Constant string used to define a bad HTTP request.
        INVALID_CHARACTERS: Constant string used to state that invalid characters have been set.
        INVALID_INPUT: Constant string used to state that an invalid input has been set.
        UID_DOES_NOT_EXIST: Constant string used to indicate that the Unique Identifier does not exist.
        SEQUENCE_EXISTS: Constant string used to indicate that the sequence already exists.
        BAD_HTTP_GET_REQUEST: Constant string used to indicate the method can only take HTTP POST requests.
        VALID_CHARACTERS: Constant string used to indicate the group of characters that are valid to define a sequence.
    """

    BAD_REQUEST = 'Bad request.'
    INVALID_CHARACTERS = 'Invalid characters input.'
    INVALID_INPUT = 'Invalid sample input.'
    UID_DOES_NOT_EXIST = 'Unique Identifier does not exist.'
    SEQUENCE_EXISTS = 'Sequence already exists.'
    BAD_HTTP_GET_REQUEST = 'Method only valid for HTTP POST requests.'
    VALID_CHARACTERS = 'ACGT'

    def insert(self, method, sequence):
        """Inserts a new sequence to the database.

        Parameters:
            method: The HTTP method.
            sequence: The DNA sequence to insert into the database.

        Returns:
            A JSON indicating the new ID (Unique Identifier) of the sequence inserted in the database.
        """

        if method == 'POST':
            dnaSequence = DNASequence.objects.filter(sequence=sequence)
            validString = bool(re.match(r"^([%s])+$" % self.VALID_CHARACTERS, sequence))

            if not validString:
                return JsonResponse({
                    'status' : self.BAD_REQUEST,
                    'message': self.INVALID_CHARACTERS,
                }, status=status.HTTP_400_BAD_REQUEST)
            elif dnaSequence.exists():
                return JsonResponse({
                    'status' : self.BAD_REQUEST,
                    'message': self.SEQUENCE_EXISTS,
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                newSequence = DNASequence(sequence=sequence)
                newSequence.save()

                serializer = DNASerializerId(dnaSequence, many=True)
                response = Response(serializer.data, status=status.HTTP_201_CREATED)
                responseJSON = self.generateResponseRender(response)
            
                return responseJSON
        else: 
            return JsonResponse({
                'status' : self.BAD_REQUEST,
                'message': self.BAD_HTTP_GET_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, uid):
        """Gets the DNA sequence of a particular Unique Identifier.

        Parameters:
            uid: The Unique Identifier of the sequence.

        Returns:
            A JSON indicating the DNA sequence of the uid.
        """

        sequence = DNASequence.objects.filter(id=uid)

        if not sequence.exists():
            return JsonResponse({
                'status' : self.BAD_REQUEST,
                'message': self.UID_DOES_NOT_EXIST,
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = DNASerializerSequence(sequence, many=True)
            response = Response(serializer.data)
            responseJSON = self.generateResponseRender(response)

            return responseJSON

    def find(self, sample):
        """Finds a list of DNA sequences that contain a sample.

        Parameters:
            sample: A sample string to match with the DNA sequences in the database.

        Returns:
            A JSON indicating a list of ids (Unique Identifiers) of DNA sequences.
        """

        validString = bool(re.match(r"^([%s])+$" % self.VALID_CHARACTERS, sample))

        if not validString:
            return JsonResponse({
                'status' : self.BAD_REQUEST,
                'message': self.INVALID_INPUT,
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            sequence = DNASequence.objects.filter(sequence__icontains = sample)
            serializer = DNASerializerId(sequence, many=True)
            response = Response(serializer.data)
            responseJSON = self.generateResponseRender(response)

            return responseJSON

    def overlap(self, sample, uid):
        """Indicates if a sample overlaps the sequence of a DNA.

        Parameters:
            sample: A sample string to match with the DNA sequences in the database.
            uid: The Unique Identifier of the sequence.

        Returns:
            A JSON representing a Boolean that indicates if a DNA sequence of a particular Unique Identifier is overlapped by a sample.
        """

        validString = bool(re.match(r"^([%s])+$" % self.VALID_CHARACTERS, sample))

        if not validString:
            return JsonResponse({
                'status' : self.BAD_REQUEST,
                'message': self.INVALID_INPUT,
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            sequence = DNASequence.objects.filter(id=uid)

            if not sequence.exists():
                return JsonResponse({
                    'status' : self.BAD_REQUEST,
                    'message': self.UID_DOES_NOT_EXIST,
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                repeatedWord = self.getRepeatedWord(sample)
                sequenceToOverlap = str(sequence[0])
                overlapResult = False

                if sequenceToOverlap[0:len(repeatedWord)] == repeatedWord or sequenceToOverlap[len(sequenceToOverlap)-len(repeatedWord):len(sequenceToOverlap)] == repeatedWord:
                    overlapResult = True

                return JsonResponse({
                    'overlap' : overlapResult,
                })

    def getRepeatedWord(self, string):
        """Finds the repeating substring a string is composed of, if it exists.

        Parameters:
            string: A string to determine a repeating substring it is composed of.
        Returns:
            A string which bases are identical starting from or ending with the end of the sequence.
        """

        index = (string+string)[1:-1].find(string)

        if index == -1:
            return string
        else:
            return string[:index+1]

    def generateResponseRender(self, response):
        """generates the response in JSON format.

        Parameters:
            response: A Response object without proper initialization.
        Returns:
            A Response object JSONRenderer.
        """

        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}

        return response