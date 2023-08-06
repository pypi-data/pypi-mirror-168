# openapi_client.AuthenticationApi

All URIs are relative to *https://44.196.44.132*

Method | HTTP request | Description
------------- | ------------- | -------------
[**dataservice_client_token_get**](AuthenticationApi.md#dataservice_client_token_get) | **GET** /dataservice/client/token | Token
[**j_security_check_post**](AuthenticationApi.md#j_security_check_post) | **POST** /j_security_check | Authentication


# **dataservice_client_token_get**
> dataservice_client_token_get()

Token

### Example


```python
import time
import openapi_client
from openapi_client.api import authentication_api
from pprint import pprint
# Defining the host is optional and defaults to https://44.196.44.132
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://44.196.44.132"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = authentication_api.AuthenticationApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Token
        api_instance.dataservice_client_token_get()
    except openapi_client.ApiException as e:
        print("Exception when calling AuthenticationApi->dataservice_client_token_get: %s\n" % e)
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

# **j_security_check_post**
> j_security_check_post()

Authentication

### Example


```python
import time
import openapi_client
from openapi_client.api import authentication_api
from pprint import pprint
# Defining the host is optional and defaults to https://44.196.44.132
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://44.196.44.132"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = authentication_api.AuthenticationApi(api_client)
    content_type = "application/x-www-form-urlencoded" # str |  (optional)
    j_username = "admin" # str |  (optional)
    j_password = "Fun_Nfvis1" # str |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Authentication
        api_instance.j_security_check_post(content_type=content_type, j_username=j_username, j_password=j_password)
    except openapi_client.ApiException as e:
        print("Exception when calling AuthenticationApi->j_security_check_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **content_type** | **str**|  | [optional]
 **j_username** | **str**|  | [optional]
 **j_password** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

