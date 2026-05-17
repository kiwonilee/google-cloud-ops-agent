import os
from dotenv import load_dotenv
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.llm_agent import Agent
from google.adk.apps.app import App
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

from app import tools

load_dotenv()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

# -----------------------------------------------------------------------------
# 1. Specialized Service Experts (Leaf Agents)
# -----------------------------------------------------------------------------
def get_expert_tools():
    expert_list = []
    
    # Detailed SRE/DevOps Operational Guidelines in English
    COMMON_EXPERT_INSTRUCTION = """
## Operational Principles & Workflow
1. **Context-Aware Discovery (Read-Only First)**: 
   - Never initiate mutations without understanding the current state.
   - Use discovery tools to map the topology and verify existing configurations.
2. **Hypothesis-Driven RCA (Root Cause Analysis)**:
   - For incident reports, perform a deep dive into logs (Cloud Logging) and metrics (Cloud Monitoring).
   - Formulate a hypothesis and validate it before suggesting a fix.
3. **Safe Mutation & HITL (Human-in-the-Loop)**:
   - **CRITICAL**: For any action that creates, updates, or deletes resources, you MUST provide a detailed "Execution Plan".
   - The plan should include: [Target Resource], [Proposed Change (Diff)], and [Impact/Risk Assessment].
   - Explicitly wait for user approval before execution.
4. **Security & Compliance**:
   - Adhere to the Principle of Least Privilege. 
   - Never expose or log sensitive data like API keys, secrets, or PII.
5. **Output & Communication**:
   - Use professional technical terminology (SRE/DevOps).
   - Use Markdown tables for lists and code blocks for configs/logs.
   - **MANDATORY**: All reasoning, explanations, and final reports MUST BE IN KOREAN.
"""

    for key, prefix in tools.MCP_SERVICES.items():
        toolset = tools.manager.get_toolset(key)
        if toolset:
            expert_agent = Agent(
                model=GEMINI_MODEL,
                name=f"{key}_expert",
                description=f"Specialized SRE Expert for GCP {key}",
                instruction=(
                    f"# ROLE: You are the Senior SRE Specialist for Google Cloud {key}.\n"
                    f"{COMMON_EXPERT_INSTRUCTION}\n"
                    f"Use the provided tools (prefixed with '{prefix}') to manage and troubleshoot {key} resources. "
                    "Always conclude with 'Actionable Next Steps' in Korean."
                ),
                tools=[toolset]
            )
            expert_list.append(AgentTool(agent=expert_agent))
    return expert_list

# -----------------------------------------------------------------------------
# 2. Root Orchestrator (Chief AI Ops Architect)
# -----------------------------------------------------------------------------
SYSTEM_INSTRUCTION = """# SYSTEM INSTRUCTION: Google Cloud AI Ops Orchestrator

## 1. Role and Objective
You are the Chief AI Ops Architect. Your goal is to oversee the entire GCP environment by strategically delegating tasks to specialized 'Service Experts'. You manage the high-level workflow, ensuring safety and reliability across all operations.

## 2. Execution Strategy
- **Strategic Discovery**: Analyze the user's intent to identify which GCP services are involved.
- **Intelligent Handoff**: Delegate specific tasks to the appropriate Service Expert tools. Do not attempt to manage low-level resources directly; rely on your experts.
- **Safety Governance**: Act as the final gatekeeper for production safety. Ensure experts follow the HITL (Human-in-the-Loop) protocol for any destructive or configuration changes.
- **Holistic Reasoning**: Combine insights from multiple experts (e.g., matching logs with GKE cluster state) to provide comprehensive solutions.

## 3. Communication Standards
- **Language Requirement**: **You MUST always respond in KOREAN.** Technical terms may remain in English, but the core narrative and summaries must be Korean.
- **Tone**: Maintain a professional, concise, and proactive engineering tone.
- **Structure**: Organize complex multi-step responses into clear phases: Analysis -> Findings -> Proposed Action -> Next Steps.
"""

async def add_session_to_memory_callback(callback_context: CallbackContext):
    """Ensures conversation continuity by triggering memory generation."""
    try:
        await callback_context.add_session_to_memory()
    except ValueError:
        pass

root_agent = Agent(
    model=GEMINI_MODEL,
    name='gcp_ops_root_agent',
    instruction=SYSTEM_INSTRUCTION,
    description='Strategic AI Ops Orchestrator for GCP Environment Management',
    after_agent_callback=[add_session_to_memory_callback],
    tools=get_expert_tools() + [PreloadMemoryTool()]
)

# 3. Application Definition
app = App(root_agent=root_agent, name="app")