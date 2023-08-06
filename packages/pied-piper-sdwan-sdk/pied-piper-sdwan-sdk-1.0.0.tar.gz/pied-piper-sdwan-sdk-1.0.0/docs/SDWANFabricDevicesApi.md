# openapi_client.SDWANFabricDevicesApi

All URIs are relative to *https://44.196.44.132*

Method | HTTP request | Description
------------- | ------------- | -------------
[**dataservice_device_counters_get**](SDWANFabricDevicesApi.md#dataservice_device_counters_get) | **GET** /dataservice/device/counters | Device Counters
[**dataservice_device_get**](SDWANFabricDevicesApi.md#dataservice_device_get) | **GET** /dataservice/device | Fabric Devices
[**dataservice_device_monitor_get**](SDWANFabricDevicesApi.md#dataservice_device_monitor_get) | **GET** /dataservice/device/monitor | Devices Status
[**dataservice_statistics_interface_get**](SDWANFabricDevicesApi.md#dataservice_statistics_interface_get) | **GET** /dataservice/statistics/interface | Interface statistics


# **dataservice_device_counters_get**
> dataservice_device_counters_get()

Device Counters

### Example


```python
import time
import openapi_client
from openapi_client.api import sdwan_fabric_devices_api
from pprint import pprint
# Defining the host is optional and defaults to https://44.196.44.132
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://44.196.44.132"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sdwan_fabric_devices_api.SDWANFabricDevicesApi(api_client)
    x_xsrf_token = "{{X-XSRF-TOKEN}}" # str |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Device Counters
        api_instance.dataservice_device_counters_get(x_xsrf_token=x_xsrf_token)
    except openapi_client.ApiException as e:
        print("Exception when calling SDWANFabricDevicesApi->dataservice_device_counters_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_xsrf_token** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataservice_device_get**
> dataservice_device_get()

Fabric Devices

### Example


```python
import time
import openapi_client
from openapi_client.api import sdwan_fabric_devices_api
from pprint import pprint
# Defining the host is optional and defaults to https://44.196.44.132
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://44.196.44.132"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sdwan_fabric_devices_api.SDWANFabricDevicesApi(api_client)
    x_xsrf_token = "{{X-XSRF-TOKEN}}" # str |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Fabric Devices
        api_instance.dataservice_device_get(x_xsrf_token=x_xsrf_token)
    except openapi_client.ApiException as e:
        print("Exception when calling SDWANFabricDevicesApi->dataservice_device_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_xsrf_token** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataservice_device_monitor_get**
> dataservice_device_monitor_get()

Devices Status

### Example


```python
import time
import openapi_client
from openapi_client.api import sdwan_fabric_devices_api
from pprint import pprint
# Defining the host is optional and defaults to https://44.196.44.132
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://44.196.44.132"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sdwan_fabric_devices_api.SDWANFabricDevicesApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Devices Status
        api_instance.dataservice_device_monitor_get()
    except openapi_client.ApiException as e:
        print("Exception when calling SDWANFabricDevicesApi->dataservice_device_monitor_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataservice_statistics_interface_get**
> dataservice_statistics_interface_get()

Interface statistics

### Example


```python
import time
import openapi_client
from openapi_client.api import sdwan_fabric_devices_api
from pprint import pprint
# Defining the host is optional and defaults to https://44.196.44.132
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://44.196.44.132"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sdwan_fabric_devices_api.SDWANFabricDevicesApi(api_client)
    x_xsrf_token = "{{X-XSRF-TOKEN}}" # str |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Interface statistics
        api_instance.dataservice_statistics_interface_get(x_xsrf_token=x_xsrf_token)
    except openapi_client.ApiException as e:
        print("Exception when calling SDWANFabricDevicesApi->dataservice_statistics_interface_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_xsrf_token** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

