from flask import Flask, send_from_directory, jsonify, request
from engine.mas_orchestrator import run_reconciliation

app = Flask(__name__, static_folder='.')

# 1. Host the Front-End Website
@app.route('/')
def serve_index():
    """Serves the main single-page website."""
    return send_from_directory('.', 'index.html')

# 2. Connect the MAS Engine (API Endpoints)
@app.route('/api/simulate', methods=['POST'])
def trigger_simulation():
    """
    Endpoint to trigger the Python MAS Engine.
    The frontend 'Run Simulation' button calls this API.
    """
    data = request.json or {}
    ledger_data = data.get("ledger_data", "Default Q3 Ledger Data")
    
    # Trigger the AutoGen Multi-Agent Engine
    chat_history = run_reconciliation(ledger_data)
    
    return jsonify({
        "status": "success",
        "message": "MAS Engine finished.",
        "chat_history": chat_history
    })

if __name__ == '__main__':
    print("========================================")
    print("Starting MAS Reconciliation Server...")
    print("Serving full UI at: http://localhost:5000")
    print("========================================")
    app.run(port=5000, debug=True)
