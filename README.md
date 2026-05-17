# google-cloud-ops-agent

Google Cloud Ops Agent
이 에이전트는 **계층적 전문가 구조(Hierarchical Expert System)**를 사용하여 GKE, GCE, Storage, Logging, Monitoring 등 다양한 GCP 리소스를 지능적으로 관리합니다.

## 1. Prerequisites

### Enable Google Cloud APIs
에이전트가 사용하는 주요 서비스와 MCP 서버 연동을 위해 다음 API들을 활성화해야 합니다.
```bash
gcloud services enable \
  aiplatform.googleapis.com \
  iam.googleapis.com \
  cloudresourcemanager.googleapis.com \
  cloudtrace.googleapis.com \
  monitoring.googleapis.com \
  logging.googleapis.com \
  container.googleapis.com \
  compute.googleapis.com \
  storage.googleapis.com \
  bigquery.googleapis.com \
  clouderrorreporting.googleapis.com
```

### ProjectID setting
```bash
export PROJECT_ID=$(gcloud config get-value project)
```

### Install CLI Tools
```bash
# Install google-agents-cli
uv tool install google-agents-cli
```

## 2. Getting Started

### Authentication
로컬 테스트를 위해 Application Default Credentials를 설정합니다.
```bash
gcloud auth application-default login
```

### Setup Environment Variables
`.env` 파일에 각 서비스별 MCP 엔드포인트를 설정해야 합니다. (자세한 내용은 `.env.template` 참조)
```bash
cd google-cloud-ops-agent
cp .env.template .env
# PROJECT_ID 및 필요한 MCP_ENDPOINT_XXX 값들을 설정하세요.
```

## 3. Local Testing
```bash
agents-cli playground
```

## 4. Infrastructure & Permissions (CRITICAL)

에이전트는 단순히 조회(Viewer)하는 수준을 넘어 **분석 및 트러블슈팅 전문가**로 동작하므로, 서비스 계정(SA)에 충분한 권한이 필요합니다.

### Create Service Account
```bash
gcloud iam service-accounts create gcp-ops-agent-sa \
--description="Service account for Google Cloud Ops Agent" \
--display-name="Google Cloud Ops Agent SA"
```

### Add IAM Policy Bindings
에이전트가 관리하는 각 영역에 대한 권한을 부여합니다. 운영 환경에서는 필요에 따라 권한을 조정하십시오.
> **필수**: 이 부분은 테스트 목적으로 포함된 MCP 들에 권한을 주기 위해 문서상에 필요한 권한들을 모두 추가했습니다. 실제 사용시에는 [`RequiredRoles.md`](./RequiredRoles.md) 파일과 해당 링크를 참조하고 필요한 권한들을 줘야 합니다.
```bash
# 권한 범위를 전문가 에이전트의 역할에 맞춰 확장했습니다.
ROLES=(
  "roles/aiplatform.user"                 # Gemini 모델 호출
  "roles/mcp.toolUser"                    # MCP 도구 사용 권- 
  "roles/container.admin"                 # GKE 클러스터 및 워크로드 상세 관리
  "roles/compute.admin"                   # GCE 인스턴스 및 리소스 관리
  "roles/storage.admin"                   # Cloud Storage 버킷/객체 관리
  "roles/logging.viewer"                  # 로그 조회 및 분석 (RCA)
  "roles/monitoring.viewer"               # 메트릭 모니터링
  "roles/cloudtrace.user"                 # 분산 트레이싱 분석  
  "roles/telemetry.tracesWriter"          # 분산 트레이싱 기록
  "roles/errorreporting.viewer"           # 애플리케이션 오류 보고 확인
  "roles/bigquery.jobUser"                # BigQuery 쿼리 실행
  "roles/iam.serviceAccountUser"          # 배포 시 서비스 계정 사용
  "roles/run.developer"                   # Cloud Run 서비스 생성
  "roles/artifactregistry.reader"         # Artifact Registry 저장소 읽기
  "roles/iam.serviceAccountTokenCreator"  # 서비스 계정 토큰 생성
  "roles/container.clusterViewer"         # GKE 클러스터 조회
  "roles/storage.objectViewer"            # Storage 객체 조회
  "roles/storage.objectCreator"           # Storage 객체 생성
  "roles/networkmanagement.admin"         # 네트워크 관리자
  "roles/networkmanagement.viewer"        # 네트워크 관리 뷰어
  "roles/compute.networkViewer"           # Compute 네트워크 뷰어
  "roles/geminicloudassist.user"          # Gemini Cloud Assist 사용자
  "roles/geminicloudassist.editor"        # Gemini Cloud Assist 편집자
  "roles/geminicloudassist.admin"         # Gemini Cloud Assist 관리자
  "roles/bigquery.dataViewer"             # BigQuery 데이터 뷰어
  "roles/bigtable.admin"                  # Bigtable 관리자
  "roles/cloudsql.editor"                 # Cloud SQL 편집자
  "roles/oauthconfig.editor"              # OAuth 구성 편집자
  "roles/cloudsql.admin"                  # Cloud SQL 관리자
  "roles/secretmanager.admin"             # Secret Manager 관리자
  "roles/cloudsql.StudioUser"             # Cloud SQL Studio 사용자
  "roles/cloudsql.viewer"                 # Cloud SQL 뷰어
  "roles/datastore.user"                  # Firestore 사용자
  "roles/alloydb.admin"                   # AlloyDB 관리자
  "roles/alloydb.databaseUser"            # AlloyDB 데이터베이스 사용자
  "roles/databasesconsole.studioQueryUser" # 데이터베이스 콘솔 스튜디오 쿼리 사용자
  "roles/alloydb.viewer"                  # AlloyDB 뷰어
  "roles/databasecenter.viewer"           # 데이터베이스 센터 뷰어
)

# Loop through and add each role
for ROLE in "${ROLES[@]}"; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:gcp-ops-agent-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="$ROLE"
done
```

