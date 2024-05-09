# Platform for taxonomy annotation. 

This repository contains the source code of the annotation platform for the Broad Sound Taxonomy.

## How to setup

1. Clone the repo and make the Django migrations for creating the models.
2. To import the necessary data, you would have to request the files that have the available classes, the sounds data and the top level descriptions (`class_choices.csv`, `sounds.csv` and `top_level_info.csv`).
You can import them by running `python manage.py import_classes`, `python manage.py import_sounds` and `python manage.py import_top_descriptions` respectively.

## Instructions for Docker

1. Copy the 3 `csv` files to `annotation/data/` folder.

2. `docker-compose build`

3. `docker-compose run --rm app python manage.py migrate`

4a. `docker-compose run --rm app python manage.py import_classes /code/classurvey/data/class_choices.csv`

4b. `docker-compose run --rm app python manage.py import_top_descriptions /code/classurvey/data/top_level_info.csv`

4c. `docker-compose run --rm app python manage.py import_sounds /code/classurvey/data/sounds.csv`

5. `docker-compose run --rm app python manage.py createsuperuser`

6. `docker-compose up`

7. Open `localhost:8500/` to see the experiment page.

If you want to run an interactive python shell:

`docker-compose run --rm app python manage.py shell_plus`

To import sounds that have been already annotated, run 
`docker-compose run --rm app python manage.py import_sounds_with_annotations /code/classurvey/data/<filename>`.
Be careful not to import groups that have the same group number with the existing ones. 

To expand your sounds for annotation with additional sound groups (post-initial deployment), simply create a new file named `sounds.csv` and import it too (4c). These new sounds will be added alongside the existing ones. 
