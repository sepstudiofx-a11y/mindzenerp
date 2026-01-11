"""
Demo script to test the MindZen ERP core engine
"""

import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from mindzen_erp.core import Engine

def main():
    """Demonstrate core engine functionality"""
    print("=" * 60)
    print("MindZen ERP - Core Engine Demo")
    print("=" * 60)
    print()
    
    # Create and initialize the engine
    print("1. Initializing engine...")
    engine = Engine()
    engine.initialize()
    print()
    
    # Show configuration
    print("2. Configuration:")
    print(f"   App Name: {engine.config.get('app_name')}")
    print(f"   Version: {engine.config.get('version')}")
    print(f"   Debug Mode: {engine.config.get('debug')}")
    print(f"   Database: {engine.config.get('database.type')}")
    print()
    
    # Discover modules
    print("3. Discovering modules...")
    engine.discover_modules()
    available = engine.modules.get_available()
    print(f"   Available modules: {available if available else 'None (modules directory empty)'}")
    print()
    
    # Test event bus
    print("4. Testing event bus...")
    
    def on_test_event(data):
        print(f"   Event received: {data}")
    
    engine.events.subscribe('test.event', on_test_event)
    engine.events.publish('test.event', {'message': 'Hello from event bus!'})
    print()
    
    # Test hooks
    print("5. Testing hook system...")
    
    def test_hook(**kwargs):
        print(f"   Hook executed with args: {kwargs}")
        return "hook_result"
    
    engine.hooks.register_hook('test_hook', test_hook)
    results = engine.hooks.execute('test_hook', param1='value1', param2='value2')
    print(f"   Hook results: {results}")
    print()
    
    # Show engine status
    print("6. Engine status:")
    print(f"   Initialized: {engine.is_initialized}")
    print(f"   Installed modules: {engine.get_installed_modules()}")
    print(f"   Event subscriptions: {engine.events.get_event_names()}")
    print()
    
    # Shutdown
    print("7. Shutting down engine...")
    engine.shutdown()
    print()
    
    print("=" * 60)
    print("Demo complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
