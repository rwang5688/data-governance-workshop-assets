#!/bin/sh

# A: Create domain
ACCOUNTID=`aws sts get-caller-identity --query "Account"  --output text`
DOMAINID=`aws datazone create-domain --domain-execution-role arn:aws:iam::$ACCOUNTID:role/DataZoneDomainExecutionRole --name CorporateDomain --query 'id' --output text`

# B: Prepare domain - Revised to always set ACCOUNTID and DOMAINID; change role to Admin
ACCOUNTID=`aws sts get-caller-identity --query "Account"  --output text`
DOMAINID=`aws datazone list-domains --query "items[?name=='CorporateDomain'].id" --output text`
ROOTDOMAINUNITID=`aws datazone get-domain --identifier $DOMAINID --query 'rootDomainUnitId' --output text`
INSDOMAINUNITID=`aws datazone create-domain-unit --domain-identifier $DOMAINID --name "Insurance" --parent-domain-unit-identifier $ROOTDOMAINUNITID --query 'id' --output text`
WLTHDOMAINUNITID=`aws datazone create-domain-unit --domain-identifier $DOMAINID --name "Wealth Management" --parent-domain-unit-identifier $ROOTDOMAINUNITID --query 'id' --output text`
PERSDOMAINUNITID=`aws datazone create-domain-unit --domain-identifier $DOMAINID --name "Personal Banking" --parent-domain-unit-identifier $ROOTDOMAINUNITID --query 'id' --output text`
SHAREDDOMAINUNITID=`aws datazone create-domain-unit --domain-identifier $DOMAINID --name "Shared Services" --parent-domain-unit-identifier $ROOTDOMAINUNITID --query 'id' --output text`
aws datazone add-policy-grant --detail createProject={includeChildDomainUnits=true} --domain-identifier $DOMAINID --entity-identifier $ROOTDOMAINUNITID --entity-type DOMAIN_UNIT --policy-type CREATE_PROJECT --principal user={userIdentifier="arn:aws:iam::$ACCOUNTID:role/Admin"}

# C-1: Create Projects - Revised to always set ACCOUNTID and DOMAINID
ACCOUNTID=`aws sts get-caller-identity --query "Account"  --output text`
DOMAINID=`aws datazone list-domains --query "items[?name=='CorporateDomain'].id" --output text`
DOMAINMETAPROJECTID=`aws datazone create-project --domain-identifier $DOMAINID --domain-unit-id $ROOTDOMAINUNITID --name "Domain Metadata" --query 'id' --output text`
INSMETAPROJECTID=`aws datazone create-project --domain-identifier $DOMAINID --domain-unit-id $INSDOMAINUNITID --name "Insurance Metadata" --query 'id' --output text`
WLTHMETAPROJECTID=`aws datazone create-project --domain-identifier $DOMAINID --domain-unit-id $WLTHDOMAINUNITID --name "Wealth Management Metadata" --query 'id' --output text`
PERSMETAPROJECTID=`aws datazone create-project --domain-identifier $DOMAINID --domain-unit-id $PERSDOMAINUNITID --name "Personal Banking Metadata" --query 'id' --output text`
INSDATAPROJECTID=`aws datazone create-project --domain-identifier $DOMAINID --domain-unit-id $INSDOMAINUNITID --name "Insurance Data Products" --query 'id' --output text`
WLTHDATAPROJECTID=`aws datazone create-project --domain-identifier $DOMAINID --domain-unit-id $WLTHDOMAINUNITID --name "Wealth Management Data Products" --query 'id' --output text`
PERSDATAPROJECTID=`aws datazone create-project --domain-identifier $DOMAINID --domain-unit-id $PERSDOMAINUNITID --name "Personal Banking Data Products" --query 'id' --output text`
CUST360PROJECTID=`aws datazone create-project --domain-identifier $DOMAINID --domain-unit-id $SHAREDDOMAINUNITID --name "Customer 360" --query 'id' --output text`
aws datazone add-policy-grant --detail createGlossary={includeChildDomainUnits=false} --domain-identifier $DOMAINID --entity-identifier $INSDOMAINUNITID --entity-type DOMAIN_UNIT --policy-type CREATE_GLOSSARY --principal '{"project": {"projectDesignation": "CONTRIBUTOR", "projectIdentifier":"'$INSMETAPROJECTID'"}}'
aws datazone add-policy-grant --detail createGlossary={includeChildDomainUnits=false} --domain-identifier $DOMAINID --entity-identifier $WLTHDOMAINUNITID --entity-type DOMAIN_UNIT --policy-type CREATE_GLOSSARY --principal '{"project": {"projectDesignation": "CONTRIBUTOR", "projectIdentifier":"'$WLTHMETAPROJECTID'"}}'
aws datazone add-policy-grant --detail createGlossary={includeChildDomainUnits=false} --domain-identifier $DOMAINID --entity-identifier $PERSDOMAINUNITID --entity-type DOMAIN_UNIT --policy-type CREATE_GLOSSARY --principal '{"project": {"projectDesignation": "CONTRIBUTOR", "projectIdentifier":"'$PERSMETAPROJECTID'"}}'
aws datazone add-policy-grant --detail createGlossary={includeChildDomainUnits=false} --domain-identifier $DOMAINID --entity-identifier $ROOTDOMAINUNITID --entity-type DOMAIN_UNIT --policy-type CREATE_GLOSSARY --principal '{"project": {"projectDesignation": "CONTRIBUTOR", "projectIdentifier":"'$DOMAINMETAPROJECTID'"}}'

