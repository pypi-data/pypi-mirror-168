# vim: set fileencoding=utf-8:


from coronado import TripleObject
from coronado.address import Address
from coronado.baseobjects import BASE_PUBLISHER_DICT

import json

import requests


# +++ constants +++

SERVICE_PATH = 'partner/publishers'
"""
The default service path associated with CardAccount operations.

Usage:

```
CardAccount.initialize(serviceURL, SERVICE_PATH, auth)
```

Users are welcome to initialize the class' service path from regular strings.
This constant is defined for convenience.
"""


# *** classes and objects ***

class Publisher(TripleObject):
    """
    Publisher objects are used for managing portfolios of publishers.  Partners
    who manage card programs for multiple publishers may wish to organize them
    into portfolios.  Portfolios allow offer exclusions which may be applied
    across multiple publishers without having to add individual publishers to
    an offer exclusion.
    """

    requiredAttributes = [
        'address',
        'assumedName',
        'createdAt',
        'updatedAt',
    ]
    allAttributes = TripleObject(BASE_PUBLISHER_DICT).listAttributes()


    def __init__(self, obj = BASE_PUBLISHER_DICT):
        """
        Create a new instance of a publisher.  `obj` must correspond to a
        valid, existing object ID if it's not a collection or JSON.

        Arguments
        ---------
            obj
        An object used for building a valid publisher.  The object can
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
    def create(klass, spec: dict) -> object:
        """
        For full details see `coronado.TripleObject.create()`.

        spec:

        ```
        {
          'address': {
            'city': 'PITTSBURGH',
            'complete': '7370 BAKER ST, STE 100\nPITTSBURGH, PA 15206',
            'country_code': 'US',
            'country_subdivision_code': 'PA',
            'latitude': 40.440624,
            'longitude': -79.995888,
            'postal_code': '15206',
            'street_address': '7370 BAKER ST, STE 100\n'
          },
          'assumed_name': 'string',
          'external_id': 'string',
          'revenue_share': 1.125
        }
        ```
        """
        return Publisher(super().create(spec))


    @classmethod
    def list(klass : object) -> list:
        """
        Return a list of publishers.

        Returns
        -------
            list
        A list of Publisher objects
        """
        endpoint = '/'.join([Publisher._serviceURL, SERVICE_PATH]) # URL fix later
        response = requests.request('GET', endpoint, headers = Publisher.headers)
        result = [ TripleObject(obj) for obj in json.loads(response.content)['publishers'] ]

        return result


    @classmethod
    def byID(klass, objID: str) -> object:
        result = super().byID(objID)

        if result:
            result.address = Address(result.address)

        return result

