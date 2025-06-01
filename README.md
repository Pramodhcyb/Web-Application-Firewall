# MiniWAF - A Simple Web Application Firewall Rule Engine

[![GitHub license](https://img.shields.io/github/license/yourusername/miniwaf)](https://github.com/yourusername/miniwaf)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/miniwaf)](https://github.com/yourusername/miniwaf/issues)

MiniWAF is a simplified Web Application Firewall (WAF) implementation that demonstrates core WAF functionality. It acts as a middleware component in a Flask web application, inspecting incoming HTTP requests against predefined security rules and blocking malicious traffic.

## 🚀 Features

- 🔍 HTTP request inspection and blocking
- 📄 Configurable security rules using YAML
- 🛡️ Detection of common web vulnerabilities:
  - SQL Injection
  - Cross-Site Scripting (XSS)
  - Path Traversal
  - Command Injection
- 📝 Comprehensive logging of blocked requests
- 🔄 Easy to extend with additional rules
- 📊 Real-time request monitoring
- 📚 Detailed documentation

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/miniwaf.git
cd miniwaf
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the WAF:
```bash
python waf.py
```

The WAF will start on http://localhost:5000

## 🧪 Testing

You can test the WAF by making requests to different endpoints:

1. Normal request (should pass):
```bash
curl http://localhost:5000/
```

2. SQL Injection attempt (should be blocked):
```bash
curl "http://localhost:5000/test-sqli?id=1' OR '1'='1"
```

3. XSS attempt (should be blocked):
```bash
curl "http://localhost:5000/test-xss?data=<script>alert('XSS')</script>"
```

4. Path Traversal attempt (should be blocked):
```bash
curl "http://localhost:5000/../../../../etc/passwd"
```

## 📝 Rule Configuration

The WAF uses YAML configuration for its rules. You can find the default rules in `rules.yaml`. Each rule contains:

- `id`: Unique identifier for the rule
- `pattern`: Regular expression pattern to match against
- `target`: Parts of the HTTP request to inspect (url, query_params, headers, post_body)
- `action`: What to do when the rule matches (block/log_only)
- `description`: Human-readable description of what the rule detects

Example rule:
```yaml
rules:
  - id: SQLI-001
    pattern: "['\"\\s](or|and)\\s+\\d+=\\d+.*"
    target: ["query_params", "post_body"]
    action: "block"
    description: "Detects common SQL Injection patterns (e.g., ' OR 1=1--)"
```

## 📊 Logging

All blocked requests are logged to `waf.log` with detailed information about:
- Timestamp
- Client IP address
- Matched rule
- Request details
- Action taken

Example log entry:
```
2025-06-01 00:05:22 - WARNING - Blocked request: 
    Timestamp: 2025-06-01T00:05:22+05:30
    Client IP: 127.0.0.1
    Rule ID: SQLI-001
    Description: Detects common SQL Injection patterns
    Action: block
```

## 🛠️ Adding New Rules

1. Open `rules.yaml`
2. Add a new rule following the existing format
3. The WAF will automatically load the new rules on restart

Example of adding a new rule:
```yaml
rules:
  - id: CMD-002
    pattern: "exec\(|system\(|shell_exec\(|popen\("
    target: ["post_body", "query_params"]
    action: "block"
    description: "Detects PHP command execution attempts"
```

## 🚦 Security Considerations

This is a simplified implementation for educational purposes. In a production environment:
- Use HTTPS for secure communication
- Implement rate limiting
- Use more sophisticated pattern matching
- Add request/response normalization
- Consider performance optimizations
- Implement proper error handling
- Add request/response logging
- Consider implementing whitelisting
- Regular security audits

## 📚 Documentation

### Project Structure
```
mini-waf/
├── waf.py              # Main WAF implementation
├── rules.yaml          # Security rules configuration
├── requirements.txt    # Python dependencies
├── waf.log             # Log file for blocked requests
├── README.md           # Project documentation
└── docs/               # Additional documentation
```

### Configuration Files

- `rules.yaml`: Contains all security rules
- `waf.log`: Stores blocked request logs
- `requirements.txt`: Lists Python dependencies

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- Thanks to the Flask community for their excellent web framework
- Special thanks to contributors who have helped improve this project

## 📞 Support

For support, please:
- Open an issue in the GitHub repository
- Check the documentation first
- Provide detailed information about your problem

## 🔍 Project Status

This project is actively maintained and open to contributions. We welcome feedback and improvements from the community.

## 🎯 Future Improvements

- Add more sophisticated pattern matching
- Implement machine learning-based threat detection
- Add real-time dashboard for monitoring
- Improve performance optimization
- Add support for more web vulnerabilities
- Implement request/response normalization
- Add comprehensive testing suite
