from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
from . sequencedb import SequenceDb

class APISequenceView(APIView):
    """Class used to define the methods that are responsible for making the GET and POST HTTP requests for the API and for rendering the result (a JSON) to the view.
    These methods create an instance of SequenceDb and call its 'insert', 'get', 'find' and 'overlap' method.
    """

    @api_view(["POST"])
    def insertSequence(self):
        """Method used to define an instance of SequenceDb in order to call its 'insert' method, that aims to create a new DNA sequence in the database.

        Returns:
            The result of the sequenceDb.insert method, which is a JSON indicating the new ID (UID) of the sequence inserted in the database.
        """
        try:
            sequenceDb = SequenceDb()
            sequence = self.GET.get('sequence')

            return sequenceDb.insert(self.method, sequence)
        except RuntimeError as e:
            return JsonResponse({'error' : e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def getSequence(self, uid):
        """Method used to define an instance of SequenceDb in order to call its 'get' method, that aims to give the DNA sequence of a uid.

        Parameters:
            uid: The Unique Identifier that represents the DNA sequence.

        Returns:
            The result of the sequenceDb.get method, which is a JSON indicating the DNA sequence of the uid.
        """
        try:
            sequenceDb = SequenceDb()

            return sequenceDb.get(uid)
        except RuntimeError as e:
            return JsonResponse({'error' : e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def findSequence(self):
        """Method used to define an instance of SequenceDb to call its 'find' method, that aims to find a list of DNA sequences that contain a sample. 

        Returns:
            The result of the sequenceDb.find method, which is a JSON indicating a list of ids (Unique Identifiers) of DNA sequences.
        """

        try:
            sequenceDb = SequenceDb()
            sample = self.GET.get('sample')

            return sequenceDb.find(sample)
        except RuntimeError as e:
            return JsonResponse({'error' : e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def overlapSequence(self):
        """Method used to define an instance of SequenceDb to call its 'overlap' method, which intends to indicate if a sample overlaps the sequence of a DNA.

        Returns:
            The result of the sequenceDb.overlap method, 
            which is a JSON representing a Boolean that indicates if a DNA sequence of a particular Unique Identifier is overlapped by a sample.
        """
        try:
            sequenceDb = SequenceDb()
            sample = self.GET.get('sample')
            uid = self.GET.get('uid')

            return sequenceDb.overlap(sample, uid)
        except RuntimeError as e:
            return JsonResponse({'error' : e.args[0]}, status=status.HTTP_400_BAD_REQUEST)