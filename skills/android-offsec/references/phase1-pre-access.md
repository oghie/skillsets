# Phase 1: Pre-Device Access

**When:** You do NOT have physical possession of the target device. Goal: gain initial access — code execution, network position, or physical proximity.

## OSINT Reconnaissance (ALWAYS START HERE)

Before any technical action, gather intelligence:

- **Social footprint:** Search social media, forums, data breach databases. What apps? What phone model? When was last OS update?
- **Device fingerprinting:** Correlate known email/phone with device models in breach data. Samsung S22 on Android 12 ≠ Pixel 8 on Android 15.
- **SIM/Telecom:** Is target's carrier vulnerable to SIM swap? SS7 interception feasible?
- **Network habits:** Where do they connect? Coffee shops, airports, hotels, gyms? Map their routine.

## Attack Vectors

### Network-Based

**Evil Twin WiFi:**
- Deploy rogue AP mimicking SSIDs the target trusts (Starbucks, airport WiFi, hotel guest network)
- Use `scripts/captive_portal/deploy_evil_twin.sh` for automated deployment
- Bettercap for credential harvesting + traffic interception

**Auto-Join Exploit:**
- Devices auto-reconnect to previously saved networks
- If you know target's trusted SSIDs (from OSINT), create matching evil twins — no user interaction needed

**DNS Hijacking + Captive Portal:**
- Redirect all DNS through rogue AP
- Serve fake "System Update Required" page (`scripts/captive_portal/index.html`)
- Deliver trojanized APK disguised as security update

**IMSI Catching (Stingray):**
- Deploy IMSI catcher to intercept calls/SMS
- Pair with BladeRF jamming to force target off 4G/5G onto vulnerable 2G/3G

### Signal Jamming + Forced WiFi

- Jam 2G/3G/4G/5G bands with BladeRF or HackRF
- Target loses cellular → forced to use WiFi
- Deploy evil twin simultaneously — target connects voluntarily
- Law enforcement technique: create necessity, provide controlled alternative

### SS7 Interception

SS7 (Signaling System 7) is the protocol backbone of global telecom networks. It was designed without authentication — any operator with SS7 access can intercept or redirect another operator's subscribers.

**What SS7 enables:**
- **Location tracking:** Any subscriber's location via MAP-ATI (AnyTimeInterrogation), ~50m accuracy
- **SMS interception:** Redirect incoming SMS via MAP-RegisterSS/MSISDN manipulation — intercept 2FA codes
- **Call interception:** Redirect calls via MAP-InsertSubscriberData manipulation
- **USSD interception:** Redirect USSD sessions (banking confirmation messages)

**Prerequisites:**
- SS7 connectivity (GSMA membership, roaming agreement with a carrier)
- Target's MSISDN (phone number) and IMSI (from OSINT or carrier lookup)
- Target carrier's Global Title (GT) for SCCP routing

**Tools:**
- **P1 Security:** Commercial SS7 security testing platform
- **Osmocom SS7:** Open-source SS7 stack with MAP/TCAP/SCCP
- **jSS7:** Java SS7 stack (Restcomm) — REST API for MAP operations
- **Yate:** Open-source telephony engine with SS7 support

**Attack Flow (Location):**
```
1. Identify target carrier's GT and verify SS7 interconnect
2. Send MAP-ATI request: subscriberIdentity = target IMSI
3. Target's HLR responds with Cell Global Identity (CGI)
4. CGI → MCC+MNC+LAC+CI → physical location (~50m radius)
```

**Attack Flow (SMS Intercept):**
```
1. Send MAP-RegisterSS to target's HLR: forward all SMS to attacker MSISDN
2. Wait for 2FA codes, banking alerts, or password reset SMS
3. After intercept period: deregister forwarding to avoid detection
```

**Detection:**
- Modern carriers deploy SS7 firewalls (AdaptiveMobile, Cellusys, Mavenir)
- Firewalls detect abnormal MAP operations (excessive ATI, RegisterSS from unknown GTs)
- Some carriers require mutual TLS for inter-operator SS7 (Diameter upgrade)
- **Countermeasure:** Use a carrier that does NOT filter SS7 (many in developing regions still have open SS7)

