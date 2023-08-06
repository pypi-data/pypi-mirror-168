## Project description
Athena is the core SDK for requesting the EnOS API

### Example

#### 1.1 Query 
```python
from poseidon import poseidon

appkey = '7b51b354-f200-45a9-a349-40cc97730c5a'
appsecret = '65417473-2da3-40cc-b235-513b9123aefg'

url = 'http://{apim-url}/someservice/v1/tyy?sid=28654780'

req = poseidon.urlopen(appkey, appsecret, url)
print(req)
```
#### 1.2 Header
```python
from poseidon import poseidon

appkey = '7b51b354-f200-45a9-a349-40cc97730c5a'
appsecret = '65417473-2da3-40cc-b235-513b9123aefg'

url = 'http://{apim-url}/someservice/v1/tyy?sid=28654780'

header={}

req = poseidon.urlopen(appkey, appsecret, url, None, header)
print(req)

```

#### 1.3 Body
```python
from poseidon import poseidon

appkey = '7b51b354-f200-45a9-a349-40cc97730c5a'
appsecret = '65417473-2da3-40cc-b235-513b9123aefg'

url = 'http://{apim-url}/someservice/v1/tyy?sid=28654780'

data = {"username": "11111", "password": "11111"}

req = poseidon.urlopen(appkey, appsecret, url, data)
print(req)

```