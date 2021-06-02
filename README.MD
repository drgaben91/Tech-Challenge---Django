### Installing the project

###### Installing requirements

`$ ./install.sh`

###### Create admin
The admin is needed to create API users and to manage the database 

`$ python manage.py createsuperuser`

### Launching the application

`$ python manage.py runserver`

###### API Usage examples
I have attached a Postman collection, but I write the features I have added to the API:

- Getting all the records: api/ppd_records
- Getting a record with a specific Transaction ID: /api/ppd_records/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/
- Getting transactions between two dates: /api/ppd_records/?date_of_transfer__gt=2020-03-12 00:00&date_of_transfer__lt=2021-12-12 00:00

The API is not fully online (because of the large file size), so every now and then, a schelued import is due. Simply put the input file in the /PPDDataHandler/input_files/ folder and call the /api/ppd_records/import_csv?filename=xxxxx.csv endpoint
The application runs on SQLite for demonstrative purposes, in production, I'd advise a NoSQL (for example MondgoDB) solution, where we can search the database really fast and efficiently, and since we dont update these records often.

