#!/usr/bin/env python3
"""Reference decoder for the TKGS layouts described in docs/03-05.

Dependency-free. Covers only what the spec documents. Fields marked
unconfirmed in docs/09-open-questions.md are deliberately not guessed.

    python3 tools/tkgs_decode.py           # run self-test
    python3 tools/tkgs_decode.py HEX...    # decode a descriptor loop given as hex
"""
from __future__ import annotations

import sys
from dataclasses import dataclass

TAG_SERVICE = 0x48
TAG_CATEGORY_NAME = 0x90
TAG_SERVICE_NAME = 0x93
TAG_LOCATOR = 0x94

LCN_MASK = 0x1FFF  # low 13 bits


# --- framing (§3, §4.5) ----------------------------------------------------

def len12(b: bytes, off: int = 0) -> int:
    return ((b[off] & 0x0F) << 8) | b[off + 1]


def len20(b: bytes, off: int = 0) -> int:
    return ((b[off] & 0x0F) << 16) | (b[off + 1] << 8) | b[off + 2]


def crc32_mpeg2(data: bytes) -> int:
    """CRC-32/MPEG-2: poly 0x04C11DB7, init 0xFFFFFFFF, no reflection, no xorout."""
    crc = 0xFFFFFFFF
    for byte in data:
        crc ^= byte << 24
        for _ in range(8):
            crc = ((crc << 1) ^ 0x04C11DB7) if crc & 0x80000000 else (crc << 1)
            crc &= 0xFFFFFFFF
    return crc


def section_crc_ok(section: bytes) -> bool:
    """A whole section, including its trailing CRC, yields 0."""
    return crc32_mpeg2(section) == 0


# --- descriptors (§4) -------------------------------------------------------

@dataclass
class Descriptor:
    tag: int
    payload: bytes


def iter_descriptors(loop: bytes):
    """Walk a tag/len/payload loop. Raise ValueError on overrun (§4)."""
    i = 0
    while i < len(loop):
        if i + 2 > len(loop):
            raise ValueError(f"truncated descriptor header at offset {i}")
        tag, ln = loop[i], loop[i + 1]
        end = i + 2 + ln
        if end > len(loop):
            raise ValueError(f"descriptor 0x{tag:02X} at {i} overruns loop ({ln} bytes)")
        yield Descriptor(tag, loop[i + 2:end])
        i = end


def decode_locator(payload: bytes) -> list[tuple[int, int]]:
    """0x94: repeated {locator:16, reserved:3, lcn:13} (§4.4)."""
    if len(payload) == 0 or len(payload) % 4:
        raise ValueError(f"locator payload length {len(payload)} is not a positive multiple of 4")
    out = []
    for j in range(0, len(payload), 4):
        locator = (payload[j] << 8) | payload[j + 1]
        lcn = ((payload[j + 2] << 8) | payload[j + 3]) & LCN_MASK
        out.append((locator, lcn))
    return out


def decode_text(raw: bytes) -> str:
    """EN 300 468 Annex A subset; ISO 8859-9 when there is no prefix (§4.3.1)."""
    if not raw:
        return ""
    first = raw[0]
    if first >= 0x20:
        return raw.decode("iso8859_9", errors="replace")
    if first == 0x05:
        return raw[1:].decode("iso8859_9", errors="replace")
    if first == 0x10 and len(raw) >= 3:
        part = (raw[1] << 8) | raw[2]
        try:
            return raw[3:].decode(f"iso8859_{part}", errors="replace")
        except LookupError:
            return raw[3:].decode("latin-1", errors="replace")
    if first == 0x15:
        return raw[1:].decode("utf-8", errors="replace")
    return raw[1:].decode("latin-1", errors="replace")  # unsupported table: best effort


def decode_multilingual(payload: bytes) -> list[tuple[str, str]]:
    """0x90 / 0x93: repeated {lang:3, len:1, text:len} (§4.3)."""
    out, i = [], 0
    while i < len(payload):
        if i + 4 > len(payload):
            raise ValueError(f"truncated language block at offset {i}")
        lang = payload[i:i + 3].decode("ascii", errors="replace")
        t = payload[i + 3]
        text = payload[i + 4:i + 4 + t]  # truncate defensively if t overruns
        out.append((lang, decode_text(text)))
        i += 4 + t
    return out


def select_language(blocks: list[tuple[str, str]], osd: str, default: str = "tur") -> str | None:
    fallback = None
    for lang, text in blocks:
        if lang.lower() == osd.lower():
            return text
        if fallback is None and lang.lower() == default.lower():
            fallback = text
    return fallback if fallback is not None else (blocks[0][1] if blocks else None)


# --- resolution (§5) -------------------------------------------------------

def build_table(pairs: list[tuple[int, int]]) -> dict[int, int]:
    table: dict[int, int] = {}
    for locator, lcn in pairs:
        table[locator] = lcn  # last writer wins (§5.2)
    return table


def resolve(locator: int, table: dict[int, int]) -> int | None:
    """Return the LCN, or None on a miss. The caller applies §5.5 miss policy."""
    lcn = table.get(locator)
    return None if lcn == 0 else lcn


# --- CLI / self-test -------------------------------------------------------

def dump(loop: bytes) -> None:
    for d in iter_descriptors(loop):
        if d.tag == TAG_LOCATOR:
            body = ", ".join(f"0x{l:04X}->{n}" for l, n in decode_locator(d.payload))
        elif d.tag in (TAG_CATEGORY_NAME, TAG_SERVICE_NAME):
            body = ", ".join(f"{l}:{t!r}" for l, t in decode_multilingual(d.payload))
        else:
            body = d.payload.hex(" ")
        print(f"0x{d.tag:02X} ({len(d.payload)} B): {body}")


EXAMPLE_4_6 = bytes.fromhex(
    "94 08 00 2A E0 07 01 F4 E0 64"
    "93 11 54 55 52 05 48 61 62 65 72 45 4E 47 04 4E 65 77 73"
)


def self_test() -> None:
    assert crc32_mpeg2(b"123456789") == 0x0376E6E7  # CRC-32/MPEG-2 check value
    sec = b"\x42\xF0\x05\x00\x01\xC1\x00\x00"
    crc = crc32_mpeg2(sec)
    assert section_crc_ok(sec + crc.to_bytes(4, "big"))

    assert len12(b"\xF1\x23") == 0x123
    assert len20(b"\xF1\x23\x45") == 0x12345

    ds = list(iter_descriptors(EXAMPLE_4_6))
    assert [d.tag for d in ds] == [0x94, 0x93]
    assert decode_locator(ds[0].payload) == [(0x002A, 7), (0x01F4, 100)]
    names = decode_multilingual(ds[1].payload)
    assert names == [("TUR", "Haber"), ("ENG", "News")]
    assert select_language(names, "eng") == "News"
    assert select_language(names, "deu") == "Haber"  # falls back to tur

    table = build_table([(1, 5), (1, 9), (2, 0)])
    assert resolve(1, table) == 9      # last writer wins
    assert resolve(2, table) is None   # LCN 0 -> unnumbered
    assert resolve(3, table) is None   # miss

    assert decode_text(b"\x05\xF0\xFE") == "ğş"
    assert decode_text(b"\x15\xc4\x9f") == "ğ"

    try:
        list(iter_descriptors(b"\x94\x08\x00"))
    except ValueError:
        pass
    else:
        raise AssertionError("overrun not detected")
    print("self-test OK")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        dump(bytes.fromhex("".join(sys.argv[1:])))
    else:
        self_test()
