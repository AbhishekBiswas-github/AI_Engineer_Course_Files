Understand the below situation

I am working on a Power BI report where client is using excel files which is being uploaded in the sharepoint to create the dashboard. After importing the excel files, the modify the tables based on the accounts presents in sca_database Accounts table. 
Now the client's new requirement is to replace the sharepoint excel file with semantic model. So I used IVM team semantic model to create a master table from the tables in the semantic model. 

Below are the master tables.
All Active Master Table = 
SELECTCOLUMNS (
    FILTER (
        'IVM Dataset',

        /* Existing conditions */
        LOWER ( TRIM ( 'IVM Dataset'[vuln_ivm_scope] ) ) = "yes"
        &&
        LOWER ( TRIM ( 'IVM Dataset'[Vuln Status] ) ) = "active"
        &&
        LOWER ( TRIM ( 'IVM Dataset'[Device Use Case] ) ) = "ivm"
    ),

    /* Keep everything else EXACTLY SAME */
    "Cloud Provider", RELATED ( 'Active Accounts'[Cloud Provider] ),
    "Engineering Leader", RELATED ( 'Active Accounts'[Engineering Leader] ),
    "Product Support Group", RELATED ( 'Active Accounts'[Product Support Group] ),
    "Cloud Accountable BU", RELATED ( 'Master Account Mappings'[Accountable BU] ),

    "Device Cloud Account ID", 'IVM Dataset'[accountId],
    "Device Cloud Resource Name", 'IVM Dataset'[cloudResourceName],
    "Device Cloud CI", 'IVM Dataset'[cloudTagCI],
    "Device Cloud Environment", 'IVM Dataset'[cloudTagenv],
    "Device Cloud Tags", 'IVM Dataset'[cloudTagList],
    "Device Cloud UAI", 'IVM Dataset'[cloudTagUAI],
    "Device CI", 'IVM Dataset'[config_item_id],
    "Vuln Days Open", 'IVM Dataset'[days_open],
    "Device Unique Key", 'IVM Dataset'[device_unique_key],
    "Device Owner Email", 'IVM Dataset'[email],
    "Vuln First Found Date", 'IVM Dataset'[first_detected],
    "Device Support Group", 'IVM Dataset'[group],
    "Device Support Group Email", 'IVM Dataset'[group_email],
    "Device Hostname", 'IVM Dataset'[hostname],
    "Device Cloud Resource ID", 'IVM Dataset'[instanceId],
    "App Internet Facing", 'IVM Dataset'[internet_facing],
    "Device IPv4 Address", 'IVM Dataset'[ipv4Address],
    "Vuln Last Found Date", 'IVM Dataset'[last_detected],
    "Device Operating System", 'IVM Dataset'[os],
    "App Class", 'IVM Dataset'[pulse_app_class_name],
    "App CI", 'IVM Dataset'[pulse_app_config_item_id],
    "App Department", 'IVM Dataset'[pulse_app_department],
    "App Life Cycle", 'IVM Dataset'[pulse_app_life_cycle],
    "App Life Stage", 'IVM Dataset'[pulse_app_life_stage],
    "App Name", 'IVM Dataset'[pulse_app_name],
    "App Business Owner", 'IVM Dataset'[pulse_app_owned_by],
    "App IT Owner", 'IVM Dataset'[pulse_app_owner],
    "Device Owner", 'IVM Dataset'[owned_by],
    "App IT Owner Email", 'IVM Dataset'[pulse_app_owned_email],
    "App Business Owner Email", 'IVM Dataset'[pulse_app_owner_email],
    "App Support Group", 'IVM Dataset'[pulse_app_support_group],
    "App Support Group Email", 'IVM Dataset'[pulse_app_support_group_email],
    "App Support Vendor", 'IVM Dataset'[pulse_app_support_vendor],
    "App UAI", 'IVM Dataset'[pulse_app_uai],
    "Device Qualys Tags", 'IVM Dataset'[qualysTags],
    "Vuln Scan Results", 'IVM Dataset'[result],
    "Vuln Solution", 'IVM Dataset'[solution],
    "Vuln Title", 'IVM Dataset'[title],
    "Device VPC ID", 'IVM Dataset'[vpcId],
    "Vuln Backlog", 'IVM Dataset'[vuln_backlog],
    "Vuln Days Open Range", 'IVM Dataset'[vuln_days_open_range],
    "Vuln SLA Met", 'IVM Dataset'[vuln_sla_met],
    "Vuln Target SLA Date", 'IVM Dataset'[vuln_target_sla],
    "Vuln Unique ID", 'IVM Dataset'[vuln_unique_id],

    /* =============================
       Measures
       ============================= */
    "App Business Portfolio", 'IVM Dataset'[App Business Portfolio],
    "App Executive", 'IVM Dataset'[App Business Portfolio Owner],
    "Device Ephemeral", 'IVM Dataset'[Device Ephemeral],
    "Device Use Case", 'IVM Dataset'[Device Use Case],
    "Vuln Category", 'IVM Dataset'[Vuln Category],
    "Vuln Code Level", 'IVM Dataset'[Vuln Code Level],
    "Vuln EOL Tech", 'IVM Dataset'[Vuln EOL Tech],
    "Vuln Has Remediation Plan", 'IVM Dataset'[Vuln Has Remediation Plan],
    "Vuln HCL Remediation Scope", 'IVM Dataset'[Vuln HCL Remediation Scope],
    "Vuln Owner Category", 'IVM Dataset'[Vuln Owner Category],
    "Vuln Remediation Plan IDs", 'IVM Dataset'[Vuln Remediation Plan IDs],
    "Vuln Status", 'IVM Dataset'[Vuln Status],
    "Vuln TCS Remediation Scope", 'IVM Dataset'[Vuln TCS Remediation Scope]
)

