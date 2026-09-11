# Lakeflow Connect, In Detail: Connector Types Explained

## What Lakeflow Connect Is

Lakeflow Connect is Databricks' managed ingestion layer — 100+ connectors that bring data into Unity Catalog-governed streaming tables, using incremental reads/writes so pipelines stay fast and cost-efficient rather than re-pulling entire datasets on every run.

```mermaid
graph TD
    A[Lakeflow Connect] --> B[Managed Connectors<br/>fully automated]
    A --> J[Partner Connectors<br/>Fivetran, Qlik, Informatica]
    A --> C[Standard Connectors<br/>more control, more setup]
    B --> D[SaaS]
    B --> E[Database / CDC]
    B --> F[Query-Based]
    B --> G[File Source]
    B --> H[Streaming]
    C --> I[Auto Loader, COPY INTO,<br/>custom Structured Streaming]
```

The core tradeoff across the platform: **managed connectors** automate almost everything (schema handling, scheduling, retries) but support a defined list of sources; **partner connectors** trade some platform-nativeness for dramatically broader source coverage via a third party; **standard connectors** (Auto Loader, COPY INTO, custom streaming) give you the most control and broadest flexibility, at the cost of more manual setup.

## Connector Type 1: SaaS Connectors

Managed, point-and-click connectors for enterprise applications — Salesforce, HubSpot, Jira, Workday, Confluence, and more.

```mermaid
graph LR
    A[Connection<br/>UC auth object] --> B[Ingestion Pipeline]
    B --> C[Destination<br/>Streaming Tables]
```

**Components:**

| Component | Role |
|---|---|
| Connection | Unity Catalog object storing the app's authentication details (API keys, OAuth tokens) |
| Ingestion Pipeline | Runs on serverless compute, pulls data via the app's API, writes to streaming tables |
| Destination Tables | Streaming tables governed by Unity Catalog |

**How you'd set one up (Salesforce example):** select or create a Unity Catalog connection storing the app's auth details, then configure the ingestion pipeline with a destination catalog/schema — no custom API integration code required.

Some SaaS connectors use browser-based OAuth (Confluence, Google Ads, HubSpot, Jira, Meta Ads, Slack, TikTok Ads, Zendesk) and require interactive sign-in — these can't be set up purely programmatically.

> **Setup steps (Salesforce example):**
> 1. Confirm prerequisites: Unity Catalog enabled, serverless compute enabled on the workspace, and `CREATE CONNECTION` privilege on the metastore if creating a new connection
> 2. In the workspace sidebar, click **Data Ingestion** → **Add data** → select the connector (e.g. **Salesforce**) under Databricks connectors
> 3. On the Connection page, either select an existing connection or create a new one — this triggers an OAuth 2.0 login flow against the source app (only authenticate via the link Databricks itself provides)
> 4. Salesforce specifically requires the connected Databricks app be authorized by an admin if API Access Control is enabled — use a dedicated ingestion user, not a personal login
> 5. Once authenticated, click **Create connection**, then continue the wizard to select objects/tables to ingest
> 6. Configure the destination catalog/schema and a sync schedule, then create the pipeline — Lakeflow Connect auto-creates a job for that schedule

## Connector Type 2: Database Connectors (CDC)

Managed connectors for relational databases, using **change data capture** to track every row-level change (insert/update/delete) rather than re-scanning tables.

```mermaid
graph LR
    A[Connection] --> B[Ingestion Gateway]
    B --> C[Staging Storage]
    C --> D[Ingestion Pipeline]
    D --> E[Destination<br/>Delta / Streaming Tables]
```

**Supported connectors:**

| Database | Mechanism |
|---|---|
| MySQL | CDC, for efficient incremental loads |
| PostgreSQL | CDC |
| Microsoft SQL Server | CDC or full snapshot |
| Oracle | CDC via LogMiner |

**Components:**

- **Connection** — Unity Catalog object with the database's authentication details
- **Ingestion Gateway** — a pipeline that runs *continuously*, extracting snapshots, change logs, and metadata directly from the source database; runs on classic compute inside your workspace's VPC/VNet so it can reach the database over the network
- **Staging Storage** — holds captured changes before they're applied downstream
- **Ingestion Pipeline** — applies the staged changes incrementally to Delta tables
- **Destination Tables** — the resulting Delta tables in Unity Catalog

