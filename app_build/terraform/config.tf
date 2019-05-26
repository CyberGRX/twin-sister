terraform {
  backend "s3" {
    bucket         = "grx-core-tfstate"
    key            = "younger-twin-sister-buildpipe"
    region         = "us-east-1"
    dynamodb_table = "cybergrx-tflock"
  }
}

provider "aws" {
  alias  = "core"
  region = "${var.region}"

  assume_role {
    role_arn = "arn:aws:iam::${lookup(var.account_numbers, "core")}:role/terraform-role"
  }
}

provider "aws" {
  alias  = "main"
  region = "${var.region}"

  assume_role {
    role_arn = "arn:aws:iam::${lookup(var.account_numbers, "main")}:role/terraform-role"
  }
}

provider "aws" {
  region = "${var.region}"

  assume_role {
    role_arn = "arn:aws:iam::${lookup(var.account_numbers, var.env)}:role/terraform-role"
  }
}

data "terraform_remote_state" "vpc" {
  backend = "s3"

  config {
    bucket = "grx-core-tfstate"
    key    = "vpc"
    region = "us-east-1"
  }
}
