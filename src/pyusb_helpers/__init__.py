import bz2
import json
import logging

import conda_helpers as ch

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


USB_IDS = json.loads(bz2.decompress(ch.conda_prefix()
                                    .joinpath('Library', 'share', 'usb-ids',
                                              'usb-ids.json.bz2').bytes()))

logger = logging.getLogger(__name__)


def summarize_device(device):
    '''
    Generate a summary dictionary describing a USB device.

    Parameters
    ----------
    device : usb.core.Device
        USB device to describe.

    Returns
    -------
    dict
        Summary dictionary describing specified USB device.

    Example
    -------

    Generate list of summaries of all USB devices found:

    >>> import pprint
    >>> import pyusb_helpers as pyuh
    >>> import usb.core
    >>>
    >>> pprint.pprint(map(pyuh.summarize_device, usb.core.find(find_all=True)))
    [{'product_id': '20d0',
      'vendor': u'Elan Microelectronics Corp.',
      'vendor_id': '04f3'},
     {'product_id': '670c', 'vendor': u'Microdia', 'vendor_id': '0c45'},
     {'product_id': '670c', 'vendor': u'Microdia', 'vendor_id': '0c45'},
     {'product': u'Teensyduino Serial',
      'product_id': '0483',
      'vendor': u'Van Ooijen Technische Informatica',
      'vendor_id': '16c0'},
     {'product_id': '0037', 'vendor': u'Arduino SA', 'vendor_id': '2341'},
     {'product_id': '9d2f', 'vendor': u'Intel Corp.', 'vendor_id': '8086'},
     {'product_id': 'e301',
      'vendor': u'Qualcomm Atheros Communications',
      'vendor_id': '0cf3'}]
    '''
    summary = {}
    try:
        vendor_id = '{:04x}'.format(device.idVendor)
        product_id = '{:04x}'.format(device.idProduct)
        summary = {'vendor_id': vendor_id, 'product_id': product_id}

        if vendor_id not in USB_IDS:
            logger.debug('vendor not found `{}:{}`'.format(vendor_id,
                                                           product_id))
            return summary

        summary['vendor'] = USB_IDS[vendor_id]['name']

        if product_id not in USB_IDS[vendor_id].get('products', {}):
            logger.debug('product not found `{}:{}`'.format(vendor_id,
                                                            product_id))
            return summary

        product = USB_IDS[vendor_id]['products'][product_id]
        if 'name' in product:
            summary['product'] = product['name']

    except Exception:
        pass
    return summary
