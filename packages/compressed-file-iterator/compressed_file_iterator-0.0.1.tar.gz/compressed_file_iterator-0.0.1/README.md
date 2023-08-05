# compressed_file_iterator
Configurable iterator-based access to compressed files.

This is a simple package to provide configurable iterator-based access to compressed files.

### Usage:
foo.json
```
{
    ".gz": {
        "base_command": {
            "posix": "/bin/gzip"
        },
        "base_options": {
            "posix": [ '-d', '-c', ]
        },
        "type": "Gzip"
    },
    ".*": {
        "base_command": {
            "posix": "/bin/cat"
        },
        "base_options": {
            "posix": []
        },
        "type": "Plain"
    }
}
```

```py
import compressed_file_iterator
# ...
    my_iterator = compressed_file_iterator.MyIterator(
                                                      'foo.txt',
                                                      config_file='foo.json',
                                                      case_sensitive=True,
                                                      )

    for line in my_iterator:
        print(line)
# ...
```


### Installation

_TODO_: (Upload to allow for install via pip.)

```
$ pip install compressed_file_iterator
```


### Documentation

#### Class definition

```py
class compressed_file_iterator():
        def __init__(self, 
                     args, 
                     cwd='./',
                     config_file='compressed_file_iterator.json',
                     case_sensitive=True,
                     ):
```



#### Parameters
- args : list
  - Contains file name to open.
- cwd : string, optional
  - Working directory. (Default: '.').
- config_file : string, optional
  - JSON configuration defining extensions and how to handle them.
- case_sensitive : boolean, optional
  - Perform match attempts against JSON configuration in a 
case-sensitive manner. If False, process via string.casefold() 
before testing. (Default: True)



#### JSON Format
```
{
        '.extension': {
                'base_command': {
                    os_name: path_to_executable,
                },
                'base_options': {
                        os_name: [ command_line_options ],
                'type': string
        },
}
```



#### Parameters
- .extension: string
  - A string representation of a file extension, as separated by pathlib.Path().suffixes.
  - _A default definition should be included for '.*' to be used if 
no other match can be made._
- base_command: dictionary
  - Contains one or more commands, indexed by the value of os.name on the system.
- base_options: dictionary
  - Contains one or more lists consisting of zero or more options 
required by the appropriate base_command to output content on STDOUT.
Indexed by the value of os.name.
- type: string
  - String identifier for the compression configuration. (Currently unused.)



## Acknowledgements
- To my friend, Chris Jones, for suggesting I add the option of case-insensitive extension matching.
- To the members of #python on the Libera.Chat IRC network, for patiently enduring my numerous questions.

