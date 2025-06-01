import yaml
import re
import logging
from flask import Flask, request, jsonify
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('waf.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

class WAF:
    def __init__(self, rules_file):
        self.rules = self._load_rules(rules_file)

    def _load_rules(self, rules_file):
        """Load rules from YAML file"""
        with open(rules_file, 'r') as f:
            rules_data = yaml.safe_load(f)
            return rules_data['rules']

    def _extract_request_parts(self, request):
        """Extract different parts of the HTTP request"""
        return {
            'url': request.url,
            'query_params': request.args,
            'headers': request.headers,
            'post_body': request.get_data(as_text=True)
        }

    def _match_rule(self, rule, request_parts):
        """Check if request matches a specific rule"""
        for target in rule['target']:
            target_data = request_parts.get(target, '')
            if isinstance(target_data, dict):
                target_data = '&'.join([f"{k}={v}" for k, v in target_data.items()])
            
            if re.search(rule['pattern'], target_data, re.IGNORECASE):
                return True
        return False

    def inspect_request(self, request):
        """Inspect request against all rules"""
        request_parts = self._extract_request_parts(request)
        
        for rule in self.rules:
            if self._match_rule(rule, request_parts):
                # Log the blocked attempt
                log_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'client_ip': request.remote_addr,
                    'rule_id': rule['id'],
                    'description': rule['description'],
                    'action': rule['action'],
                    'request': {
                        'url': request.url,
                        'method': request.method,
                        'headers': dict(request.headers)
                    }
                }
                logging.warning(f"Blocked request: {log_entry}")
                
                if rule['action'] == 'block':
                    return False, log_entry
        return True, None

# Initialize WAF
waf = WAF('rules.yaml')

@app.before_request
def waf_middleware():
    """WAF middleware to inspect all incoming requests"""
    allowed, log_entry = waf.inspect_request(request)
    if not allowed:
        return jsonify({
            'error': 'Request blocked by WAF',
            'rule': log_entry['rule_id'],
            'description': log_entry['description']
        }), 403

@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'Welcome to MiniWAF protected application'
    })

@app.route('/test-sqli')
def test_sqli():
    return jsonify({
        'status': 'ok',
        'message': 'SQLi test endpoint'
    })

@app.route('/test-xss')
def test_xss():
    return jsonify({
        'status': 'ok',
        'message': 'XSS test endpoint'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
