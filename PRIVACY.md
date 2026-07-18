# Public Benchmark Privacy Notice

**Last updated:** July 18, 2026
**Effective:** July 20, 2026

This notice describes personal-data processing associated with the NanoFDO hosted public benchmark. GitHub separately processes data when you browse, clone, star, fork, or contribute to this repository under GitHub's own privacy documentation.

## Controller and contact

NanoFDO is operated in France by buro66, which acts as controller for the hosted benchmark registration and usage data described below.

Privacy requests may be sent to `contact@buro66.com`.

## Data processed

### Registration and account data

- Email address supplied during registration.
- Random benchmark account identifier.
- Secret benchmark access key.
- Account scope and active or revoked status.
- Creation and last-activity timestamps.

### Usage and security data

- Daily and monthly run counters.
- Last benchmark timestamp.
- Rate-limit and concurrency events.
- Source network address processed for abuse prevention and converted to a one-way in-memory identifier for application rate limiting.
- Technical request and error information required to secure and operate the service.

### Benchmark payload and results

The payload is processed in memory to perform the requested benchmark. The hosted benchmark does not persist the payload or detailed benchmark result in its account database.

A SHA-256 payload fingerprint is returned to the user for reproducibility. It identifies identical payload content; it is not a user or device fingerprint. Users must nevertheless avoid real or predictable sensitive content.

The client saves results locally in `results.json`. NanoFDO does not control the user's local copy or any result the user chooses to publish.

## Data not intentionally collected by the benchmark client

The public client does not intentionally collect or transmit a hardware serial number, MAC address, persistent device identifier, hostname, browser fingerprint, or GitHub account identity.

## Purposes and legal bases

Data is processed to:

- Provide and administer requested benchmark access.
- Enforce quotas and the agreed terms.
- Protect availability, prevent abuse, and investigate security incidents.
- Maintain an auditable record of administrative revocation and reactivation actions.
- Respond to support, privacy, legal, and research allowance requests.

Provision and administration of requested access are based on performance of the service terms. Security, abuse prevention, capacity management, and audit are based on the operator's legitimate interests in protecting the service and its users.

Benchmark registration is not consent to marketing. A separate optional choice would be required for unrelated promotional communications.

## Data minimisation and key protection

Administrative lists expose only a one-way abbreviated key fingerprint, not the usable access key. Access keys, payloads, and source network addresses must not be written to application logs in clear text.

Only data needed for access, quota, security, support, and audit is processed.

## Retention criteria

- In-memory application rate-limit counters stop affecting access when their configured window expires. Application keys use one-way network identifiers rather than clear source addresses and are removed opportunistically or when the process restarts.
- Payloads and detailed results are not retained in the benchmark account database.
- Active account data is retained while the key remains active and is used for the benchmark.
- Inactive or revoked account data is retained only as long as required for account administration, abuse prevention, legal claims, and audit, then deleted or anonymised.
- Infrastructure security logs are retained under the applicable operational security schedule and are not used for marketing or user profiling.

Retention may be extended where required by law, a security investigation, or the establishment, exercise, or defence of legal claims.

## Recipients

Data is accessible only to authorised NanoFDO operators and infrastructure providers where needed to host, secure, and maintain the service. It may be disclosed to public authorities when legally required.

Personal benchmark data is not sold. It is not published in this repository. Aggregate statistics may be published only where they do not identify an individual.

## International context

The hosted benchmark is operated in France. GitHub repository activity is separately processed by GitHub and may involve international transfers under GitHub's own terms and safeguards.

## Your rights

Subject to applicable law, you may request access, rectification, erasure, restriction, portability where applicable, or object to processing based on legitimate interests. You may also lodge a complaint with the French data-protection authority, the CNIL, or your competent supervisory authority.

A request should include enough information to identify the benchmark registration. Do not send the full access key by email. NanoFDO may request proportionate verification before acting on a request.

## Changes

Material changes will be published in this repository with an updated effective date.
