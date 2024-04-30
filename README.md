# Riget Zoo Adventures Booking Website

This website built for RZA includes booking, booking management, lesson article management, lesson article viewing and authentication features.

This is all built on the basis of Python 3.11.4 and Flask 3.0.2.

## Installation

To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```

## Configuration

To configure the website, duplicate the `config.example.json` file and rename it to `config.json`. Then, fill in the required fields.

```json
{
    "SECRET_KEY": "YOUR_SECRET_KEY",
    "DATABASE_URI": "YOUR_DATABASE_URI",
    "DATABASE_USER": "YOUR_DATABASE_USERNAME",
    "DATABASE_PASSWORD": "YOUR_DATABASE_PASSWORD",
    "DATABASE_NAME": "YOUR_DATABASE_NAME",
    "DEBUG": false
}
```

## First Time Setup

To setup the database, run the following command:

```bash
python website setup
```

## Usage

To run the development server for the website, run the following command:

```bash
python website run
```

If you want to run the website in a production mode, you can use something like gunicorn behind a reverse proxy like Nginx to serve the website.
This can be done with a command like this:

```bash
gunicorn -w 4 -b 0.0.0.0 -k gevent wsgi:app
```
However if you didn't already know that, you should probably stick to the development server and not run the website in production.

## License

[MIT](https://choosealicense.com/licenses/mit/)