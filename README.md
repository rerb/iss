[![Build Status](https://travis-ci.org/AASHE/iss.svg?branch=master)](https://travis-ci.org/AASHE/iss) [![Coverage Status](https://coveralls.io/repos/github/AASHE/iss/badge.svg?branch=master)](https://coveralls.io/github/AASHE/iss?branch=master) [![Issue Count](https://codeclimate.com/github/AASHE/iss/badges/issue_count.svg)](https://codeclimate.com/github/AASHE/iss)

# iss

Want the ISS Organization data in your local database?
This app is for you!

## These files make up the ISS/Salesforce sync

* salesforce.py pulls data from MemberSuite.

* models.py includes the logic to translate from the MemberSuite object
  to its matching ISS object.

## Django management commands

* `upsert_iss_organizations` is a Django management command to sync
  the Salesforce Account data into the ISS Organization table.  It
  upserts organizations for MemberSuite Organizations that have been
  modified within the past seven days.  The number of days to go back
  is settable via the --modified-since/-m command-line argument. To
  upsert Organizations modified within the last 14 days, e.g., do
  `manage.py upsert_iss_organizations -m 14`.
  

* `delete_iss_organizations` is a Django management command to delete
  ISS Organizations that have no matching MemberSuite Account (presumably
  because the Account has been deleted). __Note:__ You may want to protect
  your foreign key relationships to Organizations from cascade delete by
  using `on_delete=models.SET_NULL`.

## Installation

* Add `iss` to your project's settings.INSTALLED_APPS.

* Run `manage.py migrate iss`.

* Set the following environmental variables, used to connect to Salesforce:

  * `MS_ACCESS_KEY`

  * `MS_SECRET_KEY`

  * `MS_ASSOCIATION_ID`
