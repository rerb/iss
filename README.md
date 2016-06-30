# iss

Want the ISS Organization and Domain data in your local database?
This app is for you!

## These files make up the ISS/Salesforce sync

* salesforce.py pulls data from Salesforce.com.

* models.py includes the logic to translate from the Salesforce object
  (Account, Domain, etc.) to its matching ISS object.

## Django management commands

* `upsert_iss_organizations` is a Django management command to sync
  the Salesforce Account data into the ISS Organization table.  It
  upserts organizations for Salesforce Accounts that have been
  modified within the past seven days.  The number of days to go back
  is settable via the --modified-since/-m command-line argument. To
  upsert Organizations modified within the last 14 days, e.g., do
  `manage.py upsert_iss_organizations -m 14`.
  

* `delete_iss_organizations` is a Django management command to delete
  ISS Organizations that have no matching Salesforce Account (presumably
  because the Account has been deleted). __Note:__ You may want to protect
  your foreign key relationships to Organizations from cascade delete by
  using `on_delete=models.SET_NULL`.

* `upsert_iss_domains` is a Django management command to sync the
  Salesforce `Domain__c` objects into the ISS Domain table.  Like
  `upsert_iss_organizations`, it upserts domains for Salesforce
  `Domain__c` objects that have been modified within the past seven
  days, though the number of days can be overridden by command-line
  argument.

* `sync_iss_domains2orgs` is a Django management command to copy
  the Salesforce `DomainsToOrgs__c` objects into the ISS DomainsToOrgs
  table.  It's a one-way sync, from Salesforce to ISS (i.e., changes
  made directly to iss.Domains2Orgs records won't bubble up into
  Salesforce).  It doesn't care about `DomainsToOrgs__c` objects that
  might get deleted, either; if there's a matching iss.Domains2Orgs
  record for a deletion, it lives on in iss.db.  We're assuming
  Salesforce Domains2Orgs don't get deleted.

## Installation

* Add `iss` to your project's settings.INSTALLED_APPS.

* Run `manage.py migrate iss`.

* Set the following environmental variables, used to connect to Salesforce:

  * `SALESFORCE_USERNAME`

  * `SALESFORCE_PASSWORD`

  * `SALESFORCE_SECURITY_TOKEN`

## About TLS 1.2 Support 

From https://github.com/superfell/Beatbox:

<blockquote>
During 2016 Salesforce plans to
[disable TLS 1.0](https://help.salesforce.com/apex/HTViewSolution?id=000221207)
support on their service.  In order for Beatbox to continue working
you need to use a python environment that supports TLS 1.2, to do that
you need to use Python 2.7.9 (or any newer 2.x version) and your
OpenSSL version needs to be 1.0.1 or greater. You can run `python
--version` to check your python version and `openssl version` to check
your openSSL version. Note that if you're on OSX, its bundled with an
older version of openSSL than is required.  If you see an error
similar to `ssl.SSLError: [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3
alert handshake failure` you need to update your python and/or openSSL
versions.
</blockquote>

Updating your openssl version so Python finds it on OSX is
tricky. Here's what worked for me:

* brew update

* brew install openssl

* brew link openssl --force

* brew uninstall python

* brew install python --with-brewed-openssl

* delete and then recreate any virtualenvs that depend on the updated
  openSSL
