# Contributing

Thanks for helping improve the TKGS protocol reference. The goal is a clean,
**vendor-neutral** description of the on-air protocol that anyone can verify.

## Principles

- **Describe the protocol, not a product.** Avoid device names, firmware builds,
  memory addresses, or decompiler output in the spec text. Those belong, if
  anywhere, in your PR discussion as evidence — not in the document.
- **Cite observable evidence.** When adding or correcting a field, say how it was
  observed: the carrying table (`table_id`), the descriptor `tag`, and the raw
  bytes you decoded. On-air captures beat any single implementation.
- **Prefer "observed in practice" over "always".** Where a value is conventional
  rather than guaranteed, mark it as such.

## How to propose a change

1. Open an issue describing the field or behaviour and your evidence, **or**
2. Submit a PR editing the relevant file in `docs/`.

Keep edits focused: one topic per PR makes review and verification easier.

## Style

- Markdown, one sentence-ish per line is fine; tables for field layouts.
- Byte offsets zero-based; integers big-endian; bit fields MSB-first.
- Diagrams use [Mermaid](https://mermaid.js.org/) fenced code blocks so they render
  on GitHub without a build step.

## Scope

In scope: transport/carriage, section framing, descriptor layouts, locator→LCN
semantics, operating modes, versioning, and update **signalling**.

Out of scope: proprietary firmware image formats, flashing procedures, keys, or
anything that only makes sense for one device.

By contributing you agree your contributions are licensed under
[CC BY 4.0](LICENSE).
