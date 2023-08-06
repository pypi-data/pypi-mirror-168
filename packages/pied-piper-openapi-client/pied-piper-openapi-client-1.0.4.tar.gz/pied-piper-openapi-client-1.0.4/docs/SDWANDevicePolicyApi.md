# openapi_client.SDWANDevicePolicyApi

All URIs are relative to *https://44.196.44.132*

Method | HTTP request | Description
------------- | ------------- | -------------
[**dataservice_template_policy_list_get**](SDWANDevicePolicyApi.md#dataservice_template_policy_list_get) | **GET** /dataservice/template/policy/list | Policy List
[**dataservice_template_policy_vedge_devices_get**](SDWANDevicePolicyApi.md#dataservice_template_policy_vedge_devices_get) | **GET** /dataservice/template/policy/vedge/devices | vEdge Template Policy


# **dataservice_template_policy_list_get**
> dataservice_template_policy_list_get()

Policy List

### Example


```python
import time
import openapi_client
from openapi_client.api import sdwan_device_policy_api
from pprint import pprint
# Defining the host is optional and defaults to https://44.196.44.132
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://44.196.44.132"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sdwan_device_policy_api.SDWANDevicePolicyApi(api_client)
    x_xsrf_token = "{{X-XSRF-TOKEN}}" # str |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Policy List
        api_instance.dataservice_template_policy_list_get(x_xsrf_token=x_xsrf_token)
    except openapi_client.ApiException as e:
        print("Exception when calling SDWANDevicePolicyApi->dataservice_template_policy_list_get: %s\n" % e)
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

# **dataservice_template_policy_vedge_devices_get**
> dataservice_template_policy_vedge_devices_get()

vEdge Template Policy

### Example


```python
import time
import openapi_client
from openapi_client.api import sdwan_device_policy_api
from pprint import pprint
# Defining the host is optional and defaults to https://44.196.44.132
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://44.196.44.132"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sdwan_device_policy_api.SDWANDevicePolicyApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # vEdge Template Policy
        api_instance.dataservice_template_policy_vedge_devices_get()
    except openapi_client.ApiException as e:
        print("Exception when calling SDWANDevicePolicyApi->dataservice_template_policy_vedge_devices_get: %s\n" % e)
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

