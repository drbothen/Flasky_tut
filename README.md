## Flasky Tutorial

* To get started clone the repo
* run db_create.py to initialize the database and create the migration repo to track database schema changes
* run db_migrate.py to populate the database with the require tables.
* only run db_upgrade.py and db_downgrade.py if you know what you are doing. those are for moving  between versions of the database during development