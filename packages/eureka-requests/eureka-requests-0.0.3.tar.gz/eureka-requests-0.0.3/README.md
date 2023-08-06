# Eureka Requests

Use eureka to find all possible endpoints and then make requests until it works
starting with the best locations

## Install
```
pip install eureka_requests
```

## Usage
```python
import eureka_requests

dbApi = eureka_requests.RequestsApi(
    "DB-SERVE",
    _eureka_url,
    _db_token,
)

dbApi.post("/testdb",
    json = {"query": "SELECT * FROM USERS"}
)
```