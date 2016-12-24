# libdrafter-py

[![Build Status](https://travis-ci.org/realityone/libdrafter-py.svg?branch=master)](https://travis-ci.org/realityone/libdrafter-py)

> Drafter is complex builder of API Blueprint. Internally it uses Snowcrash library, reference API Blueprint parser.

Drafter binding for python.

## Requirements

- Python 2.7 or greater
- Python 3.5 or greater
- `libdrafter.so` installed correctly


## Installation

### For `libdrafter-py`

```bash
$ pip install libdrafter-py
```

### For `libdrafter.so`

#### Linux

You have to compile `libdrafter.so` by yourself.

```
$ git clone --recursive git://github.com/apiaryio/drafter.git
$ cd drafter
$ python2 ./configure --shared
$ make drafter
$ file ./build/out/Release/lib.target/libdrafter.so
```

*Optional*

Copy `./build/out/Release/lib.target/libdrafter.so` to your library path.

```bash
$ cp ./build/out/Release/lib.target/libdrafter.so /usr/local/lib/libdrafter.so
$ ldconfig
```

#### macOS

If you are using macOS and work with `brew`, you can install `Drafter` by Homebrew.

```bash
$ brew install --HEAD \
  https://raw.github.com/apiaryio/drafter/master/tools/homebrew/drafter.rb
```

## Example/Usage

### Basic usage

For parsing this api blueprint source:

```apib
# GET /message
+ Response 200 (text/plain)

        Hello World!
```

```python
import json
import libdrafter

parser = libdrafter.Parser()

apib = """
# GET /message
+ Response 200 (text/plain)

        Hello World!
"""

parsed = parser.drafter_parse_blueprint_to(apib, drafter_format=libdrafter.Parser.JSON)
print(
    parsed.decode('utf-8')
)
```

Will output:

```json
{
  "element": "parseResult",
  "content": [
    {
      "element": "category",
      "meta": {
        "classes": [
          "api"
        ],
        "title": ""
      },
      "content": [
        {
          "element": "category",
          "meta": {
            "classes": [
              "resourceGroup"
            ],
            "title": ""
          },
          "content": [
            {
              "element": "resource",
              "meta": {
                "title": ""
              },
              "attributes": {
                "href": {
                  "element": "string",
                  "attributes": {
                    "sourceMap": [
                      {
                        "element": "sourceMap",
                        "content": [
                          [
                            1,
                            15
                          ]
                        ]
                      }
                    ]
                  },
                  "content": "/message"
                }
              },
              "content": [
                {
                  "element": "transition",
                  "meta": {
                    "title": ""
                  },
                  "content": [
...
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

### Check API Blueprint

Here is an error API Blueprint:

```apib
# GET /message
+ Response 200 (text/plain)

Hello World!
```

```python
import json
import libdrafter

parser = libdrafter.Parser()

apib = """
# GET /message
+ Response 200 (text/plain)

Hello World!
"""

parsed = parser.drafter_check_blueprint(apib, drafter_format=libdrafter.Parser.JSON)
print(
    parsed.decode('utf-8')
)
```

Will output:

```
...
            ]
          }
        ]
      },
      "content": "dangling message-body asset, expected a pre-formatted code block, indent every of it's line by 8 spaces or 2 tabs"
    }
  ]
}

```

### Avoid Memory leak

To avoid memory leak, pay attention to method `Parser.drafter_parse_blueprint` or `Parser.drafter_check_blueprint` with `serialize_result` is False, you have to free `drafter_result` manually by method `Parser.drafter_free_result`.

## License
libdrafter-py is licensed under the MIT License - see the 
[LICENSE](https://github.com/realityone/libdrafter-py/blob/master/LICENSE) file for details