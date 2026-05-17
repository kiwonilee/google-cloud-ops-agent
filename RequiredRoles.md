# Required Roles for GCP Services

## Compute Engine
[documentation](https://docs.cloud.google.com/compute/docs/use-compute-engine-mcp#required-roles)
- **Make MCP tool calls**: MCP Tool User (roles/mcp.toolUser)

---

## Cloud Run
[documentation](https://docs.cloud.google.com/run/docs/use-cloud-run-mcp#required-roles)
- **Create Cloud Run services**: Cloud Run Developer (roles/run.developer)
- **Run operations as the service account**: Service Account User (roles/iam.serviceAccountUser)
- **Access the Artifact Registry repository of the deployed container image**: Artifact Registry Reader (roles/artifactregistry.reader)
- **Use a cross-project service account to deploy a service**: Service Account Token Creator (roles/iam.serviceAccountTokenCreator)
- **Make MCP tool calls**: MCP Tool User (roles/mcp.toolUser)

---

## GKE
[documentation](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/use-gke-mcp#required-roles)
- **MCP Tool User (roles/mcp.toolUser)**: Grants permission to make tool calls to the MCP server endpoint.
- **Kubernetes Engine Cluster Viewer (roles/container.clusterViewer)**: This role provides the read-only access needed for the remote server's tools.

---

## GCS
[documentation](https://docs.cloud.google.com/storage/docs/use-cloud-storage-mcp#required-roles)
- **Make MCP tool calls**: MCP Tool User (roles/mcp.toolUser)
- **List objects, read objects and their contents, or get an object's metadata**: Storage Object Viewer (roles/storage.objectViewer)
- **Write content to an object**: Storage Object Creator (roles/storage.objectCreator)
- **Create buckets and list buckets**: Storage Admin (roles/storage.admin)

---

## Network Intelligence Center
[documentation](https://docs.cloud.google.com/network-intelligence-center/docs/use-network-management-mcp#required-roles)
- **Make MCP tool calls**: MCP Tool User (roles/mcp.toolUser)
- **Perform all operations on a connectivity test**: Network Management Admin (roles/networkmanagement.admin)
- **Get and list connectivity tests**: Network Management Viewer (roles/networkmanagement.viewer)
- **Run a connectivity test against specific Google Cloud resources**: Compute Network Viewer (roles/compute.networkViewer)

---

## Gemini Cloud Assist
[documentation](https://docs.cloud.google.com/cloud-assist/use-gemini-cloud-assist-mcp#required-roles)
- **Make MCP tool calls**: MCP Tool User (roles/mcp.toolUser)
- **Use Gemini Cloud Assist**: one of Gemini Cloud Assist User (roles/geminicloudassist.user), Gemini Cloud Assist Editor (roles/geminicloudassist.editor), or Gemini Cloud Assist Admin (roles/geminicloudassist.admin)

---

## BigQuery
[documentation](https://docs.cloud.google.com/bigquery/docs/use-bigquery-mcp#required-roles) 
- **Make MCP tool calls**: MCP Tool User (roles/mcp.toolUser)
- **Run BigQuery jobs**: BigQuery Job User (roles/bigquery.jobUser)
- **Query BigQuery data**: BigQuery Data Viewer (roles/bigquery.dataViewer)

---

## BigTable
[documentation](https://docs.cloud.google.com/bigtable/docs/use-bigtable-mcp#required-roles)
- **Make MCP tool calls**: MCP Tool User (roles/mcp.toolUser)
- **Full access to Bigtable resources**: Bigtable Administrator (roles/bigtable.admin)

---

## Cloud SQL for MySQL
[documentation](https://docs.cloud.google.com/sql/docs/mysql/use-cloudsql-mcp#required-roles)
- **Make MCP tool calls in a project**: MCP Tool User (roles/mcp.toolUser)
- **Create a backup of a Cloud SQL instance**: Cloud SQL Editor (roles/cloudsql.editor)
- **Create an OAuth client ID**: OAuth Config Editor (roles/oauthconfig.editor)
- **Create, clone, restore from backup, or update a Cloud SQL instance**: Cloud SQL Admin (roles/cloudsql.admin)
- **Create or update a Cloud SQL user**: Cloud SQL Admin (roles/cloudsql.admin)
- **Create secrets and access secret versions in Secret Manager**: Secret Manager Admin (roles/secretmanager.admin)
- **Execute SQL statements (including read-only) in Cloud SQL**:
    - Cloud SQL Admin (roles/cloudsql.admin)
    - Cloud SQL Studio User (roles/cloudsql.StudioUser)
- **Get a Cloud SQL instance or list all Cloud SQL instances in a project**: Cloud SQL Viewer (roles/cloudsql.viewer)
- **Import data into a Cloud SQL instance**:
    - Cloud SQL Admin (roles/cloudsql.admin)
    - Storage Admin (roles/storage.admin)
- **List Cloud SQL users**: Cloud SQL Viewer (roles/cloudsql.viewer)

---

## Cloud SQL for Postgre
[documentation](https://docs.cloud.google.com/sql/docs/postgres/use-cloudsql-mcp#required-roles)
- **Make MCP tool calls in a project**: MCP Tool User (roles/mcp.toolUser)
- **Create a backup of a Cloud SQL instance**: Cloud SQL Editor (roles/cloudsql.editor)
- **Create an OAuth client ID**: OAuth Config Editor (roles/oauthconfig.editor)
- **Create, clone, restore from backup, or update a Cloud SQL instance**: Cloud SQL Admin (roles/cloudsql.admin)
- **Create or update a Cloud SQL user**: Cloud SQL Admin (roles/cloudsql.admin)
- **Create secrets and access secret versions in Secret Manager**: Secret Manager Admin (roles/secretmanager.admin)
- **Execute SQL statements (including read-only) in Cloud SQL**:
    - Cloud SQL Admin (roles/cloudsql.admin)
    - Cloud SQL Studio User (roles/cloudsql.StudioUser)
- **Get a Cloud SQL instance or list all Cloud SQL instances in a project**: Cloud SQL Viewer (roles/cloudsql.viewer)
- **Import data into a Cloud SQL instance**:
    - Cloud SQL Admin (roles/cloudsql.admin)
    - Storage Admin (roles/storage.admin)
- **List Cloud SQL users**: Cloud SQL Viewer (roles/cloudsql.viewer)
- **Perform a precheck before upgrading the major version of PostgreSQL**: Cloud SQL Admin (roles/cloudsql.admin)

---

## Firestore
[documentation](https://docs.cloud.google.com/firestore/native/docs/use-firestore-mcp#required-roles)
- **Make MCP tool calls**: MCP Tool User (roles/mcp.toolUser)
- **Read and edit Firestore documents**: Firestore User (roles/datastore.user)

---

## AlloyDB
[documentation](https://docs.cloud.google.com/alloydb/docs/ai/use-alloydb-mcp#required-roles)
- **Create an AlloyDB instance**: AlloyDB Admin (roles/alloydb.admin)
- **Create an AlloyDB user**: AlloyDB Admin (roles/alloydb.admin)
- **Execute SQL queries in AlloyDB**:
    - AlloyDB Admin (roles/alloydb.admin)
    - AlloyDB Database User (roles/alloydb.databaseUser) (Studio Query User (roles/databasesconsole.studioQueryUser) also works)
- **Execute read-only SQL queries in AlloyDB**:
    - AlloyDB Viewer (roles/alloydb.viewer)
    - AlloyDB Admin (roles/alloydb.admin)
    - AlloyDB Database User (roles/alloydb.databaseUser)
- **Get a AlloyDB instance or list all AlloyDB instances in a project**: AlloyDB Viewer (roles/alloydb.viewer)
- **List AlloyDB users**: AlloyDB Viewer (roles/alloydb.viewer)

---

## DatabaseCenter
[documentation](https://docs.cloud.google.com/database-center/docs/use-database-center-mcp#required-roles)
- **Make MCP tool calls**: MCP Tool User (roles/mcp.toolUser)
- **Use Database Center MCP tools**: Database Center Viewer (roles/databasecenter.viewer)
