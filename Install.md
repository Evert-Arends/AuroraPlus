#AuroraPlus install guide.

This guide is created to install and maintain the software, Aurora is officially split in 3 parts (dashboard, API, agent). We will try and handle them in that order. *This guide is only for unix users, this is a django application, so it will run on windows, we just don’t  have the resources at the moment to handle the documentation.*

First off, download all 3 of the projects onto the specific servers, you can find them <a href="https://github.com/Evert-Arends/AuroraPlus/">HERE</a>, <a href="https://github.com/Evert-Arends/AuroraPlusBackend/">HERE</a> and <a href="https://github.com/Evert-Arends/AuroraPlusClient/">HERE</a>. Next off install apache and mod_wsgi, if you prefer nginx, you can go wild, it will not affect the application, but it is not official supported by Aurora. You can use the official guides for those installs.

# Dashboard
Go to the home folder of your user, and create a new folder: ‘Applications’, enter it and place ‘master.zip’ there. Unzip it, rename AuroraPlus-master to AuroraPlus, and if everything is right this should be your filetree:

	berm@batsboem:~/Applications $ find . -maxdepth 2 -type d 
	. 
	./AuroraPlus 
	./AuroraPlus/AuroraPlus
	./AuroraPlus/static 
	./AuroraPlus/Aurora 
	./AuroraPlus/controllers
	./AuroraPlus/bin 
	./AuroraPlus/templates
	./AuroraPlus/testing 
	./AuroraPlus/assets

To let the Aurora dashboard run we need to configure apache to work with our application, therefore we need to configure the default website config. 

  	sudo nano /etc/apache2/sites-available/000-default.conf

If there is a document root specified in the config, it would be recommended to remove / out comment that line.

Proceed to add the following:

    Alias /static  /home/USER_HERE/Applications/AuroraPlus/static
    <Directory  /home/USER_HERE/Applications/AuroraPlus/static>
        Require all granted
    </Directory>

    <Directory  /home/USER_HERE/Applications/AuroraPlus/Aurora>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIDaemonProcess AuroraPlus python-path=/home/USER_HERE/Applications/AuroraPlus/ python-home=/home/USER_HERE/Applications/AuroraPlus/
    WSGIProcessGroup AuroraPlus
    WSGIScriptAlias / /home/USER_HERE/Applications/AuroraPlus/Aurora/wsgi.py

It should look something like this:

	<VirtualHost *:80>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		CustomLog ${APACHE_LOG_DIR}/access.log combined

	    Alias /static  /home/USER_HERE/Applications/AuroraPlus/static
	    <Directory  /home/USER_HERE/Applications/AuroraPlus/static>
		Require all granted
	    </Directory>

	    <Directory  /home/USER_HERE/Applications/AuroraPlus/Aurora>
		<Files wsgi.py>
		    Require all granted
		</Files>
	    </Directory>

	    WSGIDaemonProcess AuroraPlus python-path=/home/USER_HERE/Applications/AuroraPlus/ python-home=/home/USER_HERE/Applications/AuroraPlus/
	    WSGIProcessGroup AuroraPlus
	    WSGIScriptAlias / /home/USER_HERE/Applications/AuroraPlus/Aurora/wsgi.py
	</VirtualHost>

Go to the AuroraPlus folder, and chmod the database file to 664:

	chmod 664 db.sqlite3
After the permissions, chown the user to let  apache access:

	sudo chown :www-data ~/Applications/AuroraPlus/db.sqlite3
	sudo chown :www-data ~/Applications/AuroraPlus/

Now we should edit the application to add your server IP to the known hosts, and setup the staticfiles.

	cd ~/Applications/AuroraPlus/Aurora



Edit the settings.py file, and search for STATIC_ROOT

	nano settings.py 
Replace 

	STATIC_ROOT 
With:

	STATIC_ROOT = os.path.join(BASE_DIR, "assets/")
And replace

	ALLOWED_HOSTS = []
With:

	ALLOWED_HOSTS = ['127.0.0.1', 'YOUR SERVER IP HERE']

Set DEBUG false.

Close nano, and go back to the project folder (AuroraPlus) 

Run the following commands:

	./manage.py collectstatic
	./manage.py makemigrations
	./manage.py migrate
	
That should do it. Run apache2ctl configtest, if everything went right, you won’t have any problems. If there are try to resolve those, and after that, run apache2ctl restart.

# API

In this part we will show you how you should run the API. In this scenario we will run the API alongside of the Dashboard, we will run the API on port 8001. This is basically exactly the same, but we change the apache configuration to the right ports. And some other minor tweaks.

Go to the Applications folder, and download (or place) the zip file there, unzip and rename the folder to AuroraPlusBackend. 

Now we have our application, let’s point to  apache  where it has to look

	sudo nano /etc/apache2/sites-enabled/000-default.conf

There is already a virtualhost for 80, let’s create a new host for 8001, because that is the port assigned to the API. Add the following, under the last '</Virtualhost>'. Oh and change 'USERNAME' for your username (of course).

	<VirtualHost *:8001>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		CustomLog ${APACHE_LOG_DIR}/access.log combined

		Alias /static  /home/USERNAME/Applications/AuroraPlusBackend/static
		<Directory  /home/USERNAME/Applications/AuroraPlusBackend/static>
			Require all granted
		</Directory>

		<Directory  /home/USERNAME/Applications/AuroraPlusBackend/AuroraPlusBackend>
			<Files wsgi.py>
				Require all granted
			</Files>
		</Directory>

		WSGIDaemonProcess AuroraPlusBackend python-path=/home/USERNAME/Applications/AuroraPlusBackend/ python-home=/home/USERNAME/Applications/AuroraPlusBackend/
		WSGIProcessGroup AuroraPlusBackend
		WSGIScriptAlias / /home/USERNAME/Applications/AuroraPlusBackend/AuroraPlusBackend/wsgi.py
	</VirtualHost>

Sweet, run the test again (sudo apache2ctl configtest), and if there is an okay, restart apache.

Next up, let’s modify the permissions of the files, navigate to the AuroraPlusBackend folder, and chmod the database.
	
	chmod 664 db.sqlite3
Let’s chown the folders for apache.
	
	sudo chown :www-data ~/Applications/AuroraPlusBackend/db.sqlite3
	sudo chown :www-data ~/Applications/AuroraPlusBackend/
Navigate to the AuroraPlusBackend in the AuroraPlusBackend folder. And edit settings:

	nano settings.py

Edit the settings.py file, and search for STATIC_ROOT
	
	nano settings.py 
Replace STATIC_ROOT with:
	
	STATIC_ROOT = os.path.join(BASE_DIR, "assets/")

And replace

	ALLOWED_HOSTS = []
With:

	ALLOWED_HOSTS = ['127.0.0.1', 'YOUR SERVER IP HERE']
	
Set 'DEBUG' false.

Close nano, and go back to the project folder (AuroraPlusBackend) 

Run the following commands:

	./manage.py collectstatic
	./manage.py makemigrations
	./manage.py migrate

Run the configuration test
	
	sudo apache2ctl configtest
	sudo apache2ctl restart
	
And there you go, API up & running.

# Agent

To get the Agent running:
Unzip the file, and execute:

	python run.py

Follow the steps requested to you by the application, and you should be up & running.

We hope Aurora will be as pleasing to you as it is to us.

Best regards,

The community.
