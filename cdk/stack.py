from aws_cdk import BundlingOptions, Duration, Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as lambda_
from constructs import Construct

from cdk.settings import CdkSettings


class Archer(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stage: str,
        settings: CdkSettings,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        interactions_function = lambda_.Function(
            self,
            "InteractionsHandler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset(
                "src",
                bundling=BundlingOptions(
                    image=lambda_.Runtime.PYTHON_3_12.bundling_image,
                    command=[
                        "bash",
                        "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -r . /asset-output",
                    ],
                ),
            ),
            handler="archer.handler.lambda_handler",
            timeout=Duration.seconds(15),
            memory_size=128,
            reserved_concurrent_executions=2,
            environment={
                "ARCHER_PUBLIC_KEY": settings.archer_public_key,
            },
        )

        api = apigateway.LambdaRestApi(
            self,
            "InteractionsApi",
            handler=interactions_function,
            proxy=False,
            deploy_options=apigateway.StageOptions(
                stage_name=stage,
                throttling_rate_limit=1,
                throttling_burst_limit=2,
            ),
        )

        api.root.add_resource("interactions").add_method("POST")
