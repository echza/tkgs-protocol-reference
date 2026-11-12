# 4. Descriptors

TKGS carries its payload as **descriptors** inside the per-service descriptor loop
of the SDT (and, where used, the BAT/NIT loops). Every descriptor uses the
standard DVB two-byte header:

```
+--------+--------+--------------------------+
| tag(1) | len(1) |   payload (len bytes)    |
+--------+--------+--------------------------+
```

`len` is the number of payload bytes that follow. A parser walks a loop by
reading `tag`, `len`, consuming `len` bytes, and repeating until the loop's byte
budget is exhausted. Unknown tags are skipped using `len`, which is what makes
TKGS backward-compatible with non-TKGS receivers.

## 4.1 Tag allocation

| Tag | Name | Scope | Purpose |
|-----|------|-------|---------|
| `0x48` | `service_descriptor` | DVB standard | service type + provider/service name |
| `0x90` | category / bouquet name | TKGS private | multilingual group name |
| `0x93` | service name | TKGS private | multilingual service name |
| `0x94` | locator | TKGS private | maps the service to a logical channel number |

`0x90`, `0x93`, `0x94` fall in the DVB **user-defined** range (`0x80`–`0xFE`), so
they are only meaningful to TKGS-aware receivers.

## 4.2 `service_descriptor` (0x48) — standard

Included for completeness; defined by DVB (EN 300 468).

| Offset | Size | Field |
|--------|------|-------|
| 0 | 1 | `service_type` |
| 1 | 1 | `service_provider_name_length` = *p* |
| 2 | *p* | `service_provider_name` |
| 2+*p* | 1 | `service_name_length` = *n* |
| 3+*p* | *n* | `service_name` |

## 4.3 Multilingual name descriptors (0x90, 0x93)

Both the category/bouquet name (`0x90`) and the service name (`0x93`) use a
**multilingual** layout: the payload is a sequence of language blocks, each
tagged with an ISO 639-2 three-letter language code. The receiver picks the block
matching the user's configured OSD language, falling back to a default language.

Payload = one or more blocks of:

| Offset | Size | Field |
|--------|------|-------|
| 0 | 3 | `ISO_639_language_code` (e.g. `"TUR"`) |
| 3 | 1 | `text_length` = *t* |
| 4 | *t* | `text` (character-encoded name) |

Block *i*+1 begins at offset `4 + t` of block *i*. Selection algorithm:

```text
for each block:
    if block.lang == user_osd_language: use block.text; stop
    else remember first block whose lang == default_language
if none matched: use the remembered default block
```

A common fallback language on TÜRKSAT is Turkish (`"TUR"` / `"tur"`). Name text
length is bounded in practice (service names are short); receivers should treat
an over-long `text_length` defensively and truncate.

## 4.4 Locator descriptor (0x94)

The locator descriptor binds a service to a **Logical Channel Number (LCN)** via
an abstract **locator** key. This is the mechanism that lets the operator move a
service without the receiver caring where it physically lives.

Payload (4 bytes per mapping; the descriptor carries at least one):

| Offset | Size | Field | Encoding |
|--------|------|-------|----------|
| 0 | 2 | `locator` | 16-bit big-endian key |
| 2 | 2 | `reserved` + `logical_channel_number` | high 3 bits reserved, low **13 bits** = LCN |

Bit layout of the second 16-bit word:

```
 15 14 13 | 12 .................. 0
  r  r  r | logical_channel_number (13 bits)
```

Decode:

```text
locator = (payload[0] << 8) | payload[1]
lcn     = ((payload[2] & 0x1F) << 8) | payload[3]
```

The `locator` is **not** a frequency or a service_id in disguise; it is an
operator-assigned handle. Its resolution to a concrete channel number — and the
in-receiver table that stores these pairs — is described in
[§5 Locator → LCN](05-locator-lcn.md).

## 4.5 Nested length fields

Around the descriptor loops, TKGS tables use nested length-prefixed regions with
the DVB 12-/20-bit length convention:

```text
len12 = (b[0] & 0x0F) << 8  | b[1]
len20 = (b[0] & 0x0F) << 16 | (b[1] << 8) | b[2]
```

A parser advances by each region's length to reach the next, exactly as it does
for `section_length`. This is what allows the service list, the per-service
descriptor loop, and the category block to be delimited inside one section.

Continue to [§5 Locator → LCN](05-locator-lcn.md).
