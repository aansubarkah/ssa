# Plan to Accelerate PDF Processing in ConvertPDFNonOCRPakeAI/local_converter.html

Objective: Reduce wall-clock time for PDF-to-Excel conversion by removing duplicate rendering, shrinking image payloads, lowering raster workload, cutting redundant PDF opens, and controlling concurrency, while maintaining extraction accuracy.

References to current hotspots use clickable anchors to code locations from ["local_converter.html"](ConvertPDFNonOCRPakeAI/local_converter.html).

---

## Phase 1 — Fast, High-Impact Changes

1) Switch processing encode from PNG to JPEG
- Why: PNG encoding is CPU-heavy and creates large base64 payloads; JPEG is faster and smaller for table pages.
- Where to change:
  - Replace PNG with JPEG in the processing pipeline at ["convertPdfToImages()"](ConvertPDFNonOCRPakeAI/local_converter.html:676-709), lines ["704-705"](ConvertPDFNonOCRPakeAI/local_converter.html:704-705).
- Implementation:
  - canvas.toDataURL('image/jpeg', 0.8) instead of 'image/png'.
  - Add a quality variable (default 0.8) with possible UI select: 0.7, 0.8, 0.9.
- Expected effect: 2x–10x faster encoding and smaller request bodies to Ollama with negligible accuracy loss on tables.

2) Lower default processing DPI; add on-demand escalation
- Why: Raster cost grows ~quadratic with scale. Excess DPI massively increases render and encode times.
- Where:
  - Default DPI select options at ["dpiSelect"](ConvertPDFNonOCRPakeAI/local_converter.html:151-159).
  - DPI read at ["startProcessing()"](ConvertPDFNonOCRPakeAI/local_converter.html:955).
- Implementation:
  - Set default to 120–150 DPI.
  - Add a “Reprocess page at higher DPI” action for pages with no/sparse data to try 225–300 DPI.
  - Optional: a “Fast first pass” toggle to auto-escalate only failed pages.
- Expected effect: Large average speedup; still able to recover accuracy on difficult pages.

3) Tune concurrency (reduce contention)
- Why: Too many parallel page renders cause CPU/GPU contention and overall slowdown.
- Where:
  - File-level concurrency computed at ["startProcessing()"](ConvertPDFNonOCRPakeAI/local_converter.html:985).
  - Page-level concurrency per file at ["startProcessing()"](ConvertPDFNonOCRPakeAI/local_converter.html:1004-1006).
- Implementation:
  - maxFileConcurrency = Math.max(1, Math.floor((navigator.hardwareConcurrency || 4) / 3))
  - maxPageConcurrency = Math.max(2, Math.floor((navigator.hardwareConcurrency || 4) / 4))
  - Optional UI toggle: “Aggressive parallelism”
- Expected effect: Smoother UI, fewer stalls, similar or better throughput.

4) Remove extra PDF pre-scan open for page counting
- Why: Code opens PDFs again just to count pages before processing.
- Where:
  - Pre-scan loop at ["startProcessing()"](ConvertPDFNonOCRPakeAI/local_converter.html:961-976).
- Implementation:
  - Eliminate this open; in Phase 2 we’ll cache pdfDoc and numPages from the first open and use that everywhere.
- Expected effect: Avoid redundant IO/CPU overhead.

---

## Phase 2 — Structural Improvements (Remove Duplicate Work)

5) Single-pass render per page and reuse for thumbnails
- Why: Current code renders each PDF page twice: once at 0.5 scale for thumbnails in ["generateFileThumbnails()"](ConvertPDFNonOCRPakeAI/local_converter.html:537-559) and again at processing DPI in ["convertPdfToImages()"](ConvertPDFNonOCRPakeAI/local_converter.html:691-709).
- Implementation:
  - Introduce global page raster cache:
    - pageRasterCache: Map<string fileName, Map<number page, { dpi, quality, canvas, fullDataUrlJpeg, thumbDataUrlJpeg }>>
  - Create function renderPdfPage(file, pageNum, dpi, quality):
    - Uses cached pdfDoc (see Task 6) to get page.
    - Renders once with viewport scale = dpi/72 onto a canvas.
    - Produces:
      - fullDataUrlJpeg via canvas.toDataURL('image/jpeg', quality)
      - thumbDataUrlJpeg by drawing the full canvas onto a smaller offscreen canvas (e.g., max long edge 200px) and encoding JPEG (0.7).
    - Stores outputs in pageRasterCache.
  - Refactor thumbnail flow:
    - Replace the PDF branch of ["generateFileThumbnails()"](ConvertPDFNonOCRPakeAI/local_converter.html:541-559) to retrieve thumbDataUrlJpeg from pageRasterCache (rendering the page once if not present).
  - Refactor processing flow:
    - Replace re-rendering in ["convertPdfToImages()"](ConvertPDFNonOCRPakeAI/local_converter.html:691-709) with pulling fullDataUrlJpeg from pageRasterCache.
