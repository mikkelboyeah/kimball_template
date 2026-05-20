"""Convenient launcher for the DuckDB UI to visualize and explore analytics data."""

import duckdb
import os
import time

def main():
    """
    Launch the DuckDB UI server for the analytics database.

    Connects to the ``db.duckdb`` database in the ``data`` directory,
    installs and loads the DuckDB UI extension, starts the embedded UI server
    (opening it in a web browser), and keeps the process alive until interrupted.
    On Ctrl+C, the UI server is stopped and the process exits cleanly.
    """
    db_path = os.path.join("data", "db.duckdb")
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    print(f"Connecting to {db_path}...")
    # Connect to the database
    con = duckdb.connect(db_path)
    try:
        print("Installing and loading UI extension...")
        con.execute("INSTALL ui; LOAD ui;")
        
        print("Launching DuckDB UI in your browser...")
        print("Press Ctrl+C to close the UI and exit.")
        
        # This opens the browser and starts the embedded server
        con.execute("CALL start_ui();")
        
        # Keep the process alive so the server continues to run
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping DuckDB UI server...")
            con.execute("CALL stop_ui_server();")
            print("Done.")
    finally:
        con.close()

if __name__ == "__main__":
    main()
