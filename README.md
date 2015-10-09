# iss

Want the ISS Organization data in your local database?  This this app
is for you!

Depends on the issdjango app.  You'll have to install and configure
that.

Then, after installing this app (i.e., adding it to INSTALLED_APPS
in your Django settings file), run `iss.utils.update_iss_organizations()`.
That'll copy the ISS Organization data into your local database.

Note that the local model name is 'Organization', even though the ISS
table name is 'organizations'.

That is all.
