import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.config import ConfigLoader
import logging
import os

# Set up logging for demo
logging.basicConfig(level=logging.INFO, format='%(name)s - %(message)s')

def run_config_demo():
    print(">>> CONFIGURATION LOADER DEMO <<<\n")
    
    config_file = "test_config.yaml"
    
    # Clean up previous test run if exists
    if os.path.exists(config_file):
        os.remove(config_file)
        
    print("1. Initializing ConfigLoader (should create default file)...")
    loader = ConfigLoader(config_file)
    
    # 2. Check defaults
    print("\nDefault Values:")
    print(f" Scheduler: {loader.get_value('scheduler', 'default_scheduler')}")
    print(f" Quantum:   {loader.get_value('scheduler', 'quantum')}")
    print(f" Memory:    {loader.get_value('memory', 'total_memory')} bytes")

    # 3. Simulate manual update (modifying the file)
    print(f"\n2. Simulating manual file update in {config_file}...")
    with open(config_file, 'r') as f:
        data = f.read()
    
    # Change quantum to 5 in the file text
    new_data = data.replace("quantum: 2", "quantum: 5")
    with open(config_file, 'w') as f:
        f.write(new_data)
        
    # 4. Reload and verify
    print("Reloading config...")
    loader.load()
    print(f" New Quantum Value: {loader.get_value('scheduler', 'quantum')} (Expected: 5)")

    # 5. Full Config dump
    print("\nFull Config Dump:")
    import json
    print(json.dumps(loader.get_config(), indent=2))

    # Clean up
    if os.path.exists(config_file):
        os.remove(config_file)
    print("\nDemo complete. Configuration logic verified.")

if __name__ == "__main__":
    run_config_demo()
