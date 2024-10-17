# convert json to json-ld

import json
from pyld import jsonld


json_data = {
    "NAME": "Test_1",
    "Description": "Validating_shacl",
    "PSI_Voltage": "5",
    "PSI_Current": "5",
    "XMA_ANA": [
        {
            "0": 0,
            "Measurement_NO": "",
            "Channel_type": "",
            "Min": "",
            "Accuracy": "",
            "Status": "",
            "Config_Delay": ""
        }
    ],
    "XMA_THC": [
        {
            "0": 0,
            "Measurement_NO": "1",
            "Channel_type": "Thermocouple k",
            "Min": "20",
            "Accuracy": "22",
            "Status": "progress",
            "Config_Delay": "1"
        }
    ]
}

context={
    
}

