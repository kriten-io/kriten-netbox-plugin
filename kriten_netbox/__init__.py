from netbox.plugins import PluginConfig

__author__ = "Steve Corp"
__email__ = "steve@kubecode.io"
__version__ = "0.1.0"

class KritenConfig(PluginConfig):
    name = 'kriten_netbox'
    verbose_name = 'Kriten - API-driven Automation Platform.'
    description = 'Configure Kriten and run jobs from NetBox'
    author = __author__
    author_email = __email__
    version = __version__
    base_url = 'kriten_netbox'

config = KritenConfig