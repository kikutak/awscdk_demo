from aws_cdk import (core,
                     aws_apigateway as apigateway,
                     aws_lambda as lambda_,
                     aws_s3 as s3,
                     aws_s3_deployment as s3deploy)

class DemoStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create s3 bucket
        bucket = s3.Bucket(self, "cdkdemobucket",
                    block_public_access = s3.BlockPublicAccess(
                        block_public_acls = True,
                        block_public_policy = True,
                        ignore_public_acls = True,
                        restrict_public_buckets = True
                    ),
                    bucket_name = "cdkdemobucket"
                    )

        # upload local file to s3 bucket
        deploy = s3deploy.BucketDeployment(self, 'DeployLocal',
                    sources = [s3deploy.Source.asset('resources/s3')],
                    destination_bucket = bucket)

        handler = lambda_.Function(self, "toppage",
                    runtime=lambda_.Runtime.PYTHON_3_7,
                    code=lambda_.Code.asset("resources/webapp/artifact"),
                    handler="webapp.main",
                    environment=dict(
                        BUCKET=bucket.bucket_name)
                    )

        bucket.grant_read_write(handler)

        #api gateway
        api = apigateway.RestApi(self, "demo page",
                    rest_api_name="demo page"
                    )
#        api.root.add_resource("{id}")
        get_top_page = apigateway.LambdaIntegration(handler,
                    request_templates={"application/json": '{ "statusCode": "200" }'}
                    )

        api.root.add_method("GET", get_top_page)
#        api.root.add_method("POST", get_top_page)
#        api.root.add_method("DELETE", get_top_page)