
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from openapi_client.api.1_authentication_api import 1AuthenticationApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from openapi_client.api.1_authentication_api import 1AuthenticationApi
from openapi_client.api.2_sdwan_fabric_devices_api import 2SDWANFabricDevicesApi
from openapi_client.api.3_sdwan_device_template_api import 3SDWANDeviceTemplateApi
from openapi_client.api.4_sdwan_device_policy_api import 4SDWANDevicePolicyApi