# If new session after C-1 step, set prerequisites for C-2 step
DOMAINID=`aws datazone list-domains --query "items[?name=='CorporateDomain'].id" --output text`
PERSDATAPROJECTID=`aws datazone list-projects --domain-identifier $DOMAINID --query "items[?name=='Personal Banking Data Products'].id" --output text`
DOMAINMETAPROJECTID=`aws datazone list-projects --domain-identifier $DOMAINID --query "items[?name=='Domain Metadata'].id" --output text`
INSMETAPROJECTID=`aws datazone list-projects --domain-identifier $DOMAINID --query "items[?name=='Insurance Metadata'].id" --output text`
WLTHMETAPROJECTID=`aws datazone list-projects --domain-identifier $DOMAINID --query "items[?name=='Wealth Management Metadata'].id" --output text`
PERSMETAPROJECTID=`aws datazone list-projects --domain-identifier $DOMAINID --query "items[?name=='Personal Banking Metadata'].id" --output text`
INSDATAPROJECTID=`aws datazone list-projects --domain-identifier $DOMAINID --query "items[?name=='Insurance Data Products'].id" --output text`
WLTHDATAPROJECTID=`aws datazone list-projects --domain-identifier $DOMAINID --query "items[?name=='Wealth Management Data Products'].id" --output text`
CUST360PROJECTID=`aws datazone list-projects --domain-identifier $DOMAINID --query "items[?name=='Customer 360'].id" --output text`

