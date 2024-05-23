
provider "google" {
  credentials = file("/home/michal12tomczyk/footprintapp-cc-2024l-klucz.json")
  project     = "footprintapp-cc-2024l"
  region      = "europe-west1"
}

# APIs enabled by hand beforhand
# Service Usage API
# Cloud Resource Manager API


# Enabling APIs
resource "google_project_service" "service_usage_api" {
  service = "serviceusage.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloud_resource_manager_api" {
  service = "cloudresourcemanager.googleapis.com"
  disable_on_destroy = false
  depends_on = [google_project_service.service_usage_api]
}

resource "google_project_service" "app_engine_api" {
  service = "appengine.googleapis.com"
  depends_on = [google_project_service.cloud_resource_manager_api]
}

resource "google_project_service" "cloud_sql_api" {
  service = "sqladmin.googleapis.com"
  depends_on = [google_project_service.cloud_resource_manager_api]
}

resource "google_app_engine_application" "app" {
  project     = "footprintapp-cc-2024l"
  location_id = "europe-west"
  depends_on  = [google_project_service.app_engine_api]
}

resource "google_sql_database_instance" "postgres_instance" {
  name             = "postgres-instance"
  database_version = "POSTGRES_12"
  region           = "europe-west1"
  settings {
    tier = "db-f1-micro"
  }
  deletion_protection = false
  depends_on = [google_project_service.cloud_sql_api]
}

resource "google_sql_database" "footprint_db" {
  name     = "footprint_db"
  instance = google_sql_database_instance.postgres_instance.name
  depends_on = [google_project_service.cloud_sql_api]
}

resource "google_storage_bucket" "static_resources" {
  name          = "static-resources-bucket-${google_project_service.service_usage_api.project}"
  location      = "EU"
  force_destroy = true
  uniform_bucket_level_access = true
  depends_on    = [google_project_service.service_usage_api]
}