SLA Master Table = 
SELECTCOLUMNS (
    FILTER (
        'IVM Dataset',
        LOWER ( TRIM ( 'IVM Dataset'[vuln_ivm_scope] ) ) = "yes"
            &&
        LOWER ( TRIM ( 'IVM Dataset'[Vuln SLA Metric Scope] ) ) = "yes"
            &&
        LOWER (
            TRIM (
                RELATED ( 'Master Account Mappings'[Accountable BU] )
            )
        ) IN { "sbu - avs", "sbu - imaging", "sbu - international", "sbu - pcs", "sbu - sto", "sbu - sto ai", "sbu - uscan" }
        /*
        &&
        LOWER ( TRIM ( 'IVM Dataset'[Device Use Case] ) ) = "ivm"
        */
    ),

    /* =============================
       Columns from Active Accounts
       ============================= */
    "Cloud Provider",
        RELATED ( 'Active Accounts'[Cloud Provider] ),

    "Engineering Leader",
        RELATED ( 'Active Accounts'[Engineering Leader] ),

    "Product Support Group",
        RELATED ( 'Active Accounts'[Product Support Group] ),

    /* =============================
       Columns from Master Account Mappings
       ============================= */
    "Cloud Accountable BU",
        RELATED ( 'Master Account Mappings'[Accountable BU] ),

    /* =============================
       Columns from IVM Dataset
       ============================= */
    "Device Cloud Account ID",
        'IVM Dataset'[accountId],

    "Device Cloud Resource Name",
        'IVM Dataset'[cloudResourceName],

    "Device Cloud CI",
        'IVM Dataset'[cloudTagCI],

    "Device Cloud Environment",
        'IVM Dataset'[cloudTagenv],

    "Device Cloud Tags",
        'IVM Dataset'[cloudTagList],

    "Device Cloud UAI",
        'IVM Dataset'[cloudTagUAI],

    "Device CI",
        'IVM Dataset'[config_item_id],

    "Vuln Days Open",
        'IVM Dataset'[days_open],

    "Device Unique Key",
        'IVM Dataset'[device_unique_key],

    "Device Owner Email",
        'IVM Dataset'[email],

    "Vuln First Found Date",
        'IVM Dataset'[first_detected],

    "Device Support Group",
        'IVM Dataset'[group],

    "Device Support Group Email",
        'IVM Dataset'[group_email],

    "Device Hostname",
        'IVM Dataset'[hostname],

    "Device Cloud Resource ID",
        'IVM Dataset'[instanceId],

    "App Internet Facing",
        'IVM Dataset'[internet_facing],

    "Device IPv4 Address",
        'IVM Dataset'[ipv4Address],

    "Vuln Last Found Date",
        'IVM Dataset'[last_detected],

    "Device Operating System",
        'IVM Dataset'[os],

    "App Class",
        'IVM Dataset'[pulse_app_class_name],

    "App CI",
        'IVM Dataset'[pulse_app_config_item_id],

    "App Department",
        'IVM Dataset'[pulse_app_department],

    "App Life Cycle",
        'IVM Dataset'[pulse_app_life_cycle],

    "App Life Stage",
        'IVM Dataset'[pulse_app_life_stage],

    "App Name",
        'IVM Dataset'[pulse_app_name],

    "App Business Owner",
        'IVM Dataset'[pulse_app_owned_by],

    "App IT Owner",
        'IVM Dataset'[pulse_app_owner],

    "Device Owner",
        'IVM Dataset'[owned_by],

    "App IT Owner Email",
        'IVM Dataset'[pulse_app_owned_email],

    "App Business Owner Email",
        'IVM Dataset'[pulse_app_owner_email],

    "App Support Group",
        'IVM Dataset'[pulse_app_support_group],

    "App Support Group Email",
        'IVM Dataset'[pulse_app_support_group_email],

    "App Support Vendor",
        'IVM Dataset'[pulse_app_support_vendor],

    "App UAI",
        'IVM Dataset'[pulse_app_uai],

    "Device Qualys Tags",
        'IVM Dataset'[qualysTags],

    "Vuln Scan Results",
        'IVM Dataset'[result],

    "Vuln Solution",
        'IVM Dataset'[solution],

    "Vuln Title",
        'IVM Dataset'[title],

    "Device VPC ID",
        'IVM Dataset'[vpcId],

    "Vuln Backlog",
        'IVM Dataset'[vuln_backlog],

    "Vuln Days Open Range",
        'IVM Dataset'[vuln_days_open_range],

    "Vuln SLA Met",
        'IVM Dataset'[vuln_sla_met],

    "Vuln Target SLA Date",
        'IVM Dataset'[vuln_target_sla],

    "Vuln Unique ID",
        'IVM Dataset'[vuln_unique_id],

    "Vuln SLA Metric Scope",
        'IVM Dataset'[Vuln SLA Metric Scope],

    "Vuln IVM Scope",
        'IVM Dataset'[vuln_ivm_scope],

    /* =============================
       Measures
       ============================= */
    "App Business Portfolio", 'IVM Dataset'[App Business Portfolio],
    "App Executive", 'IVM Dataset'[App Business Portfolio Owner],
    "Device Ephemeral", 'IVM Dataset'[Device Ephemeral],
    "Device Use Case", 'IVM Dataset'[Device Use Case],
    "Vuln Category", 'IVM Dataset'[Vuln Category],
    "Vuln Code Level", 'IVM Dataset'[Vuln Code Level],
    "Vuln EOL Tech", 'IVM Dataset'[Vuln EOL Tech],
    "Vuln Has Remediation Plan", 'IVM Dataset'[Vuln Has Remediation Plan],
    "Vuln HCL Remediation Scope", 'IVM Dataset'[Vuln HCL Remediation Scope],
    "Vuln Owner Category", 'IVM Dataset'[Vuln Owner Category],
    "Vuln Remediation Plan IDs", 'IVM Dataset'[Vuln Remediation Plan IDs],
    "Vuln Status", 'IVM Dataset'[Vuln Status],
    "Vuln TCS Remediation Scope", 'IVM Dataset'[Vuln TCS Remediation Scope]
)

