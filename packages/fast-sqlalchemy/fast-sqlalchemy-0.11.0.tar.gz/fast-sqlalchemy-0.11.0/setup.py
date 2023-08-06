# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_sqlalchemy',
 'fast_sqlalchemy.authentication',
 'fast_sqlalchemy.cli',
 'fast_sqlalchemy.config',
 'fast_sqlalchemy.event_bus',
 'fast_sqlalchemy.logging',
 'fast_sqlalchemy.persistence',
 'fast_sqlalchemy.testing']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyJWT>=2.4.0,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'SQLAlchemy-Utils>=0.38.3,<0.39.0',
 'SQLAlchemy>=1.4.40,<2.0.0',
 'alembic>=1.8.1,<2.0.0',
 'factory-boy>=3.2.1,<4.0.0',
 'fastapi>=0.79.0,<0.80.0',
 'html2text>=2020.1.16,<2021.0.0',
 'pyhumps>=3.7.2,<4.0.0',
 'python-dotenv>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['fast-sqla = fast_sqlalchemy.cli.entry_point:main'],
 'pytest11': ['fast_sqlalchemy = fast_sqlalchemy.testing.pytest']}

setup_kwargs = {
    'name': 'fast-sqlalchemy',
    'version': '0.11.0',
    'description': 'Make application with Fastapi and Sqlalchemy with ease',
    'long_description': '# Welcome to fast-sqlalchemy\n\nThis project was first made to provide some tools to use Fastapi with SQLAlchemy with ease.\n## Contents\n\n- [Installation](#installation)\n- [The database middlewares](#the-database-middlewares)\n    - [The DatabaseMiddleware](#the-databasemiddleware)\n    - [The AutocommitMiddleware](#the-autocommitmiddleware)\n- [The event bus](#the-event-bus)\n- [The yaml config reader](#the-yaml-configuration-loader)\n\n## Installation\n\nInstallation using pip:\n```shell\npip install fast_sqlalchemy\n```\n\nOr with poetry:\n```shell\npoetry add fast_sqlalchemy\n```\n\n## The database middlewares\nFast-sqlalchemy provide multiple middlewares to use SQLAlchemy with Fastapi easily\n\n### The DatabaseMiddleware\nThe main middleware is the database middleware which is made to provide a sqlalchemy session accessible throughout your\napplication. We use the ContextVar api of python to have unique session in the context of each request.\n\nTo use this middleware you must at first create a Database object where you must pass the url of your database and the \nengine options of SQLAlchemy:\n\n```python\ndb = Database(\n    URL.create(\n        drivername="mariadb+pymysql", username = config["database"]["user"].get(str),\n        password=config["database"]["password"].get(str),\n        host =config["database"]["host"].get(str), database = config["database"]["name"].get(str)),\n    autoflush=False\n)\n```\nAnd then register the database middleware:\n\n```python\nfastapi = FastAPI()\nfastapi.add_middleware(DatabaseMiddleware, db=db)\n```\nAfter that you can have access to the sqlalchemy session of the current request, through the property session of the Database object in the entire application:\n\n```python\ndb.session.query(User).first()\n```\nNote that if you want to have access to a sqlalchemy session outside a request context, you must create a session by \nusing the session contextmanager of the Database object:\n\n```python\nwith db.session_ctx():\n    db.session.query(User).all()\n```\nThe middleware is actually using this contextmanager for each request.\n\n### The AutocommitMiddleware\nThe auto commit middleware as its name suggest is a middleware which automatically commit at the end of each request. \nIt must be used with the database middleware and must be registered before otherwise it won\'t work:\n\n```python\nfastapi = Fastapi()\nfastapi.add_middleware(AutocommitMiddleware, db=db)\nfastapi.add_middleware(DatabaseMiddleware, db=db)\n```\n\n## The event bus\nThe event bus provide you a way to emit event in your application and register handlers to handle them. This allows\nyou to create an event-driven architecture for your application. \n\nTo use the event bus within your application, you must create at least one event bus\nand register the event bus middleware to the fastapi middlewares stack\n```python\nfastapi = FastAPI()\nevent_bus = LocalEventBus()\nfastapi.add_middleware(EventBusMiddleware, buses=[event_bus])\n```\nOnce the middleware is registered with an event bus you can start creating events and event handlers.\nEvent can be any python object, the most practical way is to create dataclass object:\n\n```python\n@dataclass\nclass EmailChanged:\n    email: str\n```\nThen you can add an event handler for this event:\n\n```python\n@local_event_bus.handler(EmailChanged)\ndef check_email_uniqueness(e: EmailChanged):\n    # some logic\n    pass\n```\nThere are two kinds of handler sync and async handler. Sync handlers are called once the event is emitted, \nwhereas async handlers are called at the end of the current request.\nTo register an async handler is nearly the same as above\n\n```python\n@local_event_bus.async_handler(EmailChanged, OtherEvent)\ndef check_email_uniqueness(e: EmailChanged | OtherEvent):\n    # some logic\n    pass\n```\nNote that a handler can handle multiple types of event\n\nAfter that you can emit events wherever you want in your Fastapi application:\n\n```python\nemit(EmailChanged(email=email))\n```\n\n## The database testing class\n\nFast-sqlalchemy provide a utility class named TestDatabase which can be used to test your Fastapi application with \nSQLAlchemy with ease. This class allow you to have isolated test by having each test wrapped in a transaction that is \nrollback at the end of each test, so that each test have a fresh database.\n\nTo use it with pytest, you can simply create two fixtures.\nA primary fixture with a scope of \'session\' which will create a connection to the database and create the database if it \ndoesn\'t exist (A testing database is created with the same name of your application\'s database prefixed with \'test_\'). \nThe testing database is then dropped at the end (You can optionally turn if off).\n\n```python\nfrom my_app import factories\n\n@pytest.fixture(scope="session")\ndef db_client():\n    db_client = TestDatabase(db=app_db, factories_modules=[factories])\n    with db_client.start_connection(metadata=metadata):\n        yield db_client\n```\nNote that this class is compatible with the library factory_boy, you can register as shown in the example above a list \nof modules which contains your factory classes so that each factory wil be bound to the session provided by the TestDatabase object.\n\nAfter that you can create a second fixture:\n\n```python\n@pytest.fixture()\ndef sqla_session(db_client):\n    with db_client.start_session() as session:\n        yield session\n```\nThis fixture will provide a sqlalchemy session to your tests:\n\n```python\ndef test_create_user(sqla_session):\n    user = UserFactory()\n    assert sqla_session.query(User).first().id == user.id\n```\n\n## The yaml configuration loader\n\nFast-sqlalchemy provide a class named Configuration which allow you to have your application\'s configuration store in yaml files:\n\n```python\nROOT_DIR = os.path.dirname(os.path.abspath(__file__))\nconfig = Configuration(os.path.join(ROOT_DIR, "config"), env_path=os.path.join(ROOT_DIR, ".env"))\nconfig.load_config(config="test")\n```\nWhen you\'re creating the object you must specify the path of your configuration directory, this directory will contain all of your yaml files.\nYou can also specify a .env file which will be read thanks to the dotenv library.\nThen you can load these configurations file by calling __load_config__, you can specify a config name, this config name must\nmatch a subdirectory within the configuration directory. This subdirectory should contain yaml files that will be merged\nwith the yaml files present at the root of the configuration directory. This way you can have multiple configurations witch \nwill share the same base configuration.\nThe configuration folder may look like this:\n```\n+-- config\n|   +-- base.yaml\n|   +-- other.yaml\n|   +-- test\n|    |   +-- base.yaml\n|   +-- prod\n|    |   +-- base.yaml\n```\n\nNote that you can use your environment variables within your yaml files, these variables will be parsed.\n\n```yaml\nproject_name: ${PROJECT_NAME}\nsecret_key: ${SECRET_KEY}\nlocal: fr_FR\n```\nThen you can have access to your configuration within your application like this:\n\n```python\nconfig["general"]["project_name"]\n```\nor with the __get__ method witch accept dot-separated notation and a default\nvalue as second parameter.\n```python\nconfig.get("general.project_name", "default_name")\n```\nNote that, if a key is not found in yaml files, as fallback we\'ll try to find the\nkey in environment or raise a KeyError exception if not present. \n\n## Licence\n\nThis project is licensed under the terms of the MIT license.\n\n',
    'author': 'Clement_Hue',
    'author_email': 'clementhue@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Chaisenbois/fast-alchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
