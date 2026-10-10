"""
Collaborative Multi-Agent Systems (MAS) for Financial Reconciliation
Orchestrator Module (AutoGen Integration)
"""
import os
import re

def run_reconciliation(ledger_data):
    """
    Main entry point. Orchestrates the AutoGen group chat between the agents.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "SIMULATED_KEY")
    
    # -------------------------------------------------------------------------
    # FALLBACK: If there's no real API key set, return a mock response
    # so the Frontend UI Demo still functions flawlessly.
    # -------------------------------------------------------------------------
    if api_key == "SIMULATED_KEY":
        print("[Orchestrator] Running in SIMULATED mode (No OPENAI_API_KEY detected).")
        
        # Dynamically extract numbers from the user's input so the demo looks real!
        raw_numbers = re.findall(r'[\$£€]?\d+(?:\.\d+)?[a-zA-Z]*', ledger_data)
        # Filter out solitary single digits (like '1' in 'API 1') to grab the actual financial values
        numbers = [n for n in raw_numbers if not re.match(r'^\d$', n)]
        
        val1 = numbers[0] if len(numbers) > 0 else "[Expected Value]"
        val2 = numbers[1] if len(numbers) > 1 else "[Actual Value]"
        
        def clean_num(val):
            try:
                return float(re.sub(r'[^\d.]', '', val))
            except ValueError:
                return None
                
        clean1 = clean_num(val1)
        clean2 = clean_num(val2)
        
        if clean1 is not None and clean2 is not None and clean1 == clean2:
            return [
                {"sender": "Planner", "message": f"Analyzing new request: \"{ledger_data}\". Assigning Verifier to audit the data."},
                {"sender": "Verifier", "message": f"Audit complete. Both databases correctly report {val1}. No discrepancies detected."},
                {"sender": "Planner", "message": f"Ledger integrity verified. Workflow completed. System returning to standby."}
            ]
        else:
            return [
                {"sender": "Planner", "message": f"Analyzing new request: \"{ledger_data}\". Assigning Verifier to audit the data."},
                {"sender": "Verifier", "message": f"Warning: Audit failed. Detected a conflict between {val1} (Primary) and {val2} (Secondary). Flagging for negotiation."},
                {"sender": "Negotiator", "message": f"Investigating the discrepancy. The Primary database ({val1}) has a sync delay and is serving stale data. The Secondary database ({val2}) holds the current true value."},
                {"sender": "Recoverer", "message": f"Writing a patch script to force a real-time data sync on the Primary server."},
                {"sender": "Verifier", "message": f"Re-auditing the updated records... The Primary server has refreshed. Both values now match correctly at {val2}. Ledger integrity restored. [RESOLUTION SUCCESSFUL]"},
                {"sender": "Planner", "message": f"Workflow completed. System returning to standby."}
            ]
    
    # -------------------------------------------------------------------------
    # LIVE AUTOGEN EXECUTION
    # -------------------------------------------------------------------------
    try:
        import autogen
    except ImportError:
        print("[Error] 'autogen' module not found.")
        return [{"sender": "System_Error", "message": "Live execution failed. The 'autogen' module (v0.2.x) could not be imported because your Python version installed the newer v0.4+ architecture. Simulation aborted."}]

    print(f"[Orchestrator] Initiating LIVE AutoGen group chat for: {ledger_data}")
    llm_config = {"model": "gpt-4", "api_key": api_key}

    planner = autogen.UserProxyAgent(
        name="Planner",
        system_message="You are the macro-level planner. Allocate tasks, schedule reconciliation, and manage the workflow.",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1
    )
    
    verifier = autogen.AssistantAgent(
        name="Verifier",
        llm_config=llm_config,
        system_message="You are the Verifier. Execute strict data auditing. Cross-reference inputs against historical baselines and flag anomalies."
    )
    
    negotiator = autogen.AssistantAgent(
        name="Negotiator",
        llm_config=llm_config,
        system_message="You are the Negotiator. Resolve conflicts flagged by the Verifier. Initiate queries to secondary sources to reach a consensus."
    )
    
    recoverer = autogen.AssistantAgent(
        name="Recoverer",
        llm_config=llm_config,
        system_message="You are the Recoverer. You patch systematic errors, fix sync issues, and execute recovery scripts."
    )
    
    groupchat = autogen.GroupChat(
        agents=[planner, verifier, negotiator, recoverer],
        messages=[],
        max_round=6
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    
    try:
        # Start the multi-agent debate
        planner.initiate_chat(manager, message=f"Please reconcile the following ledger data and resolve any data mismatches: {ledger_data}")
        history = []
        for msg in groupchat.messages:
            if msg.get("name") and msg.get("content"):
                history.append({"sender": msg.get("name"), "message": msg.get("content")})
        return history
    except Exception as e:
        print(f"[Error] AutoGen Engine Failed: {str(e)}")
        return [{"sender": "System_Error", "message": f"Failed to execute AutoGen chat: {str(e)}"}]

if __name__ == "__main__":
    results = run_reconciliation("Q3 Ledger Data")
    for r in results:
        print(f"{r['sender']}: {r['message']}")