- Expected effect: Eliminate duplicate rendering and encoding per page.

6) Cache pdfjsLib.getDocument() and numPages per file
- Why: Prevent multiple opens of the same PDF in different steps.
- Implementation:
  - pdfDocCache: Map<string fileName, { pdfDoc, numPages }>
  - When a file is first needed (thumbnail or processing), load once:
    - const pdfDoc = await pdfjsLib.getDocument(arrayBuffer).promise
    - Cache pdfDoc and pdfDoc.numPages
  - Use cached numPages in ["startProcessing()"](ConvertPDFNonOCRPakeAI/local_converter.html:957-977) instead of re-opening.
  - Cleanup: pdfDoc.cleanup()/pdfDoc.destroy() after processing if memory needs to be released; clear cached canvases.
- Expected effect: Less IO/CPU duplication and quicker startup.

7) Cancel in-flight thumbnail renders on start
- Why: If the user clicks Start while thumbnails render, those tasks consume resources and delay processing.
- Where:
  - Thumbnail rendering call returns a renderTask in ["generateFileThumbnails()"](ConvertPDFNonOCRPakeAI/local_converter.html:551).
  - Processing entry point is ["startProcessing()"](ConvertPDFNonOCRPakeAI/local_converter.html:943-1090).
- Implementation:
  - Track renderTask(s) globally for thumbnails.
  - On startProcessing(), call renderTask.cancel() for any unfinished thumbnail renders.
  - Optionally delay/lazy-generate thumbnails from pageRasterCache after processing begins.
- Expected effect: Immediate processing priority and reduced contention.

---

## Phase 3 — Main-thread and Payload Optimizations

8) Use toBlob + FileReader instead of toDataURL for base64
- Why: toDataURL is synchronous and can block the main thread; toBlob is async and may be more memory efficient.
- Where:
  - Processing encode currently set in ["convertPdfToImages()"](ConvertPDFNonOCRPakeAI/local_converter.html:691-709).
  - Base64 consumption in ["extractTableFromImage()"](ConvertPDFNonOCRPakeAI/local_converter.html:713-825).
- Implementation:
  - Replace canvas.toDataURL with:
    - const blob = await new Promise(res => canvas.toBlob(res, 'image/jpeg', quality));
    - Convert blob to base64 via FileReader.readAsDataURL(blob) then split(',')[1].
  - Adjust extractTableFromImage to accept base64 produced by this async step.
- Expected effect: Reduced main-thread stalls during encoding.

9) Adaptive DPI/Quality per page
- Why: Not all pages require high DPI/quality; adaptive strategy reduces average cost.
- Implementation:
  - Initial render at 150 DPI, JPEG Q=0.75 for all pages.
  - If a page returns no tables, re-render that page at 225–300 DPI or Q=0.85 and retry extraction.
  - Add a toggle: “Fast-first pass with per-page escalation.”
- Expected effect: Lower average cost with maintained final accuracy.

10) Concurrency backoff driven by observed timings
- Why: Dynamic adaptation improves throughput across diverse hardware/PDFs.
- Where:
  - You already track ["pageProcessingTimes"](ConvertPDFNonOCRPakeAI/local_converter.html:1271-1273).
- Implementation:
  - Maintain a rolling average of per-page time.
  - If average exceeds threshold (e.g., 3–5s), decrement maxPageConcurrency by 1 down to a minimum; if very fast, cautiously increase within a cap.
- Expected effect: Stable processing rates with fewer spikes.

---

## Phase 4 — Optional Advanced Enhancements

11) OffscreenCanvas and dedicated worker for raster/encode
- Why: Reduce main-thread jank for UI and scheduling.
- Implementation:
  - Detect OffscreenCanvas; move raster and encode to a Web Worker.
  - PDF.js already uses a worker for parsing; this adds another for rendering pipeline.
- Expected effect: More responsive UI during heavy workloads.

12) ROI cropping to reduce payload
- Why: Large margins/borders add pixels without useful content.
- Implementation:
  - Quick grayscale + threshold to detect the bounding box of non-white content on the canvas.
  - Draw only ROI to the encoding canvas for JPEG; pass cropped base64 to the model.
- Expected effect: Smaller payloads and faster encode, especially on pages with big margins.

13) Use local proxy to accept binary/multipart and handle base64 server-side
- Why: Offload base64 work from the main thread.
- Where:
  - There is a local server candidate: ["ollama-proxy-server.py"](ConvertPDFNonOCRPakeAI/ollama-proxy-server.py:1).
- Implementation:
  - Add an endpoint that accepts multipart/form-data; encode server-side and forward to Ollama.
  - Client sends blobs (no toDataURL).
- Expected effect: Reduced client CPU usage; same functional result.

---

