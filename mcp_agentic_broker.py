# ==========================================================================
# 🤖 SOVEREIGN MCP AGENTIC BROKER CORE ENGINE - INTEGRATED RATE LIMITER UPGRADE
# ==========================================================================
import sys
import os
import json
import sqlite3
import time
import asyncio
from datetime import datetime

class SovereignMCPAgenticBroker:
    """
    Enterprise-Grade Model Context Protocol (MCP) Server engineered to expose 
    sub-millisecond relational telemetry logs securely to Autonomous AI Agents,
    insulated via an active Asynchronous Token Bucket Rate Limiter.
    """
    def __init__(self, db_path="medical_registry_production.db"):
        self.db_path = db_path
        self.broker_status = "OPERATIONAL"
        self.protocol_version = "2026.1.0"
        
        # ⚡ THE SECURITY UPGRADE: Token Bucket Rate Limiting Parameters
        self.rate_limiter_enabled = True
        self.max_burst_capacity = 100        # Max tokens in a single surge wave
        self.current_tokens = 100.0          # Initial bucket pool allocation
        self.refill_rate_per_sec = 10        # Refill velocity of core resources
        self.last_refill_timestamp = time.time()
        
        print("🤖 [MCP Armed] Model Context Protocol Ingress Broker initialized safely.")
        print(f"📡 Target Persistence Layer: {os.path.abspath(self.db_path)}")
        print(f"🔒 [Security Active] Rate Limiter Bucket Installed: Capacity ({self.max_burst_capacity}), Refill ({self.refill_rate_per_sec}/sec).\n")
        
        # Initialize internal table schemas automatically if missing in this directory
        self.ensure_table_exists()

    def ensure_table_exists(self):
        """Guarantees the tracking table exists so the AI agent doesn't catch OperationalErrors."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS async_router_telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                latency REAL NOT NULL,
                shield_status INTEGER NOT NULL,
                threads INTEGER NOT NULL,
                recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # Seed a mock telemetry trace instantly if the database is brand new
        cursor.execute("SELECT COUNT(*) FROM async_router_telemetry;")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO async_router_telemetry (source, latency, shield_status, threads)
                VALUES ('Sovereign_AI_Agent_Node', 0.1117, 1, 8);
            """)
        conn.commit()
        conn.close()

    def synchronize_token_bucket_pool(self):
        """Calculates token regeneration velocity dynamically based on microsecond delta times."""
        current_time = time.time()
        elapsed_time = current_time - self.last_refill_timestamp
        
        generated_tokens = elapsed_time * self.refill_rate_per_sec
        if generated_tokens > 0:
            self.current_tokens = min(float(self.max_burst_capacity), self.current_tokens + generated_tokens)
            self.last_refill_timestamp = current_time

    def read_telemetry_metrics(self) -> dict:
        """Exposes the internal database parameters to the AI Agent thread context."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*), AVG(latency) FROM async_router_telemetry;")
            total_records, avg_latency = cursor.fetchone()
            
            cursor.execute("""
                SELECT source, latency, shield_status, recorded_at 
                FROM async_router_telemetry 
                ORDER BY id DESC LIMIT 3;
            """)
            raw_rows = cursor.fetchall()
            conn.close()
            
            latest_logs = []
            for row in raw_rows:
                latest_logs.append({
                    "node_source": row[0],
                    "latency_ms": row[1],
                    "shield_active": True if row[2] == 1 else False,
                    "timestamp": row[3]
                })
                
            return {
                "status": "SUCCESS",
                "mcp_protocol_version": self.protocol_version,
                "analytics": {
                    "total_ingested_vectors": total_records or 0,
                    "mean_system_latency_ms": round(avg_latency or 0.0, 4)
                },
                "latest_telemetry_stream": latest_logs
            }
        except Exception as e:
            return {"status": "ERROR", "error_details": str(e)}

    def process_agent_command(self, incoming_mcp_rpc: str) -> str:
        """Processes standardized JSON-RPC query blocks sent by the AI Agent with active rate limiting protection."""
        try:
            # 🛡️ INTERCEPTOR EXECUTOR: Synchronize and evaluate remaining token allocation density
            self.synchronize_token_bucket_pool()
            if self.current_tokens < 1.0:
                print("🚨 [INGRESS DENIED] Thread starvation risk blocked via active Token Bucket Shield.")
                response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32000, 
                        "message": "HTTP 429 Too Many Requests: Rate ceiling exceeded. Connection pool insulated cleanly."
                    },
                    "principal_architect": "Sudhir Kumar Mishra"
                }
                return json.dumps(response, indent=2)

            # Deduct token upon successful security clearance pass
            self.current_tokens -= 1.0

            payload = json.loads(incoming_mcp_rpc)
            method = payload.get("method")
            
            print(f"📡 [AI Agent Ingress] Intercepted JSON-RPC Request Method: '{method}'")
            
            if method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "result": {
                        "tools": [
                            {
                                "name": "get_database_telemetry",
                                "description": "Fetches real-time sub-millisecond latency records from Sudhir's SQLite3 WAL vault."
                            }
                        ]
                    },
                    "id": payload.get("id")
                }
            elif method == "tools/call" and payload.get("params", {}).get("name") == "get_database_telemetry":
                db_data = self.read_telemetry_metrics()
                response = {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(db_data, indent=2)}]
                    },
                    "id": payload.get("id")
                }
            else:
                response = {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": payload.get("id")}
                
            return json.dumps(response, indent=2)
        except Exception as json_err:
            return json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": f"Parse error: {json_err}"}})

if __name__ == "__main__":
    broker = SovereignMCPAgenticBroker()
    
    print("=" * 80)
    print("🤖 [AI AGENT INVOCATION] Simulation Case 1: Fetching Available MCP Tools List:")
    mock_rpc_query_1 = '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
    print(broker.process_agent_command(mock_rpc_query_1))
    print("=" * 80)
    
    print("\n" + "=" * 80)
    print("🤖 [AI AGENT INVOCATION] Simulation Case 2: AI Triggers 'get_database_telemetry' dynamic call:")
    mock_rpc_query_2 = '{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "get_database_telemetry"}, "id": 2}'
    print(broker.process_agent_command(mock_rpc_query_2))
    print("=" * 80)
