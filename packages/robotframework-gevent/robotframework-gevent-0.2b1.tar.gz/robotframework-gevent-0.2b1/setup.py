# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['GeventLibrary', 'GeventLibrary.exceptions', 'GeventLibrary.keywords']

package_data = \
{'': ['*']}

install_requires = \
['gevent>=21.12.0,<22.0.0',
 'robotframework-pythonlibcore>=3.0.0,<4.0.0',
 'robotframework>=5.0.1,<6.0.0']

setup_kwargs = {
    'name': 'robotframework-gevent',
    'version': '0.2b1',
    'description': 'Run keywords asynchronously with the power of gevent',
    'long_description': '# robotframework-gevent\nRun keywords asynchronously with the power of gevent\n\n![Coverage](./docs/badges/coverage-badge.svg) ![MutationScore](./docs/badges/mutscore.svg) ![Pylint](./docs/badges/pylint.svg)  [![Version](https://img.shields.io/pypi/v/robotframework-gevent.svg)](https://pypi.python.org/pypi/robotframework-gevent)\n\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n\n## installation:\n```\n>>> pip install robotframework-gevent\n```\n\n## Usage:\n\n```\n# simple-test.robot\n*** Settings ***\n\nLibrary             Collections\nLibrary             String\nLibrary             GeventLibrary\nLibrary             RequestsLibrary\n\n\n*** Test Cases ***\nTest1\n    [Documentation]    Simple test flow with gevent greenlets\n    Log    Hello World\n    Create Gevent Bundle    alias=alias1 # Create a bundle of coroutines\n    Sleep    10s    alias=alias1    # run your synchronous keyword\n    # register all your keywords as coroutines to the gevent bundle\n    Add Coroutine    Sleep Wrapper    alias=alias1\n    Add Coroutine    Sleep    20s    alias=alias1\n    Add Coroutine    Sleep    10s    alias=alias1\n    Add Coroutine    GET    https://jsonplaceholder.typicode.com/posts/1    alias=alias1\n    Add Coroutine    Convert To Lower Case    UPPER\n\n    # Run your coroutines and get the values by order\n    ${values}    Run Coroutines    alias=alias1\n    Log Many    @{values}\n\n    # The 3rd coroutine was a request, take it\'s value\n    ${jsonplaceholder_resp}    Get From List    ${values}    3\n\n    # assert the returned response code to be 200\n    Status Should Be    200    ${jsonplaceholder_resp}\n    # assert that the returned `userId` field equals to 1\n    Should Be Equal As Strings    1    ${jsonplaceholder_resp.json()[\'userId\']}\n\n\n*** Keywords ***\nSleep Wrapper\n    Sleep    1s\n\n```\n\n\nSee -  [Keyword Documentation](https://eldaduzman.github.io/robotframework-gevent/GeventLibrary.html)\n### run test:\n```\n>>> robot simple-test.robot\n```\n### Possible result\n\nAfter test is completed go to `log.html`:\n\n![](./docs/images/Possible-Log-File.png)\n\n\nOwing to the fact that keywords are executed asynchronously, we cannot know the order of keyword execution, so instead they are printed in a table format\n\n## Motivation\n\nModern software architecture is `event driven`, with many background process.\nServers are being more pro-active instead of re-active as we see in a `client server` architecture.\n\nIn order to test such systems, we need the ability to run coroutines in our test scripts.\n\nWith the power of [gevent](http://www.gevent.org/), we can run several coroutines in greenlets, so integrating them into our robotframework test script will provide super powers to our testing efforts!\n\n## Why gevent?\n\nConcurrency can be achieved in 3 different ways:\n\n1.  Multiprocessing - running each task in it\'s own `process`.\n    The cons of such an approach would be massive consumption of resources, namely CPU and memory, as this means to allocate an entire `memory heap` to each task.\n    Another problem is a possible need for `Inter-Process Communication (IPC)` that might be costly.\n\n2.  Multithreading - running each task in a `thread`.\n    Unlike multiprocessing, now all tasks run on the same memory heap and separated by threads, which the CPU coordinates using `round-robin`.\n    However, python\'s  `Global Interpreter Lock` (GIL) prevents these threads from acting concurrently, it might perform context switching when IO operation occurs but there\'s no control for that.\n\n\n3.  Asynchronous IO - running all tasks on a single thread, while IO operations won\'t block the progress of the program, while code execution is committed by an   `event loop` that `selects` between attached `coroutines`.\n    This is highly efficient in resources consumption when compared to multithreading and multiprocessing, but it requires some modifications to the original code.\n    `Blocking` IO statements can hog the event loop and the code will not be concurrent.\n    `gevent` allows programmers to write seemingly regular "blocking" python code, but it will enforce asynchronous IO compliance by `monkey patching`\n\n## File structure\n```\n\n|   LICENSE\n|   .gitignore\n|   .pylintrc\n|   pyproject.toml\n|   poetry.lock\n|   README.md\n\n|           \n+---src\n|   \\---GeventLibrary\n|       |   \\---exceptions\n|       |       |   __init__.py\n|       |   \\---keywords\n|       |       |   __init__.py\n|       |       |   gevent_keywords.py\n|       |   __init__.py\n|       |   gevent_library.py\n|               \n+---atests\n|   |   __init__.robot\n|   |   simple-test.robot\n|   |   \n|   \\---utests\n|       |   __init__.py\n|       |   test_bundle_creation.py\n\n```\n## Code styling\n### `black` used for auto-formatting code [read](https://pypi.org/project/black/),\n### `pylint` used for code linting and pep8 compliance [read](https://pypi.org/project/pylint/),\n### `mypy` used for type hinting [read](https://pypi.org/project/mypy/),\n### `robocop` static code analyzer for robotframework [read](https://pypi.org/project/robotframework-robocop/),\n### `perflint` pylint extension for performance linting [read](https://betterprogramming.pub/use-perflint-a-performance-linter-for-python-eae8e54f1e99)\n### `cosmic-ray` Python tool for mutation testing [read](https://python.plainenglish.io/python-mutation-testing-with-cosmic-ray-4b78eb9e0676)\n\n## links\n1. [Robotframework](https://robotframework.org/)\n2. [gevent](http://www.gevent.org/)',
    'author': 'Eldad Uzman',
    'author_email': 'eldadu1985@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eldaduzman/robotframework-gevent',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
