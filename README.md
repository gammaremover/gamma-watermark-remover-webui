# Gamma Watermark Remover — Local Web UI

[![PyPI](https://img.shields.io/pypi/v/gamma-watermark-remover-webui?color=8b3dff&label=PyPI)](https://pypi.org/project/gamma-watermark-remover-webui/)
[![License: MIT](https://img.shields.io/badge/License-MIT-8b3dff.svg)](LICENSE)
[![Hosted version](https://img.shields.io/badge/Hosted%20version-gammaremover.com-8b3dff)](https://gammaremover.com)

![Gamma Watermark Remover local web UI — drag & drop, files stay on your machine](assets/banner.webp)

A **local web tool** to remove the **"Made with Gamma"** watermark from PDF and PowerPoint (.pptx) files exported from [Gamma.app](https://gamma.app). One command starts a drag-and-drop page on `localhost` — your files are processed in memory on your own machine and **never leave it**.

> No Python? No problem — [gammaremover.com](https://gammaremover.com) runs the same engine directly in your browser (WebAssembly, no upload either).

## What is this?

Gamma Watermark Remover Web UI is a self-hosted, local web application for removing the "Made with Gamma" watermark from Gamma.app exports. It gives you the convenience of a drag-and-drop browser interface with the privacy of local processing: the server binds to `127.0.0.1` only, files are handled in memory, and nothing is written to disk except the cleaned copy you download. It is the right choice when you want a visual tool but your documents are too sensitive for any online service.

Under the hood it uses the same structural removal engine as the [gammaremover.com](https://gammaremover.com) web app and the [CLI](https://github.com/gammaremover/gamma-watermark-remover): the Gamma badge and its gamma.app hyperlink are deleted as document objects, so PDF text stays selectable and PPTX slides stay fully editable.

## Quickstart

```bash
pipx install gamma-watermark-remover-webui   # or: pip install gamma-watermark-remover-webui
gamma-watermark-remover-webui
```

Then open **http://127.0.0.1:8330**, drop your exported `.pdf` or `.pptx`, and the cleaned copy downloads automatically with a report of how many watermark objects were removed.

## Why local?

Presentations often contain client names, financials, or unpublished work. Uploading them to a random "watermark remover" server is a real privacy risk. This tool binds to `127.0.0.1` only, keeps files in memory, and writes nothing to disk except your downloaded result.

## How removal works

Powered by the [gamma-watermark-remover](https://github.com/gammaremover/gamma-watermark-remover) library — **structural, lossless deletion**, not repainting:

- **PDF**: the gamma.app link annotation is dropped, and the draw operation of the small bottom-right badge image is removed from the content stream (position-tracked, size-guarded so backgrounds are never touched)
- **PPTX**: the gamma-hyperlinked shape is removed from slide masters/layouts — which is why the badge disappears from every slide at once

Text stays selectable, slides stay editable. If an export flattened the badge into the page image (rare), the UI tells you honestly that a watermark may remain.

## FAQ

**How is this different from the web version at gammaremover.com?**
Both process files without uploading. The hosted web app runs the engine inside your browser via WebAssembly — zero install. This local UI runs a small Python server on your machine — useful behind restrictive networks, for air-gapped machines, or when you prefer running auditable code yourself.

**Which formats are supported?**
PDF and PowerPoint (.pptx) files exported from Gamma.app.

**Does it change my slides or text?**
No. Removal is structural — only the watermark object is deleted. Fonts, layout, images, and animations are untouched.

**Can I run it on a different port?**
The server listens on `127.0.0.1:8330` by default; run behind any reverse proxy if you need something else.

## Related Tools

- **Web app** (browser-based, no upload): [gammaremover.com](https://gammaremover.com)
- **CLI + Python library**: [gamma-watermark-remover](https://github.com/gammaremover/gamma-watermark-remover)
- **Local web UI**: [gamma-watermark-remover-webui](https://github.com/gammaremover/gamma-watermark-remover-webui)
- **MCP server** for Claude and AI agents: [gamma-watermark-remover-mcp](https://github.com/gammaremover/gamma-watermark-remover-mcp)
- **Agent skill** for Claude Code and OpenClaw: [gamma-watermark-remover-skill](https://github.com/gammaremover/gamma-watermark-remover-skill)
- **Curated Gamma resources**: [awesome-gamma](https://github.com/gammaremover/awesome-gamma)

## Responsible use

Only process files you created or have the right to modify. Keep your originals and review cleaned files before sharing. Gamma's official watermark-free route is its [paid plan](https://gammaremover.com/en/blog/gamma-free-vs-pro-watermark/).

## License

MIT
