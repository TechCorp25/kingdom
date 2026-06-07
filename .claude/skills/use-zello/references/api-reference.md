# Zello SDK API Reference

> Source: `@zelloptt/react-native-zello-sdk@2.0.1`
> Load this reference when you need exact method signatures or type definitions.

## Connection

| Method | Signature | Purpose |
|--------|-----------|---------|
| `connect` | `(config: ZelloConfig) → void` | Authenticate and connect to Zello Work |
| `disconnect` | `() → void` | End session gracefully |
| `setLogLevel` | `(level: string) → void` | Set SDK log verbosity ('debug', 'info', 'warn', 'error') |

## Voice

| Method | Signature | Purpose |
|--------|-----------|---------|
| `send` | `(contact: ZelloContact) → void` | Start PTT stream to contact/channel/group |
| `stopSending` | `() → void` | End PTT transmission |
| `playHistory` | `(message: ZelloHistoryMessage) → void` | Replay a history voice message |
| `stopPlayback` | `() → void` | Stop history playback |

## Messaging

| Method | Signature | Purpose |
|--------|-----------|---------|
| `sendText` | `(contact: ZelloContact, text: string) → void` | Send text message |
| `sendImage` | `(contact: ZelloContact, uri: string) → void` | Send image (local file URI) |
| `sendLocation` | `(contact: ZelloContact) → void` | Send current GPS location |
| `sendAlert` | `(contact: ZelloContact, text: string, level: number) → void` | Send priority alert (1-3) |

## Channels & Contacts

| Method | Signature | Purpose |
|--------|-----------|---------|
| `connectChannel` | `(name: string) → void` | Join a channel |
| `disconnectChannel` | `(name: string) → void` | Leave a channel |
| `muteContact` | `(contact: ZelloContact) → void` | Mute a contact or channel |
| `unmuteContact` | `(contact: ZelloContact) → void` | Unmute |
| `createGroupConversation` | `(contacts: ZelloContact[]) → ZelloContact` | Create ad-hoc group |

## Emergency & Dispatch

| Method | Signature | Purpose |
|--------|-----------|---------|
| `startEmergency` | `() → void` | Activate emergency mode |
| `stopEmergency` | `() → void` | Deactivate emergency mode |
| `sendDispatchCall` | `(channel: ZelloContact) → void` | Request dispatch attention |

## Core Types

```typescript
interface ZelloConfig {
  network: string;   // Network issuer URL (from env var)
  username: string;  // Officer Zello username (e.g., 'officer_629')
  password: string;  // Credential key (from env var)
}

interface ZelloContact {
  name: string;
  displayName: string;
  type: 'user' | 'channel' | 'group_conversation';
  status: 'online' | 'offline' | 'busy' | 'standby';
  isMuted: boolean;
}

interface ZelloChannel {
  name: string;
  status: 'connected' | 'disconnected' | 'connecting';
  usersOnline: number;
}

interface ZelloHistoryMessage {
  messageId: string;
  contact: ZelloContact;
  timestamp: number;
  type: 'voice' | 'text' | 'image' | 'location' | 'alert';
}
```

## Official Resources

- SDK docs: https://sdk.zello.com
- RN SDK repo: https://github.com/zelloptt/react-native-zello-sdk
- Android SDK repo: https://github.com/zelloptt/zello-android-client-sdk
