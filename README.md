# EcoFootprint-app
### How to deploy on GCP:
* clone the repository
* copy your terraform credentials to the repository's root directory (EcoFootprint-app)
* go to the repository root directory
* run `terraform plan` and `terraform apply` commands
* if necessary, turn on AppEngine app (AppEngine -> settings -> turn on)
* go to the django website directory (`cd ./django_website` if you're in the repository's root directory)
* run `gcloud app deploy footprint_webapp.yaml`
* after the deployment is finished, the website should be visible under this [link](https://footprintapp-cc-2024l.ew.r.appspot.com/)
* download Cloud SQL Auth Proxy (see point 2 of `Download Cloud SQL Auth Proxy to connect to Cloud SQL from your local machine` section from [this tutorial](https://cloud.google.com/python/django/appengine#windows_3)
* run the cloud sql proxy with the parameter footprintapp-cc-2024l:europe-west1:postgres-instance
* set the environment variables (this is for Windows, on linux change `set` to `export` and add "" between the values of variables:
  * set DB_NAME=footprint_db
  * set DB_USER=postgres
  * set DB_PASSWORD=postgres
  * set DJANGO_SETTINGS_MODULE=footprint_webapp.settings
  * set INSTANCE_CONNECTION_NAME=footprintapp-cc-2024l:europe-west1:postgres-instance
  * set DB_HOST=127.0.0.1
  * set DB_PORT=5432
