# SECURITY POLICY 

The Dashfena project is committed to maintaining a secure environment
for all users and contributors. This document describes the security
policies, responsible disclosure process, and supported versions.

## SUPPORTED VERSIONS 

Only the following versions of Dashfena receive security updates:

| Version | Supported |
|----------|------------|
| 3.x      | Yes        |
| 2.x      | Security patches only |
| 1.x      | No longer supported |

## REPORTING A VULNERABILITY 

If you discover a security vulnerability, please report it responsibly
and privately instead of disclosing it publicly.

### Contact Information: 
- Email: security@dashfena.bps.go.id
- GitHub: https://github.com/fbrianzy/dashfena/issues (mark as "Security")

Please include the following in your report:
- Detailed description of the vulnerability
- Steps to reproduce
- Potential impact and affected components
- Suggested fix or mitigation (if available)

You will receive an acknowledgment within 72 hours.
If confirmed, we will issue a patch as soon as possible
and credit you in the release notes (if desired).

## DISCLOSURE PROCESS 

1. Vulnerability is reported privately to the maintainer.
2. The issue is verified and classified by severity.
3. A patch is developed and tested internally.
4. A security advisory is published with a fix and version update.
5. Users are advised to update to the latest secure version.

## SECURITY BEST PRACTICES 

Developers and administrators should follow these guidelines: 

- Always use environment variables (.env) for sensitive information.
- Never hardcode GitHub tokens, passwords, or API keys.
- Rotate access tokens regularly.
- Use HTTPS for all external communication.
- Deploy behind a reverse proxy such as Nginx or Caddy.
- Use Flask's built-in CSRF and session protection.
- Regularly update all dependencies using `pip install -U -r requirements.txt`.
- Limit file upload types and validate CSV content.
- Enable server logs for suspicious activity monitoring.

## INFRASTRUCTURE SECURITY 

- Flask should be run in production mode using Gunicorn or Waitress.
- Database or storage credentials (if applicable) must not be public.
- Ensure proper permission levels for deployment directories.
- Disable directory listing in web servers.
- Keep OS and Python runtime up to date.

## PATCH MANAGEMENT 

- All fixes will be tested before release.
- Patch versions will follow Semantic Versioning (MAJOR.MINOR.PATCH).
- Security updates are always noted in the CHANGELOG.md.

## INCIDENT RESPONSE 

In case of a verified security incident:
1. Immediately notify the project maintainers.
2. Isolate the affected environment.
3. Rotate all API tokens and credentials.
4. Deploy emergency patches where necessary.
5. Perform post-mortem analysis and document findings.

All incidents are logged internally and may be disclosed publicly
if deemed necessary for transparency.
