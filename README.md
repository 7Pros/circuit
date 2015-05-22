# circuit

[![Stories in Ready](https://badge.waffle.io/7pros/circuit.png?label=ready&title=Ready)](http://waffle.io/7pros/circuit) [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/7Pros/circuit?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## Installation

First make sure that you have [python](https://www.python.org/), [django](https://docs.djangoproject.com/en/1.8/intro/install/) & [Node.js](https://nodejs.org/) installed.

Now clone this project to your machine

    git clone https://github.com/7Pros/circuit.git

After that's done go into the created `circuit` folder.

Run

    python manage.py makemigrations
    python manage.py migrate

We use [Bootstrap](http://www.getbootstrap.com/) for the frontend.

To pull in all Bootstrap dependencies we use [bower](http://bower.io/).  
At this point you should already have node installed, so run the following to get bower, if not installed.

    npm install -g bower

Now you can use bower to fetch all dependencies

    bower install

You're ready to start the django webserver with

    python manage.py runserver

Open [127.0.0.1:8000](http://127.0.0.1:8000/) - DONE

### Contributing

If you want to contribute you should take a look at [CONTRIBUTING.md](CONTRIBUTING.md).

