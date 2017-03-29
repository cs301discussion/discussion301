## CS 301 Discussion Parser

This utility allows you to parse the disussion posts on blackboard to determine
who has posted and who has not. It uploads the results to a Google Spreadsheet
that you have to make yourself.

## Requirements

To use the program you need some way to handle SAML2 authentication. To do this,
we use package called 'selenium'. This package runs a browser (of our choice)
and allows us to control it programmatically. To remove the overhead of having
a browser running with the program, we use a headless browser called 'PhantomJS'.
This is a system-wide package that you should install. This can be done using
your package-manager or from source. Alternatively, you could use a normal
browser like firefox or chrome. To do this, look at the top of the 
getDiscussionPage method in the 'blackboard.py' file.

This program was written to run on Linux using python 3+. The python requirements
are gspread, selenium, and oauth2client which can be installed using pip or by 
downloading and running the install script. 
[Python module install guide](https://docs.python.org/3.6/installing/index.html)

You also need a Google account besides your university one to use this program
since the school blocks you from using the developer tools console.

## OAuth Setup
The most difficult part of this is getting your Google API setup. To use Gspread,
which allows you to interface with Google Spreadsheet, you need to enable Drive
API and create a project. Then you generate service account credentials for use
by the gsread module. Take a look at the [documents from gspread](http://gspread.readthedocs.io/en/latest/oauth2.html?highlight=oauth). 

Once you do this, you need to download the json file with your credentials and place
it in the same directory as this code. Then, open google.py and look for the 
`CREDENTIALS_FILE_NAME` variable up top. Replace this file name with the name of the 
json credentials you just downloaded. 

Next, create an empty spreadsheet in your Google drive account (not Binghamton one). I
would avoid using spaces in this name. Then, in `google.py`, change the 
`SPREADSHEET_NAME` variable to match your file name. Now you're all set to interact with
Google drive. You can test this by running the `google.py` script directly like 
`./google.py`, or if the permissions are changed `python3 google.py`. This will
initialize the file. I wouldn't run this after you've been collecting data, but you
will have to run it again once you setup your common file.

## Common File\Student Names
In `common.py` there are two lists for storing some constant data. The first is 
`STUDENTS` and it is the one that you will have to change. You need to copy students
names exactly as they appear on blackbaord so that they can be properly found
on the webpages. 

You can alter the `DISUCSSIONS` variable if new posts are added or if the names are
altered. 

## Main Program Setup
These program requires a few things to run. You will need to change the `BB_USERNAME` 
variable to match your username and you will have to accommodate for your password. 
However it is not smart to store passwords in plaintext, so I have been using 
environment variables. I call mine `BBPASS` and I set it by doing
```
export BBPASS='MyPasswordhere'
```
You can put this line in something like a `.bash_profile` or other similar file that
runs on startup if you do not want to run it manually when you restart your computer. 
Besides login credentials you also need to change the `COURSE_TEXT` variable to match
your section name. Take a look on your blackboard home page and take the corresponding
part as shown in the code.

Last, you need to specify the browser you are using. I am using firefox installed
in a non-standard location so I have added some extra lines up top for that sake.
You will not need this and can comment them out if you want. You still need to then
change the first line in the `getDiscussionPage()` method to use your corresponding
browser. In a comment I show what to do for a normal FireFox install, but you can
take a look at the Selenium documentation for how to use it with Chrome or something
else. Now you're ready to run it.

## Running the Program
Now that it is all setup, you can run it!! To run it, simply execute like any other
command line program and pass to it section numbers separated by spaces. e.g.
```
./blackboard.py 2.1 2.2 2.3
```
Then, you can watch your browser open up and navigate through the pages. Once it looks
through the posts you will see it pause a little, and you can take a look at the 
spreadsheet and see it input values in to it. Then it will resume and finish off the 
remaining posts.
