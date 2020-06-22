# MemesBD
A simplified platform for meme lovers to upload/create/publish/share memes with ease.

### How to run (First time):
1. First create a virtual environment for the project & activate it.  
2. Now install all the dependencies from `requirements.txt`.  
   ```shell script
    pip install -r requirements.txt
   ```
3. Now make migrations and migrate the models.
   ```shell script
   python manage.py makemigrations coreapp accounts memesbd 
   python manage.py migrate
   python manage.py runserver
   ```
This will cause the server to run on localhost:8000 by default.  

#### N.B.
To login/register, a facebook social login app needs to be set up and its credentials are to be configured into the database via admin.
For simplicity a sample data is already dumped to `db.json` with configurations set-up. You can simply load the data using the following command after setting up the project as instructed above.    
```bash
python manage.py loaddata db.json -e contenttypes -e auth -e sessions -e admin  
```
**Or** you can configure the database yourself by going through the following steps:  
**Skip if you have already loaded the data from `db.json`**  
- Create a superuser
    ```shell script
    python manage.py createsuperuser
    ```  
- Now create & configure a facebook login app at https://developers.facebook.com/
- Go to database of project at http://localhost:8000/admin/
- Login with a superuser account you created before.
- After that go to the `Sites` table & add a site with domain name `localhost:8000`.
- Then go to the `Social applications` table.
- Finally add a social app here with your facebook app's `Client id`, `Secret key`, provider as `facebook` and add the site `localhost` to it.  
  
Now you should be able to login to the site at http://localhost:8000/accounts/login/
  
  
### Resetting database:
If you need to reset the previous migrations and migrate new changes, you can easily do that at once with:
- For Windows:
```cmd  
initdb.bat
```
- For Linux:
```bash  
chmod +x initdb.sh
./initdb.sh
```