## Concrete Code Tasks Checklist

A) JPEG processing encode
- [ ] In ["convertPdfToImages()"](ConvertPDFNonOCRPakeAI/local_converter.html:691-709) at ["704-705"](ConvertPDFNonOCRPakeAI/local_converter.html:704-705), change:
  - dataUrl: canvas.toDataURL('image/jpeg', 0.8)
- [ ] Add quality control (hardcoded or UI).
- [ ] Sanity check model accuracy vs. 0.7–0.9 quality.

B) Reduce default DPI and add escalation
- [ ] Update default selection in ["dpiSelect"](ConvertPDFNonOCRPakeAI/local_converter.html:151-159) to 150.
- [ ] Add per-page “Reprocess at higher DPI” UI or auto-escalation when no data returned.

C) Concurrency tuning
- [ ] Update ["maxFileConcurrency"](ConvertPDFNonOCRPakeAI/local_converter.html:985) to suggested formula.
- [ ] Update ["maxPageConcurrency"](ConvertPDFNonOCRPakeAI/local_converter.html:1004-1006) to suggested formula.
- [ ] Optional toggle for aggressive mode.

D) Remove pre-scan opens
- [ ] Delete the re-open logic in ["startProcessing()"](ConvertPDFNonOCRPakeAI/local_converter.html:961-976).
- [ ] Rely on cached numPages (Task E).

E) Cache pdfDoc and numPages
- [ ] Create pdfDocCache and preload/get on first need.
- [ ] Share across thumbnail and processing.
- [ ] Add cleanup after a file is fully processed.

F) Single-pass render with thumbnail reuse
- [ ] Implement renderPdfPage(file, page, dpi, q) returning and caching fullDataUrlJpeg + thumbDataUrlJpeg.
- [ ] Replace PDF branch of ["generateFileThumbnails()"](ConvertPDFNonOCRPakeAI/local_converter.html:541-559) to read from cache or trigger single render.
- [ ] Replace processing page images pull in ["convertPdfToImages()"](ConvertPDFNonOCRPakeAI/local_converter.html:691-709) with cached fullDataUrlJpeg.

G) Cancel unfinished thumbnail renders on Start
- [ ] Track renderTask in thumbnails and call cancel() in ["startProcessing()"](ConvertPDFNonOCRPakeAI/local_converter.html:943-1090) before processing.

H) Switch to toBlob + FileReader for base64 (optional but recommended)
- [ ] Replace toDataURL usage for processing with toBlob + async FileReader.
- [ ] Update ["extractTableFromImage()"](ConvertPDFNonOCRPakeAI/local_converter.html:713-825) to accept that base64.

I) Adaptive DPI/quality + backoff (optional in Phase 3)
- [ ] Implement per-page retry with higher DPI/quality on no data.
- [ ] Use pageProcessingTimes to throttle concurrency dynamically.

J) Optional advanced (later)
- [ ] OffscreenCanvas rendering worker.
- [ ] ROI auto-cropping pre-encode.
- [ ] Proxy binary upload to offload base64 work.

---

## Validation & Benchmarking

Functional
- [ ] Single-page PDF: ensure only one render per page; thumbs reuse the same raster.
- [ ] Multi-page: reordering and deletion work without extra renders; cache hits verified.
- [ ] Image inputs: path unchanged; JPEG encode applies where used.

Performance
- [ ] Record before/after on a 10-page report at 150 DPI on a 4-core laptop.
- [ ] Metrics: average render time, encode time, request payload bytes, total wall clock.
- [ ] Expect 30–70% total time reduction depending on document and hardware.

Quality
- [ ] Validate extraction on diverse PDFs (thin lines, dense tables, rotated).
- [ ] Confirm DPI escalation recovers difficult cases.

---

## Code Hotspots Summary

- Double render and thumbnails:
  - ["generateFileThumbnails()"](ConvertPDFNonOCRPakeAI/local_converter.html:537-559)
  - ["displayThumbnails()"](ConvertPDFNonOCRPakeAI/local_converter.html:560-591)
- Processing images producer:
  - ["convertPdfToImages()"](ConvertPDFNonOCRPakeAI/local_converter.html:676-709)
- Model payload preparation:
  - ["extractTableFromImage()"](ConvertPDFNonOCRPakeAI/local_converter.html:713-825)
- Orchestration and concurrency:
  - ["startProcessing()"](ConvertPDFNonOCRPakeAI/local_converter.html:943-1090)
- Existing caches:
  - ["processingCache"](ConvertPDFNonOCRPakeAI/local_converter.html:710-721) — extend to include page raster cache keyed by file+page+DPI+quality.

Executing Phases 1–2 will remove the largest bottlenecks (PNG encoding, duplicate renders, redundant opens). Phase 3 improves main-thread responsiveness and adapts cost per page. Phase 4 offers advanced optimizations if needed for further gains.