from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _


# Language Type (see model `Member` and `Client`)
LANG_TYPE = (
    ('en', _('English')),
    ('fr', _('French')),
    ('gr', _('Germany')),
    ('es', _('Spain')),

)


STORE_CAT = (
    ('fa', _('Fashion')),
    ('jw', _('Jewelery')),
    ('ga', _('Games')),

)


PROVIDER_CHOICE = (
    ('shopify', _('Shopify')),
    ('prestashop', _('PrestaShop')),
    ('woocommerce', _('WooCommerce')),
    ('opencard', _('OpenCard')),
    ('magento', _('Magento'))
)
FONT = (
    ('AR', 'Arial'),
    ('ARB', 'Arial Black'),
    ('CN', 'Courier New')
)
ALLIGNMENT = (
    ('center', 'center'),
    ('left', 'left'),
    ('right', 'right'),
)

SIZE =(
    ('8','8'),
    ('10','10'),
    ('12','12'),
    ('14','14'),
    ('16','16'),
    ('18','18'),
    ('20','20'),
    ('24','24'),
)
STATUS = (
    ('IT', 'In Transit'),
    ('DL', 'Delivered'),
    ('OFD', 'Out for delivery'),
    ('RTG', 'Ready togo'),
    ('FA', 'Failed attempt'),
)
