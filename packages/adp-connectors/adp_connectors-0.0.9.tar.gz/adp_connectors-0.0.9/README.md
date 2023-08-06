### Connectors for Discovery Platform Applications

The current version supports 3 kind of API connections: AWS S3, Box, PostgreSQL.
The required secret file formats are as follows.
- S3 Connector
  ```
  {
    "aws_access_key_id": "",
    "aws_secret_access_key": ""
  }

- Box Connector
  ```
    {
      "boxAppSettings": {
        "clientID": "",
        "clientSecret": "",
        "appAuth": {
          "publicKeyID": "",
          "privateKey": "",
          "passphrase": ""
          }
        },
        "enterpriseID": ""
      }

- Postgresql Connector
  ```
  {
    "host": "",
    "port": 5432,
    "database": "",
    "user": "",
    "password": ""
  }
