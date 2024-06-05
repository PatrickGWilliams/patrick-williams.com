terraform {
  backend "pg" {
    conn_str = "postgres://localhost/PatWillWebsiteDB?sslmode=disable"
  }
}

