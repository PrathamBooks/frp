# Pratham FRP

Fund raising platform for Pratham books.

## Directories

* `docs` - Documentation for the project
* `frp` - The main project directory
  * `alembic.ini` - Alembic config file.
  * `frp` - The frp python package.
     * `models.py` - Database models
	 * `templates` - Jinja2 templates
	 * `_version.py` - Version of the project (included in app footer)
	 * `views.py` - View functions.
  * `manage.py` - Flask-script entry point for management tasks. 
  * `migrations` - Alembic migration data (automatically created)
  * `run.py` - Run `python run.py` to start the application.
  * `settings.py` - Local settings file
* `Makefile` - Top level tasks (like making documentation etc.)
* `notes.org` - Notes that I (Noufal Ibrahim) keep while working on the project.
* `README.md` - This file.
* `requirements.txt` - External dependencies for the app.
* `vagrant` - Vagrant VM for non Linux users (Currently out of date)
