# vim: set fileencoding=utf-8:


from coronado import TripleObject
from coronado.baseobjects import BASE_MERCHANT_DICT
from coronado.baseobjects import BASE_MERCHANT_LOCATION_DICT
from coronado.exceptions import CallError

import json
import logging


# +++ constants +++

SERVICE_PATH = 'partner/merchants'
"""
The default service path associated with Merchant operations.

Usage:

```python
Merchant.initialize(serviceURL, SERVICE_PATH, auth)
```

Users are welcome to initialize the class' service path from regular strings.
This constant is defined for convenience.
"""


# *** classes and objects ***


# --- globals ---

log = logging.getLogger(__name__)


class MerchantLocation(TripleObject):
    """
    A merchant's business adddress, whether physical or on-line.

    See `coronado.address.Address`
    """

    requiredAttributes = [
        'address',
        'objID',
    ]

    def __init__(self, obj = BASE_MERCHANT_LOCATION_DICT):
        """
        Create a new MerchantLocation instance.
        """
        TripleObject.__init__(self, obj)


    @classmethod
    def create(klass, **args) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def byID(klass, objID: str) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def updateWith(klass, objID: str, spec: dict) -> object:
        """
        **Disabled for this class.**
        """
        None


    @classmethod
    def list(klass, paraMap = None, **args) -> list:
        """
        **Disabled for this class.**
        """
        None


class Merchant(TripleObject):
    """
    Merchant is a company or person involved in trade, most often retail, that
    processes card payments as a result of that trade.
    """
    requiredAttributes = [
        'address',
        'assumedName',
        'createdAt',
        'updatedAt',
    ]
    allAttributes = TripleObject(BASE_MERCHANT_DICT).listAttributes()


    def __init__(self, obj = BASE_MERCHANT_DICT):
        """
        Create a new Merchant instance.
        """
        TripleObject.__init__(self, obj)


    @classmethod
    def create(klass, **args) -> object:
        """
        Creates a merchant and returns an instance of the new object.

        Arguments
        ---------

            extMerchantID: str
        The external, non-triple merchant ID

            address: Address
        An instance of `coronado.address.Address` initialized to the merchant's
        physical address

            assumedName: str
        The merchant's assumed name

            logoURL: string
        A URL to the merchant's logo.

            merchantCategoryCode: MerchantCategoryCode
        The 4-digit standardized merchant category code (MCC).  See
        `coronado.merchantcodes.MerchantCategoryCode` for a full list.

        Returns
        -------

        An instance of `Merchant` if it was created by the triple back-end,, or
        `None`.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        spec = dict()

        try:
            spec['external_id'] = args['extMerchantID']
            spec['address'] = args['address'].asSnakeCaseDictionary()
            spec['assumed_name'] = args['assumedName']
            spec['logo_url'] = args.get('logoURL', None)
            spec['merchant_category_code'] = args['merchantCategoryCode']
        except:
            raise CallError('Malrformed spec - invalid or incomplete arguments - spec = %s ' % spec)

        return Merchant(super().create(spec))


    @classmethod
    def list(klass: object, paramMap = None, **args) -> list:
        """
        List all merchants that match any of the criteria set by the
        arguments to this method.

        Arguments
        ---------
            externalMerchantID
        String, 1-50 characters partner-provided external ID

        Returns
        -------
            list
        A list of Merchant objects; can be `None`.
        """
        paramMap = {
            'externalMerchantID': 'merchant_external_id',
        }
        response = super().list(paramMap, **args)
        result = [ TripleObject(obj) for obj in json.loads(response.content)['card_accounts'] ]
        return result

