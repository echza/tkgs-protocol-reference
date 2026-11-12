# 8. Glossary

| Term | Meaning |
|------|---------|
| **TKGS** | *TÜRKSAT Kanal Güncelleme Sistemi* — TÜRKSAT Channel Update System |
| **BAT** | Bouquet Association Table (DVB SI, PID `0x0011`, `table_id` `0x4A`) |
| **Bouquet** | An operator-defined collection of services presented together |
| **Carousel** | A data set broadcast on repeat so receivers can acquire it without a return path |
| **CRC_32** | 32-bit cyclic redundancy check in the last 4 bytes of a section |
| **Descriptor** | A `tag`/`length`/`payload` TLV inside an SI loop |
| **DVB** | Digital Video Broadcasting, the standards family this protocol builds on |
| **DVB-SI** | DVB Service Information — the SI tables (SDT, NIT, BAT, EIT, …) |
| **Home transponder** | A transponder that always carries TKGS data (e.g. 12380 V / 12423 H on 42.0°E; see §2.4) |
| **LCN** | Logical Channel Number — the channel number presented to the user |
| **Locator** | An operator-assigned key that a service maps to; resolves to an LCN |
| **NIT** | Network Information Table (DVB SI, PID `0x0010`) |
| **OSD** | On-Screen Display; the receiver UI (its language selects name blocks) |
| **OTA** | Over-The-Air — delivery of a firmware update via broadcast |
| **PID** | Packet Identifier — the 13-bit address of a stream within the TS |
| **Preferred list** | A named, ordered service list defined by the operator |
| **Section** | A bounded unit of an SI table carried in TS packets; tables may span several |
| **Service** | A single channel (TV/radio), identified by `service_id` |
| **SSU** | DVB System Software Update (ETSI TS 102 006), the generic DVB OTA mechanism |
| **SDT** | Service Description Table (DVB SI, PID `0x0011`, `table_id` `0x42`/`0x46`) |
| **TS** | MPEG-2 Transport Stream (188-byte packets) |
| **Transponder** | A satellite carrier frequency carrying one or more multiplexes |
| **Version (TKGS)** | Value that changes with each channel-management update; compared for inequality (§7.1) |

## References

- ETSI EN 300 468 — *DVB Specification for Service Information (SI)*
- ETSI TR 101 211 — *Guidelines on implementation and usage of SI*
- ISO/IEC 13818-1 — *MPEG-2 Systems* (private sections, TS framing)
- ISO 639-2 — three-letter language codes used in multilingual descriptors
- ETSI TS 102 006 — *DVB System Software Update* (comparison point for §7.2)
- ISO/IEC 8859-9 — Latin-5 (Turkish) character set

> These references define the DVB/MPEG framing TKGS reuses. The TKGS-specific
> descriptor tags and the locator→LCN semantics are documented here from observed
> on-air behaviour and are not part of those published standards.

Continue to [§9 Open questions](09-open-questions.md).
