from django.db import models

class DNASequence(models.Model):
    """
    Class that defines the model for DNASequence.

    Attributes:
    sequence: The DNA sequence.
    id: The Unique Identifier that represents the DNA sequence.
        This attribute is handled automatically by the Django's ORM and increases by 1 for each insertion, starting by the id 1.
    """

    sequence = models.CharField(max_length=200)

    def __str__(self):
        return self.sequence