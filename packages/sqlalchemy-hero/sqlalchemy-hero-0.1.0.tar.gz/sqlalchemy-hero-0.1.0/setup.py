# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_hero', 'sqlalchemy_hero.types']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'SQLAlchemy-Utils>=0.38,<0.39',
 'SQLAlchemy>=1.4,<2.0',
 'arrow>=1.2,<2.0']

setup_kwargs = {
    'name': 'sqlalchemy-hero',
    'version': '0.1.0',
    'description': 'SchemaHero table generator from SQLAlchemy models.',
    'long_description': '# SQLAlchemy Hero\n\nSQLAlchemy Hero is a package to generate table YAMLs for\n[SchemaHero](https://schemahero.io/) from a\n[SQLAlchemy](https://www.sqlalchemy.org/) Base.\n\nLet\'s look at an example how to use it.\nThere is a `Parent` and a `Child` model both\ninheriting from a abstract base model with some common fields.\nThe goal is to generate the table YAML files for `SchemaHero`.\n\nThe `HeroGenerator` class implements the methods to extract the model.\nIt is initialized with your declarative base from `SQLAlchemy`,\nthe database type you\'re using (currently `postgres` and `mysql`),\nthe namespace where the tables should be deployed and the database name.\n\nThe `to_yaml_files` method allowes to specify the output path for the\ngenerated YAMLs (defaults to `Path("./out")`).\n\n```python\nfrom pathlib import Path\n\nfrom sqlalchemy import Column\nfrom sqlalchemy import ForeignKey\nfrom sqlalchemy import Integer\nfrom sqlalchemy import Text\nfrom sqlalchemy import func\nfrom sqlalchemy.orm import declarative_base\nfrom sqlalchemy.orm import relationship\nfrom sqlalchemy_utils import ArrowType\n\nfrom sqlalchemy_hero.hero_database import HeroDatabase\nfrom sqlalchemy_hero.hero_generator import HeroGenerator\n\nDeclarativeBase = declarative_base()\n\n\nclass Base(DeclarativeBase):\n    __abstract__ = True\n\n    id = Column(Integer, primary_key=True)\n    created_on = Column(ArrowType, default=func.now())\n    updated_on = Column(ArrowType, default=func.now(), onupdate=func.now())\n\n\nclass Parent(Base):\n    __tablename__ = "parent"\n\n    name = Column(Text)\n    ss_number = Column(Integer, autoincrement=True)\n    children = relationship("Child")\n\n\nclass Child(Base):\n    __tablename__ = "child"\n\n    name = Column(Text, nullable=False)\n    description = Column(Text, nullable=False, index=True)\n    parent_id = Column(Integer, ForeignKey("parent.id"))\n\n\nhero_generator = HeroGenerator(\n    base=Base,\n    db_type=HeroDatabase.postgres,\n    namespace="hero-ns",\n    database="hero-db",\n)\nhero_generator.to_yaml_files(out_path=Path("./out"))\n```\n\n### Type Overrides\n\nThe library tries to implement the most common types but it\'s hard to\nkeep up with all the possiblities for the different databases.\nIf you find a not yet mapped type (commonly used with `SQLAlchemy`) please\nopen a pull request to add it.\n\nFor custom types or quick fixes you can override the types\n(the dict entries override/add to the current types).\n\n```python\nCUSTOM_TYPE_MAPPINGS = {\n    MyCustomType: "text",  # add new type mappings\n    Integer: "serial",  # override existing mappings\n}\n\nhero_generator = HeroGenerator(\n    base=Base,\n    db_type=HeroDatabase.postgres,\n    namespace="hero-ns",\n    database="hero-db",\n    db_type_override=CUSTOM_TYPE_MAPPINGS,  # add the mappings on init\n)\nhero_generator.to_yaml_files()\n```\n\n### API Version\n\nWe try to update the default API version for `SchemaHero` to the latest.\nIf you wish to use another version or if we haven\'t updated yet it can be\nspecified on initializing the `HeroGenerator`.\n\n```python\nhero_generator = HeroGenerator(\n    base=Base,\n    db_type=HeroDatabase.postgres,\n    namespace="hero-ns",\n    database="hero-db",\n    api_version="schemas.schemahero.io/custom-version",\n)\nhero_generator.to_yaml_files()\n```\n\n## QA Commands\n\nThe below commands are run in the pipeline and the according checks\nare expected to pass.\n\n```bash\npoetry run pytest\npoetry run black .\npoetry run isort .\npoetry run pylint tests sqlalchemy_hero\npoetry run -r sqlalchemy_hero\n```\n',
    'author': 'Matthias Osswald',
    'author_email': 'matthias@busykoala.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/busykoala/sqlalchemy-hero',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
