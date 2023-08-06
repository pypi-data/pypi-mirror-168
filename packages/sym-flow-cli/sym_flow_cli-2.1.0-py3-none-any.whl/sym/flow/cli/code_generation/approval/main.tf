locals {
  environment_name = "main"
}

provider "sym" {
  org = "${var.sym_org_slug}"
}

resource "sym_flow" "this" {
  name  = "approval"
  label = "Approval"

  template       = "sym:template:approval:1.0.0"
  implementation = "${path.module}/impl.py"
  environment_id = sym_environment.this.id

  # These variables are made available in your impl.py via `event.flow.vars`
  vars = {
    # You can add more emails to this as a comma separated list, e.g. auto_approve = "jon@doe.com,jane@doe.com"
    # This variable is used in the `on_request` hook in impl.py!
    auto_approve = "${var.user_email}"
  }

  params = {
    # If you want a Flow with an escalation strategy, add your strategy_id here!
    # strategy_id = ...

    # prompt_fields_json defines custom form fields for the Slack modal that
    # requesters fill out to make their requests.
    prompt_fields_json = jsonencode([
      {
        name     = "resource"
        label    = "What do you need access to?"
        type     = "string"
        required = true
      },
      {
        name     = "reason"
        label    = "Why do you need access?"
        type     = "string"
        required = true
      }
    ])
  }
}

# The sym_environment is a container for sym_flows that share configuration values
# (e.g. shared integrations or error logging)
resource "sym_environment" "this" {
  name            = local.environment_name
  runtime_id      = sym_runtime.this.id
  error_logger_id = sym_error_logger.slack.id

  integrations = {
    slack_id = sym_integration.slack.id

    # Add your integration IDs here!
  }
}

resource "sym_integration" "slack" {
  type = "slack"
  name = "${local.environment_name}-slack"

  external_id = "${var.slack_workspace_id}"
}

# This sym_error_logger will output any warnings and errors that occur during
# execution of a sym_flow to a specified channel in Slack.
resource "sym_error_logger" "slack" {
  integration_id = sym_integration.slack.id

  # Make sure that this channel has been created in your workspace
  destination    = "#sym-errors"
}

resource "sym_runtime" "this" {
  name = local.environment_name

  # For AWS IAM, SSO, Lambda strategies, add your context ID here! For example:
  # context_id = sym_integration.runtime_context.id
}
