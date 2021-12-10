
A tool for an easier doujinshi download experience.

# USAGE

## Cookies configure example

```json
[{
	"Host raw": ".e-hentai.org",
	"Name raw": "ipb_session_id",
	"Path raw": "/",
	"Content raw": "<value>",
	"Expires": "At the end of the session",
	"Expires raw": "0",
	"Send for": "Any type of connection",
	"Send for raw": "false",
	"HTTP only raw": "false",
	"SameSite raw": "lax",
	"This domain only": "Valid for subdomains",
	"This domain only raw": "false",
	"Store raw": "firefox-default",
	"First Party Domain": ""
},
{
	"Host raw": ".e-hentai.org",
	"Name raw": "ipb_member_id",
	"Path raw": "/",
	"Content raw": "<value>",
	"Expires": "08-12-2022 22:55:39",
	"Expires raw": "1670511339",
	"Send for": "Any type of connection",
	"Send for raw": "false",
	"HTTP only raw": "false",
	"SameSite raw": "lax",
	"This domain only": "Valid for subdomains",
	"This domain only raw": "false",
	"Store raw": "firefox-default",
	"First Party Domain": ""
},
{
	"Host raw": ".e-hentai.org",
	"Name raw": "ipb_pass_hash",
	"Path raw": "/",
	"Content raw": "<value>",
	"Expires": "08-12-2022 22:55:39",
	"Expires raw": "1670511339",
	"Send for": "Any type of connection",
	"Send for raw": "false",
	"HTTP only raw": "false",
	"SameSite raw": "lax",
	"This domain only": "Valid for subdomains",
	"This domain only raw": "false",
	"Store raw": "firefox-default",
	"First Party Domain": ""
}]
```

## Run

```bash
# install requirements
pip install -r requirements.txt
# start geckowedriver
$ ./geckodriver -b <path_to_firefox>
# start download
$ python download.py <doujinshi_url> --save-path ./ --gecko-path /home/scarlet/geckodriver --socks-proxy <proxy_address>
```



# TODO

- support download low quality image
- no credit notification