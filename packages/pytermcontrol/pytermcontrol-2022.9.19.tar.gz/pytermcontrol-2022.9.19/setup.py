# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytermcontrol']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['with_termcontrol = pytermcontrol.termcontrol:main']}

setup_kwargs = {
    'name': 'pytermcontrol',
    'version': '2022.9.19',
    'description': 'Python Terminal Control',
    'long_description': '# PyTermControl\n\nPython only version of https://github.com/axiros/termcontrol\n\nStarts a command within a pty from a controlling process, which reads "keystrokes" from a fifo and forwards into the child.\nUser input may be forwarded to another fifo, instead of sending it into the child process\' pty.\n\nThis way any terminal process waiting for user input can be controlled from outside.\n\nUSAGE: with_termcontrol [Params] COMMAND\n\n- The fifo filename (`fn_fifo`) is available as `$STDIN_FIFO` within the child. All data on this fifo will be sent into the pty.\n- If fn_fifo is set to \'auto\' then we\'ll create a tempfile fifo\n- If you configure a forward fifo (`fn_user`), then all _user_ input will be forwarded to it,\n  instead of sending into the pty\n- The program will block(!) until a reader is attached to that user fifo\n- `fn_user` simply set to true will result in its filename set to `$STDIN_FIFO` + \'.user\' (and exported as `$USER_INPUT_FIFO`)\n- Fifos will be created only if they don\'t exist at process start\n- Fifos will be unlinked at exit only if they where created by us\n\nParams:\n--fn_user[=False]\n--fn_fifo[=auto]\n',
    'author': 'Gunther Klessinger',
    'author_email': 'g_kle_ss_ing_er@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AXGKl/pytermcontrol',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
