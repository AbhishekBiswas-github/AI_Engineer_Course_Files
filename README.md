I have created the below table form 3 tables of semantic model

All Active Master Table = 
SELECTCOLUMNS (
    FILTER (
        'IVM Dataset',
        LOWER ( TRIM ( 'IVM Dataset'[vuln_ivm_scope] ) ) = "yes"
            &&
        LOWER(TRIM('IVM Dataset'[Vuln Status])) = "active"
            &&
        LOWER(TRIM('IVM Dataset'[Device Use Case])) = "ivm"
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
       Columns from Master Account Mapping
       ============================= */
    "Cloud Accountable BU",
        RELATED ( 'Master Account Mappings'[Accountable BU] ),

    // "Account ID",
    //     RELA

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

    /* =============================
       Measures from IVM Dataset
       ============================= */
    "App Business Portfolio",
        [App Business Portfolio],

    "App Executive",
        [App Business Portfolio Owner],

    "Device Ephemeral",
        [Device Ephemeral],

    "Device Use Case",
        [Device Use Case],

    "Vuln Category",
        [Vuln Category],

    "Vuln Code Level",
        [Vuln Code Level],

    "Vuln EOL Tech",
        [Vuln EOL Tech],

    "Vuln Has Remediation Plan",
        [Vuln Has Remediation Plan],

    "Vuln HCL Remediation Scope",
        [Vuln HCL Remediation Scope],

    "Vuln Owner Category",
        [Vuln Owner Category],

    "Vuln Remediation Plan IDs",
        [Vuln Remediation Plan IDs],

    "Vuln Status",
        [Vuln Status],

    "Vuln TCS Remediation Scope",
        [Vuln TCS Remediation Scope]
)

And then created one more table 
Qualys All Active Table = 
CALCULATETABLE(
    'All Active Master Table',
    TREATAS(
        VALUES('sca_database Accounts'[cloud_account_id]),
        'All Active Master Table'[Device Cloud Account ID]
    )
)

when i am trying to create a relationship between "sca_database Accounts'[cloud_account_id]" and "Qualys All Active Table[Device Cloud Account ID], 
I am betting below error
A circular dependency was detected: Qualys All Active Table[Qualys All Active Table], 993a4493-768d-590e-c694-50eb2c3311ab, Qualys All Active Table[Device Cloud Account ID], Qualys All Active Table[Qualys All Active Table].

Below are the table list
AgentList
Archer Remediation Plans
Cost Center Accountability
Last Refresh Date
Missing Agent
Missing Agent Name
Qualys All Active Table
Qualys Report
Qualys Report All Active
Report Refresh Date
sca_database AccountEnvironments
sca_database Accounts
sca_database AccountStatuses
sca_database AccountWorkflows
sca_database LandingZones
sca_database Programs
sca_database QuickSightGroups
sca_database StrategicBusinessUnits
sca_database SupportCategories
sca_database Users
Wiz Report