# C-2: Create User Profiles and add to Projects
BAUSERID=`aws datazone create-user-profile --domain-identifier $DOMAINID --user-type IAM_ROLE --user-identifier arn:aws:iam::$ACCOUNTID:role/BusinessAnalyst --query "id" --output text`
DAUSERID=`aws datazone create-user-profile --domain-identifier $DOMAINID --user-type IAM_ROLE --user-identifier arn:aws:iam::$ACCOUNTID:role/DomainAdmin --query "id" --output text`
WMDSUSERID=`aws datazone create-user-profile --domain-identifier $DOMAINID --user-type IAM_ROLE --user-identifier arn:aws:iam::$ACCOUNTID:role/WealthMgntDataSteward --query "id" --output text`
PBDAUSERID=`aws datazone create-user-profile --domain-identifier $DOMAINID --user-type IAM_ROLE --user-identifier arn:aws:iam::$ACCOUNTID:role/PersonalBankingDataSteward --query "id" --output text`
IDSUSERID=`aws datazone create-user-profile --domain-identifier $DOMAINID --user-type IAM_ROLE --user-identifier arn:aws:iam::$ACCOUNTID:role/InsuranceDataSteward --query "id" --output text`
IMSUSERID=`aws datazone create-user-profile --domain-identifier $DOMAINID --user-type IAM_ROLE --user-identifier arn:aws:iam::$ACCOUNTID:role/InsuranceMetadataSteward --query "id" --output text`
WMMSSERID=`aws datazone create-user-profile --domain-identifier $DOMAINID --user-type IAM_ROLE --user-identifier arn:aws:iam::$ACCOUNTID:role/WealthMgntMetadataSteward --query "id" --output text`
PBMSUSERID=`aws datazone create-user-profile --domain-identifier $DOMAINID --user-type IAM_ROLE --user-identifier arn:aws:iam::$ACCOUNTID:role/PersonalBankingMetadataSteward --query "id" --output text`
DMSUSERID=`aws datazone create-user-profile --domain-identifier $DOMAINID --user-type IAM_ROLE --user-identifier arn:aws:iam::$ACCOUNTID:role/DomainMetadataSteward --query "id" --output text`
aws datazone add-policy-grant --detail addToProjectMemberPool={includeChildDomainUnits=true} --domain-identifier $DOMAINID --entity-identifier $ROOTDOMAINUNITID --entity-type DOMAIN_UNIT --policy-type ADD_TO_PROJECT_MEMBER_POOL --principal '{"user":{"allUsersGrantFilter": { }}}'
aws datazone create-project-membership --designation PROJECT_CONTRIBUTOR  --domain-identifier $DOMAINID --project-identifier $CUST360PROJECTID  --member userIdentifier=$BAUSERID
aws datazone create-project-membership --designation PROJECT_CONTRIBUTOR  --domain-identifier $DOMAINID --project-identifier $WLTHDATAPROJECTID  --member userIdentifier=$WMDSUSERID
aws datazone create-project-membership --designation PROJECT_CONTRIBUTOR  --domain-identifier $DOMAINID --project-identifier $PERSDATAPROJECTID  --member userIdentifier=$PBDAUSERID
aws datazone create-project-membership --designation PROJECT_CONTRIBUTOR  --domain-identifier $DOMAINID --project-identifier $INSMETAPROJECTID  --member userIdentifier=$IMSUSERID
aws datazone create-project-membership --designation PROJECT_CONTRIBUTOR  --domain-identifier $DOMAINID --project-identifier $INSMETAPROJECTID  --member userIdentifier=$WMMSSERID
aws datazone create-project-membership --designation PROJECT_CONTRIBUTOR  --domain-identifier $DOMAINID --project-identifier $PERSMETAPROJECTID  --member userIdentifier=$PBMSUSERID
aws datazone create-project-membership --designation PROJECT_CONTRIBUTOR  --domain-identifier $DOMAINID --project-identifier $DOMAINMETAPROJECTID  --member userIdentifier=$PBMSUSERID

