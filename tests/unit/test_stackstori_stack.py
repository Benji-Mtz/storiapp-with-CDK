import aws_cdk as core
import aws_cdk.assertions as assertions

from stackstori.stackstori_stack import StackstoriStack

# example tests. To run these tests, uncomment this file along with the example
# resource in stackstori/stackstori_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = StackstoriStack(app, "stackstori")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
