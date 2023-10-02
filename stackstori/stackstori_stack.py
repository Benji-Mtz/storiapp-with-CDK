import os
from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_,
    Tags as tags_,
    aws_iam as iam_,
    aws_s3 as s3_,
    aws_s3_notifications as notification_,
    Fn as fn_,
    BundlingOptions, Duration, CfnElement
)
from constructs import Construct


class StackstoriStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # The code that defines your stack goes here

        # region Parametros
        ProjectName = fn_.import_value('projectStori')
        EnvName = fn_.import_value('environmentStori')
        # endregion

        LambdaRoleS3Account = iam_.Role(self, "lambdaroles3account",
                                        assumed_by=iam_.ServicePrincipal(
                                            "lambda.amazonaws.com"),
                                        path="/service-role/",
                                        managed_policies=[
                                            iam_.ManagedPolicy.from_aws_managed_policy_name(
                                                "service-role/AWSLambdaVPCAccessExecutionRole"),
                                            iam_.ManagedPolicy.from_aws_managed_policy_name(
                                                "service-role/AWSLambdaBasicExecutionRole"),
                                            iam_.ManagedPolicy.from_aws_managed_policy_name(
                                                "AmazonS3ReadOnlyAccess"),
                                        ],
                                        inline_policies={
                                            "lambdapolices3account": iam_.PolicyDocument(
                                                statements=[iam_.PolicyStatement(
                                                    actions=["logs:CreateLogGroup",
                                                             "logs:CreateLogStream",
                                                             "logs:PutLogEvents",
                                                             "lambda:InvokeFunction",
                                                             "lambda:InvokeAsync",],
                                                    resources=["*"],
                                                    effect=iam_.Effect.ALLOW,
                                                )]
                                            )
                                        }
                                        )

        # Lambda that reads CCL and load elements in accounts table
        lambdaTriggerFromS3 = lambda_.Function(self, "lambdaTriggerFromS3",
                                               architecture=lambda_.Architecture.X86_64,
                                               environment={
                                                   'EMAIL_ADDRESS': "",
                                                   'EMAIL_PASSWORD': "",
                                                   'EMAIL_RECEIVER': "",
                                               },
                                               runtime=lambda_.Runtime.PYTHON_3_9,
                                               timeout=Duration.seconds(15),
                                               handler="lambda_function.lambda_handler",
                                               code=lambda_.Code.from_asset("Functions",
                                                                            bundling=BundlingOptions(
                                                                                image=lambda_.Runtime.PYTHON_3_9.bundling_image,
                                                                                command=["bash", "-c", "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
                                                                                         ]
                                                                            )
                                                                            ),
                                               role=LambdaRoleS3Account,
                                               )

        # Adding Tags to Lambda Data informatio User
        tags_.of(lambdaTriggerFromS3).add('Name', 'storiApp')
        tags_.of(lambdaTriggerFromS3).add('Ambiente', 'Dev')
        tags_.of(lambdaTriggerFromS3).add('Runtime', 'Python 3.9')
        tags_.of(lambdaTriggerFromS3).add('Tipo', 'Lambda')

        s3 = s3_.Bucket.from_bucket_arn(
            self, "storiapp", "arn:aws:s3:::storiapp")

        # create trigger for lambda function
        notification = notification_.LambdaDestination(lambdaTriggerFromS3)
        notification.bind(self, s3)

        # assign notification for the s3 event type (ex: OBJECT_CREATED)
        s3.add_object_created_notification(
            notification, s3_.NotificationKeyFilter(prefix="", suffix=".csv"))