```mermaid
graph TD
    A[Source DB<br/>row inserted/updated/deleted] --> B[Gateway captures<br/>change log entry]
    B --> C[Staging Storage]
    C --> D[Pipeline applies change<br/>to Delta table]
```

**Networking:** the gateway needs a real network path to the database — VPN, AWS Direct Connect, Azure ExpressRoute, VPC/VNet peering, or a public endpoint all work, and cross-cloud connectivity is supported (e.g. gateway in Azure reaching a database in AWS).

**Orchestration quirk:** because the gateway needs to run continuously (change capture doesn't happen on a fixed schedule), it runs as its own **continuous task** in a separate job from the ingestion pipeline itself.

> **Setup steps (SQL Server example):**
> 1. Ensure network connectivity between your Databricks workspace and the database — set up VPN, Direct Connect/ExpressRoute, or VPC/VNet peering beforehand, since the gateway must reach the source directly
> 2. On the source database, enable CDC (or confirm it's already enabled) and create a dedicated database user with the required read/replication permissions for Databricks to use
> 3. In the workspace, go to **Data Ingestion** → **Add data** → select the database connector (e.g. **SQL Server**)
> 4. Create a Unity Catalog **connection** with the database's host, port, and credentials
> 5. Configure the **ingestion gateway** — choose where it runs (inside your VPC/VNet if using peering) and which staging location to use
> 6. Select the tables/schemas to ingest, and choose CDC or full-snapshot mode per table if the connector supports both
> 7. Set the destination catalog/schema and create the pipeline — the gateway starts running continuously as its own job, separate from the scheduled ingestion pipeline job

## Connector Type 3: Query-Based Connectors

For databases where CDC isn't available or isn't enabled — these query the source **directly**, on a schedule, using a **cursor column** instead of change logs.

```mermaid
graph LR
    A[Connection +<br/>Lakehouse Federation] --> B[Ingestion Pipeline<br/>queries source directly]
    B --> C[Streaming Tables]
```

### How the Cursor Column Works

The cursor is a monotonically increasing column (timestamp or integer, like `updated_at` or an auto-incrementing ID) that tracks progress between runs.

```mermaid
sequenceDiagram
    participant Pipeline
    participant Source DB

    Note over Pipeline: Stored high-water mark: cursor = 1050
    Pipeline->>Source DB: SELECT * WHERE cursor_col > 1050
    Source DB-->>Pipeline: Only new/updated rows
    Note over Pipeline: New high-water mark: cursor = 1200
```

- Only a **single** cursor column is allowed — no composite/multi-column cursors (a pipeline with more than one fails with `INVALID_CURSOR_COLUMNS`)
- Cursor values must never decrease — rows at or below the stored high-water mark are never re-ingested
- No gateway or staging volume needed — it queries the source directly via a Unity Catalog connection and **Lakehouse Federation**

### History Tracking Modes (SCD)

Query-based connectors support different modes for how destination tables handle historical changes:

| Mode | Behavior |
|---|---|
| `SCD_TYPE_1` | Overwrites existing rows with the latest version — no history preserved |
| `SCD_TYPE_2` | Preserves full history by adding new versioned rows for every change |
| `APPEND_ONLY` | Every ingested row is appended, nothing merged or overwritten |

```mermaid
graph TD
    A[New row from source] --> B{SCD Mode}
    B -->|SCD_TYPE_1| C[Overwrite existing row]
    B -->|SCD_TYPE_2| D[Insert new versioned row,<br/>keep old ones]
    B -->|APPEND_ONLY| E[Always insert,<br/>never overwrite]
```

Query-based connectors also support a `deletion_condition` parameter to detect soft deletes (e.g. a row flagged `is_deleted = true` rather than physically removed).

> **Setup steps:**
> 1. Identify a column on the source table that increases monotonically and never decreases (e.g. `updated_at`, `id`) — this becomes your cursor column
> 2. Ensure network connectivity from serverless compute to the source database (query-based connectors use Lakehouse Federation, so check federation networking requirements specifically)
> 3. Create a Unity Catalog **connection** (or foreign catalog, for Lakehouse Federation-based ingestion) storing the database's credentials
> 4. Define the **ingestion pipeline**, specifying the source table, the cursor column, and the desired history-tracking mode (`SCD_TYPE_1`, `SCD_TYPE_2`, or `APPEND_ONLY`)
> 5. Optionally set a `deletion_condition` if the source uses soft deletes you want reflected downstream
> 6. Set the destination catalog/schema and a schedule, then create the pipeline — no gateway or staging volume needs to be provisioned

## Connector Type 4: File Source Connectors

For structured and unstructured files sitting in enterprise file storage — Google Drive, SharePoint — as opposed to cloud object storage (which typically uses Auto Loader, a standard connector).

```mermaid
graph LR
    A[Connection] --> B[Ingestion Pipeline]
    B --> C[Destination Tables]
```

Same basic shape as SaaS connectors: connection, pipeline, destination tables. These are particularly useful for feeding unstructured content (PDFs, documents) into AI/RAG applications via Unity Catalog governance.

> **Setup steps (SharePoint example):**
> 1. Register an app / service credential on the source platform (e.g. an Azure AD app registration for SharePoint) with read access to the target site/drive
> 2. In the workspace, go to **Data Ingestion** → **Add data** → select the file source connector (e.g. **SharePoint**)
> 3. Create a Unity Catalog **connection** using that credential
> 4. Select the site, folder, or drive to ingest from, and choose which file types to include
> 5. Set the destination catalog/schema and a sync schedule, then create the pipeline

## Connector Type 5: Streaming Connectors

For continuously ingesting from message buses and event streams — Kafka, RabbitMQ, and similar.

```mermaid
graph LR
    A[Connection<br/>endpoint + auth] --> B[Ingestion Pipeline<br/>continuous read]
    B --> C[Streaming Tables]
```

The pipeline runs continuously on serverless compute, reading messages as they arrive rather than on a batch schedule — the connection stores the source endpoint and credentials so the pipeline can authenticate without needing credentials embedded in its own configuration.

> **Setup steps (Kafka example):**
> 1. Confirm network reachability from Databricks serverless compute to the Kafka bootstrap servers (VPC peering, Private Link, or public endpoint with proper security group/firewall rules)
> 2. Gather the broker endpoint(s) and authentication details (SASL credentials, mTLS certs, or similar)
> 3. In the workspace, go to **Data Ingestion** → **Add data** → select the streaming connector (e.g. **Kafka**)
> 4. Create a Unity Catalog **connection** storing the endpoint and credentials
> 5. Configure the ingestion pipeline: topic(s) to subscribe to, starting offset behavior, and the destination streaming table
> 6. Create the pipeline — it runs continuously rather than on a fixed schedule, since it's reading a live stream

## Connector Type 6: Community and Custom Connectors

For sources with no managed connector support:

```mermaid
graph TD
    A[Unsupported source] --> B{Community connector<br/>available?}
    B -->|Yes| C[Use open-source,<br/>community-built connector]
    B -->|No| D[Build a custom connector,<br/>run it in your own workspace]
```

Community connectors are open-source and community-maintained rather than built by Databricks. Custom connectors are fully self-built when nothing else fits — you take on the maintenance burden yourself.

> **Setup steps (community connector):**
> 1. Search Databricks' community connector listings/repos for one matching your source
> 2. Review its source code and maintenance status — since Databricks doesn't build or support these, check for recent activity/issues before relying on it
> 3. Install/import the connector into your workspace (typically as a library or notebook-based package)
> 4. Configure it with your source's credentials, following that connector's own documentation, since configuration isn't standardized across community connectors
> 5. Wire it into a Lakeflow Job so it runs on a schedule alongside your other pipelines
>
> **Setup steps (custom connector):**
> 1. Design the ingestion logic using the Structured Streaming or batch APIs, targeting your source's specific SDK/API
> 2. Write the connector to read from the source and write incrementally to a Delta/streaming table, handling your own checkpointing for incremental reads
> 3. Package and deploy it as a notebook or job task in your workspace
> 4. Orchestrate it with Lakeflow Jobs like any other pipeline — you're responsible for its error handling, retries, and monitoring going forward

## Connector Type 7: Partner Connectors

Beyond Databricks-built managed connectors, Databricks partners with third-party ingestion platforms — most notably **Fivetran**, along with Qlik and Informatica — that bring their own connector libraries (hundreds of sources) directly into the Databricks ecosystem, accessible through **Partner Connect**.

```mermaid
graph LR
    A[Partner Connect] --> B[Fivetran<br/>500+ connectors]
    A --> C[Qlik]
    A --> D[Informatica]
    B & C & D --> E[Delta Lake tables<br/>via Unity Catalog]
```

### Why Partner Connectors Exist

Databricks' own managed connectors cover the most common, high-value sources (Salesforce, SQL Server, Workday, etc.), but no single vendor can maintain connectors for every SaaS app, database, or file format in existence. Partner Connect fills that gap — Fivetran alone brings 500+ pre-built connectors (Salesforce, Google Analytics, Facebook Ads, hundreds more) that sync directly into Delta Lake, with automated schema migration and change data capture handled by the partner, not by Databricks itself.

```mermaid
graph TD
    A[Partner Connector<br/>e.g. Fivetran] --> B[Pulls full initial snapshot]
    B --> C[Uses source's own CDC/<br/>change tracking mechanism]
    C --> D[Syncs incrementally<br/>into Delta tables]
```

### Key Characteristics

- **Not built or maintained by Databricks** — the partner owns connector logic, reliability, and support; Databricks provides the integration surface (Partner Connect UI, Unity Catalog governance on the destination side)
- **Broader source coverage** than Databricks' own managed connectors, since partners like Fivetran have built out hundreds of integrations over years
- **Requires Unity Catalog** on the Databricks side — legacy Hive Metastore-only workspaces aren't supported by newer partner integrations like Fivetran's Databricks connector
- **Per-user or admin-managed connections** — historically only admins could establish a Partner Connect connection; this has opened up so regular users with the right permissions can self-serve too

> **Setup steps (Fivetran example):**
> 1. Confirm you have the Databricks workspace admin role, or the specific permissions required for per-user Partner Connect connections
> 2. In the Databricks workspace sidebar, open **Partner Connect** (or, in newer workspaces, find the partner listed directly in the **Add data** ingestion UI)
> 3. Select **Fivetran** from the partner tile grid
> 4. Databricks auto-generates the connection details (SQL warehouse/cluster endpoint, a scoped access token) and hands them to Fivetran automatically — no manual credential copying required
> 5. In the Fivetran UI that opens, choose the source you want to sync from (e.g. Salesforce, PostgreSQL) and authenticate to that source
> 6. Configure the destination schema naming and sync frequency in Fivetran
> 7. Fivetran performs an initial full sync, then continues incremental syncs using the source's own change-tracking mechanism, landing data as Delta tables governed by Unity Catalog

## Connector Type 8: Standard Connectors

Standard connectors trade some of the managed connectors' automation for **broader source support and finer control** — they're the right choice when a managed connector doesn't exist for your source, or when you need to customize behavior a managed pipeline won't let you touch.

```mermaid
graph TD
    A[Three Layers of Ingestion<br/>most customizable → most managed] --> B[Structured Streaming<br/>full code-level control]
    A --> C[Lakeflow Declarative Pipelines<br/>with a standard connector source]
    A --> D[Databricks SQL<br/>e.g. CREATE STREAMING TABLE]
```

Databricks recommends starting at the *most managed* layer that supports your source, and only dropping down to a more customizable layer if that doesn't meet your needs.

### The Main Standard Connectors

| Source | Most customizable | Some customization | Most automated |
|---|---|---|---|
| Cloud object storage (S3/ADLS/GCS) | Auto Loader + Structured Streaming | Auto Loader + Lakeflow Declarative Pipelines | Auto Loader + Databricks SQL |
| Apache Kafka | Structured Streaming with Kafka source | Declarative Pipelines with Kafka source | Databricks SQL with Kafka source |
| Google Pub/Sub | Structured Streaming with Pub/Sub source | Declarative Pipelines with Pub/Sub source | — |
| SFTP servers | Ingest via Python/SQL | — | — |

### Auto Loader — The Most Common Standard Connector

Auto Loader incrementally and efficiently processes new files as they land in cloud object storage — built for high file volumes (it can handle billions of files for migration/backfill scenarios), tracking which files have already been processed so re-runs don't duplicate data.

```python
df = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("cloudFiles.inferSchema", "true")
    .load("/mnt/raw/patients/"))
```

```mermaid
graph LR
    A[New files land<br/>in cloud storage] --> B[Auto Loader detects them]
    B --> C[Incrementally processes<br/>only new files]
    C --> D[Writes to Delta table]
```

### COPY INTO — The SQL-Only Alternative

For simpler, smaller-scale batch loads, `COPY INTO` is a SQL-native option — though Databricks now recommends `CREATE STREAMING TABLE` syntax over it for incremental cloud storage ingestion, since it offers a more scalable, robust experience for SQL users.

```sql
COPY INTO patients
FROM 's3://my-bucket/raw/patients/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true');
```

### read_files — The Simplest Option

For a quick full reload (not incremental), the `read_files` SQL function reads files of any format from a location and returns tabular data directly — no streaming state to manage, but it re-ingests everything on every run.

```sql
SELECT * FROM read_files('/mnt/raw/patients/', format => 'csv');
```

### Open-Source Connector Libraries

Databricks also supports importing popular open-source ingestion libraries — **dlt (data load tool)**, **Airbyte**, and **Debezium** — for sources with no managed, partner, or built-in standard option.

> **Setup steps (Auto Loader example):**
> 1. Set up a Unity Catalog **storage credential** for the cloud storage account (e.g. an access connector resource ID in Azure, an IAM role in AWS)
> 2. Create an **external location** pointing at the specific cloud storage path, secured by that storage credential
> 3. Choose your automation layer: raw PySpark with `readStream.format("cloudFiles")` for full control, a Lakeflow Declarative Pipeline for a more managed experience, or `CREATE STREAMING TABLE` in Databricks SQL for the most automated option
> 4. Specify the file format (`csv`, `json`, `parquet`, etc.) and destination table
> 5. Start the stream (or let the pipeline/SQL statement manage it) — Auto Loader tracks processed files automatically, so re-running the job won't reprocess files it already ingested



```mermaid
graph TD
    A[What are you ingesting?] --> B{Enterprise SaaS app?}
    B -->|Yes| C[SaaS Connector]
    B -->|No| D{Relational database?}
    D -->|Yes, CDC available| E[Database CDC Connector]
    D -->|Yes, no CDC, has cursor column| F[Query-Based Connector]
    D -->|No| G{Files in Drive/SharePoint?}
    G -->|Yes| H[File Source Connector]
    G -->|No| I{Message bus / event stream?}
    I -->|Yes| J[Streaming Connector]
    I -->|No| K{Cloud object storage<br/>like S3/ADLS/GCS?}
    K -->|Yes| L[Auto Loader<br/>standard connector]
    K -->|No| M[Community or<br/>Custom Connector]
```

Real examples of this decision in practice:

| Scenario | Right connector |
|---|---|
| Supported Salesforce source, no custom API code needed | Managed SaaS connector |
| SQL Server with native change logs available | Managed database CDC connector |
| Database can't enable CDC, but has an `updated_at` column | Query-based connector with that column as cursor |
| Millions of JSON files landing in ADLS | Auto Loader (standard connector) |
| A few thousand files, SQL-only, scheduled load | `COPY INTO` (standard connector) |
| Kafka events needing custom transformations/offset control | Standard streaming connector via Structured Streaming |

## Why the Component Differences Matter

```mermaid
graph TD
    A[Component set differs<br/>by connector type] --> B["SaaS / File:<br/>Connection + Pipeline + Tables"]
    A --> C["Database CDC:<br/>adds Gateway + Staging Storage"]
    A --> D["Query-Based:<br/>no Gateway/Staging — queries directly"]
```

The database connector's extra components (gateway, staging) exist specifically because CDC requires *continuously* watching a database's change log — that's fundamentally different work from a scheduled API pull or a scheduled `SELECT` query, which is why query-based and SaaS connectors don't need them.

## Summary

- **SaaS connectors** — API-based, point-and-click, for apps like Salesforce/Workday/HubSpot
- **Database (CDC) connectors** — track every row change via change logs; need a continuous gateway + staging storage; support MySQL, PostgreSQL, SQL Server, Oracle
- **Query-based connectors** — no CDC needed, use a single monotonically increasing cursor column instead; support SCD_TYPE_1/SCD_TYPE_2/APPEND_ONLY history modes
- **File source connectors** — for enterprise file storage (SharePoint, Google Drive), distinct from cloud object storage ingestion (which uses Auto Loader)
- **Streaming connectors** — continuous ingestion from message buses like Kafka/RabbitMQ
- **Community/custom connectors** — fallback for anything with no managed option, at the cost of self-maintenance
