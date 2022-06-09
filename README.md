# cloudverse-web-service-backend

### URL : https://gwkxtyxjfc.execute-api.ca-central-1.amazonaws.com/dev/
## API Description

Available API:
* /createWorkstation
* /resumeWorkstation
* /listWorkstation


The json payload format is as follows:
### Create New Workstation (createWorkstation)
```
{
    "action": "new",
    "userId": "545yui4y3489175",
    "instanceType": "t2.small",
    "volumeSize": 30
}
```

### Provision Existing Workstation (resumeWorkstation)
```
{
    "action": "existing",
    "workstationId": "",
    "userId": "545yui4y3489175",
    "instanceType": "t2.small",
    "volumeSize": 30
}
```

### List Workstation (listWorkstation)
```
{
    "userId": "545yui4y3489175"
}
```
