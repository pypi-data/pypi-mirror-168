# vim: set fileencoding=utf-8:


from coronado import TripleObject
from coronado.baseobjects import BASE_CARD_PROGRAM_DICT

import json


# *** constants ***

SERVICE_PATH = 'partner/card-programs'
"""
The default service path associated with CardProgram operations.

Usage:

```
CardProgram.initialize(serviceURL, SERVICE_PATH, auth)
```

Users are welcome to initialize the class' service path from regular strings.
This constant is defined for convenience.
"""


# ***

class CardProgram(TripleObject):
    """
    Card programs are logical groupings of card accounts.  A card program is
    often a specific type of card offering by a CardProgram, like a payment card
    associated with its own rewards like miles or cash back.  Card programs may
    also be used for organizing card accounts in arbirtrary groupings.

    Card accounts may not move between card programs, and cannot be represented
    in more than one card program at a time.
    """

    requiredAttributes = [
        'defaultPostalCode',
        'externalID',
        'name',
        'programCurrency',
    ]
    allAttributes = TripleObject(BASE_CARD_PROGRAM_DICT).listAttributes()


    def __init__(self, obj = BASE_CARD_PROGRAM_DICT):
        """
        Create a new instance of a card program.  `obj` must correspond to a
        valid, existing object ID if it's not a collection or JSON.

        Arguments
        ---------
            obj
        An object used for building a valid card program.  The object can
        be one of:

        - A dictionary - a dictionary with instantiation values as described
          in the API documentation
        - A JSON string
        - A triple objectID

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        TripleObject.__init__(self, obj)


    @classmethod
    def list(klass: object, paramMap = None, **args) -> list:
        """
        Return a list of card programs.

        Arguments
        ---------
            extPublisherID
        An external publisher ID; optional

            extCardProgramID
        An external card program ID; optional

        Returns
        -------
            list
        A list of CardProgram objects

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        paramMap = {
            'extCardProgramID': 'card_program_external_id',
            'extPublisherID': 'publisher_external_id',
        }

        response = super().list(paramMap, **args)
        result = [ CardProgram(obj) for obj in json.loads(response.content)['card_programs'] ]

        return result


    @classmethod
    def create(klass, spec: dict) -> object:
        """
        For full details see `coronado.TripleObject.create()`.

        spec:

        ```
        {
          'card_bins': [
            '444789'
          ],
          'default_country_code': 'US',
          'default_postal_code': '15206',
          'external_id': 'string',
          'name': 'string',
          'program_currency': 'USD',
          'publisher_external_id': 'string',
        }
        ```
        """
        return CardProgram(super().create(spec))

