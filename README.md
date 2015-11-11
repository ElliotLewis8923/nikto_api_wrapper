# Nikto wrapper API

Set up:
```bash
$ git clone https://github.com/sullo/nikto.git
$ python index.py
```
Test:
```bash
$ python -m SimpleHTTPServer 9000&
$ curl "localhost:8080/?host=127.0.0.1:9000&cgidirs=all"
```

* The API assumes that nikto has been cloned into the same directory. This can be reconfigured by modifying `NIKTO_PATH`.
* Both `host` and `cgidirs` are mandatory parameters.  Any incorrect formatting will result in a 400 status code.