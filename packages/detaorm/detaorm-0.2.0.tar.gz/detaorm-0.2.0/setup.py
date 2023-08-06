# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['detaorm']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0']

setup_kwargs = {
    'name': 'detaorm',
    'version': '0.2.0',
    'description': 'An async ORM for DetaBase.',
    'long_description': '# DetaORM\nAn async ORM for DetaBase.\n\n## Example Usage\nHere\'s some examples of DetaORM, with commentary. I\'ll add real documentation at some point.\n\n```py\nfrom detaorm import Client, Base, Field\n\n\n# create your base(s) (or models)\nclass User(Base):\n    # the name of your base\n    __base_name__ = "users"\n\n    # all bases have a `key` field already.\n\n    # typehints are optional. You could write this instead:\n    # username = Field()\n    username: Field[str] = Field()\n    nicknames: Field[list[str]] = Field()\n\n\n# create the client\n# you have to list the bases when creating the client to\n# allow the client to setup properly.\nclient = Client("<project key>", [User])\n\n# actual usage:\nnew_user = User(username="CircuitSacul")\n\n# all fields are optional, but they will raise a KeyError\n# if you try to access them.\n# The following line will raise a KeyError\nnew_user.nicknames\n\n# to actually create the user, you have to call .insert():\ncreated_user = await new_user.insert()\n# created_user and new_user will be identical\n\n# to update an item:\nupdated_user = await new_user.update(\n    User.nicknames.set(["circuit"])\n)\nprint(updated_user)\n# > User({"key": ..., "username": "CircuitSacul", "nicknames": ["Awesome Person"]})\nupdated_user = await updated_user.update(\n    User.nicknames.append(["sacul"])\n)\nprint(updated_user)\n# > User({"key": ..., "username": "CircuitSacul", "nicknames": ["circuit", "sacul"]})\n\n# updated_user and new_user will be different now.\n# DetaORM sends the query to DetaBase, but also tries\n# to determine the updated value and returns a new item.\nprint(new_user)\n# > User({"key": ..., "username": "CircuitSacul"]})\n\n# you can also use Base.insert_many to insert up to 25 items:\nawait User.insert_many([\n    User(username="BatMan", nicknames=["superhero"]),\n    User(username="SuperMan", nicknames=["superhero"]),\n])\n\n# The easiest way to query items is with .where():\nasync for page in await User.where(User.nicknames.contains("superhero")):\n    for user in page.items:\n        print(user)\n# > User({"key": ..., "username": "BatMan", "nicknames": ["superhero"]})\n# > User({"key": ..., "username": "SuperMan", "nicknames": ["superhero"]})\n```\n',
    'author': 'CircuitSacul',
    'author_email': 'circuitsacul@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