# D: Create Environments
BPIDDL=`aws datazone list-environment-blueprints --domain-identifier $DOMAINID --managed --query "items[?name=='DefaultDataLake'].id" --output text`
ENVBPCONFIGID=$ACCOUNTID:$BPIDDL
aws datazone put-environment-blueprint-configuration --environment-blueprint-identifier $BPIDDL --domain-identifier $DOMAINID --enabled-regions $AWS_DEFAULT_REGION --manage-access-role-arn arn:aws:iam::$ACCOUNTID:role/DataZoneGlueManageAccessRole --provisioning-role-arn arn:aws:iam::$ACCOUNTID:role/DataZoneProvisioningRole --regional-parameters '{ "'$AWS_DEFAULT_REGION'": {"S3Location": "s3://'$ACCOUNTID'-'$AWS_DEFAULT_REGION'-datazone-default","lineageSyncEnabled": "true" }}'
aws datazone add-policy-grant --detail createEnvironmentProfile={domainUnitId=$INSDOMAINUNITID} --domain-identifier $DOMAINID --entity-identifier $ENVBPCONFIGID --entity-type ENVIRONMENT_BLUEPRINT_CONFIGURATION --policy-type CREATE_ENVIRONMENT_PROFILE --principal '{"project": {"projectDesignation": "OWNER", "projectIdentifier":"'$INSDATAPROJECTID'"}}'
aws datazone add-policy-grant --detail createEnvironmentProfile={domainUnitId=$PERSDOMAINUNITID} --domain-identifier $DOMAINID --entity-identifier $ENVBPCONFIGID --entity-type ENVIRONMENT_BLUEPRINT_CONFIGURATION --policy-type CREATE_ENVIRONMENT_PROFILE --principal '{"project": {"projectDesignation": "OWNER", "projectIdentifier":"'$PERSDATAPROJECTID'"}}'
aws datazone add-policy-grant --detail createEnvironmentProfile={domainUnitId=$WLTHDOMAINUNITID} --domain-identifier $DOMAINID --entity-identifier $ENVBPCONFIGID --entity-type ENVIRONMENT_BLUEPRINT_CONFIGURATION --policy-type CREATE_ENVIRONMENT_PROFILE --principal '{"project": {"projectDesignation": "OWNER", "projectIdentifier":"'$WLTHDATAPROJECTID'"}}'
aws datazone add-policy-grant --detail createEnvironmentProfile={domainUnitId=$SHAREDDOMAINUNITID} --domain-identifier $DOMAINID --entity-identifier $ENVBPCONFIGID --entity-type ENVIRONMENT_BLUEPRINT_CONFIGURATION --policy-type CREATE_ENVIRONMENT_PROFILE --principal '{"project": {"projectDesignation": "OWNER", "projectIdentifier":"'$CUST360PROJECTID'"}}'
INSENVPROFILE=`aws datazone create-environment-profile --domain-identifier $DOMAINID --environment-blueprint-identifier $BPIDDL --name "EnvProfile_Insurance" --project-identifier $INSDATAPROJECTID --aws-account-id $ACCOUNTID --user-parameters name=allowedProjects,value=$INSDATAPROJECTID name=profilePermissionLevel,value=FULL_ACCESS --aws-account-region $AWS_DEFAULT_REGION --query "id" --output text`
INSENV=`aws datazone create-environment --domain-identifier $DOMAINID --environment-profile-identifier $INSENVPROFILE --name Env_Insurance --project-identifier $INSDATAPROJECTID --environment-account-region $AWS_DEFAULT_REGION --query "id" --output text`
INSDATASOURCEID=`aws datazone create-data-source --configuration '{"glueRunConfiguration": {"autoImportDataQualityResult": true,"dataAccessRole": "arn:aws:iam::'$ACCOUNTID':role/DataZoneGlueManageAccessRole","relationalFilterConfigurations": [{"databaseName": "insurance_curated","filterExpressions": [{"expression": "*","type": "INCLUDE"}]}]}}'  --domain-identifier $DOMAINID --environment-identifier $INSENV --name DataSource_Insurance --project-identifier $INSDATAPROJECTID --no-publish-on-import --enable-setting ENABLED --recommendation enableBusinessNameGeneration=true --type GLUE --query  "id" --output text`
WEALTHENVPROFILE=`aws datazone create-environment-profile --domain-identifier $DOMAINID --environment-blueprint-identifier $BPIDDL --name "EnvProfile_WealthMgnt" --project-identifier $WLTHDATAPROJECTID --aws-account-id $ACCOUNTID --user-parameters name=allowedProjects,value=$WLTHDATAPROJECTID name=profilePermissionLevel,value=FULL_ACCESS --aws-account-region $AWS_DEFAULT_REGION --query "id" --output text`
WMENV=`aws datazone create-environment --domain-identifier $DOMAINID --environment-profile-identifier $WEALTHENVPROFILE --name Env_WealthMgnt --project-identifier $WLTHDATAPROJECTID --environment-account-region $AWS_DEFAULT_REGION --query "id" --output text`
WEALTHDATASOURCEID=`aws datazone create-data-source --configuration '{"glueRunConfiguration": {"autoImportDataQualityResult": true,"dataAccessRole": "arn:aws:iam::'$ACCOUNTID':role/DataZoneGlueManageAccessRole","relationalFilterConfigurations": [{"databaseName": "wealthmgmt_curated","filterExpressions": [{"expression": "*","type": "INCLUDE"}]}]}}'  --domain-identifier $DOMAINID --environment-identifier $WMENV --name DataSource_WealthMgnt --project-identifier $WLTHDATAPROJECTID --no-publish-on-import --enable-setting ENABLED --recommendation enableBusinessNameGeneration=true --type GLUE --query  "id" --output text`
PERSENVPROFILE=`aws datazone create-environment-profile --domain-identifier $DOMAINID --environment-blueprint-identifier $BPIDDL --name "EnvProfile_PersonalBanking" --project-identifier $PERSDATAPROJECTID --aws-account-id $ACCOUNTID --user-parameters name=allowedProjects,value=$PERSDATAPROJECTID name=profilePermissionLevel,value=FULL_ACCESS --aws-account-region $AWS_DEFAULT_REGION --query "id" --output text`
PBENV=`aws datazone create-environment --domain-identifier $DOMAINID --environment-profile-identifier $PERSENVPROFILE --name Env_PersonalBanking --project-identifier $PERSDATAPROJECTID --environment-account-region $AWS_DEFAULT_REGION --query "id" --output text`
PERSONALDATASOURCEID=`aws datazone create-data-source --configuration '{"glueRunConfiguration": {"autoImportDataQualityResult": true,"dataAccessRole": "arn:aws:iam::'$ACCOUNTID':role/DataZoneGlueManageAccessRole","relationalFilterConfigurations": [{"databaseName": "personalbanking_curated","filterExpressions": [{"expression": "*","type": "INCLUDE"}]}]}}'  --domain-identifier $DOMAINID --environment-identifier $PBENV --name DataSource_PersonalBanking --project-identifier $PERSDATAPROJECTID --no-publish-on-import --enable-setting ENABLED --recommendation enableBusinessNameGeneration=true --type GLUE --query  "id" --output text`
aws datazone start-data-source-run --data-source-identifier $PERSONALDATASOURCEID --domain-identifier $DOMAINID
CUSTENVPROFILE=`aws datazone create-environment-profile --domain-identifier $DOMAINID --environment-blueprint-identifier $BPIDDL --name "EnvProfile_Customer360" --project-identifier $CUST360PROJECTID --aws-account-id $ACCOUNTID --user-parameters name=allowedProjects,value=$CUST360PROJECTID name=profilePermissionLevel,value=FULL_ACCESS --aws-account-region $AWS_DEFAULT_REGION --query "id" --output text`
CUSTENV=`aws datazone create-environment --domain-identifier $DOMAINID --environment-profile-identifier $CUSTENVPROFILE --name Env_Customer360 --project-identifier $CUST360PROJECTID --environment-account-region $AWS_DEFAULT_REGION --query "id" --output text`

