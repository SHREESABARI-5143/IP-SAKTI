# ADR-004: Password Hashing Upgrade to bcrypt and Multi-Tenant Namespace Isolation

## Status
Accepted

## Context
Initial prototypes used plain SHA-256 for user password hashing, which is susceptible to GPU brute-force attacks. Furthermore, user uploaded formulation documents required cryptographic tenant isolation to prevent cross-user document leakage during retrieval.

## Decision
1. Adopt **`passlib[bcrypt]`** with salt rounds for all user authentication.
2. Implement strict **tenant namespace isolation** (`USER_{user_id}`) at both the database schema layer and retrieval query filtering level.

## Consequences
- **Positive**: Cryptographic resistance against rainbow table and brute force attacks.
- **Positive**: Guaranteed multi-tenant separation for sensitive Ayurvedic intellectual property and clinical trial data.
