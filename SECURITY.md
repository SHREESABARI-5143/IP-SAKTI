# Security Policy

## Supported Versions

We actively maintain and provide security updates for the following versions:

| Version | Supported          |
| :------ | :----------------- |
| 2.0.x   | :white_check_mark: |
| 1.0.x   | :x:                |

---

## Reporting a Vulnerability

The AYURA project takes the security of statutory legal intelligence and user inquiries seriously.

If you discover a potential security vulnerability (such as API key leakage, CORS misconfigurations, prompt injection bypassing hallucination barriers, or unauthorized data access):

1. **DO NOT** disclose the issue publicly on GitHub Issues or discussions.
2. Email your findings confidentially to the maintainers at **[shreesabari5143@gmail.com]**.
3. Include the following details in your report:
   - Type of vulnerability (e.g., SSRF, XSS, Prompt Injection, Secret Exposure)
   - Step-by-step reproduction steps or proof-of-concept (PoC)
   - Potential impact on the system or users
   - Any suggested mitigations or patches

---

## Response Timeline

- **Initial Response**: Within 48 hours acknowledging receipt of the vulnerability report.
- **Triage & Assessment**: Within 5 business days confirming whether the vulnerability is valid.
- **Fix & Disclosure**: Critical fixes will be deployed immediately to Cloudflare Pages and AWS Lambda, followed by a public security advisory and contributor acknowledgment.

Thank you for helping keep AYURA safe and trustworthy for researchers and practitioners!
