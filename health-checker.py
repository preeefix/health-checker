import yaml
import requests
import time
from urllib.parse import urlparse
from collections import defaultdict
import sys
import signal

class HealthChecker:
    def __init__(self, config_path):
        """Initialize the health checker with a config file path."""
        self.config_path = config_path
        self.endpoints = self._load_config()
        # Track requests and successes per domain
        self.domain_stats = defaultdict(lambda: {"requests": 0, "successes": 0})
        # Setup signal handler for graceful exit
        signal.signal(signal.SIGINT, self._handle_exit)

    def _load_config(self):
        """Load and parse the YAML configuration file."""
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
                # Ensure default values are set for optional fields
                for endpoint in config:
                    endpoint.setdefault('method', 'GET')
                    endpoint.setdefault('headers', {})
                    endpoint.setdefault('body', None)
                return config
        except Exception as e:
            print(f"Error loading configuration: {e}")
            sys.exit(1)

    def _get_domain(self, url):
        """Extract domain from URL."""
        return urlparse(url).netloc

    def _check_endpoint(self, endpoint):
        """Check a single endpoint and return whether it's UP or DOWN."""
        start_time = time.time()
        try:
            response = requests.request(
                method=endpoint['method'],
                url=endpoint['url'],
                headers=endpoint['headers'],
                data=endpoint['body'],
                timeout=0.5  # 500ms timeout
            )
            latency = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Check if response is successful (2xx) and latency is under 500ms
            return (200 <= response.status_code < 300) and (latency < 500)
        except Exception:
            return False

    def _update_stats(self, domain, is_up):
        """Update statistics for a domain."""
        self.domain_stats[domain]['requests'] += 1
        if is_up:
            self.domain_stats[domain]['successes'] += 1

    def _log_availability(self):
        """Log the availability percentage for each domain."""
        for domain, stats in self.domain_stats.items():
            availability = round(100 * stats['successes'] / stats['requests'])
            print(f"{domain} has {availability}% availability percentage")

    def _handle_exit(self, signum, frame):
        """Handle graceful exit on CTRL+C."""
        print("\nExiting...")
        sys.exit(0)

    def run(self):
        """Run the health checker in an infinite loop."""
        try:
            while True:
                # Check each endpoint
                for endpoint in self.endpoints:
                    domain = self._get_domain(endpoint['url'])
                    is_up = self._check_endpoint(endpoint)
                    self._update_stats(domain, is_up)
                
                # Log results after checking all endpoints
                self._log_availability()
                
                # Wait for next cycle
                time.sleep(15)
        except KeyboardInterrupt:
            self._handle_exit(None, None)

def main():
    if len(sys.argv) != 2:
        print("Usage: python health_checker.py <config_file_path>")
        sys.exit(1)
    
    checker = HealthChecker(sys.argv[1])
    checker.run()

if __name__ == "__main__":
    main()