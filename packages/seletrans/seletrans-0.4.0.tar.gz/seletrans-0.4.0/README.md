# SeleTrans

Translate phase using selenium. And you can also play the sound of the phase you are querying.

Currently support `Baidu`, `DeepL` and `Google`.

## Usage

```python
from seletrans.api import *

with Google() as ts:
    res = ts.query("book", target="zh-CN")
    print(res.result)
    print(res.dict_result)
    res.play_sound()
```

Check the test case for more information, or run it yourself to see the results.

## Explain

Why use selenium? Why not use requests?

Although selenium is slower than requests, it is more convenient to adapt when API changes.

## Notice
On the mac, you have to run `/Applications/Python 3.10/Install Certificates.command` to avoid 

```
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)>
```
