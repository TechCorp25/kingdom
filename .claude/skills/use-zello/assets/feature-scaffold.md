# Zello Feature Module Scaffold

Use this template when creating the `src/features/zello/` directory. It follows the established EnforcementMAPS feature module pattern (see `src/features/code21/`, `src/features/presence/`, `src/features/patrol/`).

## Directory Structure

```
src/features/zello/
├── api/
│   └── zello-provisioning.ts    # Optional: Zello Work provisioning API calls
├── components/
│   ├── PTTButton.tsx             # Press-to-talk button (press-and-hold)
│   ├── ChannelList.tsx           # Channel picker / zone selector
│   ├── ContactList.tsx           # Online officer list with status
│   ├── MessageFeed.tsx           # Incoming message display (voice, text, image)
│   └── EmergencyButton.tsx       # Emergency activation (long-press)
├── hooks/
│   ├── useZelloPTT.ts            # PTT state: send, stop, receiving
│   ├── useZelloEvents.ts         # Event subscriptions: connected, contacts, channels
│   ├── useZelloMessaging.ts      # Rich messaging: text, image, location, alert
│   ├── useZelloEmergency.ts      # Emergency mode + Code21 dual-trigger
│   ├── useZelloPermissions.ts    # Runtime permission requests (mic, bluetooth, notifications)
│   └── useZelloChannels.ts       # Channel connect/disconnect/mute
├── domain.ts                     # Zello types, username mapping, business logic
├── zello-provider.tsx            # Context provider: auth lifecycle → connect/disconnect
└── zello-fcm-handler.ts          # Firebase background message handler
```

## Naming Conventions

- Hooks: `useZello<Concern>.ts` — single responsibility
- Components: PascalCase `.tsx` — presentational, receive hooks via props
- Provider: single `zello-provider.tsx` — mounted in `app/_layout.tsx`
- Types go in `domain.ts` (matches `code21/domain.ts` pattern)

## Integration Points

| File | Mounts/Imports |
|------|---------------|
| `app/_layout.tsx` | `<ZelloProvider>` inside `<AuthProvider>` |
| `app/tabs/radio.tsx` (new) | PTT screen with channel list + PTT button |
| `src/shared/infra/auth-context.tsx` | Referenced by ZelloProvider for token/user |
| `src/features/presence/presence.api.ts` | Augmented by Zello contact status |
| `src/features/code21/` | Emergency dual-trigger integration |
