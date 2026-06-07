# Zello SDK Events Catalog

> Load this reference when wiring event listeners or debugging event flow.

## Listener Registration Pattern

```typescript
import Zello from '@zelloptt/react-native-zello-sdk';

// Register
const subscription = Zello.Listener.on('eventName', handler);

// Unregister (in useEffect cleanup)
subscription.remove();
```

## Connection Events

| Event | Payload | When |
|-------|---------|------|
| `onConnected` | — | SDK authenticated with Zello servers |
| `onDisconnected` | — | SDK disconnected |
| `onWillReconnect` | — | SDK will auto-reconnect after connection drop |
| `onConnectFailed` | `{ error }` | Authentication or network failure |

## Contact & Channel Events

| Event | Payload | When |
|-------|---------|------|
| `onContactsChanged` | `ZelloContact[]` | Contact list or status updated |
| `onChannelsChanged` | `ZelloChannel[]` | Channel list or status updated |
| `onSelectedContactChanged` | `ZelloContact` | Active contact changed |

## Voice Message Events

| Event | Payload | When |
|-------|---------|------|
| `onOutgoingVoiceMessageConnecting` | `message` | PTT send initiated, connecting to server |
| `onOutgoingVoiceMessageStarted` | `message` | Server accepted audio stream |
| `onOutgoingVoiceMessageStopped` | `message` | Send completed |
| `onOutgoingVoiceMessageFailed` | `{ error }` | PTT send failed |
| `onIncomingVoiceMessage` | `message` | Receiving live audio from another user |
| `onIncomingVoiceMessageStopped` | `message` | Incoming audio ended |

## Rich Message Events

| Event | Payload | When |
|-------|---------|------|
| `onIncomingTextMessage` | `{ contact, text, channel }` | Text message received |
| `onIncomingImageMessage` | `{ contact, image, channel }` | Image message received |
| `onIncomingLocationMessage` | `{ contact, lat, lng, channel }` | Location received |
| `onIncomingAlertMessage` | `{ contact, text, level, channel }` | Alert received |

## Emergency Events

| Event | Payload | When |
|-------|---------|------|
| `onEmergencyStarted` | `{ contact }` | An officer activated emergency mode |
| `onEmergencyStopped` | `{ contact }` | Emergency mode deactivated |

## History Events

| Event | Payload | When |
|-------|---------|------|
| `onHistoryUpdated` | `messages[]` | New history messages available |
| `onHistoryPlaybackStarted` | `message` | History playback began |
| `onHistoryPlaybackStopped` | — | History playback ended |

## Error Events

| Event | Payload | When |
|-------|---------|------|
| `onError` | `{ error, context }` | General SDK error |
| `onOutgoingVoiceMessageFailed` | `{ error }` | PTT send failed |

## Hook Pattern

Follow the project's hook conventions:

```typescript
// src/features/zello/hooks/useZelloEvents.ts
import { useEffect, useState } from 'react';
import Zello, { ZelloContact, ZelloChannel } from '@zelloptt/react-native-zello-sdk';

export function useZelloStatus() {
  const [connected, setConnected] = useState(false);
  const [contacts, setContacts] = useState<ZelloContact[]>([]);
  const [channels, setChannels] = useState<ZelloChannel[]>([]);

  useEffect(() => {
    const subs = [
      Zello.Listener.on('onConnected', () => setConnected(true)),
      Zello.Listener.on('onDisconnected', () => setConnected(false)),
      Zello.Listener.on('onContactsChanged', setContacts),
      Zello.Listener.on('onChannelsChanged', setChannels),
    ];
    return () => subs.forEach((s) => s.remove());
  }, []);

  return { connected, contacts, channels };
}
```
