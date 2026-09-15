import os
import cv2
import numpy as np
import base64
import streamlit as st
import streamlit.components.v1 as components

# =========================================================================
# 1. GENERADOR AUTOMÁTICO DE FRONTEND
# =========================================================================
st.set_page_config(page_title="MidePlanos PRO", layout="wide", initial_sidebar_state="collapsed")

os.makedirs("frontend", exist_ok=True)

HTML_FRONTEND = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MidePlanos PRO - Pure Python Backend</title>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/streamlit-component-lib@1.3.0/dist/streamlit-component-lib.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root { --primary: #0ea5e9; --success: #10b981; --warning: #f59e0b; --danger: #ef4444; --magic: #a855f7; --circle: #ec4899; --curve: #14b8a6; --cad: #64748b; --bg-body: #0f172a; --bg-panel: rgba(30, 41, 59, 0.96); --border: #334155; --text-main: #f8fafc; --text-muted: #94a3b8; }
        ::-webkit-scrollbar { width: 8px; height: 8px; } ::-webkit-scrollbar-track { background: transparent; } ::-webkit-scrollbar-thumb { background: #475569; border-radius: 10px; }
        body { font-family: 'Inter', sans-serif; background-color: var(--bg-body); margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; color: var(--text-main); }
        .header { background: var(--bg-panel); backdrop-filter: blur(12px); padding: 6px 16px; border-bottom: 1px solid var(--border); z-index: 100; display: flex; flex-direction: column; gap: 6px; }
        .toolbar-row { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; }
        .toolbar-group { display: flex; gap: 8px; align-items: center; } .toolbar-group.tools-top { border-left: 1px solid var(--border); border-right: 1px solid var(--border); padding: 0 12px; }
        button { border: none; cursor: pointer; font-family: inherit; outline: none; }
        button:not(.tool-btn) { padding: 6px 10px; border: 1px solid var(--border); border-radius: 6px; font-weight: 600; font-size: 11px; transition: 0.2s; background: #1e293b; color: var(--text-main); }
        button:not(.tool-btn):hover { background: #334155; border-color: #475569; }
        .btn-action { background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%) !important; color: white !important; border-color: #1d4ed8 !important; }
        .tool-trigger.active { background: #0ea5e9; color: white; border-color: #0ea5e9; box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.3); }
        .tool-trigger.btn-success.active { background: var(--success); color: white; border-color: var(--success); }
        .tool-trigger.btn-magic.active { background: var(--magic); color: white; border-color: var(--magic); }
        input[type="file"] { display: none; } .file-label { padding: 6px 10px; background: linear-gradient(180deg, #334155 0%, #1e293b 100%); color: white; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 11px; display: inline-block; border: 1px solid #475569; }
        .controls-bar { display: flex; justify-content: space-between; align-items: center; background: rgba(15, 23, 42, 0.4); padding: 4px 12px; border-radius: 6px; border: 1px solid var(--border); }
        .controls-left { display: flex; gap: 16px; align-items: center; } .pdf-controls { display: none; align-items: center; gap: 6px; border-right: 1px solid var(--border); padding-right: 12px; }
        .page-input { width: 35px; text-align: center; font-size: 12px; font-weight: 600; background: #0f172a; color: white; border: 1px solid var(--border); border-radius: 4px; padding: 4px; }
        .zoom-controls { display: flex; align-items: center; gap: 6px; } .zoom-controls span { font-weight: 600; color: var(--text-muted); font-size: 11px; text-transform: uppercase; } .zoom-btn { padding: 2px 8px !important; border-radius: 4px !important; font-size: 13px !important;}
        .status-text { font-size: 12px; font-weight: 500; color: #fcd34d; background: rgba(245, 158, 11, 0.1); padding: 4px 10px; border-radius: 4px; border: 1px solid rgba(245, 158, 11, 0.2); }
        .scale-badge { font-size: 11px; font-weight: 700; color: #fca5a5; padding: 4px 8px; border-radius: 4px; background: rgba(239, 68, 68, 0.1); border: 1px dashed #ef4444; transition: 0.3s;} .scale-badge.calibrated { color: #6ee7b7; border-color: #10b981; background: rgba(16, 185, 129, 0.1); border-style: solid; }
        .left-toolbar { width: 54px; background: var(--bg-panel); border-right: 1px solid var(--border); display: flex; flex-direction: column; align-items: center; padding: 10px 0; gap: 6px; z-index: 50; overflow: visible; }
        .tool-btn { width: 36px; height: 36px; flex-shrink: 0; border-radius: 8px; background: #1e293b; border: 1px solid var(--border); color: var(--text-main); display: flex; align-items: center; justify-content: center; font-size: 15px; transition: 0.2s; position: relative; padding: 0;} .tool-btn:hover { background: #334155; border-color: #475569;}
        .tool-btn::after { content: attr(data-tooltip); position: absolute; left: 100%; top: 50%; transform: translateY(-50%) translateX(5px); margin-left: 8px; background: #0f172a; color: #fff; padding: 6px 12px; border-radius: 6px; font-size: 11px; font-weight: 600; white-space: nowrap; opacity: 0; visibility: hidden; transition: 0.2s; pointer-events: none; border: 1px solid var(--border); z-index: 9999; box-shadow: 0 4px 10px rgba(0,0,0,0.3); } .tool-btn:hover::after { opacity: 1; visibility: visible; transform: translateY(-50%) translateX(0); }
        .main-container { display: flex; flex: 1; overflow: hidden; }
        .workspace { flex: 1; display: flex; flex-direction: column; padding: 20px; overflow: hidden; background-color: var(--bg-body); background-image: radial-gradient(#334155 1.5px, transparent 1.5px); background-size: 24px 24px; z-index: 1;}
        .canvas-container { flex: 1; overflow: auto; background: white; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.4); position: relative; border: 1px solid #000; }
        canvas { display: block; transform-origin: top left; transition: width 0.1s, height 0.1s; }
        #loupeCanvas { position: fixed; pointer-events: none; border-radius: 50%; border: 2px solid #0ea5e9; box-shadow: 0 5px 15px rgba(0,0,0,0.6); display: none; z-index: 9999; background: white; }
        .resizer { width: 5px; background: var(--bg-body); cursor: ew-resize; transition: 0.2s; z-index: 20; border-left: 1px solid var(--border); } .resizer:hover, .resizer.resizing { background: #0ea5e9; }
        .sidebar { width: 340px; background: var(--bg-panel); display: flex; flex-direction: column; z-index: 5; }
        .sidebar-header { padding: 12px 16px; border-bottom: 1px solid var(--border); background: rgba(15, 23, 42, 0.4); } .sidebar-header h3 { margin: 0; font-size: 13px; font-weight: 700; display: flex; justify-content: space-between; }
        .measurement-list { flex: 1; overflow-y: auto; padding: 12px; display: flex; flex-direction: column; gap: 8px; } .empty-state { text-align: center; color: var(--text-muted); font-size: 12px; margin-top: 20px; }
        .measure-item { border: 1px solid var(--border); border-radius: 6px; padding: 6px 8px; background: #1e293b; display: flex; flex-direction: row; align-items: center; justify-content: space-between; gap: 8px; border-left: 4px solid var(--primary); transition: 0.2s; cursor: pointer; } .measure-item:hover, .measure-item.highlighted { background: #334155; border-color: #64748b; transform: translateX(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.2); } .measure-item.selected { background: #1e293b; border-color: #0ea5e9; box-shadow: inset 0 0 0 1px #0ea5e9; }
        .color-picker { -webkit-appearance: none; border: none; width: 16px; height: 16px; border-radius: 4px; cursor: pointer; padding: 0; background: transparent; flex-shrink: 0;} .color-picker::-webkit-color-swatch-wrapper { padding: 0; } .color-picker::-webkit-color-swatch { border: 1px solid #475569; border-radius: 4px; }
        .measure-name { font-family: inherit; font-size: 11px; font-weight: 600; border: 1px solid transparent; padding: 2px 4px; border-radius: 4px; flex-grow: 1; min-width: 40px; background: transparent; color: white; cursor: text; } .measure-name:focus { border-color: #0ea5e9; background: #0f172a; outline: none; }
        .measure-values { font-size: 11px; color: var(--text-muted); display: flex; flex-direction: row; align-items: center; gap: 4px; white-space: nowrap; flex-shrink: 0; cursor: default; } .measure-values span { font-weight: 700; color: #e2e8f0; font-size: 11px; }
        .btn-delete { background: #0f172a !important; border: 1px solid var(--border) !important; color: var(--text-muted) !important; padding: 4px 6px !important; border-radius: 4px !important; font-size: 10px; transition: 0.2s; flex-shrink: 0; cursor: pointer;} .btn-delete:hover { color: #fca5a5 !important; background: #7f1d1d !important; }
        .sidebar-footer { padding: 16px; border-top: 1px solid var(--border); background: rgba(15, 23, 42, 0.4); } .btn-export { width: 100%; background: linear-gradient(180deg, #10b981 0%, #059669 100%) !important; color: white !important; border-color: #059669 !important; padding: 10px !important; font-size: 13px; border-radius: 6px;}

        #customModal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15,23,42,0.8); z-index: 99999; display: none; justify-content: center; align-items: center; backdrop-filter: blur(4px); }
        .modal-content { background: #1e293b; padding: 24px; border-radius: 12px; border: 1px solid #334155; color: white; width: 320px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .modal-content h3 { margin-top: 0; font-size: 15px; font-weight: 600; color: #f8fafc; }
        .modal-content input { width: 100%; box-sizing: border-box; padding: 10px; margin: 15px 0; background: #0f172a; border: 1px solid #0ea5e9; color: white; border-radius: 6px; outline: none; display: none; font-size: 14px; text-align: center; }
        .modal-buttons { display: flex; justify-content: center; gap: 12px; margin-top: 20px; } .modal-buttons button { padding: 8px 16px; border-radius: 6px; border: none; cursor: pointer; font-weight: 600; transition: 0.2s; }
        .modal-cancel { background: #334155; color: #f8fafc; display: none; } .modal-cancel:hover { background: #475569; }
        .modal-ok { background: #0ea5e9; color: white; } .modal-ok:hover { background: #0284c7; }
    </style>
</head>
<body>
    <div id="customModal"><div class="modal-content"><h3 id="modalTitle"></h3><input type="text" id="modalInput" onkeyup="if(event.key === 'Enter') document.getElementById('modalBtnOk').click();" autocomplete="off"><div class="modal-buttons"><button id="modalBtnCancel" class="modal-cancel">Cancelar</button><button id="modalBtnOk" class="modal-ok">Aceptar</button></div></div></div>
    <canvas id="loupeCanvas" width="120" height="120"></canvas>

    <div class="header">
        <div class="toolbar-row">
            <div class="toolbar-group">
                <label class="file-label">📄 Nuevo <input type="file" id="imageLoader" accept="image/png, image/jpeg, image/webp, application/pdf"/></label>
                <button id="btnSave" class="btn-action">💾 Guardar Proyecto</button>
            </div>
            <div class="toolbar-group tools-top">
                <button data-mode="select" class="tool-trigger active">↖️ Seleccionar</button>
                <button data-mode="calibrate" class="tool-trigger">📏 Calibrar</button>
                <button data-mode="distance" class="tool-trigger">➖ Recta</button>
                <button data-mode="area" class="tool-trigger btn-success">⬟ Área Manual</button>
                <button data-mode="autoLine" class="tool-trigger btn-magic" style="color:#d8b4fe;">⚡ Auto-Línea (IA)</button>
                <button data-mode="autoArea" class="tool-trigger btn-magic" style="color:#d8b4fe;">✨ Auto-Área (IA)</button>
            </div>
            <div class="toolbar-group"><button id="btnToggleSidebar" style="background:#334155; color:white;">🗂️ Panel</button></div>
        </div>
        <div class="toolbar-row controls-bar">
            <div class="controls-left">
                <div class="pdf-controls" id="pdfControls"><button class="zoom-btn" id="btnPrev">◀</button><span style="font-size: 12px; font-weight: 600;">Pág <input type="number" id="pageInput" class="page-input" value="1" min="1"> de <span id="pageTotal">1</span></span><button class="zoom-btn" id="btnNext">▶</button></div>
                <div class="zoom-controls"><span>🔍 Zoom:</span><button class="zoom-btn" id="btnZoomOut">➖</button><span id="zoomLevel">100%</span><button class="zoom-btn" id="btnZoomIn">➕</button></div>
                <div id="statusText" class="status-text">✅ Servidor Python conectado y listo.</div>
            </div>
            <div id="scaleInfo" class="scale-badge">ESCALA NO CALIBRADA</div>
        </div>
    </div>

    <div class="main-container">
        <div class="left-toolbar">
            <button data-mode="select" class="tool-btn tool-trigger" data-tooltip="Seleccionar">↖️</button><hr style="width: 50%; border: 0; border-top: 1px solid var(--border); margin: 0;">
            <button data-mode="calibrate" class="tool-btn tool-trigger" data-tooltip="Calibrar">📏</button>
            <button data-mode="distance" class="tool-btn tool-trigger" data-tooltip="Línea">➖</button>
            <button data-mode="area" class="tool-btn btn-success tool-trigger" data-tooltip="Área">⬟</button><hr style="width: 50%; border: 0; border-top: 1px solid var(--border); margin: 0;">
            <button data-mode="autoLine" class="tool-btn btn-magic tool-trigger" data-tooltip="Auto-Línea (Python)">⚡</button>
            <button data-mode="autoArea" class="tool-btn btn-magic tool-trigger" data-tooltip="Auto-Área (Python)">✨</button>
        </div>
        <div class="workspace"><div class="canvas-container" id="canvasContainer"><canvas id="planCanvas"></canvas></div></div>
        <div class="resizer" id="sidebarResizer"></div>
        <div class="sidebar" id="rightSidebar">
            <div class="sidebar-header"><h3>Mediciones <span id="sbPageTitle" style="color:var(--text-muted); font-size:11px;"></span></h3></div>
            <div class="measurement-list" id="measurementList"><div class="empty-state">No hay medidas en esta página.</div></div>
            <div class="sidebar-footer"><button id="btnExport" class="btn-export">Descargar Excel (.CSV)</button></div>
        </div>
    </div>

    <script>
        try {
            const pdfWorkerUrl = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';
            const blob = new Blob([`importScripts('${pdfWorkerUrl}');`], { type: 'text/javascript' });
            pdfjsLib.GlobalWorkerOptions.workerSrc = URL.createObjectURL(blob);
        } catch (e) { console.warn("Motor PDF seguro."); }

        function cAlert(msg, callback) { const m = document.getElementById('customModal'); m.style.display = 'flex'; document.getElementById('modalTitle').innerText = msg; document.getElementById('modalInput').style.display = 'none'; document.getElementById('modalBtnCancel').style.display = 'none'; document.getElementById('modalBtnOk').onclick = () => { m.style.display = 'none'; if(callback) callback(); }; }
        function cPrompt(msg, callback) { const m = document.getElementById('customModal'); m.style.display = 'flex'; document.getElementById('modalTitle').innerText = msg; const inp = document.getElementById('modalInput'); inp.style.display = 'block'; inp.value = ''; setTimeout(() => inp.focus(), 50); document.getElementById('modalBtnCancel').style.display = 'block'; document.getElementById('modalBtnCancel').onclick = () => { m.style.display = 'none'; callback(null); }; document.getElementById('modalBtnOk').onclick = () => { m.style.display = 'none'; callback(inp.value); }; }

        const canvas = document.getElementById('planCanvas'); const ctx = canvas.getContext('2d', { willReadFrequently: true });
        const canvasContainer = document.getElementById('canvasContainer'); const imageLoader = document.getElementById('imageLoader');
        const measurementListEl = document.getElementById('measurementList'); const pageInput = document.getElementById('pageInput');
        const loupeCanvas = document.getElementById('loupeCanvas'); const loupeCtx = loupeCanvas.getContext('2d');
        const resizer = document.getElementById('sidebarResizer'); const rightSidebar = document.getElementById('rightSidebar');
        
        let img = new Image(); let mode = 'select'; let currentZoom = 1; let measurementsByPage = {}; let counters = { line: 1, area: 1, circle: 1, arc: 1, dimension: 1 };
        let scaleByPage = {}; let currentFileDataURL = null; let currentFileType = null; let pdfDoc = null; let pageNum = 1; 
        let isDrawing = false; let startX, startY, endX, endY; let currentPath = []; let tempPoint = null; let measureStep = 0; 
        let isPanning = false; let panStartX, panStartY, panScrollLeft, panScrollTop; let draggingLabel = null; let dragOffsetX = 0, dragOffsetY = 0;
        let editingMeasureId = null; let draggingPointIndex = -1; let highlightedMeasureId = null; let isResizing = false;

        function getDefaultColor(type) { if (type === 'straight') return '#0ea5e9'; if (type === 'area' || type === 'autoArea') return '#10b981'; if (type === 'autoLine') return '#a855f7'; return '#ffffff'; }
        function hexToRgba(hex, alpha) { if(!hex) return `rgba(255,255,255,${alpha})`; hex = hex.replace('#', ''); if(hex.length === 3) hex = hex.split('').map(x => x + x).join(''); let r = parseInt(hex.substring(0,2), 16), g = parseInt(hex.substring(2,4), 16), b = parseInt(hex.substring(4,6), 16); return `rgba(${r}, ${g}, ${b}, ${alpha})`; }
        function getMousePos(e) { const rect = canvas.getBoundingClientRect(); return { x: (e.clientX - rect.left) * (canvas.width / rect.width), y: (e.clientY - rect.top) * (canvas.height / rect.height) }; }

        resizer.addEventListener('mousedown', () => { isResizing = true; document.body.style.cursor = 'ew-resize'; });
        document.addEventListener('mousemove', (e) => { if (!isResizing) return; const newWidth = document.body.clientWidth - e.clientX; if (newWidth > 200 && newWidth < 600) rightSidebar.style.width = newWidth + 'px'; });
        document.addEventListener('mouseup', () => { if (isResizing) { isResizing = false; document.body.style.cursor = 'default'; } });
        document.getElementById('btnToggleSidebar').onclick = () => { rightSidebar.style.display = (rightSidebar.style.display === 'none') ? 'flex' : 'none'; resizer.style.display = (resizer.style.display === 'none') ? 'block' : 'none'; };

        function applyZoom() { if(canvas.width === 0) return; canvas.style.width = (canvas.width * currentZoom) + 'px'; canvas.style.height = (canvas.height * currentZoom) + 'px'; document.getElementById('zoomLevel').innerText = Math.round(currentZoom * 100) + '%'; }
        document.getElementById('btnZoomIn').onclick = () => { currentZoom *= 1.2; applyZoom(); };
        document.getElementById('btnZoomOut').onclick = () => { currentZoom /= 1.2; applyZoom(); };
        canvasContainer.addEventListener('wheel', (e) => { if (e.ctrlKey || e.metaKey) { e.preventDefault(); currentZoom *= (e.deltaY < 0 ? 1.1 : 0.9); currentZoom = Math.max(0.05, Math.min(currentZoom, 10)); applyZoom(); } }, { passive: false });

        function updateLoupe(e, x, y) {
            if (!img.src) return;
            loupeCanvas.style.display = 'block'; let loupeSize = 120; let offset = 20; let leftPos = e.clientX + offset; let topPos = e.clientY + offset;
            if (leftPos + loupeSize > window.innerWidth) leftPos = e.clientX - loupeSize - offset; if (topPos + loupeSize > window.innerHeight) topPos = e.clientY - loupeSize - offset;
            loupeCanvas.style.left = leftPos + 'px'; loupeCanvas.style.top = topPos + 'px';
            loupeCtx.fillStyle = '#ffffff'; loupeCtx.fillRect(0, 0, 120, 120); const zoomFactor = 2.5; const srcSize = 120 / (currentZoom * zoomFactor);
            loupeCtx.drawImage(canvas, x - srcSize/2, y - srcSize/2, srcSize, srcSize, 0, 0, 120, 120); loupeCtx.beginPath(); loupeCtx.moveTo(0, 60); loupeCtx.lineTo(120, 60); loupeCtx.moveTo(60, 0); loupeCtx.lineTo(60, 120); loupeCtx.strokeStyle = 'rgba(239, 68, 68, 0.8)'; loupeCtx.lineWidth = 1.5; loupeCtx.stroke();
        }

        function loadDocumentFromDataURL(isNew = false) {
            if (currentFileType === 'application/pdf') {
                const base64Index = currentFileDataURL.indexOf(';base64,') + 8; const rawBase64 = currentFileDataURL.substring(base64Index); const raw = window.atob(rawBase64); const array = new Uint8Array(raw.length);
                for(let i=0; i<raw.length; i++) array[i] = raw.charCodeAt(i);
                pdfjsLib.getDocument(array).promise.then(function(pdf) { pdfDoc = pdf; document.getElementById('pdfControls').style.display = 'flex'; document.getElementById('pageTotal').textContent = pdfDoc.numPages; pageInput.max = pdfDoc.numPages; renderPage(pageNum, isNew); }).catch(err => { cAlert("Error al abrir PDF."); });
            } else { document.getElementById('pdfControls').style.display = 'none'; pdfDoc = null; document.getElementById('sbPageTitle').textContent = `(Imagen)`; img.onload = function() { resetCanvasEnvironment(isNew); }; img.src = currentFileDataURL; }
        }

        function renderPage(num, isNew = false) {
            pdfDoc.getPage(num).then(function(page) {
                const viewport = page.getViewport({ scale: 2.0 }); const tempCanvas = document.createElement('canvas'); const tempCtx = tempCanvas.getContext('2d'); tempCanvas.height = viewport.height; tempCanvas.width = viewport.width;
                page.render({canvasContext: tempCtx, viewport: viewport}).promise.then(function() { img.onload = function() { resetCanvasEnvironment(isNew); }; img.src = tempCanvas.toDataURL('image/png'); pageInput.value = pageNum; document.getElementById('sbPageTitle').textContent = `(Pág. ${pageNum})`; });
            });
        }
        
        function resetCanvasEnvironment(isNewDocument) {
            canvas.width = img.width; canvas.height = img.height; editingMeasureId = null; draggingPointIndex = -1;
            if (isNewDocument) { const cw = canvasContainer.clientWidth - 40; const ch = canvasContainer.clientHeight - 40; if (cw > 0 && ch > 0 && img.width > 0 && img.height > 0) { currentZoom = Math.min(cw / img.width, ch / img.height) * 0.95; currentZoom = Math.max(0.05, Math.min(currentZoom, 5)); } else currentZoom = 1; setTimeout(() => { canvasContainer.scrollLeft = 0; canvasContainer.scrollTop = 0; }, 10); } 
            applyZoom(); updateSidebar(); redraw();
            const currentScale = scaleByPage[pageNum]; const txt = document.getElementById('statusText');
            if (currentScale > 0) { txt.innerText = `Plano listo. Puedes medir.`; document.getElementById('scaleInfo').innerText = `ESC. PÁG. ${pageNum} (1m = ${Math.round(currentScale)}px)`; document.getElementById('scaleInfo').className = "scale-badge calibrated"; if(mode === 'none' || mode === 'calibrate') setMode('select'); } 
            else { txt.innerText = "Calibra la escala para esta página."; document.getElementById('scaleInfo').innerText = "ESCALA NO CALIBRADA"; document.getElementById('scaleInfo').className = "scale-badge"; setMode('none'); }
        }

        imageLoader.addEventListener('change', function(e) {
            const file = e.target.files[0]; if (!file) return;
            currentFileType = file.type; measurementsByPage = {}; counters = { line: 1, area: 1, circle: 1, arc: 1, dimension: 1 }; pageNum = 1; scaleByPage = {}; document.getElementById('statusText').innerText = "Cargando plano...";
            const reader = new FileReader(); reader.onload = function(event) { currentFileDataURL = event.target.result; loadDocumentFromDataURL(true); }; reader.readAsDataURL(file); e.target.value = ""; 
        });

        document.getElementById('btnPrev').onclick = () => { if (pageNum > 1) { pageNum--; renderPage(pageNum, false); }};
        document.getElementById('btnNext').onclick = () => { if (pageNum < pdfDoc.numPages) { pageNum++; renderPage(pageNum, false); }};

        document.querySelectorAll('.tool-trigger').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const selectedMode = e.currentTarget.getAttribute('data-mode');
                if (['distance', 'area', 'autoLine', 'autoArea'].includes(selectedMode)) { if (!scaleByPage[pageNum]) { cAlert("¡Calibra la escala primero!"); return; } } 
                setMode(selectedMode);
            });
        });
        
        function setMode(newMode) {
            mode = newMode; 
            document.querySelectorAll('.tool-trigger').forEach(btn => btn.classList.remove('active'));
            if(mode !== 'none') { document.querySelectorAll(`.tool-trigger[data-mode="${mode}"]`).forEach(btn => btn.classList.add('active')); }
            canvas.style.cursor = (mode === 'select' || mode === 'pan') ? 'grab' : 'crosshair';
            
            const txts = { 'select': "Modo Selección", 'calibrate': "1º Clic (Inicio) -> 2º Clic (Fin)", 'distance': "1º Clic (Inicio) -> 2º Clic (Fin)", 'area': "Clics para esquinas. Clic derecho = Cerrar", 'autoLine': "Haz clic en la red para que Python la calcule", 'autoArea': "Haz clic en el sombreado para que Python lo calcule" };
            if(txts[mode]) document.getElementById('statusText').innerText = txts[mode];
            isDrawing = false; measureStep = 0; currentPath = []; tempPoint = null; if (mode !== 'select') editingMeasureId = null; redraw(); loupeCanvas.style.display = 'none';
        }

        // =========================================================================
        // COMUNICACIÓN CON PYTHON (STREAMLIT CLOUD)
        // =========================================================================
        function triggerCloudProcessing(startX, startY, autoMode) {
            document.getElementById('statusText').innerText = "☁️ Enviando coordenadas al servidor Python...";
            document.getElementById('statusText').style.color = "#fcd34d";
            
            // Enviamos todo a Python
            Streamlit.setComponentValue({
                action: autoMode,
                x: startX,
                y: startY,
                image: canvas.toDataURL('image/png'),
                scale: scaleByPage[pageNum] || 1,
                ts: Date.now()
            });
            setMode('select');
        }

        let lastProcessedTs = null;
        function onRender(event) {
            const data = event.detail.args;
            if (data && data.comando_desde_python) {
                const pyRes = data.comando_desde_python;
                if (pyRes.ts && pyRes.ts !== lastProcessedTs) {
                    lastProcessedTs = pyRes.ts;
                    
                    if (pyRes.error) {
                        cAlert(pyRes.error);
                        document.getElementById('statusText').innerText = "❌ Error en Python.";
                    } else {
                        let resImg = new Image();
                        resImg.onload = () => {
                            addMeasurement({
                                type: pyRes.tipo, img: resImg, cx: pyRes.cx, cy: pyRes.cy, points: pyRes.puntos, valM: pyRes.perimetro, valM2: pyRes.area
                            });
                            document.getElementById('statusText').innerText = "✅ Procesado con éxito en la Nube.";
                            document.getElementById('statusText').style.color = "#6ee7b7";
                        };
                        resImg.src = pyRes.img_base64;
                    }
                }
            }
            Streamlit.setFrameHeight(window.innerHeight);
        }

        Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
        Streamlit.setComponentReady();

        function recalculateMeasurement(m, currScale) {
            if (!currScale) return;
            if (m.type === 'straight') { let dist = Math.hypot(m.points[1].x - m.points[0].x, m.points[1].y - m.points[0].y); m.valM = (dist / currScale).toFixed(2); m.cx = (m.points[0].x + m.points[1].x)/2; m.cy = (m.points[0].y + m.points[1].y)/2; } 
            else if (m.type === 'area') { let per = 0, ar = 0, n = m.points.length, cX = 0, cY = 0; for(let i=0; i<n; i++) { let p1 = m.points[i], p2 = m.points[(i+1)%n]; per += Math.hypot(p2.x - p1.x, p2.y - p1.y); ar += (p1.x * p2.y - p2.x * p1.y); cX += p1.x; cY += p1.y; } m.valM = (per / currScale).toFixed(2); m.valM2 = (Math.abs(ar)/2/(currScale*currScale)).toFixed(2); m.cx = cX / n; m.cy = cY / n; }
        }

        function addMeasurement(data) {
            if (!measurementsByPage[pageNum]) measurementsByPage[pageNum] = []; data.id = Date.now().toString() + Math.floor(Math.random()*1000); data.lblOffset = { x: 0, y: -30 }; data.color = getDefaultColor(data.type);
            let namePrefix = "Medida"; if (data.type === 'area' || data.type === 'autoArea') namePrefix = `Área ${counters.area++}`; else namePrefix = `Línea ${counters.line++}`;
            data.name = data.name || namePrefix; measurementsByPage[pageNum].push(data); editingMeasureId = data.id; if(mode !== 'select') setMode('select'); else { updateSidebar(); redraw(); }
        }
        function deleteMeasurement(id) { if (measurementsByPage[pageNum]) { measurementsByPage[pageNum] = measurementsByPage[pageNum].filter(m => m.id !== id); if(editingMeasureId === id) editingMeasureId = null; updateSidebar(); redraw(); } }
        window.updateMeasurementName = function(id, newName) { const m = measurementsByPage[pageNum].find(x => x.id === id); if (m) { m.name = newName || "Sin Nombre"; redraw(); } }
        window.updateMeasurementColor = function(id, newColor) { const m = measurementsByPage[pageNum].find(x => x.id === id); if (m) { m.color = newColor; updateSidebar(); redraw(); } }
        window.highlightMeasurement = function(id) { highlightedMeasureId = id; redraw(); }
        window.clearHighlight = function() { highlightedMeasureId = null; redraw(); }

        function updateSidebar() {
            measurementListEl.innerHTML = ''; const list = measurementsByPage[pageNum] || []; if (list.length === 0) { measurementListEl.innerHTML = '<div class="empty-state">Aún no has medido nada.</div>'; return; }
            list.forEach(m => {
                const item = document.createElement('div'); item.className = `measure-item type-${m.type.toLowerCase()} ${m.id === editingMeasureId ? 'selected' : ''}`; item.style.borderLeftColor = m.color;
                item.onmouseenter = () => { item.classList.add('highlighted'); highlightMeasurement(m.id); }; item.onmouseleave = () => { item.classList.remove('highlighted'); clearHighlight(); };
                item.onclick = (ev) => { if(ev.target.tagName !== 'INPUT' && ev.target.tagName !== 'BUTTON') { editingMeasureId = m.id; if(mode !== 'select') setMode('select'); else { updateSidebar(); redraw(); } } };
                let valStr = ""; if (['straight', 'autoLine'].includes(m.type)) { valStr = `<span>${m.valM}</span>&nbsp;m`; } else { valStr = `<span>${m.valM2}</span>&nbsp;m²`; }
                item.innerHTML = ` <input type="color" class="color-picker" value="${m.color}" onchange="updateMeasurementColor('${m.id}', this.value)" title="Color"> <input type="text" class="measure-name" value="${m.name}" onchange="updateMeasurementName('${m.id}', this.value)" onkeyup="if(event.key === 'Enter') this.blur();"> <div class="measure-values">${valStr}</div> <button class="btn-delete" onclick="deleteMeasurement('${m.id}')" title="Borrar">✖</button> `;
                measurementListEl.appendChild(item);
            });
        }

        function getLabelAtPos(x, y) { const list = measurementsByPage[pageNum] || []; for (let i = list.length - 1; i >= 0; i--) { const m = list[i]; if (!m.lblOffset) continue; const rx = m.cx + m.lblOffset.x, ry = m.cy + m.lblOffset.y; const boxHeight = 18; if (x >= rx - 50 && x <= rx + 50 && y >= ry - 14 && y <= ry - 14 + boxHeight) return m; } return null; }
        function getPointAtPos(m, x, y) { if (!m.points) return -1; for (let i = 0; i < m.points.length; i++) { if (Math.hypot(x - m.points[i].x, y - m.points[i].y) < 15) return i; } return -1; }

        canvas.addEventListener('contextmenu', (e) => { e.preventDefault(); if (mode === 'area' && currentPath.length > 0) { if (measureStep >= 1) { finishPolyArea(); } } else { isDrawing = false; measureStep = 0; currentPath = []; tempPoint = null; redraw(); } });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') { isDrawing = false; measureStep = 0; currentPath = []; tempPoint = null; redraw(); } });

        canvas.addEventListener('mousemove', (e) => {
            const {x, y} = getMousePos(e);
            if (['calibrate', 'distance', 'area', 'autoLine', 'autoArea'].includes(mode) || draggingPointIndex !== -1) { updateLoupe(e, x, y); } else { loupeCanvas.style.display = 'none'; }
            if (mode === 'select') {
                if (draggingPointIndex !== -1 && editingMeasureId) { const m = measurementsByPage[pageNum].find(val => val.id === editingMeasureId); if (m) { m.points[draggingPointIndex] = {x, y}; recalculateMeasurement(m, scaleByPage[pageNum]); updateSidebar(); redraw(); } }
                else if (draggingLabel) { draggingLabel.lblOffset.x = x - draggingLabel.cx - dragOffsetX; draggingLabel.lblOffset.y = y - draggingLabel.cy - dragOffsetY; redraw(); }
                else if (isPanning) { canvasContainer.scrollLeft = panScrollLeft - (e.clientX - panStartX); canvasContainer.scrollTop = panScrollTop - (e.clientY - panStartY); }
                else { if (getLabelAtPos(x, y)) canvas.style.cursor = 'move'; else canvas.style.cursor = 'default'; } return;
            }
            if (mode === 'pan' && isPanning) { canvasContainer.scrollLeft = panScrollLeft - (e.clientX - panStartX); canvasContainer.scrollTop = panScrollTop - (e.clientY - panStartY); return; }
            if (isDrawing && ['calibrate', 'distance', 'area'].includes(mode)) { tempPoint = {x, y}; redraw(); }
            if (!isDrawing && !isPanning && !draggingLabel) { canvas.style.cursor = 'crosshair'; }
        });

        canvas.addEventListener('mousedown', (e) => {
            if (mode === 'none' || canvas.width === 0) return; const {x, y} = getMousePos(e);
            if (mode === 'select') {
                if (editingMeasureId) { const m = (measurementsByPage[pageNum] || []).find(val => val.id === editingMeasureId); if (m && m.type !== 'autoArea' && m.type !== 'autoLine') { const ptIdx = getPointAtPos(m, x, y); if (ptIdx !== -1) { draggingPointIndex = ptIdx; canvas.style.cursor = 'grabbing'; return; } } }
                const clickedLabel = getLabelAtPos(x, y); if (clickedLabel) { editingMeasureId = clickedLabel.id; updateSidebar(); draggingLabel = clickedLabel; dragOffsetX = x - (clickedLabel.cx + clickedLabel.lblOffset.x); dragOffsetY = y - (clickedLabel.cy + clickedLabel.lblOffset.y); canvas.style.cursor = 'move'; redraw(); return; }
                editingMeasureId = null; updateSidebar(); redraw(); isPanning = true; panStartX = e.clientX; panStartY = e.clientY; panScrollLeft = canvasContainer.scrollLeft; panScrollTop = canvasContainer.scrollTop; canvas.style.cursor = 'grabbing'; return;
            }
            if (e.button === 2) return; 

            if (['autoLine', 'autoArea'].includes(mode)) { triggerCloudProcessing(x, y, mode); return; }

            if (['calibrate', 'distance', 'area'].includes(mode)) {
                if (measureStep === 0) { startX = x; startY = y; currentPath = [{x, y}]; isDrawing = true; measureStep = 1; }
                else if (measureStep === 1) {
                    if (['calibrate', 'distance'].includes(mode)) { endX = x; endY = y; currentPath.push({x, y}); finishLineTool(); } 
                    else if (mode === 'area') { const lastP = currentPath[currentPath.length - 1]; if (Math.hypot(x - lastP.x, y - lastP.y) > 5) currentPath.push({x, y}); }
                }
            }
        });

        canvas.addEventListener('mouseup', (e) => {
            if (draggingPointIndex !== -1) { draggingPointIndex = -1; canvas.style.cursor = 'default'; redraw(); return; }
            if (draggingLabel) { draggingLabel = null; return; }
            if (isPanning) { isPanning = false; canvas.style.cursor = (mode === 'select') ? 'default' : 'grab'; return; }
        });

        function finishLineTool() {
            isDrawing = false; measureStep = 0; const dist = Math.hypot(endX - startX, endY - startY); if (dist < 5) { currentPath = []; redraw(); return; }
            if (mode === 'calibrate') {
                cPrompt("¿Cuántos metros reales tiene esta línea?", (r) => {
                    if (r) { r = parseFloat(r.replace(',', '.')); if (!isNaN(r) && r > 0) { scaleByPage[pageNum] = dist / r; lastKnownScale = scaleByPage[pageNum]; document.getElementById('scaleInfo').innerText = `ESC. PÁG. ${pageNum} (1m = ${Math.round(scaleByPage[pageNum])}px)`; document.getElementById('scaleInfo').className = "scale-badge calibrated"; cAlert(`¡Escala guardada!`); setMode('distance'); } else { cAlert("Valor no válido."); } }
                    currentPath = []; redraw();
                });
            } else if (mode === 'distance') { addMeasurement({ type: 'straight', cx: (startX+endX)/2, cy: (startY+endY)/2, points: [...currentPath], valM: (dist/scaleByPage[pageNum]).toFixed(2), valM2: null }); currentPath = []; redraw(); } 
        }

        function finishPolyArea() {
            if (currentPath.length < 2) { currentPath = []; tempPoint = null; redraw(); return; }
            isDrawing = false; measureStep = 0; const currScale = scaleByPage[pageNum];
            if (mode === 'area') { if (currentPath.length < 3) return; let per = 0, ar = 0, n = currentPath.length, cX = 0, cY = 0; for (let i = 0; i < n; i++) { const p1 = currentPath[i], p2 = currentPath[(i+1)%n]; per += Math.hypot(p2.x-p1.x, p2.y-p1.y); ar += (p1.x*p2.y - p2.x*p1.y); cX += p1.x; cY += p1.y; } addMeasurement({ type: 'area', cx: cX/n, cy: cY/n, points: [...currentPath], valM: (per/currScale).toFixed(2), valM2: (Math.abs(ar)/2/(currScale*currScale)).toFixed(2) }); } 
            currentPath = []; tempPoint = null; redraw();
        }

        function drawLine(x1, y1, x2, y2, color, isHigh) { ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.strokeStyle = isHigh ? '#ffffff' : color; ctx.lineWidth = isHigh ? 5 : 3; if(isHigh) { ctx.shadowColor = color; ctx.shadowBlur = 8; } ctx.stroke(); ctx.shadowBlur = 0; ctx.fillStyle = isHigh ? '#ffffff' : color; ctx.beginPath(); ctx.arc(x1, y1, isHigh? 4 : 2.5, 0, Math.PI*2); ctx.fill(); ctx.beginPath(); ctx.arc(x2, y2, isHigh? 4 : 2.5, 0, Math.PI*2); ctx.fill(); }
        function drawPathData(pts, color, isClosed, isHigh) { ctx.beginPath(); ctx.moveTo(pts[0].x, pts[0].y); for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i].x, pts[i].y); if (isClosed) { ctx.closePath(); ctx.fillStyle = hexToRgba(color, isHigh ? 0.3 : 0.15); ctx.fill(); } ctx.strokeStyle = isHigh ? '#ffffff' : color; ctx.lineWidth = isHigh ? 5 : 3; if(isHigh) { ctx.shadowColor = color; ctx.shadowBlur = 8; } ctx.stroke(); ctx.shadowBlur = 0; ctx.fillStyle = isHigh ? '#ffffff' : color; pts.forEach(p => { ctx.beginPath(); ctx.arc(p.x, p.y, isHigh? 4 : 2.5, 0, Math.PI*2); ctx.fill(); }); }
        function renderLabel(x, y, text, color, isHigh) { const lines = text.split('\n'); ctx.fillStyle = isHigh ? "#ffffff" : "rgba(255, 255, 255, 0.95)"; ctx.shadowColor = isHigh ? color : "rgba(0,0,0,0.15)"; ctx.shadowBlur = isHigh ? 12 : 6; ctx.shadowOffsetY = isHigh ? 0 : 3; ctx.beginPath(); ctx.roundRect(x - 50, y - 14, 100, lines.length > 1 ? 32 : 18, 4); ctx.fill(); ctx.shadowBlur = 0; ctx.shadowOffsetY = 0; ctx.fillStyle = "#0f172a"; ctx.font = "bold 10px Inter, sans-serif"; ctx.textAlign = "center"; lines.forEach((l, i) => { if(i>0) {ctx.fillStyle = color; ctx.font = "bold 10px Inter, sans-serif";} ctx.fillText(l, x, y + 0 + (i*13)); }); }
        
        function redraw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height); if (img.src) ctx.drawImage(img, 0, 0);
            const list = measurementsByPage[pageNum] || []; const sortedList = [...list.filter(m => m.id !== highlightedMeasureId), ...list.filter(m => m.id === highlightedMeasureId)];
            
            sortedList.forEach(m => {
                const isHigh = (m.id === highlightedMeasureId); const col = m.color;
                if (m.type === 'autoArea' || m.type === 'autoLine') { const tCanv = document.createElement('canvas'); tCanv.width = canvas.width; tCanv.height = canvas.height; const tc = tCanv.getContext('2d'); tc.drawImage(m.img, 0, 0); tc.globalCompositeOperation = 'source-in'; tc.fillStyle = col; tc.fillRect(0, 0, canvas.width, canvas.height); if (isHigh) { ctx.shadowColor = col; ctx.shadowBlur = 12; } ctx.drawImage(tCanv, 0, 0); ctx.shadowBlur = 0; }
                else if (m.type === 'straight') drawLine(m.points[0].x, m.points[0].y, m.points[1].x, m.points[1].y, col, isHigh);
                else if (m.type === 'area') drawPathData(m.points, col, true, isHigh);
            });
            if (isDrawing && currentPath.length > 0) {
                if (['calibrate', 'distance'].includes(mode) && tempPoint) { drawLine(currentPath[0].x, currentPath[0].y, tempPoint.x, tempPoint.y, mode==='calibrate'?'#ef4444':'#0ea5e9', false); }
                else if (mode === 'area') { ctx.beginPath(); ctx.moveTo(currentPath[0].x, currentPath[0].y); for (let i = 1; i < currentPath.length; i++) ctx.lineTo(currentPath[i].x, currentPath[i].y); if (tempPoint) ctx.lineTo(tempPoint.x, tempPoint.y); if (mode === 'area' && currentPath.length > 2 && tempPoint == null) ctx.closePath(); const dC = '#10b981'; ctx.strokeStyle = dC; ctx.lineWidth = 2; ctx.setLineDash([6, 6]); ctx.stroke(); ctx.setLineDash([]); ctx.fillStyle = dC; currentPath.forEach(p => { ctx.beginPath(); ctx.arc(p.x, p.y, 2.5, 0, Math.PI*2); ctx.fill(); }); }
            }
            sortedList.forEach(m => {
                const isHigh = (m.id === highlightedMeasureId);
                if (m.cx === undefined) { if (m.type === 'straight') { m.cx = (m.points[0].x + m.points[1].x)/2; m.cy = (m.points[0].y + m.points[1].y)/2; } else if (m.type === 'area') { let cx=0,cy=0; m.points.forEach(p=>{cx+=p.x;cy+=p.y;}); m.cx=cx/m.points.length; m.cy=cy/m.points.length; } }
                if (!m.lblOffset) m.lblOffset = { x: 0, y: -30 }; let rx = m.cx + m.lblOffset.x, ry = m.cy + m.lblOffset.y;
                let lbl = m.name + '\n'; lbl += (m.type === 'area' || m.type === 'autoArea') ? `${m.valM2} m²` : `${m.valM} m`;
                if (Math.hypot(m.lblOffset.x, m.lblOffset.y) > 25) { ctx.beginPath(); ctx.moveTo(m.cx, m.cy); ctx.lineTo(rx, ry); ctx.strokeStyle = isHigh ? m.color : "rgba(15, 23, 42, 0.4)"; ctx.setLineDash([4,4]); ctx.lineWidth = isHigh ? 2 : 1; ctx.stroke(); ctx.setLineDash([]); }
                renderLabel(rx, ry, lbl, m.color, isHigh);
            });
            if (editingMeasureId) { const m = list.find(val => val.id === editingMeasureId); if (m && m.points && m.type !== 'autoArea' && m.type !== 'autoLine') { ctx.fillStyle = '#ffffff'; ctx.lineWidth = 2; ctx.strokeStyle = '#0ea5e9'; m.points.forEach(p => { ctx.beginPath(); ctx.arc(p.x, p.y, 6, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); }); } }
        }
    </script>
</body>
</html>
"""

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(HTML_FRONTEND)

# =========================================================================
# 2. MOTOR INTELIGENTE DE OPENCV EN LA NUBE
# =========================================================================
def procesar_nube(img_b64, x, y, modo, scale, ts):
    try:
        img_data = base64.b64decode(img_b64.split(",")[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        color_obj = img[int(y), int(x)]
        tol = 40
        lower = np.clip(color_obj - tol, 0, 255)
        upper = np.clip(color_obj + tol, 0, 255)
        mask = cv2.inRange(img, lower, upper)

        if modo == "autoArea":
            # Matriz enorme de 35x35 que sella los sombreados (hatching) de CAD
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (35, 35))
            mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            contornos, _ = cv2.findContours(mask_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contornos: return {"ts": ts, "error": "No se detectó ningún sombreado."}
            
            cnt = max(contornos, key=cv2.contourArea)
            epsilon = 0.002 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            
            area_px = cv2.contourArea(approx)
            per_px = cv2.arcLength(approx, True)
            
            overlay = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.uint8)
            cv2.drawContours(overlay, [approx], -1, (129, 185, 16, 150), -1) 
            _, buffer = cv2.imencode('.png', overlay)
            res_b64 = "data:image/png;base64," + base64.b64encode(buffer).decode('utf-8')
            
            M = cv2.moments(approx)
            cx = int(M['m10']/M['m00']) if M['m00']!=0 else int(x)
            cy = int(M['m01']/M['m00']) if M['m00']!=0 else int(y)
            puntos = [{"x": float(p[0][0]), "y": float(p[0][1])} for p in approx]
            
            return {
                "ts": ts, "tipo": "autoArea", "img_base64": res_b64, "cx": cx, "cy": cy,
                "puntos": puntos, "area": f"{(area_px / (scale*scale)):.2f}", "perimetro": f"{(per_px / scale):.2f}"
            }
            
        else: # autoLine
            contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contornos: return {"ts": ts, "error": "No se detectó ninguna línea."}
            
            cnt = max(contornos, key=cv2.contourArea)
            per_px = cv2.arcLength(cnt, True) / 2
            
            overlay = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.uint8)
            cv2.drawContours(overlay, [cnt], -1, (247, 85, 168, 255), 3) 
            _, buffer = cv2.imencode('.png', overlay)
            res_b64 = "data:image/png;base64," + base64.b64encode(buffer).decode('utf-8')
            
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00']) if M['m00']!=0 else int(x)
            cy = int(M['m01']/M['m00']) if M['m00']!=0 else int(y)
            
            return {
                "ts": ts, "tipo": "autoLine", "img_base64": res_b64, "cx": cx, "cy": cy,
                "puntos": [], "area": None, "perimetro": f"{(per_px / scale):.2f}"
            }
            
    except Exception as e:
        return {"ts": ts, "error": f"Error del motor: {str(e)}"}

# =========================================================================
# 3. COMUNICADOR STREAMLIT ↔ FRONTEND
# =========================================================================
if 'ultimo_ts' not in st.session_state:
    st.session_state.ultimo_ts = None
if 'resultado_backend' not in st.session_state:
    st.session_state.resultado_backend = None

mideplanos_component = components.declare_component("mideplanos", path="frontend")

# Mandamos datos al frontend
datos_desde_js = mideplanos_component(comando_desde_python=st.session_state.resultado_backend)

# Recibimos datos del frontend
if datos_desde_js and "ts" in datos_desde_js:
    if datos_desde_js["ts"] != st.session_state.ultimo_ts:
        st.session_state.ultimo_ts = datos_desde_js["ts"]
        
        # Procesamos con Python
        res = procesar_nube(
            datos_desde_js["image"], 
            datos_desde_js["x"], 
            datos_desde_js["y"], 
            datos_desde_js["action"], 
            datos_desde_js["scale"],
            datos_desde_js["ts"]
        )
        st.session_state.resultado_backend = res
        st.rerun()
