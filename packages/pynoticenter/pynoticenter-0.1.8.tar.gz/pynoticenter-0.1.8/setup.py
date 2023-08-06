# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pynoticenter']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0']

entry_points = \
{'console_scripts': ['demo = src.example.demo:main']}

setup_kwargs = {
    'name': 'pynoticenter',
    'version': '0.1.8',
    'description': 'Python client side notification center.',
    'long_description': 'Quickstart\n==========\n\n[![Docs](https://img.shields.io/badge/docs-latest-informational)](https://dzhsurf.github.io/pynoticenter/)\n\nPyPI: [https://pypi.org/project/pynoticenter/](https://pypi.org/project/pynoticenter/)\n\nIntroduction\n------------\n\nPyNotiCenter is a multithreaded task queue and message notification center. It mainly provides in-process lightweight task scheduling management for client applications, that why we choose the multi-threaded mode. Although the multi-threaded mode is not a good practice most of the time in Python(In CPU-bound tasks it can\'t be genuinely parallel as the GIL exists). But in developing client applications, it will be one of the most important base components.\n\nAs it is based on a multi-threaded mode, multi-threaded development must pay attention to thread safety issues, which is inevitable. In order to reduce the complexity for developers, all interfaces of this library are thread safety. It is designed to be called in any thread to guarantee the same results as expected, even though this will cause some performance issues.\n\nThe library mainly provides 2 features.\n\n* Task queue: each task queue will run in a separate thread.\n* Message notification: the message notification scheduling is based on the built-in task queue.\n\nInstall\n-------\n\n```shell\npip install pynoticenter\n```\n\nCode Example\n------------\n\n* Post task to task queue.\n\n```python\ndef fn(*args: Any, **kwargs: Any):\n    print(*args)\n\ndef main():\n    PyNotiCenter.default().post_task(fn, "hello world")\n    PyNotiCenter.default().post_task_with_delay(5, False, fn, "hello", "world", "delay 5s")\n    PyNotiCenter.default().shutdown(wait=True)\n```\n\n```shell\n[2022-09-03 20:54:23,698] {task_queue.py:177} INFO - TaskQueue[4408264928]: worker thread begin.\n[2022-09-03 20:54:23,699] {task_queue.py:46} INFO - TaskQueue[4408264928]: Task queue terminate. wait: True\n[2022-09-03 20:54:23,699] {task_queue.py:105} INFO - TaskQueue[4408264928]: waiting for tasks cleanup. tasks: 2\nhello world\nhello world delay 5s\n[2022-09-03 20:54:28,721] {task_queue.py:114} INFO - TaskQueue[4408264928]: All tasks cleanup. wait time: 5.0\n[2022-09-03 20:54:28,722] {task_queue.py:117} INFO - TaskQueue[4408264928]: waiting for thread exit.\n[2022-09-03 20:54:28,722] {task_queue.py:137} INFO - TaskQueue[4408264928]: stop event run loop.\n[2022-09-03 20:54:28,723] {task_queue.py:200} INFO - TaskQueue[4408264928]: worker thread end.\n[2022-09-03 20:54:29,726] {task_queue.py:126} INFO - TaskQueue[4408264928]: thread exit. wait time: 1.0\n```\n\n```python\n# async func\nasync def async_fn(msg: str):\n  await asyncio.sleep(1)\n  print(f"msg: {msg}")\n\ndef fn(msg: str):\n  print(f"msg: {msg}")\n\ndef main():\n  PyNotiCenter.default().post_task(fn, "hello")\n  PyNotiCenter.default().post_task(async_fn, "hello")\n  PyNotiCenter.default().wait_until_task_complete()\n  PyNotiCenter.default().shutdown(wait=True)\n```\n\n* Notification\n\n```python\nclass A:\n    def say_hello(self, who: str):\n        print(f"{who}: hello")\n\ndef main():\n    receiver = A()\n    PyNotiCenter.default().add_observer("say_hello", receiver.say_hello, receiver)\n    PyNotiCenter.default().notify_observers("say_hello", "baby")\n    ...\n    PyNotiCenter.default().remove_observers(receiver)\n    PyNotiCenter.default().shutdown(wait=True)\n```\n\n* Notification on specific thread, such as Gtk main thread.\n\n```python\ndef fn():\n    pass\n\ndef switch_to_gtk_thread(fn: callable, *args: Any, **kwargs) -> bool:\n    GLib.idle_add(fn)\n    return True\n\ndef main():\n    queue = PyNotiCenter.default().create_task_queue("mytask")\n    queue.set_preprocessor(switch_to_gtk_thread)\n    queue.post_task(fn) # fn run in gtk thread\n\n    # notification run on mytask queue.\n    PyNotiCenter.default().add_observer("say_hello", fn, options=PyNotiOptions(queue="mytask"))\n    PyNotiCenter.default().notify_observers("say_hello")\n```\n',
    'author': 'dzhsurf',
    'author_email': 'dzhsurf@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dzhsurf/pynoticenter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
