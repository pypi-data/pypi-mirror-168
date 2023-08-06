# ElectronBonder
A client library for working with the Project Electron APIs.

## Getting started

Make sure this library is installed:

      pip3 install ElectronBonder


Then create a client with a baseurl, a username and a password:

``` python
from electronbonder.client import ElectronBond

client = ElectronBond(
            baseurl="http://my.aspace.backend.url.edu:4567",
            username="admin",
            password="TopSecr3t")
```

## Credits
This code is basically stolen from [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake/).


## License
ElectronBonder source code is released under an MIT License.
