# How this script works

Before you run, you will need do the following:

1. [Get an API key](https://console.developers.google.com/apis/credentials?project=lma-kft&folder&organizationId)  from Google to use with their their Civic API.

1. [Enable the API](https://console.developers.google.com/apis/library/civicinfo.googleapis.com?q=Civic&id=a7de1ed0-c5d0-44ca-8365-267daf15ca5b&project=lma-kft&folder&organizationId) to work with your key.

1. Create a config.py on your local machine and add the key there.
  ```
  g_api_key = 'YOUR_KEY_GOES_HERE'
  ```

4. Run the script

```
python get_districts.py
```


**Want to see what a sample pull looks like?**

In the URL below replace `$EXAMPLE_ADDRESS` with the address you want to look up, and replace `$API_KEY` with your actual API key.

```
https://www.googleapis.com/civicinfo/v2/representatives?address=$EXAMPLE_ADDRESS&key=$API_KEY=country&roles=legislatorLowerBody
```


## Troubleshooting

Q: **Are you getting a 400?**
A: Did you [enable the API](https://console.developers.google.com/apis/library/civicinfo.googleapis.com?q=Civic&id=a7de1ed0-c5d0-44ca-8365-267daf15ca5b&project=lma-kft&folder&organizationId)?

