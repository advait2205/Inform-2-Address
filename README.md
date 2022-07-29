# Inform-2-Address
This is public complaint system made in order to serve following purpose:
- Citizens can click an image anywhere and the system will take care of bundling it alongwith other complaints and tagging related authority of that category in social media platform like Twitter/Telegram
- Authorities can use this system to check any complaints tagged to them filtered by various criteria.
- Has an Admin Panel to manage authorities and smooth going of the system.

Tech Stack Used:
- HTML
- CSS
- Javascript
- Bootstrap
- Django
- PostgreSQL

Features Implemented till now:
- Login/Logout functionality
- Show List of Complaints
- Filter Complaints by various criteria such as Location, Own Complaints, Start-Time, Expected End Time
- Add Complaints
- Manage Authority
- Allow Admin to view particular Authority statistics
- Script done to post complaint alongwith image and description to Telegram Group
- Succesfully allow software to asynchronously post to Telegram using Script

Features to-be implemented:
- Solve Image Storage Issue

## Setting up the site locally on computer

1. Clone the repo using following commnad

```
git clone https://github.com/advait2205/Inform-2-Address.git
```

2. Fill the details in .env_example file and rename it to ".env".

3. Now, open this folder in the terminal and run the following command to install the dependencies
```
pip install -r requirements.txt
```

4. Now, run the following command to start the server locally.
```
python manage.py runserver
```

5. Click on this url to see the site: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
