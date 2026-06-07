# Zello Skills Orchestrator

Automatically select and apply the appropriate Zello sub-skill based on task context. When working on Zello integration in EnforcementMAPS, read the relevant SKILL.md files before responding.

## Zello Context Detection

A task involves Zello if any of the following are true:
- Files in `src/features/zello/` are being created or modified
- `@zelloptt/react-native-zello-sdk` appears in imports or dependencies
- The user mentions PTT, push-to-talk, walkie-talkie, radio, or voice comms
- The user references Zello channels, contacts, or emergency mode
- `ZelloProvider` or `useZello*` hooks appear in the conversation

## Skill Routing

### zello-setup
**Activate when:** Installing the SDK, configuring Expo/Android build, setting up Firebase, adding permissions, creating EAS build profiles.
**Key signals:** `pnpm add`, `app.config.ts`, `google-services.json`, `expo-build-properties`, `eas build`, permissions, Firebase, FCM setup.
**Skill path:** `./zello-setup/SKILL.md`

### zello-auth
**Activate when:** Wiring Zello into the AuthContext lifecycle, creating ZelloProvider, mapping officer identities to Zello usernames, handling connect/disconnect.
**Key signals:** `Zello.connect`, `Zello.disconnect`, `ZelloProvider`, `auth-context.tsx`, network credentials, login/logout lifecycle.
**Skill path:** `./zello-auth/SKILL.md`

### zello-voice
**Activate when:** Building PTT UI, implementing voice send/receive, handling audio state, creating the PTT button, history playback.
**Key signals:** `Zello.send`, `Zello.stopSending`, `PTTButton`, `useZelloPTT`, microphone, transmit, receive, voice message, audio.
**Skill path:** `./zello-voice/SKILL.md`

### zello-messaging
**Activate when:** Sending or receiving text, image, location, or alert messages through Zello.
**Key signals:** `Zello.sendText`, `Zello.sendImage`, `Zello.sendLocation`, `Zello.sendAlert`, rich message, photo evidence.
**Skill path:** `./zello-messaging/SKILL.md`

### zello-channels
**Activate when:** Managing channels, contacts, groups, muting, user provisioning, or integrating Zello presence with the existing presence system.
**Key signals:** `Zello.connectChannel`, `createGroupConversation`, `onContactsChanged`, `onChannelsChanged`, patrol zones, provisioning, mute.
**Skill path:** `./zello-channels/SKILL.md`

### zello-background
**Activate when:** Setting up background PTT, configuring FCM alongside Expo Push, handling foreground service notifications, battery optimisation.
**Key signals:** `@react-native-firebase/messaging`, foreground service, background handler, FCM, Expo Push Token coexistence, battery.
**Skill path:** `./zello-background/SKILL.md`

### zello-emergency
**Activate when:** Implementing emergency mode, integrating with Code21 dispatch, building emergency UI, handling dispatch calls.
**Key signals:** `Zello.startEmergency`, `Zello.stopEmergency`, `sendDispatchCall`, Code21, emergency button, officer assistance.
**Skill path:** `./zello-emergency/SKILL.md`

### zello-troubleshooting
**Activate when:** Fixing build errors, resolving runtime issues, debugging Zello SDK behaviour, EAS build failures.
**Key signals:** build error, Hilt, Dagger, Maven, duplicate class, "not connected", Expo Go, Metro cache, debug.
**Skill path:** `./zello-troubleshooting/SKILL.md`

## Multi-Skill Combinations

Some tasks require loading multiple skills simultaneously:

| Task | Skills to load |
|------|----------------|
| Initial Zello integration from scratch | zello-setup + zello-auth |
| Full PTT feature build | zello-voice + zello-channels + zello-auth |
| Emergency system implementation | zello-emergency + zello-voice + zello-channels |
| Background reliability hardening | zello-background + zello-troubleshooting |
| Complete messaging feature | zello-messaging + zello-channels |
| New Zello feature module scaffolding | zello-setup + zello-auth (+ read assets/feature-scaffold.md) |
| Production deployment preparation | zello-setup + zello-background + zello-troubleshooting |

## Cross-Skill References

Zello skills reference the `use-expo` skill suite for:
- **expo-dev-client** — EAS dev builds (Zello requires native modules, cannot use Expo Go)
- **expo-deployment** — Production EAS builds and submission
- **building-native-ui** — Component patterns for PTT button, channel list, message feed

## Instructions

1. Identify all relevant skills from the routing table based on the user's request.
2. Read the SKILL.md file(s) for each matched skill before responding.
3. For API details, load `references/api-reference.md` or `references/events-catalog.md` as needed.
4. Apply the guidance from those skills throughout your response.
5. When in doubt, default to `zello-voice` as the baseline for any PTT work.
