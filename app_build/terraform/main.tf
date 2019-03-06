module "build_pipe" {
  source          = "git::ssh://git@github.com/CyberGRX/terraform-aws-grx-codebuild.git?ref=v1.3.2"
  region          = "${var.region}"
  vpc_id          = "${lookup(data.terraform_remote_state.vpc.vpc_id,var.env)}"
  private_subnets = ["${data.terraform_remote_state.vpc.private_subnets["${var.env}"]}"]
  project_name    = "younger-twin-sister"
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
