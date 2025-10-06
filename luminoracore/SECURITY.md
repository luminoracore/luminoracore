# Security Policy

## Supported Versions

We provide security updates for the following versions of LuminoraCore:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in LuminoraCore, please report it responsibly.

### How to Report

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please:

1. **Email us directly**: Send details to security@luminoracore.dev
2. **Include the following information**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)
   - Your contact information

### What to Expect

- **Acknowledgment**: We'll acknowledge receipt within 48 hours
- **Initial Response**: We'll provide an initial response within 72 hours
- **Regular Updates**: We'll keep you informed of our progress
- **Resolution Timeline**: We aim to resolve issues within 30 days

### Responsible Disclosure

We follow responsible disclosure practices:

1. **No Public Disclosure**: We won't disclose the vulnerability publicly until it's fixed
2. **Credit**: We'll credit you for the discovery (unless you prefer anonymity)
3. **Coordination**: We'll work with you to coordinate the disclosure timeline

## Security Considerations

### Personality Validation

LuminoraCore includes several security measures for personality validation:

- **Schema Validation**: All personalities must conform to the JSON schema
- **Content Filtering**: Built-in content filters for inappropriate material
- **Safety Guards**: Configurable safety measures and forbidden topics
- **Input Sanitization**: Proper validation of all inputs

### Best Practices

When creating personalities:

1. **Avoid Sensitive Information**: Don't include personal data or credentials
2. **Set Safety Guards**: Always configure appropriate content filters
3. **Validate Thoroughly**: Use the validation tools before deployment
4. **Review Examples**: Ensure sample interactions are appropriate
5. **Test Safely**: Test personalities in controlled environments

### Compilation Security

The compilation process includes:

- **Provider Validation**: Ensures compatibility with target providers
- **Token Estimation**: Prevents overly long prompts
- **Format Validation**: Ensures proper output formatting
- **Error Handling**: Graceful handling of compilation errors

## Security Features

### Built-in Protections

- **Content Filtering**: Automatic filtering of inappropriate content
- **Input Validation**: Comprehensive validation of all inputs
- **Error Handling**: Secure error handling without information leakage
- **Dependency Management**: Regular updates of dependencies

### Configuration

You can configure security settings:

```python
# Example: Setting up safety guards
safety_guards = {
    "forbidden_topics": ["violence", "adult content"],
    "content_filters": ["profanity", "hate speech"],
    "tone_limits": {
        "max_aggression": 0.1,
        "max_informality": 0.3
    }
}
```

## Vulnerability Types

We're particularly interested in:

- **Code Injection**: Any way to execute arbitrary code
- **Data Exposure**: Unintended exposure of sensitive data
- **Authentication Bypass**: Ways to bypass security measures
- **Input Validation**: Bypassing input validation
- **Dependency Vulnerabilities**: Issues in our dependencies

## Security Updates

We regularly:

- **Update Dependencies**: Keep all dependencies up to date
- **Security Audits**: Conduct regular security reviews
- **Penetration Testing**: Test for vulnerabilities
- **Code Reviews**: Review all code changes for security issues

## Contact

For security-related questions or concerns:

- **Email**: security@luminoracore.dev
- **Response Time**: We aim to respond within 24-48 hours
- **Confidentiality**: All communications are treated as confidential

## Acknowledgments

We appreciate the security research community and responsible disclosure practices. Security researchers who help us improve LuminoraCore's security will be acknowledged (unless they prefer anonymity).

## Legal

By reporting a vulnerability, you agree to:

- Not access or modify data that doesn't belong to you
- Not disrupt our services or systems
- Not publicize the vulnerability until we've had a chance to fix it
- Act in good faith and avoid privacy violations or service disruption

Thank you for helping keep LuminoraCore secure! 🔒
