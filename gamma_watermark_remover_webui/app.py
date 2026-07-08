"""Local web UI for removing the "Made with Gamma" watermark.

Runs a small FastAPI server on localhost. Files are processed in-memory on
your machine and never leave it.
"""

from __future__ import annotations

import io
import urllib.parse

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse

from gamma_watermark_remover import clean_pdf, clean_pptx

app = FastAPI(title="Gamma Watermark Remover", docs_url=None, redoc_url=None)

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gamma Watermark Remover — local</title>
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; margin: 0; }
  body { font-family: system-ui, sans-serif; background: #0b0710; color: #e4e4e7;
         min-height: 100vh; display: grid; place-items: center;
         background-image: radial-gradient(50rem 30rem at 50% -10%, rgba(139,61,255,.18), transparent 70%); }
  main { width: min(560px, 92vw); text-align: center; padding: 2rem 0; }
  h1 { font-size: 1.6rem; margin-bottom: .4rem; }
  h1 span { color: #bd9bff; }
  p.sub { color: #a1a1aa; font-size: .92rem; margin-bottom: 1.6rem; }
  #drop { border: 2px dashed rgba(255,255,255,.18); border-radius: 16px; padding: 3rem 1.5rem;
          cursor: pointer; transition: .2s; background: rgba(26,17,38,.6); }
  #drop.drag, #drop:hover { border-color: #9f6bff; background: rgba(139,61,255,.08); }
  #drop strong { display: block; margin-bottom: .35rem; }
  #drop small { color: #a1a1aa; }
  #status { margin-top: 1.2rem; min-height: 1.4em; font-size: .95rem; }
  #status.ok { color: #6ee7b7; }
  #status.err { color: #fca5a5; }
  #status.warn { color: #fcd34d; }
  footer { margin-top: 1.6rem; font-size: .8rem; color: #71717a; }
  footer a { color: #bd9bff; }
</style>
</head>
<body>
<main>
  <h1>Gamma <span>Watermark</span> Remover</h1>
  <p class="sub">Local processing — your file never leaves this machine.</p>
  <div id="drop">
    <strong>Click or drop your Gamma export here</strong>
    <small>PDF or PowerPoint (.pptx)</small>
    <input id="file" type="file" accept=".pdf,.pptx" hidden>
  </div>
  <div id="status"></div>
  <footer>Prefer zero setup? The in-browser version lives at
    <a href="https://gammaremover.com" target="_blank" rel="noopener">gammaremover.com</a></footer>
</main>
<script>
const drop = document.getElementById('drop');
const input = document.getElementById('file');
const status = document.getElementById('status');
drop.onclick = () => input.click();
drop.ondragover = e => { e.preventDefault(); drop.classList.add('drag'); };
drop.ondragleave = () => drop.classList.remove('drag');
drop.ondrop = e => { e.preventDefault(); drop.classList.remove('drag');
                     if (e.dataTransfer.files[0]) handle(e.dataTransfer.files[0]); };
input.onchange = () => input.files[0] && handle(input.files[0]);

async function handle(file) {
  status.className = ''; status.textContent = 'Processing ' + file.name + '…';
  const fd = new FormData(); fd.append('file', file);
  try {
    const res = await fetch('/clean', { method: 'POST', body: fd });
    if (!res.ok) { const e = await res.json(); throw new Error(e.detail || 'failed'); }
    const removed = res.headers.get('x-removed');
    const mayRemain = res.headers.get('x-may-remain') === 'true';
    const blob = await res.blob();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = file.name.replace(/\\.(pdf|pptx)$/i, '') + '-no-watermark.' + file.name.split('.').pop();
    a.click(); URL.revokeObjectURL(a.href);
    status.className = mayRemain ? 'warn' : 'ok';
    status.textContent = 'Removed ' + removed + ' watermark object(s). Downloaded.' +
      (mayRemain ? ' Note: a flattened watermark may remain.' : '');
  } catch (err) {
    status.className = 'err';
    status.textContent = 'Error: ' + err.message;
  }
}
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return PAGE


@app.post("/clean")
async def clean(file: UploadFile = File(...)):
    name = (file.filename or "").lower()
    data = await file.read()
    if name.endswith(".pdf"):
        result = clean_pdf(data)
        media = "application/pdf"
    elif name.endswith(".pptx"):
        result = clean_pptx(data)
        media = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    else:
        return JSONResponse({"detail": "Only .pdf and .pptx files are supported."}, status_code=400)

    headers = {
        "x-removed": str(result.removed),
        "x-may-remain": "true" if result.may_remain else "false",
        "Content-Disposition": f"attachment; filename*=UTF-8''{urllib.parse.quote(file.filename or 'cleaned')}",
    }
    return StreamingResponse(io.BytesIO(result.cleaned), media_type=media, headers=headers)


def main() -> None:
    import uvicorn

    print("Gamma Watermark Remover — local web UI")
    print("Open http://127.0.0.1:8330 in your browser. Files never leave this machine.")
    uvicorn.run(app, host="127.0.0.1", port=8330, log_level="warning")


if __name__ == "__main__":
    main()
