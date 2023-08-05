# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asynctinydb']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'nest-asyncio>=1.5.5,<2.0.0',
 'ujson>=5.4.0,<6.0.0']

extras_require = \
{':python_version <= "3.10"': ['typing-extensions>=3.10.0,<5.0.0']}

setup_kwargs = {
    'name': 'async-tinydb',
    'version': '1.1.4',
    'description': 'Yet Another Async TinyDB',
    'long_description': '![logo](https://raw.githubusercontent.com/msiemens/tinydb/master/artwork/logo.png)\n\n## What\'s This?\n\n"An asynchronous IO version of `TinyDB` based on `aiofiles`."\n\nAlmost every method is asynchronous. And it\'s based on `TinyDB 4.7.0+`.  \nI will try to keep up with the latest version of `TinyDB`.\n\nSince I modified it in just a few hours, I\'m not sure if it\'s stable enough for production.  \nBut hey! It passed all the tests anyways.\n\n## Major Changes\n* **asynchronous** Say goodbye to blocking IO.\n* **drop support** Only supports Python 3.8+.\n* **event hooks** You can now use event hooks to do something before or after an operation. see [Event Hooks](#event-hooks) for more details.\n* **redesigned id & doc class** Now the ID class and Document class are more abstract. You can use your own class to replace the default ones in a more pleasing way.\n  As long as they are inherited from `asynctinydb.table.BaseID/BaseDocument`. The default ID class is `IncreID`, which mimics the behaviours of the original `int` ID but requires much fewer IO operations.\n\n## Minor differences from the original `TinyDB`:\n\n* **lazy-load:** When `access_mode` is set to `\'r\'`, `FileNotExistsError` is not raised until the first read operation.\n\n* **ujson:** Using `ujson` instead of `json`. Some arguments aren\'t compatible with `json`\n  Why not `orjson`? Because `ujson` is fast enough and has more features.\n  \n* **Storage `closed` property** Original `TinyDB` won\'t raise exceptions when operating on a closed file. Now the property `closed` of `Storage` classes is required to be implemented. An `IOError` will be raised.\n  \n  I strongly suggest doing the same for `middleware`.\n\n## How to use it?\n\n#### Installation\n\n```Bash\npip install async-tinydb\n```\n\n#### Importing\n```Python\nfrom asynctinydb import TinyDB, where\n```\n\n\nBasically, all you need to do is insert an `await` before every method that needs IO.\n\nNotice that some parts of the code are blocking, for example when calling `len()` on `TinyDB` or `Table` Objects.\n\n#### Event Hooks\nEvent Hooks give you more flexibility than middleware.\nFor example, you can achieve compress/decompress data without creating a new Storage class.\n\nCurrently only supports storage events: `write.pre`, `write.post`, `read.pre`, `read.post`, `close`.\n\n* `write.pre` is called before json dumping, args: `str`(event name), `Storage`, `dict`(data).\n* `write.post` is called after json dumping, args: `str`(event name), `Storage`, `str|bytes`(json str or bytes).\n  Only one function can be registered for this event. Return non `None` value will be written to the file.\n* `read.pre` is called before json loading, args: `str`(event name), `Storage`, `str|bytes`(json str or bytes).\n  Only one function can be registered for this event. Return non `None` value will be used as the data.\n* `read.post` is called after json loading, args: `str`(event name), `Storage`, `dict`(data).\n* `close` is called when the storage is closed, args: `str`(event name), `Storage`.\n\nFor `write.pre` and `read.post`, you can directly modify data to edit its content.\n\nHowever, `write.post` and `read.pre` requires you to return the value to update content because `str` is immutable in Python. If no return value or returns a `None`, you won\'t change anything.\n\n```Python\ns = Storage()\n# By accessing the attribute `on`, you can register a new func to the event\n@s.on.write.pre\nasync def f(ev, s, data):  # Will be executed on event `write.pre`\n  ...\n```\n\n\n\n## Example Codes:\n\n### Simple One\n\n```Python\nimport asyncio\nfrom asynctinydb import TinyDB, Query\n\nasync def main():\n    db = TinyDB(\'test.json\')\n    await db.insert({"answer": 42})\n    print(await db.search(Query().answer == 42))  # >>> [{\'answer\': 42}] \n\nasyncio.run(main())\n```\n### Event Hooks Example\n\n```Python\nasync def main():\n    db = TinyDB(\'test.json\')\n    @db.storage.on.write.pre\n    async def mul(ev: str, s: Storage, data: dict):\n        data["_default"]["1"][\'answer\'] *= 2  # directly manipulate on data\n    @db.storage.on.write.post\n    async def _print(ev, s, anystr):\n      \tprint(anystr)  # print json dumped string\n    await db.insert({"answer": 21})\n    await db.close()\n    # Reload\n    db = TinyDB(\'test.json\')\n    print(await db.search(Query().answer == 42))  # >>> [{\'answer\': 42}] \n```\n',
    'author': 'VermiIIi0n',
    'author_email': 'dungeon.behind0t@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/VermiIIi0n/async-tinydb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
