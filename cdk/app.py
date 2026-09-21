import aws_cdk

from cdk.settings import CdkSettings
from cdk.stack import Archer

app = aws_cdk.App()
stage = app.node.try_get_context("stage") or "test"

settings = CdkSettings(_env_file=f".env.{stage}")

stack_id = "Archer" if stage == "main" else "Archer-test"
Archer(
    app,
    stack_id,
    stage=stage,
    settings=settings,
)

app.synth()