### SIM Swap Attack

A SIM swap transfers the target's phone number to a SIM card controlled by the attacker. Once swapped, all calls, SMS, and 2FA codes go to the attacker's device.

**Attack Surface Assessment:**
- **Prepaid vs postpaid:** Postpaid numbers typically have stronger authentication
- **Carrier policies:** Some carriers require in-person ID verification; others accept phone verification alone
- **Port-out PIN:** Some carriers require a separate PIN for number porting — can this PIN be reset?
- **Online account:** Does the carrier have a web portal where a SIM swap can be initiated?

**Execution Workflow:**

1. **Gather OSINT** — full name, date of birth, address, last 4 of SSN/ID, account number (from target's bills or breach databases)
2. **Identify carrier** — from phone number prefix lookup, OSINT, or the target's device
3. **Social engineer carrier support:**
   - Call during evening/weekend (junior staff, night shift)
   - Pretext: "Lost phone, need to activate replacement SIM urgently — traveling tomorrow"
   - Provide gathered personal info to pass authentication
   - Request SIM swap to attacker-controlled SIM
4. **Post-swap actions (immediate):**
   - SIM activates on attacker device — target loses service (first indicator)
   - Password resets via SMS on all known services (email, banking, social media, crypto exchange)
   - 2FA codes arrive on attacker device
   - Complete account takeovers before target realizes and calls carrier
5. **Time window:** Typically 15-60 minutes before target notices loss of service and contacts carrier

**Carrier Vulnerability Matrix (by region):**

| Region | Risk | Notes |
|--------|------|-------|
| Southeast Asia | HIGH | Many carriers have weak authentication; phone verification often sufficient |
| South Asia | HIGH | Prepaid dominance; minimal identity verification |
| Africa | HIGH | Mobile money focus; SIM swap is primary fraud vector |
| Latin America | MEDIUM | Carriers improving but inconsistent |
| Europe | LOW | Strong KYC regulations; PSD2 requires multi-factor |
| North America | LOW | Port-out PINs, FCC regulations, carrier security teams |

**Post-Swap Intelligence:**
- Register at C2 (`scripts/c2/c2_server.py`) to log all intercepted SMS
- Maintain swap for at least 24 hours to capture delayed 2FA and alerts
- Document all intercepted communications as evidence

### Delivery Vectors

**Deeplink Attack:**
- Identify vulnerable deeplink handlers in apps the target uses
- Craft malicious intents triggering account takeover, data leak, or code execution

**Zero-Click Delivery:**
- Research active CVEs for target's OS version
- WhatsApp/Signal RCE, Bluetooth stack exploits (BlueBorne, BlueFrag), Stagefright variants
- No user interaction required

**FCM/Firebase Push Abuse:**
- If target's apps use FCM with weak configuration
- Craft push notifications redirecting to trojanized APKs

**Social Engineering:**
- Context-aware spear-phishing via SMS, WhatsApp, email
- Reference real events, people, and apps from OSINT

### Physical Opportunity

**Evil Peripheral:**
- O.MG cable, malicious USB-C hub, compromised public charging station
- Payloads delivered when target connects to charge

**Rubber Ducky / BadUSB:**
- Momentary unlocked access → inject keystroke payloads
- Install backdoors or exfiltrate data

**NFC Tag Attack:**
- Place NFC tags with malicious deeplinks in target's routine locations
- Android reads NFC tags automatically when screen is on

**Nearby Share Exploit:**
- If target has Nearby Share visibility open → forced file transfer

**Chromecast/Android TV Pivot:**
- If target shares network with exploitable Chromecast/Android TV
- Exploit casting protocols to reach the device

## Bluetooth Sub-Phase

Bluetooth attacks effective at close range, often overlooked:

- **Bluejacking:** Unsolicited messages via Bluetooth OBEX push
- **Bluesnarfing:** Extract contacts, calendar, files without pairing
- **BLE Exploitation:** Spoof BLE peripherals the target's apps trust
- **Pairing Bypass:** Exploit pairing vulnerabilities per chipset (Broadcom, Qualcomm, MediaTek)
- **Fingerprinting:** Scan discoverable devices, match BD_ADDR to chipset, cross-reference exploits
