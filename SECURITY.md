# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of PrepGenie seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to [thakurg39@gmail.com] .

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information in your report:

* Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
* Full paths of source file(s) related to the manifestation of the issue
* The location of the affected source code (tag/branch/commit or direct URL)
* Any special configuration required to reproduce the issue
* Step-by-step instructions to reproduce the issue
* Proof-of-concept or exploit code (if possible)
* Impact of the issue, including how an attacker might exploit it

## API Key Security

PrepGenie requires several API keys to function. To keep these secure:

1. Never commit API keys to version control
2. Store API keys in a `.env` file which is listed in `.gitignore`
3. Use environment variables in production environments
4. Regularly rotate API keys
5. Use the principle of least privilege when creating API keys

## Best Practices

When contributing to PrepGenie, please ensure you follow these security best practices:

1. Keep all dependencies up to date
2. Use strong input validation
3. Implement proper error handling
4. Follow the principle of least privilege
5. Use secure communication protocols
6. Properly handle sensitive data
7. Implement logging and monitoring

## Disclosure Policy

When we receive a security bug report, we will:

* Confirm the problem and determine the affected versions
* Audit code to find any potential similar problems
* Prepare fixes for all still-maintained versions
* Release new versions as soon as possible

## Comments on this Policy

If you have suggestions on how this process could be improved, please submit a pull request. 