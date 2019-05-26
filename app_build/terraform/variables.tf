#Boiler Plate Variables
variable "account_numbers" {
  description = "Map of account numbers matched to environement"
  type        = "map"

  default = {
    main    = "551321121225"
    staging = "001096032920"
    core    = "746807083977"
    dev     = "122189113537"
    prod    = "528335337478"
  }
}

variable "env" {
  description = "The environment to deploy into"
  type        = "string"
  default     = "core"
}

variable "region" {
  description = "The AWS region"
  type        = "string"
  default     = "us-east-1"
}
