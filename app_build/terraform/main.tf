module "build_pipe" {
  source          = "git::ssh://git@github.com/CyberGRX/terraform-aws-grx-codebuild.git?ref=v1.3.11"
  region          = "${var.region}"
  vpc_id          = "${lookup(data.terraform_remote_state.vpc.vpc_id,var.env)}"
  private_subnets = ["${data.terraform_remote_state.vpc.private_subnets["${var.env}"]}"]
  project_name    = "younger-twin-sister"
  build_image     = "aws/codebuild/python:3.6.5"
  create_pipe     = "yes"
  include_ecr     = "yes"
  env             = "core"

  parameter_list = [
    "/codebuild/nexus/helm-password",
  ]

  providers = {
    aws.core = "aws.core"
  }
}
