# EcoFootprint-app
### How to deploy:
* clone the repository
* copy your terraform credentials to the repository's root directory (EcoFootprint-app)
* go to the repository root directory
* run `terraform plan` and `terraform apply` commands
* if necessary, turn on AppEngine app (AppEngine -> settings -> turn on)
* go to the django website directory (`cd ./django_website` if you're in the repository's root directory)
* run `gcloud app deploy footprint_webapp.yaml`
* after the deployment is finished, the website should be visible under this [link](https://footprintapp-cc-2024l.ew.r.appspot.com/)
