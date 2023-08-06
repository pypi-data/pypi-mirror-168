from sym.sdk.annotations import hook, reducer
from sym.sdk.integrations import slack
from sym.sdk.templates import ApprovalTemplate


# Reducers fill in the blanks that your workflow needs in order to run.
@reducer
def get_approvers(event):
    """Route Sym requests to a specified channel."""

    # Make sure that this channel has been created in your workspace!
    return slack.channel("#sym-requests")


# Hooks let you change the control flow of your workflow.
@hook
def on_request(event):
    """Auto-approve people defined in the auto-approve list in the sym_flow vars"""

    flow_vars = event.flow.vars
    auto_approve = flow_vars["auto_approve"].split(",")

    if event.user.username in auto_approve:
        original_reason = event.payload.fields.get("reason")
        new_reason = f"Auto-approved! {original_reason}️"
        return ApprovalTemplate.approve(reason=new_reason)
