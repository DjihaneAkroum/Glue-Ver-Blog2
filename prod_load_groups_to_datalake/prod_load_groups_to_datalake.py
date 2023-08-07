import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3
import json

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

def get_secret():
    secret_name = "glue_prod_postgresql_secret"
    region_name = "eu-central-1"
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    secret = json.loads(secret)
    return secret
    
def get_groups_table_from_postgresql_server(spark):
    
    table = "groups"
    
    secret = get_secret()
    username = secret.get("username")
    password = secret.get("password")
    host = secret.get("host")
    port = secret.get("port")
    dbname = "live-editor"
    jdbcUrl = "jdbc:postgresql://{0}:{1}/{2}".format(host, port, dbname)
    
    groupsDF = spark.read.format("jdbc") \
                   .option("url",jdbcUrl) \
                   .option("dbtable", table) \
                   .option("user", username) \
                   .option("password", password) \
                   .option("driver", "org.postgresql.Driver") \
                   .load()
    
    #OrgUsersDF.printSchema()
    #print(OrgUsersDF.count())    
    return groupsDF    

from delta.tables import *


groupsDF = get_groups_table_from_postgresql_server(spark)

groupsDF.write.format("parquet").mode("overwrite").option("overwriteSchema", "true").save("s3://data-analysis-datalake/prod/silver/groups") 

job.commit()