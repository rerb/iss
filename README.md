# iss

Want the ISS Organization and Domain data in your local database?
This this app is for you!

## These files make up the ISS/Salesforce sync.

* salesforce.py pulls data from Salesforce.com.

* models.py includes the logic to translate from the Salesforce object
  (Account, Domain, etc.) to its matching ISS object.

* `upsert_iss_organizations.py` is a script to sync the Salesforce
  Account data into the ISS Organization table.  It upserts
  organizations for Salesforce Accounts that have been modified within
  the past seven days.  The number of days to go back is settable via
  command-line argument.

* `upsert_iss_domains.py` is a script to sync the Salesforce `Domain__c`
  objects into the ISS Domain table.  Like `upsert_iss_organizations.py`,
  it upserts domains for Salesforce `Domain__c` objects that have been
  modified within the past seven days, though the number of days can
  be overridden by command-line argument.

* `sync_iss_domains2orgs.py` is a script to copy the Salesforce
  `DomainsToOrgs__c` objects into the ISS Domains2Orgs table.  It's a
  one-way sync, from Salesforce to ISS (i.e., changes made directly to
  iss.Domains2Orgs records won't bubble up into Salesforce).  It doesn't
  care about `DomainsToOrgs__c` objects that might get deleted, either;
  if there's a matching iss.Domains2Orgs record for a deletion, it lives
  on in iss.db.  We're assuming Salesforce Domains2Orgs don't get deleted.

## Installation

* Add `iss` to your project's settings.INSTALLED_APPS.

* Set the following environmental variables, used to connect to Salesforce:

  * `SALESFORCE_USERNAME`

  * `SALESFORCE_PASSWORD`

  * `SALESFORCE_SECURITY_TOKEN`
