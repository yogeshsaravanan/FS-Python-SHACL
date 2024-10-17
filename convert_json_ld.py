import json

def convert_json_to_jsonld(data):
    """
    Convert a regular JSON object to JSON-LD format using a dynamically generated context.

    :param data: The input JSON data as a dictionary.
    :return: A JSON-LD formatted string.
    """
    context = {
        "@context": {
            "ns1": "http://schema.org/",
            "ex": "http://example.org/ex#",
            "NAME": "ns1:name",
            "Description": "ns1:description",
            "PSI_Voltage": "ns1:voltage",
            "PSI_Current": "ns1:current",
            "XMA_ANA": {
                "@id": "ns1:XMA_ANA",
                "@type": "@id"
            },
            "XMA_THC": {
                "@id": "ns1:XMA_THC",
                "@type": "@id"
            },
            "Measurement_NO": "ns1:measurementNumber",
            "Channel_type": "ns1:channelType",
            "Min": "ns1:min",
            "Accuracy": "ns1:accuracy",
            "Status": "ns1:status",
            "Config_Delay": "ns1:configDelay",
            "@type": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        },
        "@type": "http://example.org/XMA3"
    }

    json_ld = {**context, **data}
    print(json_ld)
    return json.dumps(json_ld, indent=2)

# Example usage
# data = {
#     "NAME": "Test_1",
#     "Description": "Validating_shacl",
#     "PSI_Voltage": "5",
#     "PSI_Current": "5",
#     "XMA_ANA": [
#         {
#             "0": 0,
#             "Measurement_NO": "",
#             "Channel_type": "",
#             "Min": "",
#             "Accuracy": "",
#             "Status": "",
#             "Config_Delay": ""
#         }
#     ],
#     "XMA_THC": [
#         {
#             "0": 0,
#             "Measurement_NO": "1",
#             "Channel_type": "Thermocouple k",
#             "Min": "20",
#             "Accuracy": "22",
#             "Status": "progress",
#             "Config_Delay": "1"
#         }
#     ]
# }

# json_ld_output = convert_json_to_jsonld(data)
# print(json_ld_output)
