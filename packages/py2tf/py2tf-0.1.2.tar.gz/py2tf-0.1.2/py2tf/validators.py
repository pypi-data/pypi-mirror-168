import json
import re


class Rule:
    condition: str
    message: str
    comment: str

    def __init__(self, condition, message, rule_name) -> None:
        self.condition = condition
        self.message = message
        self.comment = f"Automatically Generated from Rule: {rule_name}"


"""
The function names in this file all correspond with the attributes in
JSONSchema, which in turn are returned by pydantic. Each function returns a
Terraform conditional and an error message for when that condition is not
matched.
"""


def exclusiveminimum(name, value):
    return Rule(
        condition=f"var.{name} > {value}",
        message=f"Field should be larger than {value}",
        rule_name="gt",
    )


def minimum(name, value):
    return Rule(
        condition=f"var.{name} >= {value}",
        message=f"Field should be greater than or equal to {value}",
        rule_name="ge",
    )


def exclusivemaximum(name, value):
    return Rule(
        condition=f"var.{name} < {value}",
        message=f"Field should be smaller than {value}",
        rule_name="lt",
    )


def maximum(name, value):
    return Rule(
        condition=f"var.{name} <= {value}",
        message=f"Field should be less than or equal to {value}",
        rule_name="le",
    )


def multipleof(name, value):
    return Rule(
        condition=f"var.{name} % {value} == 0",
        message=f"Field should be a multiple of {value}",
        rule_name="multipleof",
    )


def minitems(name, value):
    return Rule(
        condition=f"length(var.{name}) >= {value}",
        message=f"Field should contain at least {value} items",
        rule_name="minitems",
    )


def maxitems(name, value):
    return Rule(
        condition=f"length(var.{name}) <= {value}",
        message=f"Field should contain at most {value} items",
        rule_name="maxitems",
    )


def minlength(name, value):
    return Rule(
        condition=f"length(var.{name}) >= {value}",
        message=f"Field should not be less than {value} characters",
        rule_name="minlength",
    )


def maxlength(name, value):
    return Rule(
        condition=f"length(var.{name}) <= {value}",
        message=f"Field should not be larger than {value} characters",
        rule_name="maxlength",
    )


def uniqueitems(name, value):
    return Rule(
        condition=f"length(distinct(var.{name})) == length(var.{name})",
        message=f"Field should only contain unique items",
        rule_name="uniqueitems",
    )


def pattern(name, value):
    # Terraform needs the pattern as a string, which means we need to escape slashes.
    pattern = make_regex_simple(value).replace("\\", "\\\\")
    return Rule(
        condition=f'length(regexall("{pattern}", var.{name})) > 0',
        message=f"Field does not match regex pattern {pattern}",
        rule_name="pattern",
    )


def oneof(name, value):
    pretty_list = ", ".join([str(x) for x in value])
    terraform_list = json.dumps(value)
    return Rule(
        condition=f"contains({terraform_list}, var.{name})",
        message=f"Field should be one of: {pretty_list}",
        rule_name="oneof",
    )


# https://stackoverflow.com/a/14919203/212774
# https://creativecommons.org/licenses/by-sa/4.0/
def make_regex_simple(verbose):
    WS_RX = r"(?<!\\)((\\{2})*)\s+"
    CM_RX = r"(?<!\\)((\\{2})*)#.*$(?m)"

    return re.sub(WS_RX, "\\1", re.sub(CM_RX, "\\1", verbose))
