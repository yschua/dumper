# dumper
Windows service for uploading files added to a watched directory to a FTP server.

#### Install and start service
```
$ py dumpersvc.py install

$ NET START DumperSvc
```

#### Stop and uninstall service
```
$ NET STOP DumperSvc

$ py dumpersvc.py remove
```

#### Run as script 
```
$ py dumper/run.py
```

#### Dependencies
* python3.5
* pywin32

#### Settings
Modify settings and FTP server credentials in [config.ini](config.ini)
