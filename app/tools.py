import os
import logging
from typing import Dict, Optional

import google.auth
import google.auth.transport.requests
from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset

# 로깅 설정
logger = logging.getLogger("google_adk.gcp_ops_agent.tools")
load_dotenv()

# -----------------------------------------------------------------------------
# MCP Service Definitions
# -----------------------------------------------------------------------------
MCP_SERVICES = {
    "compute_engine": "gce_",
    "cloud_run": "run_",
    "kubernetes_engine": "gke_",
    "cloud_storage": "gcs_",
    "network_management": "nic_",
    "gemini_cloud_assist": "gca_",
    "cloud_trace": "trace_",
    "cloud_logging": "logging_",
    "cloud_monitoring": "monitoring_",
    "error_reporting": "error_",
    "bigquery": "bq_",
    "bigtable": "bt_",
    "cloud_sql": "sql_",
    "firestore": "fs_",
    "alloydb": "alloy_",
    "database_center": "dbc_",
    "database_insights": "dbi_",
}

class McpManager:
    """MCP 연결 및 인증을 관리하는 싱글톤 클래스"""
    
    def __init__(self):
        self._cache: Dict[str, McpToolset] = {}
        self._credentials = None

    def _get_credentials(self):
        """인증 정보를 확인하고 필요시 갱신합니다."""
        if not self._credentials or not self._credentials.valid:
            logger.info("GCP 자격 증명 갱신 중...")
            scopes = ["https://www.googleapis.com/auth/cloud-platform"]
            self._credentials, _ = google.auth.default(scopes=scopes)
            auth_request = google.auth.transport.requests.Request()
            self._credentials.refresh(auth_request)
        return self._credentials

    def _get_dynamic_headers(self, context=None) -> Dict[str, str]:
        """도구 호출 직전에 최신 인증 토큰을 포함한 헤더를 제공합니다."""
        creds = self._get_credentials()
        return {"Authorization": f"Bearer {creds.token}"}

    def get_toolset(self, name: str) -> Optional[McpToolset]:
        """이름을 기반으로 MCP Toolset을 동적으로 생성하거나 캐시에서 반환합니다."""
        if name not in self._cache:
            if name not in MCP_SERVICES:
                raise ValueError(f"지원하지 않는 MCP 서비스입니다: {name}")

            prefix = MCP_SERVICES[name]
            env_key = f"MCP_ENDPOINT_{name.upper()}"
            url = os.getenv(env_key)

            if not url:
                logger.warning(f"환경 변수 {env_key}가 설정되지 않아 '{name}' MCP Toolset을 건너뜁니다.")
                return None

            try:
                logger.info(f"MCP 서버 연결 초기화: {name} ({url})")
                # header_provider를 사용하여 토큰 만료 문제를 근본적으로 해결합니다.
                self._cache[name] = McpToolset(
                    connection_params=StreamableHTTPConnectionParams(
                        url=url,
                        timeout=30.0,
                        sse_read_timeout=600.0  # 긴 작업(로깅 분석 등)을 위해 10분으로 상향
                    ),
                    tool_name_prefix=prefix,
                    header_provider=self._get_dynamic_headers
                )
            except Exception as e:
                logger.warning(f"'{name}' MCP Toolset 초기화 중 오류 발생: {e}")
                logger.warning(f"'{name}' 관련 도구는 비활성화됩니다.")
                return None
        return self._cache.get(name)

# 싱글톤 인스턴스
manager = McpManager()