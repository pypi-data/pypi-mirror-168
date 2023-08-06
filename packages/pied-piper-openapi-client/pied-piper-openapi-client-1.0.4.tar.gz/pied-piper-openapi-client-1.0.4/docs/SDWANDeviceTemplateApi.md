# openapi_client.SDWANDeviceTemplateApi

All URIs are relative to *https://44.196.44.132*

Method | HTTP request | Description
------------- | ------------- | -------------
[**dataservice_template_feature_get**](SDWANDeviceTemplateApi.md#dataservice_template_feature_get) | **GET** /dataservice/template/feature | Template Feature
[**dataservice_template_feature_types_get**](SDWANDeviceTemplateApi.md#dataservice_template_feature_types_get) | **GET** /dataservice/template/feature/types | Template Feature Type


# **dataservice_template_feature_get**
> dataservice_template_feature_get()

Template Feature

### Example


```python
import time
import openapi_client
from openapi_client.api import sdwan_device_template_api
from pprint import pprint
# Defining the host is optional and defaults to https://44.196.44.132
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://44.196.44.132"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sdwan_device_template_api.SDWANDeviceTemplateApi(api_client)
    x_xsrf_token = "{{X-XSRF-TOKEN}}" # str |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Template Feature
        api_instance.dataservice_template_feature_get(x_xsrf_token=x_xsrf_token)
    except openapi_client.ApiException as e:
        print("Exception when calling SDWANDeviceTemplateApi->dataservice_template_feature_get: %s\n" % e)
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

# **dataservice_template_feature_types_get**
> dataservice_template_feature_types_get()

Template Feature Type

### Example


```python
import time
import openapi_client
from openapi_client.api import sdwan_device_template_api
from pprint import pprint
# Defining the host is optional and defaults to https://44.196.44.132
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://44.196.44.132"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sdwan_device_template_api.SDWANDeviceTemplateApi(api_client)
    x_xsrf_token = "{{X-XSRF-TOKEN}}" # str |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Template Feature Type
        api_instance.dataservice_template_feature_types_get(x_xsrf_token=x_xsrf_token)
    except openapi_client.ApiException as e:
        print("Exception when calling SDWANDeviceTemplateApi->dataservice_template_feature_types_get: %s\n" % e)
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

