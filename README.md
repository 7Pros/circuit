# circuit

[![Stories in Ready](https://badge.waffle.io/7pros/circuit.png?label=ready&title=Ready)](http://waffle.io/7pros/circuit) [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/7Pros/circuit?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A social network created with Django.

[Live demo](http://circuit.lunarco.de/)

## Installation

First make sure that you have [python](https://www.python.org/), [django](https://docs.djangoproject.com/en/1.8/intro/install/), [redis](http://redis.io/topics/quickstart) & [Node.js](https://nodejs.org/) installed.

Now clone this project to your machine

    git clone https://github.com/7Pros/circuit.git

After that's done go into the created `circuit` folder.

Run

    python manage.py makemigrations
    python manage.py migrate

We use [Bootstrap](http://www.getbootstrap.com/) for the frontend.

To pull in all Bootstrap dependencies we use [bower](http://bower.io/).  
At this point you should already have node installed, so run the following to get bower, if not installed.

    npm install -g bower gulp
    
    npm install

Now you can use bower to fetch all dependencies

    bower install

At last we need gulp to compile all our assets. Simply run gulp

    gulp

You're ready to start the django and the notification server with

    python manage.py runserver

and

    python notification_server

Don't forget to have your redis-server. If you don't know how to do that, just go to your favorite command line program and type:

redis-server

Open [127.0.0.1:8000](http://127.0.0.1:8000/) - DONE

## Development

While developing you will need to run a smtp server, once you try to sign up.

    python -m smtpd -n -c DebuggingServer localhost:1025
    
This will start a smtp server in your command line which django will send emails to.

### Contributing

If you want to contribute you should take a look at [CONTRIBUTING.md](CONTRIBUTING.md).

## Documentation

Check out our [META](https://github.com/7Pros/META) repository. In the [README.md](https://github.com/7Pros/META/blob/master/README.md) you can find all references.

For the code documentation, you can just visit us our [official code documentation](http://7pros.github.io/circuit/)


## Mounting it into a server.

If you want to put this into a server, you should have a look at our [wiki about Amazon Web Services](https://github.com/7Pros/META/wiki/Amazon-Server).
