import aws_cdk as core
from aws_cdk import aws_lambda as lambda_

from cdk.settings import CdkSettings
from cdk.stack import Archer


def test_stack_contains_interactions_api_and_lambda():
    app = core.App()
    stack = Archer(
        app,
        "ArcherTest",
        stage="test",
        settings=CdkSettings(archer_public_key="test-public-key"),
    )

    interactions_function = stack.node.find_child("InteractionsHandler")
    interactions_api = stack.node.find_child("InteractionsApi")

    assert isinstance(interactions_function, lambda_.Function)
    assert interactions_api is not None
