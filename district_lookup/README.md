# How this script works

Before you run, you will need do the following:

1. [Get an API key credentials](https://console.developers.google.com/apis/credentials?project=lma-kft&folder&organizationId)  from Google to use with their their Civic API.

1. [Enable the API](https://console.developers.google.com/apis/library/civicinfo.googleapis.com?q=Civic&id=a7de1ed0-c5d0-44ca-8365-267daf15ca5b&project=lma-kft&folder&organizationId) to work with your key.

1. Create a config.py on your local machine and add the key there.

```
g_api_key = 'YOUR_KEY_GOES_HERE'
```

1. Run the script

```
python get_districts.py
```


**Want to see what a sample pull looks like?**

The example below uses the White House residence as an example. Replace the address value to a location that is not in the District of Columbia and you will get more results returned. This is because DC residents don't have representation in Congress.

```
https://www.googleapis.com/civicinfo/v2/representatives?address='1600 Pennsylvania Ave NW, Washington, DC 20500'&key=AIzaSyBYN5T3Mc2-Tw1orRYZDWxJ075lvO-khY8&levels=country&roles=legislatorLowerBody
```


### Troubleshooting

Q: **Are you getting a 400?**
A: Did you [enable the API](https://console.developers.google.com/apis/library/civicinfo.googleapis.com?q=Civic&id=a7de1ed0-c5d0-44ca-8365-267daf15ca5b&project=lma-kft&folder&organizationId)?

