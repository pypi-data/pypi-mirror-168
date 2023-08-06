# BLC Data Analytics tools package

Data Analytics helper functions to work with inside BLC's Cloud system.

# Changelog
## Version 0.0.1
* Basic functionality is up and running

## Version 0.0.2 ~ 0.0.4
Fixed the install issues

## Version 0.0.5
* Most of the code is Object Oriented now.
* CAMMESA's forecasts have been added.

## Version 0.0.6 ~ 0.0.7
* Bug fixes regarding file management
* Ability to customize filters when hitting CAMMESA's API
* PBA calculation according to IEC61400 is still functioning incorrectly

## Version 0.0.8
* Corrected dependencies list

## Version 0.0.9
* Removed dependencies list
* Ability to download unfiltered PPOs/DTEs without specifying parks/plants list
* Incidents are no longer loaded by default on blctools.DatosCrom() objects
* TO DO: Use SQLAlchemy to retrieve SQL data with pandas.