## 5. Deployment
agents-cli 로 배포 시 .env 를 참조하지 않아 --update-env-vars 로 값을 전달해야 합니다.
```bash
agents-cli deploy \
  --service-account gcp-ops-agent-sa@${PROJECT_ID}.iam.gserviceaccount.com \
  --region us-central1 \
  --interactive \
  --update-env-vars GOOGLE_GENAI_USE_VERTEXAI=1,GOOGLE_CLOUD_LOCATION=global,GEMINI_MODEL=gemini-3-flash-preview,GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true,OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental,OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=EVENT_ONLY,MCP_ENDPOINT_COMPUTE_ENGINE=https://compute.googleapis.com/mcp,MCP_ENDPOINT_CLOUD_RUN=https://run.googleapis.com/mcp,MCP_ENDPOINT_KUBERNETES_ENGINE=https://container.googleapis.com/mcp,MCP_ENDPOINT_CLOUD_STORAGE=https://storage.googleapis.com/storage/mcp,MCP_ENDPOINT_NETWORK_MANAGEMENT=https://networkmanagement.googleapis.com/mcp,MCP_ENDPOINT_GEMINI_CLOUD_ASSIST=https://geminicloudassist.googleapis.com/mcp,MCP_ENDPOINT_CLOUD_TRACE=https://cloudtrace.googleapis.com/mcp,MCP_ENDPOINT_CLOUD_LOGGING=https://logging.googleapis.com/mcp,MCP_ENDPOINT_CLOUD_MONITORING=https://monitoring.googleapis.com/mcp,MCP_ENDPOINT_ERROR_REPORTING=https://clouderrorreporting.googleapis.com/mcp,MCP_ENDPOINT_BIGQUERY=https://bigquery.googleapis.com/mcp,MCP_ENDPOINT_BIGTABLE=https://bigtableadmin.googleapis.com/mcp,MCP_ENDPOINT_CLOUD_SQL=https://sqladmin.googleapis.com/mcp,MCP_ENDPOINT_FIRESTORE=https://firestore.googleapis.com/mcp,MCP_ENDPOINT_ALLOYDB=https://alloydb.googleapis.com/mcp,MCP_ENDPOINT_DATABASE_CENTER=https://databasecenter.googleapis.com/mcp,MCP_ENDPOINT_DATABASE_INSIGHTS=https://databaseinsights.googleapis.com/mcp
```

## Sample Prompts

- "kiwonlee-playground 프로젝트의 GKE 클러스터 상태를 점검하고 요약해줘"
- "최근 발생한 500 에러 로그를 분석해서 원인을 찾아줘"
- "사용하지 않는 Compute Engine 인스턴스가 있는지 확인해줘"
- "특정 버킷의 권한 설정을 확인하고 보안 리스크를 알려줘"
- "클러스터의 전체 CPU/메모리 사용량을 분석하고 노드 증설이 필요한지 판단해줘"
