## Usage

#### Send free message to email, without your email!

```python
# Send free message to email, debug OFF
>>> from sendtomail import *
>>> server.send("ua", "he1zen@null.net", "hello, its a test message!")
'200'
>>>

# Send free message to email, debug ON
>>> from sendtomail import *
>>> server.debug("on")
>>> server.send("ua", "he1zen@null.net", "hello, its a test message!")
[3%] Debug mode ON
[7%] Region ua
[11%] Starting to get URL
[20%] Getting json from URL
[40%] URL json data decode
[60%] Server IP 18.189.106.45
[80%] Server connected!
[100%] Data send to server
'200'
>>>

# Servers list
>>> from sendtomail import *
>>> regions = server.regions()
>>> print(regions)
SMTP regions: tr, ru, ua, us, uk, de, fr, it
>>>

# Get Free SMTP, POP3, IMAP email
>>> from sendtomail import *
>>> server.mail()
{'google-mail': 'qcp9ex.iqu0@gmail.com', 'google-pass': 'dmxsdxqgvlcypitf'}
>>> 

# Free email checker
>>> from sendtomail import *
>>> server.validate("he1zen@null.net")
'valid'
>>> 

```

```
## Status codes
200 - Succesfully send
400 - Bad options
403 - Email protected
404 - Email not found
429 - Choose another region
500 - Internal Server Error
503 - Service Unavailable
504 - Try another region

## Other codes
valid   - mailbox exists
invalid - mailbox does not exist 

## Servers Country
tr - turkey
ru - russia
ua - ukraine
us - united states
uk - united kingdom
de - germany
fr - france
it - italia
```

**I also want to inform you that it is possible to send letters from one region to another, for example from Ukraine to USA**
