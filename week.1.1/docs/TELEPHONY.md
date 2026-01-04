# Telephony blueprint (Twilio/Exotel)

This project includes a **voice-ready** architecture. To handle real inbound calls:

## Twilio (high-level)
1. Buy a phone number
2. Configure Voice Webhook to your server endpoint (e.g., `/telephony/twilio/voice`)
3. Twilio sends audio -> you can:
   - Use Twilio's Speech Recognition (or stream to your STT service)
   - Or use Twilio Media Streams and run STT (Whisper/Google STT)

## Minimal endpoints to add
- `POST /telephony/twilio/voice`:
  - return TwiML that plays consent message, then gathers speech
- `POST /telephony/twilio/gather`:
  - receives speech transcript
  - call `/api/chat` with session_id=CallSid
  - respond via <Say> or <Play> (TTS)

## Compliance
- Play a consent statement (recording notice)
- Mask PII in logs
- Escalate to human for low confidence / out of scope

This repo already implements the agent logic + escalation + logging.
You only need the telephony glue.
