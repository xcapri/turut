## turut (to-root)
_turut_ in English to-root. is a tool to extract a list of urls that you can return to the root domain. Where the data can be used for input to other scanning tools.

```
turut
Extract the root domain from a list of domains.
usage: turut [-h] [-ld LISTDOMAIN]

Extract the root domain from a list of domains.

options:
  -h, --help            show this help message and exit
  -ld LISTDOMAIN, --listdomain LISTDOMAIN
                        File containing the list of domains
```
### Installation
```
python3 -m pip install git+https://github.com/xcapri/turut.git

or 

python3 -m pip install --upgrade git+https://github.com/xcapri/turut.git

```

### Prepare your random list
```
cat test 
asdas.redacted.com
xx.redacted.com
https://xx.redacted.com
```

### Command (Pipeline or Flag)
```
cat test | turut
redacted.com
redacted.com

or 

turut -ld test
redacted.com
redacted.com

```
