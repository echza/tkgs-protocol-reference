# 9. Open questions

Every point in this reference that is **not yet confirmed** is collected here,
together with the evidence that would settle it. When you resolve one, update
the relevant section, remove the entry, and note it in
[`CHANGELOG.md`](../CHANGELOG.md).

Most entries can be settled with a single transport-stream capture from a home
transponder ([§2.4](02-transport.md#24-home-transponders-and-the-tkgs-pid)), for
example with TSDuck:

```sh
# 12380 V 27500, keep the TKGS PID plus PAT/PMT/NIT/SDT/BAT for context
tsp -I dvb --delivery-system DVB-S --frequency 12380000000 --polarity vertical \
        --symbol-rate 27500000 \
    -P filter --pid 0x1FF5 --pid 0x0000 --pid 0x0010 --pid 0x0011 --psi-si \
    -P until --seconds 120 \
    -O file tkgs-12380V.ts
```

(Adjust the LNB options for your set-up. With `dvbsnoop`, use
`dvbsnoop -s sec -tsraw 0x1FF5`.)

## 9.1 Carriage — high priority

| # | Question | Section | Evidence that settles it |
|---|----------|---------|--------------------------|
| C1 | What `table_id`(s) are carried on PID `0x1FF5`? | §2.4 | First byte of each section on that PID |
| C2 | Is PID `0x1FF5` fixed, or announced in PAT/PMT? If announced, with which `stream_type` and descriptor? | §2.4 | PMT of the home-transponder services |
| C3 | How does the `0x1FF5` table relate to the SDT-descriptor model (§2.2–§2.3)? Does it replace it, or do they work together? | §2, §4 | Whether `0x90`/`0x93`/`0x94` appear on `0x1FF5`, in the SDT, or in both |
| C4 | Full table layout: the order of the nested regions in §4.5 (header, service loop, category loop, …) | §4.5 | Annotated section dump |
| C5 | Long- or short-form section syntax on `0x1FF5`, and what `table_id_extension` means there | §3.4 | `section_syntax_indicator` bit and the extension values |
| C6 | Are the backup transponders (12458 V, 12559 V, 11747 H) still active? What are their symbol rates and FEC? | §2.4 | Capture or tuning log per transponder |

## 9.2 Semantics

| # | Question | Section | Evidence that settles it |
|---|----------|---------|--------------------------|
| S1 | How does a locator resolve to a physical service (ONID/TSID/SID, delivery parameters)? Which descriptor carries that? | §4.4, §5.4 | Descriptors next to `0x94`, compared with the NIT/SDT of the same TS |
| S2 | Byte layouts for preferred lists / bouquets, hidden/blocked flags, and category membership | §6.4 | Descriptor tags other than `0x90`/`0x93`/`0x94` seen in captures |
| S3 | Text encoding of `0x90`/`0x93` text (Annex A prefix? ISO 8859-9 by default?) | §4.3.1 | First byte of name text; names containing `ğ ş ı İ` |
| S4 | Where the TKGS version is carried, its width, and whether it wraps | §7.1 | Two captures taken across a known list update |
| S5 | Can the broadcast force or default the operating mode? | §6.5 | A flag field that differs between captures, or a vendor statement |
| S6 | Behaviour on a locator miss (default LCN `1`?), LCN `0`, duplicate LCNs | §5.2, §5.5 | Behaviour of two or more independent receivers on the same capture |
| S7 | TKGS-specific carousel repetition rate | §2.6 | Section arrival times in a capture |

## 9.3 Software update

| # | Question | Section | Evidence that settles it |
|---|----------|---------|--------------------------|
| U1 | Which table/descriptor signals a firmware update? Is it DVB SSU (TS 102 006) or private? | §7.2 | Linkage type `0x09` in NIT/BAT; `data_broadcast_id_descriptor` `0x66`; stream type `0x0B` |
| U2 | How is an update targeted (OUI, model, hardware/software version)? | §7.2 | Fields of the signalling descriptor |
| U3 | Where is the image carried (PID, DSM-CC carousel)? | §7.2 | PMT of the signalled service |

## 9.4 Resolved

*(None yet. Move entries here, with a link to the commit or PR, as they are settled.)*
