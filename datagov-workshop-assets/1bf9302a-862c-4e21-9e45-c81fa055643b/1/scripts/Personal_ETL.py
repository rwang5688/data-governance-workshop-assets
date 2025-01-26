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

warehouse = "s3://"+ account_id + "-"+region+"-datagov-personalbanking-curated"

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

#accounts
#investments
#loans
#transactions
# Script generated for node accounts
AWSGlueDataCatalog_node1729818718870 = glueContext.create_dynamic_frame.from_catalog(database="personalbanking_raw", table_name="raw_accounts", transformation_ctx="AWSGlueDataCatalog_node1729818718870")

# Script generated for node investments
AWSGlueDataCatalog_node1729819885257 = glueContext.create_dynamic_frame.from_catalog(database="personalbanking_raw", table_name="raw_investments", transformation_ctx="AWSGlueDataCatalog_node1729819885257")

# Script generated for node loans
AWSGlueDataCatalog_node1729819992407 = glueContext.create_dynamic_frame.from_catalog(database="personalbanking_raw", table_name="raw_loans", transformation_ctx="AWSGlueDataCatalog_node1729819992407")

# Script generated for node wealth transactions
AWSGlueDataCatalog_node1729817967021 = glueContext.create_dynamic_frame.from_catalog(database="personalbanking_raw", table_name="raw_transactions", transformation_ctx="AWSGlueDataCatalog_node1729817967021")

# Script generated for node Amazon S3
additional_options = {}
tables_collection = spark.catalog.listTables("personalbanking_curated")
table_names_in_db = [table.name for table in tables_collection]
table_exists = "accounts" in table_names_in_db
output_s3_path = "s3://"+ account_id +"-"+ region + "-datagov-personalbanking-curated/accounts"
if table_exists:
    AmazonS3_node1729818782272_df = AWSGlueDataCatalog_node1729818718870.toDF()
    AmazonS3_node1729818782272_df        .writeTo("glue_catalog.personalbanking_curated.accounts") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.append()
else:
    AmazonS3_node1729818782272_df = AWSGlueDataCatalog_node1729818718870.toDF()
    AmazonS3_node1729818782272_df        .writeTo("glue_catalog.personalbanking_curated.accounts") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.create()

# Script generated for node Amazon S3
additional_options = {}
table_exists = "investments" in table_names_in_db
output_s3_path = "s3://"+ account_id +"-"+ region + "-datagov-personalbanking-curated/investments"
if table_exists:
    AmazonS3_node1729819905854_df = AWSGlueDataCatalog_node1729819885257.toDF()
    AmazonS3_node1729819905854_df        .writeTo("glue_catalog.personalbanking_curated.investments") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.append()
else:
    AmazonS3_node1729819905854_df = AWSGlueDataCatalog_node1729819885257.toDF()
    AmazonS3_node1729819905854_df        .writeTo("glue_catalog.personalbanking_curated.investments") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.create()


# Script generated for node Amazon S3
additional_options = {}
table_exists = "loans" in table_names_in_db
output_s3_path = "s3://"+ account_id +"-"+ region + "-datagov-personalbanking-curated/loans"
if table_exists:
    AmazonS3_node1729820035745_df = AWSGlueDataCatalog_node1729819992407.toDF()
    AmazonS3_node1729820035745_df        .writeTo("glue_catalog.personalbanking_curated.loans") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.append()
else:
    AmazonS3_node1729820035745_df = AWSGlueDataCatalog_node1729819992407.toDF()
    AmazonS3_node1729820035745_df        .writeTo("glue_catalog.personalbanking_curated.loans") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.create()

# Script generated for node Amazon S3
additional_options = {}
table_exists = "transactions" in table_names_in_db
output_s3_path = "s3://"+ account_id +"-"+ region + "-datagov-personalbanking-curated/transactions"
if table_exists:
    AmazonS3_node1729818483391_df = AWSGlueDataCatalog_node1729817967021.toDF()
    AmazonS3_node1729818483391_df        .writeTo("glue_catalog.personalbanking_curated.transactions") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.append()
else:
    AmazonS3_node1729818483391_df = AWSGlueDataCatalog_node1729817967021.toDF()
    AmazonS3_node1729818483391_df        .writeTo("glue_catalog.personalbanking_curated.transactions") \
        .tableProperty("format-version", "2") \
        .tableProperty("location", output_s3_path) \
        .tableProperty("write.parquet.compression-codec", "gzip") \
        .options(**additional_options) \
.create()

job.commit()
