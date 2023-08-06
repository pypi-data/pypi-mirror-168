# Integration Eskiz SMS API with Python | SMS Service 
Sourcode and Resources for Eskiz & Python <hr>
Support Telegram - http://t.me/Muhammadalive <br>
Documentation & More https://documenter.getpostman.com/view/663428/RzfmES4z?version=latest<br>
<hr>
<p align="center">
    <img style="width: 100%;" src="https://telegra.ph/file/2717ca1f2e52df46df06d.png"></img> </hr>
</p>

```
from lib.eskiz.client import SMSClient

client = SMSClient(
    api_url="https://notify.eskiz.uz/api/",
    email="test@eskiz.uz",
    password="j6DWtQjjpLDNjWEk74Sx",
)

resp = client._send_sms(
    phone_number="998888351717",
    message="Hello from Python ❤️",
)
print(resp)
```