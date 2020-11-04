# Procedures
- Get the first webpage address

- Prevent beyound top level crawling

- fix the url
- Check url protocol on the fixed url

- check to make sure file does not exist on disc

- download the data
- store common name
- check type of data
- store in a variable

- check if parsable
- parse to
  - gather more urls
  - construct fullpath
  - replace data

- Save the data

- handle external urls
  - download ext data
   - downloading data currently does not check for redirections
     because replace has already happened.
  - save data offline

- check if more urls exist

- clear all other variables

- repeat

## External Files Handling
Checking to see if external url is a file
 The url may contain dots(.)
 eg: https://www.facebook.com/we.are.xampp

## Naming
The downloaded should be kept in a folder
 - folder name should be the domain
 - filenames should be based on the filenames itself
 - resources should be organised as they are as if on the server
 - the external should be kept in folder named __external
 - external should be organised this way:
   - __external
     - facebook.com
       - javascript
         - jquery.min.js
