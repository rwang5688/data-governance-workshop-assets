import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.conf import SparkConf
conf = SparkConf()


args = getResolvedOptions(sys.argv, ['JOB_NAME', 'region', 'account_id'])
account_id = args['account_id']
region = args['region']

warehouse = "s3://"+ account_id + "-"+region+"-datagov-insurance-curated"

conf.set("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")\
        .set("spark.sql.catalog.glue_catalog", "org.apache.iceberg.spark.SparkCatalog")\
        .set("spark.sql.catalog.glue_catalog.warehouse", warehouse)\
        .set("spark.sql.catalog.glue_catalog.catalog-impl", "org.apache.iceberg.aws.glue.GlueCatalog")\
        .set("spark.sql.catalog.glue_catalog.io-impl", "org.apache.iceberg.aws.s3.S3FileIO")\
        .set("spark.sql.catalog.glue_catalog.glue.lakeformation-enabled","true")\
        .set("spark.sql.catalog.glue_catalog.glue.id",account_id)

sc = SparkContext(conf=conf)
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

#appointments
#claims
#insurance_plans
#policies
#policy_holder
#providers

# Script generated for node appointments
AWSGlueDataCatalog_node1729818718870 = glueContext.create_dynamic_frame.from_catalog(database="insurance_raw", table_name="raw_appointments", transformation_ctx="AWSGlueDataCatalog_node1729818718870")

# Script generated for node claims
AWSGlueDataCatalog_node1729819885257 = glueContext.create_dynamic_frame.from_catalog(database="insurance_raw", table_name="raw_claims", transformation_ctx="AWSGlueDataCatalog_node1729819885257")

# Script generated for node insurance_plans
AWSGlueDataCatalog_node1729820233916 = glueContext.create_dynamic_frame.from_catalog(database="insurance_raw", table_name="raw_insurance_plans", transformation_ctx="AWSGlueDataCatalog_node1729820233916")

# Script generated for node policies
AWSGlueDataCatalog_node1729820315829 = glueContext.create_dynamic_frame.from_catalog(database="insurance_raw", table_name="raw_policies", transformation_ctx="AWSGlueDataCatalog_node1729820315829")

# Script generated for node policy_holder
AWSGlueDataCatalog_node1729819992407 = glueContext.create_dynamic_frame.from_catalog(database="insurance_raw", table_name="raw_policy_holders", transformation_ctx="AWSGlueDataCatalog_node1729819992407")

# Script generated for node wealth transactions
AWSGlueDataCatalog_node1729817967021 = glueContext.create_dynamic_frame.from_catalog(database="insurance_raw", table_name="raw_providers", transformation_ctx="AWSGlueDataCatalog_node1729817967021")

# Script generated for node Amazon S3
additional_options = {}
tables_collection = spark.catalog.listTables("insurance_curated")
table_names_in_db = [table.name for table in tables_collection]
table_exists = "appointments" in table_names_in_db
output_s3_path = "s3://"+ account_id +"-"+ region + "-datagov-insurance-curated/appointments"
if table_exists:
    AmazonS3_node1729818782272_df = AWSGlueDataCatalog_node1729818718870.toDF()
    AmazonS3_node1729818782272_df        .writeTo("glue_catalog.insurance_curated.appointments") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.append()
else:
    AmazonS3_node1729818782272_df = AWSGlueDataCatalog_node1729818718870.toDF()
    AmazonS3_node1729818782272_df        .writeTo("glue_catalog.insurance_curated.appointments") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.create()

# Script generated for node Amazon S3
additional_options = {}
table_exists = "claims" in table_names_in_db
output_s3_path = "s3://"+ account_id +"-"+ region + "-datagov-insurance-curated/claims"
if table_exists:
    AmazonS3_node1729819905854_df = AWSGlueDataCatalog_node1729819885257.toDF()
    AmazonS3_node1729819905854_df        .writeTo("glue_catalog.insurance_curated.claims") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.append()
else:
    AmazonS3_node1729819905854_df = AWSGlueDataCatalog_node1729819885257.toDF()
    AmazonS3_node1729819905854_df        .writeTo("glue_catalog.insurance_curated.claims") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.create()

# Script generated for node Amazon S3
additional_options = {}
table_exists = "insurance_plans" in table_names_in_db
output_s3_path = "s3://"+ account_id +"-"+ region + "-datagov-insurance-curated/insurance_plans"
if table_exists:
    AmazonS3_node1729820255975_df = AWSGlueDataCatalog_node1729820233916.toDF()
    AmazonS3_node1729820255975_df        .writeTo("glue_catalog.insurance_curated.insurance_plans") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.append()
else:
    AmazonS3_node1729820255975_df = AWSGlueDataCatalog_node1729820233916.toDF()
    AmazonS3_node1729820255975_df        .writeTo("glue_catalog.insurance_curated.insurance_plans") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.create()

# Script generated for node Amazon S3
additional_options = {}
table_exists = "policies" in table_names_in_db
output_s3_path = "s3://"+ account_id +"-"+ region + "-datagov-insurance-curated/policies"
if table_exists:
    AmazonS3_node1729820342533_df = AWSGlueDataCatalog_node1729820315829.toDF()
    AmazonS3_node1729820342533_df        .writeTo("glue_catalog.insurance_curated.policies") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.append()
else:
    AmazonS3_node1729820342533_df = AWSGlueDataCatalog_node1729820315829.toDF()
    AmazonS3_node1729820342533_df        .writeTo("glue_catalog.insurance_curated.policies") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.create()

# Script generated for node Amazon S3
additional_options = {}
table_exists = "policy_holders" in table_names_in_db
output_s3_path = "s3://"+ account_id +"-"+ region + "-datagov-insurance-curated/policy_holders"
if table_exists:
    AmazonS3_node1729820035745_df = AWSGlueDataCatalog_node1729819992407.toDF()
    AmazonS3_node1729820035745_df        .writeTo("glue_catalog.insurance_curated.policy_holders") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.append()
else:
    AmazonS3_node1729820035745_df = AWSGlueDataCatalog_node1729819992407.toDF()
    AmazonS3_node1729820035745_df        .writeTo("glue_catalog.insurance_curated.policy_holders") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.create()

# Script generated for node Amazon S3
additional_options = {}
table_exists = "providers" in table_names_in_db
output_s3_path = "s3://"+ account_id +"-"+ region + "-datagov-insurance-curated/providers"
if table_exists:
    AmazonS3_node1729818483391_df = AWSGlueDataCatalog_node1729817967021.toDF()
    AmazonS3_node1729818483391_df        .writeTo("glue_catalog.insurance_curated.providers") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.append()
else:
    AmazonS3_node1729818483391_df = AWSGlueDataCatalog_node1729817967021.toDF()
    AmazonS3_node1729818483391_df        .writeTo("glue_catalog.insurance_curated.providers") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.create()

job.commit()
