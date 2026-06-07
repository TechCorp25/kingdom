# Zello Security & Networking Reference

> Load this reference when configuring firewalls, reviewing encryption, or auditing credential storage.

## Encryption

| Layer | Method |
|-------|--------|
| Voice data | AES-256-CBC, per-message key |
| Signalling | TLS 1.2+ (HTTPS) |
| Media transport | DTLS-SRTP |
| At rest | Not stored on device by default |

All encryption is handled by the SDK — no application-level crypto code needed.

## Network Requirements

### Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 443 | TCP/TLS | Signalling, API, authentication |
| 3478 | UDP | STUN/TURN media relay |
| 10000–20000 | UDP | Direct media (when available) |

### Firewall Allowlist

For restricted networks (e.g., council IT environments):

```
*.zellowork.com       — API and signalling
*.jfrog.io            — SDK artefact delivery (build time only)
*.firebaseio.com      — FCM push
*.googleapis.com      — FCM push
```

## Credential Storage

| Credential | Storage | Notes |
|-----------|---------|-------|
| Zello network issuer | `eas.json` env var | Build-time only |
| Zello credential key | `eas.json` env var | Build-time only |
| Zello session token | SDK internal | Not accessible to app code |
| App JWT | `expo-secure-store` | Existing — unchanged |
| `google-services.json` | `.gitignore` | Must not be committed to repo |

## Offline Behaviour

- Zello requires an active network connection for PTT
- The SDK auto-reconnects when connectivity is restored (`onWillReconnect` event)
- Show a "Radio unavailable" indicator when Zello is disconnected
- The app's existing offline-first patterns handle graceful degradation

## Audit Logging

Zello Work admin console provides:
- Message history and timestamps
- Emergency event logs
- User connection/disconnection logs
- Channel activity metrics

These complement the MAPS API's own audit trail.
