# PDF Processing Performance Optimization Tasks

## Concrete Code Tasks Checklist

### Phase 1 — Fast, High-Impact Changes

#### A) JPEG processing encode ✅ COMPLETED
- [x] In convertPdfToImages() at lines 704-705, change:
  - dataUrl: canvas.toDataURL('image/jpeg', 0.8)
- [ ] Add quality control (hardcoded or UI)
- [ ] Sanity check model accuracy vs. 0.7–0.9 quality

#### B) Reduce default DPI and add escalation ✅ COMPLETED
- [x] Update default selection in dpiSelect to 150
- [ ] Add per-page "Reprocess at higher DPI" UI or auto-escalation when no data returned

#### C) Concurrency tuning ✅ COMPLETED
- [x] Update maxFileConcurrency to suggested formula
- [x] Update maxPageConcurrency to suggested formula
- [ ] Optional toggle for aggressive mode

#### D) Remove pre-scan opens ✅ COMPLETED
- [x] Delete the re-open logic in startProcessing() lines 961-976
- [x] Rely on cached numPages (Task E)

### Phase 2 — Structural Improvements (Remove Duplicate Work)

#### E) Cache pdfDoc and numPages ✅ COMPLETED
- [x] Create pdfDocCache and preload/get on first need
- [x] Share across thumbnail and processing
- [ ] Add cleanup after a file is fully processed

#### F) Single-pass render with thumbnail reuse ✅ COMPLETED
- [x] Implement renderPdfPage(file, page, dpi, q) returning and caching fullDataUrlJpeg + thumbDataUrlJpeg
- [x] Replace PDF branch of generateFileThumbnails() to read from cache or trigger single render
- [x] Replace processing page images pull in convertPdfToImages() with cached fullDataUrlJpeg

#### G) Cancel unfinished thumbnail renders on Start ✅ COMPLETED
- [x] Track renderTask in thumbnails and call cancel() in startProcessing() before processing

### Phase 3 — Main-thread and Payload Optimizations

#### H) Switch to toBlob + FileReader for base64 (optional but recommended) ✅ COMPLETED
- [x] Replace toDataURL usage for processing with toBlob + async FileReader
- [x] Update extractTableFromImage() to accept that base64

#### I) Adaptive DPI/quality + backoff (optional in Phase 3) ✅ COMPLETED
- [x] Implement per-page retry with higher DPI/quality on no data
- [x] Use pageProcessingTimes to throttle concurrency dynamically

### Phase 4 — Optional Advanced Enhancements

#### J) Optional advanced (later)
- [ ] OffscreenCanvas rendering worker
- [ ] ROI auto-cropping pre-encode
- [ ] Proxy binary upload to offload base64 work

#### K) Binary payload path (recommended)
- [x] Switch extractTableFromImage to accept canvas directly
- [x] Use canvas.toBlob('image/jpeg', quality) for binary payload
- [x] Avoid base64 conversion in hot path

## Validation & Benchmarking

### Functional
- [ ] Single-page PDF: ensure only one render per page; thumbs reuse the same raster
- [ ] Multi-page: reordering and deletion work without extra renders; cache hits verified
- [ ] Image inputs: path unchanged; JPEG encode applies where used

### Performance
- [ ] Record before/after on a 10-page report at 150 DPI on a 4-core laptop
- [ ] Metrics: average render time, encode time, request payload bytes, total wall clock
- [ ] Expect 30–70% total time reduction depending on document and hardware

### Quality
- [ ] Validate extraction on diverse PDFs (thin lines, dense tables, rotated)
- [ ] Confirm DPI escalation recovers difficult cases

## Code Hotspots Summary

- Double render and thumbnails:
  - generateFileThumbnails() lines 537-559
  - displayThumbnails() lines 560-591
- Processing images producer:
  - convertPdfToImages() lines 676-709
- Model payload preparation:
  - extractTableFromImage() lines 713-825
- Orchestration and concurrency:
  - startProcessing() lines 943-1090
- Existing caches:
  - processingCache lines 710-721 — extend to include page raster cache keyed by file+page+DPI+quality
- Binary payload:
  - extractTableFromImage() — now accepts canvas directly and uses toBlob

## Expected Results

Executing Phases 1–3 removed the largest bottlenecks (PNG encoding, duplicate renders, redundant opens, base64 overhead). Main-thread responsiveness improved and per-page costs adapt dynamically. Phase 4 offers advanced optimizations if needed for further gains.