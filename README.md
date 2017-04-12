[![Build Status](https://travis-ci.org/AASHE/iss.svg?branch=master)](https://travis-ci.org/AASHE/iss) [![Coverage Status](https://coveralls.io/repos/github/AASHE/iss/badge.svg?branch=master)](https://coveralls.io/github/AASHE/iss?branch=master) [![Issue Count](https://codeclimate.com/github/AASHE/iss/badges/issue_count.svg)](https://codeclimate.com/github/AASHE/iss)

# iss

Want the ISS Organization data in your local database?
This app is for you!

## These files make up the ISS/Membersuite sync

* membersuite.py pulls in the Membersuite API client class and instantiates it
  for you. You can then make use of the services provided by the client for
  organization and membership objects.

* models.py includes the logic to translate from the MemberSuite object
  to its matching ISS object.

## Django management commands

* `upsert_iss_organizations` is a Django management command to sync
  the Membersuite Organizations data into the ISS Organization table.

  It upserts organizations for MemberSuite Organizations that have been
  modified within the past seven days.  The number of days to go back
  is settable via the --modified-since/-m command-line argument. To
  upsert Organizations modified within the last 14 days, e.g., do
  `manage.py upsert_iss_organizations -m 14`.

  To sync all organizations, add the flag '--all' instead.

* `upsert_iss_memberships` is a Django management command to sync
  the Membersuite Membeship objects to the ISS Membership table.

  Similar to upserting organizations, use the --modified-since/-m argument
  to set the number of days to go back, or --all to sync all memberships.

  After retrieving this data, it automatically internally syncs with the
  organizations table, updating that to add active memberships to their
  associated organization.

## Installation

* Add `iss` to your project's settings.INSTALLED_APPS. Also add
  'https://github.com/AASHE/python-membersuite-api-client/archive/master.zip'
  (until we get this working on PyPi and can fix setup.py's dependencies).

* Run `manage.py migrate iss`.

* Set the following environmental variables, used to connect to Salesforce:

  * `MS_ACCESS_KEY`

  * `MS_SECRET_KEY`

  * `MS_ASSOCIATION_ID`