# E: Ingest Data Sources and Publish to Business Catalog
aws datazone start-data-source-run --data-source-identifier $INSDATASOURCEID --domain-identifier $DOMAINID
aws datazone start-data-source-run --data-source-identifier $WEALTHDATASOURCEID --domain-identifier $DOMAINID
aws datazone start-data-source-run --data-source-identifier $PERSONALDATASOURCEID --domain-identifier $DOMAINID
sleep 10
INSASSETLIST=`aws datazone search --domain-identifier $DOMAINID --search-scope ASSET --owning-project-identifier $INSDATAPROJECTID --query "items[].assetItem.identifier" --output text`
for id in $INSASSETLIST 
do 
	aws datazone accept-predictions --domain-identifier $DOMAINID --identifier $id
	aws datazone create-listing-change-set --action PUBLISH --domain-identifier $DOMAINID --entity-identifier $id --entity-type ASSET
done
WMASSETLIST=`aws datazone search --domain-identifier $DOMAINID --search-scope ASSET --owning-project-identifier $WLTHDATAPROJECTID --query "items[].assetItem.identifier" --output text`
for id in $WMASSETLIST 
do 
	aws datazone accept-predictions --domain-identifier $DOMAINID --identifier $id
	aws datazone create-listing-change-set --action PUBLISH --domain-identifier $DOMAINID --entity-identifier $id --entity-type ASSET
done
PBASSETLIST=`aws datazone search --domain-identifier $DOMAINID --search-scope ASSET --owning-project-identifier $PERSDATAPROJECTID --query "items[].assetItem.identifier" --output text`
for id in $PBASSETLIST 
do 
	aws datazone accept-predictions --domain-identifier $DOMAINID --identifier $id
	aws datazone create-listing-change-set --action PUBLISH --domain-identifier $DOMAINID --entity-identifier $id --entity-type ASSET
done