From the master tables, we create tables which will contain only the accounts details which are in the sca_database Accounts table. Below is the code
Qualys All Active = 
FILTER (
    'All Active Master Table',
    NOT ISBLANK (
        LOOKUPVALUE (
            'sca_database Accounts'[cloud_account_id],
            'sca_database Accounts'[cloud_account_id],
            'All Active Master Table'[Device Cloud Account ID]
        )
    )
)

Qualys SLA Table = 
FILTER(
    'SLA Master Table',
    NOT ISBLANK(
        LOOKUPVALUE(
            'sca_database Accounts'[cloud_account_id],
            'sca_database Accounts'[cloud_account_id],
            'SLA Master Table'[Device Cloud Account ID]
        )
    )
)


The tables which are coming from Semantic model are coming in DirectQuery Mode. and the tables All Active Master Table, SLA Master Table, Qualys SLA Table and Qualys All Active are created in Import mode.

After publishing the Power Bi file, when I do a manual refresh or a scheduled refresh. I am getting a below error:

Data source error:	{"error":{"code":"Premium_ASWL_Error","pbi.error":{"code":"Premium_ASWL_Error","parameters":{},"details":[{"code":"Premium_ASWL_Error_Details_Label","detail":{"type":1,"value":"We cannot refresh this dataset because the dataset contains calculated tables or calculated columns based on data from a Single Sign-on (SSO)-enabled Direct Query data source. Please configure the dataset to use an explicit connection with granular access control to access this data source and then try again."}}],"exceptionCulprit":1}}}
Cluster URI:	WABI-US-EAST-A-PRIMARY-redirect.analysis.windows.net
Activity ID:	4b57c472-d2ba-43b2-a821-af9851529c69
Request ID:	c692cdc2-7465-0bf0-258c-5b8b271e1f94
Time:	2026-04-27 06:19:47Z
Details	
#	Type	Start	End	Duration	Status	Details
1	Data	4/27/2026, 11:49:16 AM	4/27/2026, 11:49:47 AM	31s	Failed	(Show)



Error

Data source error: {"error":{"code":"Premium_ASWL_Error","pbi.error":{"code":"Premium_ASWL_Error","parameters":{},"details":[{"code":"Premium_ASWL_Error_Details_Label","detail":{"type":1,"value":"We cannot refresh this dataset because the dataset contains calculated tables or calculated columns based on data from a Single Sign-on (SSO)-enabled Direct Query data source. Please configure the dataset to use an explicit connection with granular access control to access this data source and then try again."}}],"exceptionCulprit":1}}}

I want reason of the issue and the solution to resolve the issue.
