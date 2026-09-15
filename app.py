import streamlit as st
import streamlit.components.v1 as components

# Configuración obligatoria a pantalla completa
st.set_page_config(page_title="MidePlanos PRO", layout="wide", initial_sidebar_state="collapsed")

# Todo el HTML unificado con el parche de seguridad para Streamlit Cloud
codigo_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MidePlanos PRO</title>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js"></script>
    <script async src="https://docs.opencv.org/4.8.0/opencv.js" onload="onOpenCvReady()" type="text/javascript"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --primary: #0ea5e9; --primary-hover: #0284c7; --primary-glow: rgba(14, 165, 233, 0.3);
            --success: #10b981; --warning: #f59e0b; --danger: #ef4444; --magic: #a855f7;
            --circle: #ec4899; --curve: #14b8a6; --cad: #64748b;
            --bg-body: #0f172a; --bg-panel: rgba(30, 41, 59, 0.96); --border: #334155;
            --text-main: #f8fafc; --text-muted: #94a3b8;
        }
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #475569; border-radius: 10px; }
        body { font-family: 'Inter', sans-serif; background-color: var(--bg-body); margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; color: var(--text-main); }
        .header { background: var(--bg-panel); backdrop-filter: blur(12px); padding: 6px 16px; border-bottom: 1px solid var(--border); z-index: 100; display: flex; flex-direction: column; gap: 6px; }
        .toolbar-row { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; }
        .toolbar-group { display: flex; gap: 8px; align-items: center; }
        .toolbar-group.tools-top { border-left: 1px solid var(--border); border-right: 1px solid var(--border); padding: 0 12px; }
        button { border: none; cursor: pointer; font-family: inherit; outline: none; }
        button:not(.tool-btn) { padding: 6px 10px; border: 1px solid var(--border); border-radius: 6px; font-weight: 600; font-size: 11px; transition: 0.2s; background: #1e293b; color: var(--text-main); }
        button:not(.tool-btn):hover { background: #334155; border-color: #475569; }
        .btn-action { background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%) !important; color: white !important; border-color: #1d4ed8 !important; }
        .tool-trigger.active { background: #0ea5e9; color: white; border-color: #0ea5e9; box-shadow: 0 0 0 2px var(--primary-glow); }
        .tool-trigger.btn-success.active { background: var(--success); color: white; border-color: var(--success); }
        .tool-trigger.btn-magic { background: rgba(168, 85, 247, 0.1); color: #d8b4fe; border-color: rgba(168, 85, 247, 0.4); }
        .tool-trigger.btn-magic.active { background: var(--magic); color: white; border-color: var(--magic); }
        input[type="file"] { display: none; }
        .file-label { padding: 6px 10px; background: linear-gradient(180deg, #334155 0%, #1e293b 100%); color: white; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 11px; display: inline-block; border: 1px solid #475569; }
        .file-label:hover { background: #334155; }
        .controls-bar { display: flex; justify-content: space-between; align-items: center; background: rgba(15, 23, 42, 0.4); padding: 4px 12px; border-radius: 6px; border: 1px solid var(--border); }
        .controls-left { display: flex; gap: 16px; align-items: center; }
        .pdf-controls { display: none; align-items: center; gap: 6px; border-right: 1px solid var(--border); padding-right: 12px; }
        .page-input { width: 35px; text-align: center; font-size: 12px; font-weight: 600; background: #0f172a; color: white; border: 1px solid var(--border); border-radius: 4px; padding: 4px; }
        .zoom-controls { display: flex; align-items: center; gap: 6px; }
        .zoom-controls span { font-weight: 600; color: var(--text-muted); font-size: 11px; text-transform: uppercase; }
        .zoom-btn { padding: 2px 8px !important; border-radius: 4px !important; font-size: 13px !important;}
        .status-text { font-size: 12px; font-weight: 500; color: #fcd34d; background: rgba(245, 158, 11, 0.1); padding: 4px 10px; border-radius: 4px; border: 1px solid rgba(245, 158, 11, 0.2); }
        .scale-badge { font-size: 11px; font-weight: 700; color: #fca5a5; padding: 4px 8px; border-radius: 4px; background: rgba(239, 68, 68, 0.1); border: 1px dashed #ef4444; transition: 0.3s;}
        .scale-badge.calibrated { color: #6ee7b7; border-color: #10b981; background: rgba(16, 185, 129, 0.1); border-style: solid; }
        .left-toolbar { width: 54px; background: var(--bg-panel); border-right: 1px solid var(--border); display: flex; flex-direction: column; align-items: center; padding: 10px 0; gap: 6px; z-index: 50; overflow: visible; }
        .tool-btn { width: 36px; height: 36px; flex-shrink: 0; border-radius: 8px; background: #1e293b; border: 1px solid var(--border); color: var(--text-main); display: flex; align-items: center; justify-content: center; font-size: 15px; transition: 0.2s; position: relative; padding: 0;}
        .tool-btn:hover { background: #334155; border-color: #475569;}
        .tool-btn::after { content: attr(data-tooltip); position: absolute; left: 100%; top: 50%; transform: translateY(-50%) translateX(5px); margin-left: 8px; background: #0f172a; color: #fff; padding: 6px 12px; border-radius: 6px; font-size: 11px; font-weight: 600; white-space: nowrap; opacity: 0; visibility: hidden; transition: 0.2s; pointer-events: none; border: 1px solid var(--border); z-index: 9999; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        .tool-btn::before { content: ""; position: absolute; left: 100%; top: 50%; transform: translateY(-50%) translateX(5px); margin-left: 2px; border-width: 5px; border-style: solid; border-color: transparent #0f172a transparent transparent; opacity: 0; visibility: hidden; transition: 0.2s; z-index: 9999; pointer-events: none; }
        .tool-btn:hover::after, .tool-btn:hover::before { opacity: 1; visibility: visible; transform: translateY(-50%) translateX(0); }
        .main-container { display: flex; flex: 1; overflow: hidden; }
        .workspace { flex: 1; display: flex; flex-direction: column; padding: 20px; overflow: hidden; background-color: var(--bg-body); background-image: radial-gradient(#334155 1.5px, transparent 1.5px); background-size: 24px 24px; z-index: 1;}
        .canvas-container { flex: 1; overflow: auto; background: white; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.4); position: relative; border: 1px solid #000; }
        canvas { display: block; transform-origin: top left; transition: width 0.1s, height 0.1s; }
        #loupeCanvas { position: fixed; pointer-events: none; border-radius: 50%; border: 2px solid #0ea5e9; box-shadow: 0 5px 15px rgba(0,0,0,0.6); display: none; z-index: 9999; background: white; }
        .resizer { width: 5px; background: var(--bg-body); cursor: ew-resize; transition: 0.2s; z-index: 20; border-left: 1px solid var(--border); }
        .resizer:hover, .resizer.resizing { background: #0ea5e9; }
        .sidebar { width: 340px; background: var(--bg-panel); display: flex; flex-direction: column; z-index: 5; }
        .sidebar-header { padding: 12px 16px; border-bottom: 1px solid var(--border); background: rgba(15, 23, 42, 0.4); }
        .sidebar-header h3 { margin: 0; font-size: 13px; font-weight: 700; display: flex; justify-content: space-between; }
        .measurement-list { flex: 1; overflow-y: auto; padding: 12px; display: flex; flex-direction: column; gap: 8px; }
        .empty-state { text-align: center; color: var(--text-muted); font-size: 12px; margin-top: 20px; }
        .measure-item { border: 1px solid var(--border); border-radius: 6px; padding: 6px 8px; background: #1e293b; display: flex; flex-direction: row; align-items: center; justify-content: space-between; gap: 8px; border-left: 4px solid var(--primary); transition: 0.2s; cursor: pointer; }
        .measure-item:hover { background: #334155; border-color: #64748b; transform: translateX(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
        .measure-item.selected { background: #1e293b; border-color: #0ea5e9; box-shadow: inset 0 0 0 1px #0ea5e9; }
        .color-picker { -webkit-appearance: none; border: none; width: 16px; height: 16px; border-radius: 4px; cursor: pointer; padding: 0; background: transparent; flex-shrink: 0;}
        .color-picker::-webkit-color-swatch-wrapper { padding: 0; }
        .color-picker::-webkit-color-swatch { border: 1px solid #475569; border-radius: 4px; }
        .measure-name { font-family: inherit; font-size: 11px; font-weight: 600; border: 1px solid transparent; padding: 2px 4px; border-radius: 4px; flex-grow: 1; min-width: 40px; background: transparent; color: white; cursor: text; }
        .measure-name:focus { border-color: #0ea5e9; background: #0f172a; outline: none; }
        .measure-values { font-size: 11px; color: var(--text-muted); display: flex; flex-direction: row; align-items: center; gap: 4px; white-space: nowrap; flex-shrink: 0; cursor: default; }
        .measure-values span { font-weight: 700; color: #e2e8f0; font-size: 11px; }
        .btn-delete { background: #0f172a !important; border: 1px solid var(--border) !important; color: var(--text-muted) !important; padding: 4px 6px !important; border-radius: 4px !important; font-size: 10px; transition: 0.2s; flex-shrink: 0; cursor: pointer;}
        .btn-delete:hover { color: #fca5a5 !important; background: #7f1d1d !important; }
        .sidebar-footer { padding: 16px; border-top: 1px solid var(--border); background: rgba(15, 23, 42, 0.4); }
        .btn-export { width: 100%; background: linear-gradient(180deg, #10b981 0%, #059669 100%) !important; color: white !important; border-color: #059669 !important; padding: 10px !important; font-size: 13px; border-radius: 6px;}

        /* MODAL CUSTOM (Soluciona bloqueos de la nube) */
        #customModal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15,23,42,0.8); z-index: 99999; display: none; justify-content: center; align-items: center; backdrop-filter: blur(4px); }
        .modal-content { background: #1e293b; padding: 24px; border-radius: 12px; border: 1px solid #334155; color: white; width: 320px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .modal-content h3 { margin-top: 0; font-size: 15px; font-weight: 600; color: #f8fafc; }
        .modal-content input { width: 100%; box-sizing: border-box; padding: 10px; margin: 15px 0; background: #0f172a; border: 1px solid #0ea5e9; color: white; border-radius: 6px; outline: none; display: none; font-size: 14px; text-align: center; }
        .modal-buttons { display: flex; justify-content: center; gap: 12px; margin-top: 20px; }
        .modal-buttons button { padding: 8px 16px; border-radius: 6px; border: none; cursor: pointer; font-weight: 600; transition: 0.2s; }
        .modal-cancel { background: #334155; color: #f8fafc; display: none; }
        .modal-cancel:hover { background: #475569; }
        .modal-ok { background: #0ea5e9; color: white; }
        .modal-ok:hover { background: #0284c7; }
    </style>
</head>
<body>
    <!-- Ventanas Emergentes Personalizadas -->
    <div id="customModal">
        <div class="modal-content">
            <h3 id="modalTitle"></h3>
            <input type="text" id="modalInput" onkeyup="if(event.key === 'Enter') document.getElementById('modalBtnOk').click();" autocomplete="off">
            <div class="modal-buttons">
                <button id="modalBtnCancel" class="modal-cancel">Cancelar</button>
                <button id="modalBtnOk" class="modal-ok">Aceptar</button>
            </div>
        </div>
    </div>

    <canvas id="loupeCanvas" width="120" height="120"></canvas>

    <div class="header">
        <div class="toolbar-row">
            <div class="toolbar-group">
                <label class="file-label">📄 Nuevo <input type="file" id="imageLoader" accept="image/png, image/jpeg, image/webp, application/pdf"/></label>
                <button id="btnSave" class="btn-action">💾 Guardar Proyecto</button>
                <label class="file-label" style="background: linear-gradient(180deg, #475569 0%, #334155 100%); border-color:#475569;">📂 Abrir <input type="file" id="projectLoader" accept=".json"/></label>
                <button id="btnPrint" style="background:#0f172a; color:white; border-color:#334155;">🖨️ Imprimir Todo</button>
                <button data-mode="printArea" class="tool-trigger" style="background:#1e293b; color:white; border-color:#334155; display:flex; align-items:center; gap:6px;">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-dasharray="5 5"><rect x="2" y="2" width="20" height="20" rx="2"/></svg> Área
                </button>
            </div>
            <div class="toolbar-group tools-top">
                <button data-mode="select" class="tool-trigger">↖️ Seleccionar</button>
                <button data-mode="calibrate" class="tool-trigger">📏 Calibrar</button>
                <button data-mode="distance" class="tool-trigger">➖ Recta</button>
                <button data-mode="dimension" class="tool-trigger" style="color:#94a3b8;">|↔| Acotar</button>
                <button data-mode="arc" class="tool-trigger" style="color:var(--curve); border-color:transparent;">⌒ Curva</button>
                <button data-mode="polygonal" class="tool-trigger">〰️ Poligonal</button>
                <button data-mode="area" class="tool-trigger btn-success">⬟ Área</button>
                <button data-mode="circle" class="tool-trigger" style="color:var(--circle); border-color:transparent;">⭕ Círculo</button>
                <button data-mode="autoLine" class="tool-trigger btn-magic">🪄 Auto-Línea</button>
                <button data-mode="autoArea" class="tool-trigger btn-magic">🪄 Auto-Área</button>
            </div>
            <div class="toolbar-group"><button id="btnToggleSidebar" style="background:#334155; color:white; border-color:#475569;">🗂️ Panel</button></div>
        </div>
        <div class="toolbar-row controls-bar">
            <div class="controls-left">
                <div class="pdf-controls" id="pdfControls"><button class="zoom-btn" id="btnPrev">◀</button><span style="font-size: 12px; font-weight: 600;">Pág <input type="number" id="pageInput" class="page-input" value="1" min="1"> de <span id="pageTotal">1</span></span><button class="zoom-btn" id="btnNext">▶</button></div>
                <div class="zoom-controls"><span>🔍 Zoom:</span><button class="zoom-btn" id="btnZoomOut">➖</button><span id="zoomLevel">100%</span><button class="zoom-btn" id="btnZoomIn">➕</button></div>
                <div id="statusText" class="status-text">Cargando IA OpenCV en el navegador...</div>
            </div>
            <div id="scaleInfo" class="scale-badge">ESCALA NO CALIBRADA</div>
        </div>
    </div>

    <div class="main-container">
        <div class="left-toolbar">
            <button data-mode="select" class="tool-btn tool-trigger" data-tooltip="Mover / Seleccionar">↖️</button><hr style="width: 50%; border: 0; border-top: 1px solid var(--border); margin: 0;">
            <button data-mode="calibrate" class="tool-btn tool-trigger" data-tooltip="Calibrar Escala">📏</button>
            <button data-mode="distance" class="tool-btn tool-trigger" data-tooltip="Línea Recta">➖</button>
            <button data-mode="dimension" class="tool-btn tool-trigger" data-tooltip="Acotación CAD" style="color:#94a3b8; font-size:13px; font-weight:bold; letter-spacing:-1px;">|↔|</button>
            <button data-mode="arc" class="tool-btn tool-trigger" data-tooltip="Arco / Curva" style="color:var(--curve);">⌒</button>
            <button data-mode="polygonal" class="tool-btn tool-trigger" data-tooltip="Línea Poligonal">〰️</button>
            <button data-mode="area" class="tool-btn btn-success tool-trigger" data-tooltip="Área Manual">⬟</button>
            <button data-mode="circle" class="tool-btn tool-trigger" data-tooltip="Círculo" style="color:var(--circle);">⭕</button><hr style="width: 50%; border: 0; border-top: 1px solid var(--border); margin: 0;">
            <button data-mode="printArea" class="tool-btn tool-trigger" data-tooltip="Imprimir Área" style="color:var(--text-main);"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-dasharray="5 5"><rect x="2" y="2" width="20" height="20" rx="2"/></svg></button><hr style="width: 50%; border: 0; border-top: 1px solid var(--border); margin: 0;">
            <button data-mode="autoLine" class="tool-btn btn-magic tool-trigger" data-tooltip="Auto-Línea">✨</button>
            <button data-mode="autoArea" class="tool-btn btn-magic tool-trigger" data-tooltip="Auto-Área">🔮</button>
        </div>
        <div class="workspace"><div class="canvas-container" id="canvasContainer"><canvas id="planCanvas"></canvas></div></div>
        <div class="resizer" id="sidebarResizer"></div>
        <div class="sidebar" id="rightSidebar">
            <div class="sidebar-header"><h3>Mediciones <span id="sbPageTitle" style="color:var(--text-muted); font-size:11px;"></span></h3></div>
            <div class="measurement-list" id="measurementList"><div class="empty-state">No hay medidas en esta página.</div></div>
            <div class="sidebar-footer"><button id="btnExport" class="btn-export">Descargar (.CSV)</button></div>
        </div>
    </div>

    <script>
        // SOLUCIÓN AL BLOQUEO DE SEGURIDAD (CORS) EN STREAMLIT CLOUD
        try {
            const pdfWorkerUrl = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';
            const blob = new Blob([`importScripts('${pdfWorkerUrl}');`], { type: 'text/javascript' });
            pdfjsLib.GlobalWorkerOptions.workerSrc = URL.createObjectURL(blob);
        } catch (e) {
            console.warn("Usando motor PDF en modo seguro.");
        }

        let cvReady = false;
        function onOpenCvReady() {
            cvReady = true;
            document.getElementById('statusText').innerText = "✅ IA OpenCV cargada. Sube un plano.";
            document.getElementById('statusText').style.color = '#6ee7b7';
            document.getElementById('statusText').style.backgroundColor = 'rgba(16, 185, 129, 0.1)';
            document.getElementById('statusText').style.borderColor = 'rgba(16, 185, 129, 0.2)';
        }

        function cAlert(msg, callback) {
            const m = document.getElementById('customModal'); m.style.display = 'flex';
            document.getElementById('modalTitle').innerText = msg;
            document.getElementById('modalInput').style.display = 'none';
            document.getElementById('modalBtnCancel').style.display = 'none';
            document.getElementById('modalBtnOk').onclick = () => { m.style.display = 'none'; if(callback) callback(); };
        }
        function cPrompt(msg, callback) {
            const m = document.getElementById('customModal'); m.style.display = 'flex';
            document.getElementById('modalTitle').innerText = msg;
            const inp = document.getElementById('modalInput'); inp.style.display = 'block'; inp.value = ''; 
            setTimeout(() => inp.focus(), 50);
            document.getElementById('modalBtnCancel').style.display = 'block';
            document.getElementById('modalBtnCancel').onclick = () => { m.style.display = 'none'; callback(null); };
            document.getElementById('modalBtnOk').onclick = () => { m.style.display = 'none'; callback(inp.value); };
        }

        const canvas = document.getElementById('planCanvas');
        const ctx = canvas.getContext('2d', { willReadFrequently: true });
        const canvasContainer = document.getElementById('canvasContainer');
        const imageLoader = document.getElementById('imageLoader');
        const measurementListEl = document.getElementById('measurementList');
        const pageInput = document.getElementById('pageInput');
        const loupeCanvas = document.getElementById('loupeCanvas');
        const loupeCtx = loupeCanvas.getContext('2d');
        const resizer = document.getElementById('sidebarResizer'); 
        const rightSidebar = document.getElementById('rightSidebar');
        
        let img = new Image(); let mode = 'none'; let currentZoom = 1; let measurementsByPage = {}; let counters = { line: 1, area: 1, circle: 1, arc: 1, dimension: 1 };
        let scaleByPage = {}; let currentFileDataURL = null; let currentFileType = null; let currentFileName = null; let pdfDoc = null; let pageNum = 1; 
        let isDrawing = false; let startX, startY, endX, endY; let currentPath = []; let tempPoint = null; let measureStep = 0; 
        let isPanning = false; let panStartX, panStartY, panScrollLeft, panScrollTop; let draggingLabel = null; let dragOffsetX = 0, dragOffsetY = 0;
        let editingMeasureId = null; let draggingPointIndex = -1; let highlightedMeasureId = null; let isResizing = false;

        function getDefaultColor(type) {
            if (type === 'straight') return '#0ea5e9'; if (type === 'dimension') return '#3b82f6'; if (type === 'polygonal') return '#f59e0b';
            if (type === 'area' || type === 'autoArea') return '#10b981'; if (type === 'circle') return '#ec4899'; if (type === 'arc') return '#14b8a6'; if (type === 'autoLine') return '#a855f7'; return '#ffffff';
        }
        function hexToRgba(hex, alpha) {
            if(!hex) return `rgba(255,255,255,${alpha})`; hex = hex.replace('#', ''); if(hex.length === 3) hex = hex.split('').map(x => x + x).join('');
            let r = parseInt(hex.substring(0,2), 16), g = parseInt(hex.substring(2,4), 16), b = parseInt(hex.substring(4,6), 16); return `rgba(${r}, ${g}, ${b}, ${alpha})`;
        }
        function getMousePos(e) { const rect = canvas.getBoundingClientRect(); return { x: (e.clientX - rect.left) * (canvas.width / rect.width), y: (e.clientY - rect.top) * (canvas.height / rect.height) }; }

        function getArcThrough3Points(p1, p2, p3) {
            let temp = p2.x*p2.x + p2.y*p2.y; let bc = (p1.x*p1.x + p1.y*p1.y - temp) / 2; let cd = (temp - p3.x*p3.x - p3.y*p3.y) / 2;
            let det = (p1.x - p2.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p2.y); if (Math.abs(det) < 1e-5) return null; 
            let cx = (bc * (p2.y - p3.y) - cd * (p1.y - p2.y)) / det; let cy = ((p1.x - p2.x) * cd - (p2.x - p3.x) * bc) / det; let r = Math.hypot(cx - p1.x, cy - p1.y);
            let startAngle = Math.atan2(p1.y - cy, p1.x - cx); let endAngle = Math.atan2(p3.y - cy, p3.x - cx);
            let cross = (p2.x - p1.x) * (p3.y - p2.y) - (p2.y - p1.y) * (p3.x - p2.x); let anticlockwise = cross < 0; 
            let sweepAngle = endAngle - startAngle; if (anticlockwise && sweepAngle > 0) sweepAngle -= 2 * Math.PI; if (!anticlockwise && sweepAngle < 0) sweepAngle += 2 * Math.PI;
            return { cx, cy, r, startAngle, endAngle, anticlockwise, length: Math.abs(sweepAngle) * r };
        }
        function getCADOffset(p1, p2, p3) {
            let dx = p2.x - p1.x; let dy = p2.y - p1.y; let len = Math.hypot(dx, dy); if (len === 0) return { d: 0, nx: 0, ny: 0, dx: 0, dy: 0, len: 0 };
            let nx = -dy / len; let ny = dx / len; let d = (p3.x - p1.x) * nx + (p3.y - p1.y) * ny; return { d, nx, ny, dx, dy, len };
        }

        resizer.addEventListener('mousedown', () => { isResizing = true; document.body.style.cursor = 'ew-resize'; resizer.classList.add('resizing'); });
        document.addEventListener('mousemove', (e) => { if (!isResizing) return; const newWidth = document.body.clientWidth - e.clientX; if (newWidth > 200 && newWidth < 600) rightSidebar.style.width = newWidth + 'px'; });
        document.addEventListener('mouseup', () => { if (isResizing) { isResizing = false; document.body.style.cursor = 'default'; resizer.classList.remove('resizing'); } });
        document.getElementById('btnToggleSidebar').onclick = () => { if (rightSidebar.style.display === 'none') { rightSidebar.style.display = 'flex'; resizer.style.display = 'block'; } else { rightSidebar.style.display = 'none'; resizer.style.display = 'none'; } };

        document.getElementById('btnPrint').onclick = () => { if (!img.src) return cAlert("Sube un plano primero."); openPrintWindow(canvas.toDataURL('image/png')); };
        function printSelectedArea(x, y, w, h) { const tCanvas = document.createElement('canvas'); tCanvas.width = w; tCanvas.height = h; const tCtx = tCanvas.getContext('2d'); tCtx.drawImage(canvas, x, y, w, h, 0, 0, w, h); openPrintWindow(tCanvas.toDataURL('image/png')); }
        function openPrintWindow(dataUrl) { const printWindow = window.open('', '_blank'); printWindow.document.write(`<html><head><title>Imprimir</title><style>@page{size:auto;margin:0mm;}body{margin:0;display:flex;justify-content:center;align-items:center;min-height:100vh;background:#fff;}img{max-width:100vw;max-height:100vh;object-fit:contain;}</style></head><body><img src="${dataUrl}" onload="setTimeout(()=>{window.print();window.close();},250);" /></body></html>`); printWindow.document.close(); }

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
                pdfjsLib.getDocument(array).promise.then(function(pdf) { pdfDoc = pdf; document.getElementById('pdfControls').style.display = 'flex'; document.getElementById('pageTotal').textContent = pdfDoc.numPages; pageInput.max = pdfDoc.numPages; renderPage(pageNum, isNew); }).catch(err => { cAlert("Error al abrir PDF."); console.error(err); });
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
            currentFileType = file.type; currentFileName = file.name; measurementsByPage = {}; counters = { line: 1, area: 1, circle: 1, arc: 1, dimension: 1 }; pageNum = 1; scaleByPage = {}; document.getElementById('statusText').innerText = "Cargando plano...";
            const reader = new FileReader(); reader.onload = function(event) { currentFileDataURL = event.target.result; loadDocumentFromDataURL(true); }; reader.readAsDataURL(file); e.target.value = ""; 
        });

        document.getElementById('btnPrev').onclick = () => { if (pageNum > 1) { pageNum--; renderPage(pageNum, false); }};
        document.getElementById('btnNext').onclick = () => { if (pageNum < pdfDoc.numPages) { pageNum++; renderPage(pageNum, false); }};
        pageInput.addEventListener('change', (e) => { if (!pdfDoc) return; let val = parseInt(e.target.value); if (isNaN(val) || val < 1) val = 1; if (val > pdfDoc.numPages) val = pdfDoc.numPages; if (val !== pageNum) { pageNum = val; renderPage(pageNum, false); } else pageInput.value = pageNum; });

        document.querySelectorAll('.tool-trigger').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const selectedMode = e.currentTarget.getAttribute('data-mode');
                if (['distance', 'dimension', 'polygonal', 'area', 'circle', 'arc', 'autoLine', 'autoArea'].includes(selectedMode)) { if (!scaleByPage[pageNum]) { cAlert("¡Calibra la escala primero!"); return; } } 
                if (['autoLine', 'autoArea'].includes(selectedMode) && !cvReady) { cAlert("El motor OpenCV aún se está cargando. Espera unos segundos."); return; }
                setMode(selectedMode);
            });
        });
        
        function setMode(newMode) {
            mode = newMode; 
            document.querySelectorAll('.tool-trigger').forEach(btn => btn.classList.remove('active'));
            if(mode !== 'none') { document.querySelectorAll(`.tool-trigger[data-mode="${mode}"]`).forEach(btn => { btn.classList.add('active'); if(['arc', 'circle', 'dimension', 'printArea'].includes(mode)) { btn.style.borderColor = 'transparent'; btn.style.color = 'white'; } }); }
            document.querySelectorAll(`.tool-trigger[data-mode="circle"]:not(.active)`).forEach(b => { b.style.color = 'var(--circle)'; b.style.borderColor = 'transparent'; });
            document.querySelectorAll(`.tool-trigger[data-mode="arc"]:not(.active)`).forEach(b => { b.style.color = 'var(--curve)'; b.style.borderColor = 'transparent'; });
            document.querySelectorAll(`.tool-trigger[data-mode="dimension"]:not(.active)`).forEach(b => { b.style.color = '#94a3b8'; b.style.borderColor = 'transparent'; });
            document.querySelectorAll(`.tool-trigger[data-mode="printArea"]:not(.active)`).forEach(b => { b.style.color = 'var(--text-main)'; b.style.borderColor = 'transparent'; });

            canvas.style.cursor = (mode === 'select' || mode === 'pan') ? 'grab' : 'crosshair';
            isDrawing = false; measureStep = 0; currentPath = []; tempPoint = null; if (mode !== 'select') editingMeasureId = null; redraw(); loupeCanvas.style.display = 'none';
        }

        function recalculateMeasurement(m, currScale) {
            if (!currScale) return;
            if (m.type === 'straight') { let dist = Math.hypot(m.points[1].x - m.points[0].x, m.points[1].y - m.points[0].y); m.valM = (dist / currScale).toFixed(2); m.cx = (m.points[0].x + m.points[1].x)/2; m.cy = (m.points[0].y + m.points[1].y)/2; } 
            else if (m.type === 'dimension') { let dist = Math.hypot(m.points[1].x - m.points[0].x, m.points[1].y - m.points[0].y); m.valM = (dist / currScale).toFixed(2); let cad = getCADOffset(m.points[0], m.points[1], m.points[2]); m.cx = (m.points[0].x + m.points[1].x)/2 + cad.d * cad.nx; m.cy = (m.points[0].y + m.points[1].y)/2 + cad.d * cad.ny; }
            else if (m.type === 'polygonal') { let t = 0; for(let i=1; i<m.points.length; i++) t += Math.hypot(m.points[i].x - m.points[i-1].x, m.points[i].y - m.points[i-1].y); m.valM = (t / currScale).toFixed(2); m.cx = m.points[m.points.length-1].x; m.cy = m.points[m.points.length-1].y; }
            else if (m.type === 'area') { let per = 0, ar = 0, n = m.points.length, cX = 0, cY = 0; for(let i=0; i<n; i++) { let p1 = m.points[i], p2 = m.points[(i+1)%n]; per += Math.hypot(p2.x - p1.x, p2.y - p1.y); ar += (p1.x * p2.y - p2.x * p1.y); cX += p1.x; cY += p1.y; } m.valM = (per / currScale).toFixed(2); m.valM2 = (Math.abs(ar)/2/(currScale*currScale)).toFixed(2); m.cx = cX / n; m.cy = cY / n; }
            else if (m.type === 'circle' || m.type === 'arc') { let geom = getArcThrough3Points(m.points[0], m.points[2], m.points[1]); if (geom) { let rM = geom.r / currScale; m.radiusM = rM.toFixed(2); if (m.type === 'circle') { m.valM = (2 * Math.PI * rM).toFixed(2); m.valM2 = (Math.PI * rM * rM).toFixed(2); m.cx = geom.cx; m.cy = geom.cy; m.r = geom.r; } else { m.valM = (geom.length / currScale).toFixed(2); m.cx = m.points[2].x; m.cy = m.points[2].y; } } else { let dist = Math.hypot(m.points[1].x - m.points[0].x, m.points[1].y - m.points[0].y); m.valM = (dist / currScale).toFixed(2); m.radiusM = "0.00"; } }
        }

        function addMeasurement(data) {
            if (!measurementsByPage[pageNum]) measurementsByPage[pageNum] = []; data.id = Date.now().toString() + Math.floor(Math.random()*1000); data.lblOffset = { x: 0, y: -30 }; data.color = getDefaultColor(data.type);
            let namePrefix = "Medida"; if (data.type === 'area' || data.type === 'autoArea') namePrefix = `Área ${counters.area++}`; else if (data.type === 'circle') namePrefix = `Círculo ${counters.circle++}`; else if (data.type === 'arc') namePrefix = `Curva ${counters.arc++}`; else if (data.type === 'dimension') namePrefix = `Cota ${counters.dimension++}`; else namePrefix = `Línea ${counters.line++}`;
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
                let valStr = ""; if (['straight', 'polygonal', 'autoLine', 'dimension'].includes(m.type)) { valStr = `<span>${m.valM}</span>&nbsp;m`; } else if (m.type === 'arc' || m.type === 'circle') { valStr = `<span>${m.type==='arc'? m.valM : m.valM2}</span>&nbsp;${m.type==='arc'?'m':'m²'}`; } else { valStr = `<span>${m.valM2}</span>&nbsp;m²`; }
                item.innerHTML = ` <input type="color" class="color-picker" value="${m.color}" onchange="updateMeasurementColor('${m.id}', this.value)" title="Color"> <input type="text" class="measure-name" value="${m.name}" onchange="updateMeasurementName('${m.id}', this.value)" onkeyup="if(event.key === 'Enter') this.blur();"> <div class="measure-values">${valStr}</div> <button class="btn-delete" onclick="deleteMeasurement('${m.id}')" title="Borrar">✖</button> `;
                measurementListEl.appendChild(item);
            });
        }
        
        document.getElementById('btnExport').onclick = () => {
            const list = measurementsByPage[pageNum] || []; if (list.length === 0) return cAlert("No hay datos que exportar.");
            let csv = "\uFEFFHoja;Nombre;Tipo;Longitud/Perímetro (m);Área (m²);Radio (m)\n"; let pageLabel = pdfDoc ? `Página ${pageNum}` : "Imagen Única"; const typeTranslations = { 'straight': 'Línea Recta', 'dimension': 'Acotación CAD', 'polygonal': 'Línea Poligonal', 'area': 'Área Manual', 'circle': 'Círculo', 'arc': 'Arco', 'autoLine': 'Auto-Línea', 'autoArea': 'Auto-Área' };
            list.forEach(m => { let tipo = typeTranslations[m.type] || m.type; let longitud = (m.valM && m.valM !== "N/A") ? m.valM.toString().replace('.',',') : "-"; let area = m.valM2 ? m.valM2.toString().replace('.',',') : "-"; let radio = m.radiusM ? m.radiusM.toString().replace('.',',') : "-"; csv += `${pageLabel};"${m.name}";${tipo};${longitud};${area};${radio}\n`; });
            const link = document.createElement("a"); link.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8;' })); link.download = `Mediciones_${pageLabel.replace(' ', '_')}.csv`; document.body.appendChild(link); link.click(); document.body.removeChild(link);
        };

        function executeAutoMeasurement(startX, startY, autoMode) {
            setTimeout(() => {
                try {
                    let src = cv.imread(canvas); let ctxData = ctx.getImageData(startX, startY, 1, 1).data; let r = ctxData[0], g = ctxData[1], b = ctxData[2];
                    let tolerancia = 60; let low = new cv.Mat(src.rows, src.cols, src.type(), [Math.max(0, r - tolerancia), Math.max(0, g - tolerancia), Math.max(0, b - tolerancia), 0]); let high = new cv.Mat(src.rows, src.cols, src.type(), [Math.min(255, r + tolerancia), Math.min(255, g + tolerancia), Math.min(255, b + tolerancia), 255]);
                    let mask = new cv.Mat(); cv.inRange(src, low, high, mask);
                    
                    if (autoMode === 'autoArea') {
                        let M = cv.getStructuringElement(cv.MORPH_RECT, new cv.Size(15, 15)); cv.morphologyEx(mask, mask, cv.MORPH_CLOSE, M);
                        let contours = new cv.MatVector(); let hierarchy = new cv.Mat(); cv.findContours(mask, contours, hierarchy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE);
                        if (contours.size() === 0) throw new Error("Vacio");
                        let maxArea = 0; let maxCnt = null; for (let i = 0; i < contours.size(); ++i) { let cnt = contours.get(i); let area = cv.contourArea(cnt); if (area > maxArea) { maxArea = area; maxCnt = cnt; } }
                        let approx = new cv.Mat(); let epsilon = 0.002 * cv.arcLength(maxCnt, true); cv.approxPolyDP(maxCnt, approx, epsilon, true);
                        let pts = []; let cx = 0, cy = 0; for (let i = 0; i < approx.rows; i++) { let px = approx.data32S[i * 2], py = approx.data32S[i * 2 + 1]; pts.push({x: px, y: py}); cx += px; cy += py; } cx /= pts.length; cy /= pts.length;
                        let currScale = scaleByPage[pageNum] || 1; let overlay = cv.Mat.zeros(src.rows, src.cols, cv.CV_8UC4); let color = new cv.Scalar(16, 185, 129, 150); let drawCnts = new cv.MatVector(); drawCnts.push(approx); cv.drawContours(overlay, drawCnts, 0, color, -1, cv.LINE_8, hierarchy, 0);
                        let tempCanvas = document.createElement('canvas'); cv.imshow(tempCanvas, overlay); let resImg = new Image(); resImg.onload = () => { addMeasurement({ type: 'autoArea', img: resImg, cx, cy, points: pts, valM2: (maxArea / (currScale * currScale)).toFixed(2), valM: (cv.arcLength(maxCnt, true) / currScale).toFixed(2) }); }; resImg.src = tempCanvas.toDataURL();
                        M.delete(); contours.delete(); hierarchy.delete(); approx.delete(); drawCnts.delete(); overlay.delete();
                    } else if (autoMode === 'autoLine') {
                        let contours = new cv.MatVector(); let hierarchy = new cv.Mat(); cv.findContours(mask, contours, hierarchy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE);
                        if (contours.size() === 0) throw new Error("Vacio");
                        let maxLen = 0; let maxCnt = null; for (let i = 0; i < contours.size(); ++i) { let cnt = contours.get(i); let len = cv.arcLength(cnt, true) / 2; if (len > maxLen) { maxLen = len; maxCnt = cnt; } }
                        let overlay = cv.Mat.zeros(src.rows, src.cols, cv.CV_8UC4); let color = new cv.Scalar(168, 85, 247, 255); let drawCnts = new cv.MatVector(); drawCnts.push(maxCnt); cv.drawContours(overlay, drawCnts, 0, color, 3, cv.LINE_8, hierarchy, 0);
                        let M = cv.moments(maxCnt); let cx = M.m10 / M.m00, cy = M.m01 / M.m00; let tempCanvas = document.createElement('canvas'); cv.imshow(tempCanvas, overlay); let resImg = new Image(); resImg.onload = () => { addMeasurement({ type: 'autoLine', img: resImg, cx, cy, valM: (maxLen / (scaleByPage[pageNum] || 1)).toFixed(2), valM2: null }); }; resImg.src = tempCanvas.toDataURL();
                        contours.delete(); hierarchy.delete(); drawCnts.delete(); overlay.delete();
                    }
                    src.delete(); low.delete(); high.delete(); mask.delete(); setMode('select');
                } catch(err) { cAlert("No se detectó un patrón. Haz clic en una zona definida."); setMode('select'); }
            }, 50); 
        }

        function getLabelAtPos(x, y) { const list = measurementsByPage[pageNum] || []; for (let i = list.length - 1; i >= 0; i--) { const m = list[i]; if (!m.lblOffset) continue; const rx = m.cx + m.lblOffset.x, ry = m.cy + m.lblOffset.y; const boxHeight = (m.type === 'straight' || m.type === 'dimension' || m.type === 'polygonal' || m.type === 'autoLine' || m.type === 'arc') ? 18 : 32; if (x >= rx - 50 && x <= rx + 50 && y >= ry - 14 && y <= ry - 14 + boxHeight) return m; } return null; }
        function getPointAtPos(m, x, y) { if (!m.points) return -1; for (let i = 0; i < m.points.length; i++) { if (Math.hypot(x - m.points[i].x, y - m.points[i].y) < 15) return i; } return -1; }

        canvas.addEventListener('contextmenu', (e) => { e.preventDefault(); if (['polygonal', 'area'].includes(mode) && currentPath.length > 0) { if (measureStep >= 1) { finishPolyArea(); } } else { isDrawing = false; measureStep = 0; currentPath = []; tempPoint = null; redraw(); } });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') { isDrawing = false; measureStep = 0; currentPath = []; tempPoint = null; redraw(); } });

        canvas.addEventListener('mousemove', (e) => {
            const {x, y} = getMousePos(e);
            if (['calibrate', 'distance', 'dimension', 'polygonal', 'area', 'circle', 'arc', 'autoLine', 'autoArea'].includes(mode) || draggingPointIndex !== -1) { updateLoupe(e, x, y); } else { loupeCanvas.style.display = 'none'; }
            if (mode === 'select') {
                if (draggingPointIndex !== -1 && editingMeasureId) { const m = measurementsByPage[pageNum].find(val => val.id === editingMeasureId); if (m) { m.points[draggingPointIndex] = {x, y}; recalculateMeasurement(m, scaleByPage[pageNum]); updateSidebar(); redraw(); } }
                else if (draggingLabel) { draggingLabel.lblOffset.x = x - draggingLabel.cx - dragOffsetX; draggingLabel.lblOffset.y = y - draggingLabel.cy - dragOffsetY; redraw(); }
                else if (isPanning) { canvasContainer.scrollLeft = panScrollLeft - (e.clientX - panStartX); canvasContainer.scrollTop = panScrollTop - (e.clientY - panStartY); }
                else { if (getLabelAtPos(x, y)) canvas.style.cursor = 'move'; else canvas.style.cursor = 'default'; } return;
            }
            if (mode === 'pan' && isPanning) { canvasContainer.scrollLeft = panScrollLeft - (e.clientX - panStartX); canvasContainer.scrollTop = panScrollTop - (e.clientY - panStartY); return; }
            if (mode === 'printArea' && isDrawing) { endX = x; endY = y; redraw(); ctx.strokeStyle = '#0ea5e9'; ctx.lineWidth = 2; ctx.setLineDash([6, 6]); ctx.strokeRect(startX, startY, endX - startX, endY - startY); ctx.fillStyle = 'rgba(14, 165, 233, 0.15)'; ctx.fillRect(startX, startY, endX - startX, endY - startY); ctx.setLineDash([]); return; }
            if (isDrawing && ['calibrate', 'distance', 'polygonal', 'area', 'arc', 'circle', 'dimension'].includes(mode)) { tempPoint = {x, y}; redraw(); }
            if (!isDrawing && !isPanning && !draggingLabel) { canvas.style.cursor = (mode === 'pan' || mode === 'printArea') ? 'crosshair' : 'crosshair'; }
        });

        canvas.addEventListener('mousedown', (e) => {
            if (mode === 'none' || canvas.width === 0) return; const {x, y} = getMousePos(e);
            if (mode === 'select') {
                if (editingMeasureId) { const m = (measurementsByPage[pageNum] || []).find(val => val.id === editingMeasureId); if (m && m.type !== 'autoArea' && m.type !== 'autoLine') { const ptIdx = getPointAtPos(m, x, y); if (ptIdx !== -1) { draggingPointIndex = ptIdx; canvas.style.cursor = 'grabbing'; return; } } }
                const clickedLabel = getLabelAtPos(x, y); if (clickedLabel) { editingMeasureId = clickedLabel.id; updateSidebar(); draggingLabel = clickedLabel; dragOffsetX = x - (clickedLabel.cx + clickedLabel.lblOffset.x); dragOffsetY = y - (clickedLabel.cy + clickedLabel.lblOffset.y); canvas.style.cursor = 'move'; redraw(); return; }
                editingMeasureId = null; updateSidebar(); redraw(); isPanning = true; panStartX = e.clientX; panStartY = e.clientY; panScrollLeft = canvasContainer.scrollLeft; panScrollTop = canvasContainer.scrollTop; canvas.style.cursor = 'grabbing'; return;
            }
            if (mode === 'printArea') { startX = x; startY = y; isDrawing = true; return; }
            if (mode === 'pan') { isPanning = true; panStartX = e.clientX; panStartY = e.clientY; panScrollLeft = canvasContainer.scrollLeft; panScrollTop = canvasContainer.scrollTop; canvas.style.cursor = 'grabbing'; return; }
            if (e.button === 2) return; 

            if (['autoLine', 'autoArea'].includes(mode)) { executeAutoMeasurement(x, y, mode); return; }

            if (['calibrate', 'distance', 'polygonal', 'area', 'arc', 'circle', 'dimension'].includes(mode)) {
                if (measureStep === 0) { startX = x; startY = y; currentPath = [{x, y}]; isDrawing = true; measureStep = 1; }
                else if (measureStep === 1) {
                    if (['calibrate', 'distance'].includes(mode)) { endX = x; endY = y; currentPath.push({x, y}); finishLineTool(); } 
                    else if (['dimension', 'arc', 'circle'].includes(mode)) { currentPath.push({x, y}); measureStep = 2; }
                    else if (['polygonal', 'area'].includes(mode)) { const lastP = currentPath[currentPath.length - 1]; if (Math.hypot(x - lastP.x, y - lastP.y) > 5) currentPath.push({x, y}); }
                }
                else if (measureStep === 2) { if (['dimension', 'arc', 'circle'].includes(mode)) { currentPath.push({x, y}); finish3PointTool(); } }
            }
        });

        canvas.addEventListener('mouseup', (e) => {
            if (draggingPointIndex !== -1) { draggingPointIndex = -1; canvas.style.cursor = 'default'; redraw(); return; }
            if (draggingLabel) { draggingLabel = null; return; }
            if (isPanning) { isPanning = false; canvas.style.cursor = (mode === 'select') ? 'default' : 'grab'; return; }
            if (mode === 'printArea' && isDrawing) { isDrawing = false; const {x, y} = getMousePos(e); endX = x; endY = y; const rx = Math.min(startX, endX); const ry = Math.min(startY, endY); const rw = Math.abs(endX - startX); const rh = Math.abs(endY - startY); redraw(); if (rw > 10 && rh > 10) printSelectedArea(rx, ry, rw, rh); setMode('select'); }
        });

        function finishLineTool() {
            isDrawing = false; measureStep = 0; const dist = Math.hypot(endX - startX, endY - startY); if (dist < 5) { currentPath = []; redraw(); return; }
            if (mode === 'calibrate') {
                cPrompt("¿Cuántos metros reales tiene esta línea?", (r) => {
                    if (r) { r = parseFloat(r.replace(',', '.')); if (!isNaN(r) && r > 0) { scaleByPage[pageNum] = dist / r; document.getElementById('scaleInfo').innerText = `ESC. PÁG. ${pageNum} (1m = ${Math.round(scaleByPage[pageNum])}px)`; document.getElementById('scaleInfo').className = "scale-badge calibrated"; cAlert(`¡Escala guardada!`); setMode('distance'); } else { cAlert("Valor no válido."); } }
                    currentPath = []; redraw();
                });
            } else if (mode === 'distance') { addMeasurement({ type: 'straight', cx: (startX+endX)/2, cy: (startY+endY)/2, points: [...currentPath], valM: (dist/scaleByPage[pageNum]).toFixed(2), valM2: null }); currentPath = []; redraw(); } 
        }

        function finish3PointTool() {
            isDrawing = false; measureStep = 0; const currScale = scaleByPage[pageNum];
            if (mode === 'dimension') { let distPx = Math.hypot(currentPath[1].x - currentPath[0].x, currentPath[1].y - currentPath[0].y); let cad = getCADOffset(currentPath[0], currentPath[1], currentPath[2]); addMeasurement({ type: 'dimension', cx: (currentPath[0].x + currentPath[1].x)/2 + cad.d * cad.nx, cy: (currentPath[0].y + currentPath[1].y)/2 + cad.d * cad.ny, points: [...currentPath], valM: (distPx/currScale).toFixed(2), valM2: null }); }
            else if (mode === 'arc') { let arc = getArcThrough3Points(currentPath[0], currentPath[2], currentPath[1]); let lengthPx = arc ? arc.length : Math.hypot(currentPath[1].x - currentPath[0].x, currentPath[1].y - currentPath[0].y); addMeasurement({ type: 'arc', cx: currentPath[2].x, cy: currentPath[2].y, points: [...currentPath], valM: (lengthPx/currScale).toFixed(2), radiusM: (arc ? arc.r/currScale : 0).toFixed(2), valM2: null }); } 
            else if (mode === 'circle') { let circ = getArcThrough3Points(currentPath[0], currentPath[2], currentPath[1]); if (circ) { let rM = circ.r / currScale; addMeasurement({ type: 'circle', cx: circ.cx, cy: circ.cy, r: circ.r, points: [...currentPath], valM: (2 * Math.PI * rM).toFixed(2), valM2: (Math.PI * rM * rM).toFixed(2), radiusM: rM.toFixed(2) }); } }
            currentPath = []; tempPoint = null; redraw();
        }

        function finishPolyArea() {
            if (currentPath.length < 2) { currentPath = []; tempPoint = null; redraw(); return; }
            isDrawing = false; measureStep = 0; const currScale = scaleByPage[pageNum];
            if (mode === 'polygonal') { let t = 0; for (let i = 1; i < currentPath.length; i++) t += Math.hypot(currentPath[i].x - currentPath[i-1].x, currentPath[i].y - currentPath[i-1].y); addMeasurement({ type: 'polygonal', cx: currentPath[currentPath.length-1].x, cy: currentPath[currentPath.length-1].y, points: [...currentPath], valM: (t/currScale).toFixed(2), valM2: null }); } 
            else if (mode === 'area') { if (currentPath.length < 3) return; let per = 0, ar = 0, n = currentPath.length, cX = 0, cY = 0; for (let i = 0; i < n; i++) { const p1 = currentPath[i], p2 = currentPath[(i+1)%n]; per += Math.hypot(p2.x-p1.x, p2.y-p1.y); ar += (p1.x*p2.y - p2.x*p1.y); cX += p1.x; cY += p1.y; } addMeasurement({ type: 'area', cx: cX/n, cy: cY/n, points: [...currentPath], valM: (per/currScale).toFixed(2), valM2: (Math.abs(ar)/2/(currScale*currScale)).toFixed(2) }); } 
            currentPath = []; tempPoint = null; redraw();
        }

        function drawLine(x1, y1, x2, y2, color, isHigh) { ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.strokeStyle = isHigh ? '#ffffff' : color; ctx.lineWidth = isHigh ? 5 : 3; if(isHigh) { ctx.shadowColor = color; ctx.shadowBlur = 8; } ctx.stroke(); ctx.shadowBlur = 0; ctx.fillStyle = isHigh ? '#ffffff' : color; ctx.beginPath(); ctx.arc(x1, y1, isHigh? 4 : 2.5, 0, Math.PI*2); ctx.fill(); ctx.beginPath(); ctx.arc(x2, y2, isHigh? 4 : 2.5, 0, Math.PI*2); ctx.fill(); }
        function drawDimensionData(pts, color, isHigh) { let p1 = pts[0], p2 = pts[1], p3 = pts[2]; let cad = getCADOffset(p1, p2, p3); if (cad.len === 0) return; let off1x = p1.x + cad.d * cad.nx, off1y = p1.y + cad.d * cad.ny; let off2x = p2.x + cad.d * cad.nx, off2y = p2.y + cad.d * cad.ny; ctx.strokeStyle = isHigh ? '#ffffff' : color; if(isHigh) { ctx.shadowColor = color; ctx.shadowBlur = 8; } ctx.lineWidth = isHigh ? 3 : 1.5; let extDir = cad.d >= 0 ? 1 : -1; ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(off1x + extDir * 8 * cad.nx, off1y + extDir * 8 * cad.ny); ctx.moveTo(p2.x, p2.y); ctx.lineTo(off2x + extDir * 8 * cad.nx, off2y + extDir * 8 * cad.ny); ctx.stroke(); ctx.lineWidth = isHigh ? 4 : 2; ctx.beginPath(); ctx.moveTo(off1x, off1y); ctx.lineTo(off2x, off2y); ctx.stroke(); let tL = 5; let tx = cad.nx * tL; let ty = cad.ny * tL; let dxT = (cad.dx / cad.len) * tL; let dyT = (cad.dy / cad.len) * tL; ctx.lineWidth = isHigh ? 4 : 2; ctx.beginPath(); ctx.moveTo(off1x - dxT + tx, off1y - dyT + ty); ctx.lineTo(off1x + dxT - tx, off1y + dyT - ty); ctx.moveTo(off2x - dxT + tx, off2y - dyT + ty); ctx.lineTo(off2x + dxT - tx, off2y + dyT - ty); ctx.stroke(); ctx.shadowBlur = 0; }
        function drawPathData(pts, color, isClosed, isHigh) { ctx.beginPath(); ctx.moveTo(pts[0].x, pts[0].y); for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i].x, pts[i].y); if (isClosed) { ctx.closePath(); ctx.fillStyle = hexToRgba(color, isHigh ? 0.3 : 0.15); ctx.fill(); } ctx.strokeStyle = isHigh ? '#ffffff' : color; ctx.lineWidth = isHigh ? 5 : 3; if(isHigh) { ctx.shadowColor = color; ctx.shadowBlur = 8; } ctx.stroke(); ctx.shadowBlur = 0; ctx.fillStyle = isHigh ? '#ffffff' : color; pts.forEach(p => { ctx.beginPath(); ctx.arc(p.x, p.y, isHigh? 4 : 2.5, 0, Math.PI*2); ctx.fill(); }); }
        function drawCircleData(cx, cy, r, color, isHigh) { ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fillStyle = hexToRgba(color, isHigh ? 0.3 : 0.15); ctx.fill(); ctx.strokeStyle = isHigh ? '#ffffff' : color; ctx.lineWidth = isHigh ? 5 : 3; if(isHigh) { ctx.shadowColor = color; ctx.shadowBlur = 8; } ctx.stroke(); ctx.shadowBlur = 0; }
        function drawArcData(pts, color, isHigh) { let arc = getArcThrough3Points(pts[0], pts[2], pts[1]); ctx.beginPath(); if (arc) ctx.arc(arc.cx, arc.cy, arc.r, arc.startAngle, arc.endAngle, arc.anticlockwise); else { ctx.moveTo(pts[0].x, pts[0].y); ctx.lineTo(pts[1].x, pts[1].y); } ctx.strokeStyle = isHigh ? '#ffffff' : color; ctx.lineWidth = isHigh ? 5 : 3; if(isHigh) { ctx.shadowColor = color; ctx.shadowBlur = 8; } ctx.stroke(); ctx.shadowBlur = 0; ctx.fillStyle = isHigh ? '#ffffff' : color; pts.forEach(p => { ctx.beginPath(); ctx.arc(p.x, p.y, isHigh ? 4 : 2.5, 0, Math.PI*2); ctx.fill(); }); }
        function renderLabel(x, y, text, color, isHigh) { const lines = text.split('\n'); ctx.fillStyle = isHigh ? "#ffffff" : "rgba(255, 255, 255, 0.95)"; ctx.shadowColor = isHigh ? color : "rgba(0,0,0,0.15)"; ctx.shadowBlur = isHigh ? 12 : 6; ctx.shadowOffsetY = isHigh ? 0 : 3; ctx.beginPath(); ctx.roundRect(x - 50, y - 14, 100, lines.length > 1 ? 32 : 18, 4); ctx.fill(); ctx.shadowBlur = 0; ctx.shadowOffsetY = 0; ctx.fillStyle = "#0f172a"; ctx.font = "bold 10px Inter, sans-serif"; ctx.textAlign = "center"; lines.forEach((l, i) => { if(i>0) {ctx.fillStyle = color; ctx.font = "bold 10px Inter, sans-serif";} ctx.fillText(l, x, y + 0 + (i*13)); }); }
        
        function redraw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height); if (img.src) ctx.drawImage(img, 0, 0);
            const list = measurementsByPage[pageNum] || [];
            const sortedList = [...list.filter(m => m.id !== highlightedMeasureId), ...list.filter(m => m.id === highlightedMeasureId)];

            sortedList.forEach(m => {
                const isHigh = (m.id === highlightedMeasureId); const col = m.color;
                if (m.type === 'autoArea' || m.type === 'autoLine') { const tCanv = document.createElement('canvas'); tCanv.width = canvas.width; tCanv.height = canvas.height; const tc = tCanv.getContext('2d'); tc.drawImage(m.img, 0, 0); tc.globalCompositeOperation = 'source-in'; tc.fillStyle = col; tc.fillRect(0, 0, canvas.width, canvas.height); if (isHigh) { ctx.shadowColor = col; ctx.shadowBlur = 12; } ctx.drawImage(tCanv, 0, 0); ctx.shadowBlur = 0; }
                else if (m.type === 'straight') drawLine(m.points[0].x, m.points[0].y, m.points[1].x, m.points[1].y, col, isHigh);
                else if (m.type === 'dimension') drawDimensionData(m.points, col, isHigh);
                else if (m.type === 'polygonal') drawPathData(m.points, col, false, isHigh);
                else if (m.type === 'area') drawPathData(m.points, col, true, isHigh);
                else if (m.type === 'circle') drawCircleData(m.cx, m.cy, m.r, col, isHigh);
                else if (m.type === 'arc') drawArcData(m.points, col, isHigh);
            });

            if (isDrawing && currentPath.length > 0) {
                if (['calibrate', 'distance'].includes(mode) && tempPoint) { drawLine(currentPath[0].x, currentPath[0].y, tempPoint.x, tempPoint.y, mode==='calibrate'?'#ef4444':'#0ea5e9', false); }
                else if (['arc', 'circle', 'dimension'].includes(mode)) {
                    if (currentPath.length === 1 && tempPoint) { drawLine(currentPath[0].x, currentPath[0].y, tempPoint.x, tempPoint.y, mode==='dimension'?'var(--cad)':mode==='arc'?'var(--curve)':'var(--circle)', false); }
                    else if (currentPath.length === 2 && tempPoint) {
                        if (mode === 'dimension') drawDimensionData([currentPath[0], currentPath[1], tempPoint], 'var(--cad)', false);
                        else {
                            let arc = getArcThrough3Points(currentPath[0], tempPoint, currentPath[1]);
                            if (arc) { ctx.beginPath(); if(mode === 'arc') ctx.arc(arc.cx, arc.cy, arc.r, arc.startAngle, arc.endAngle, arc.anticlockwise); else ctx.arc(arc.cx, arc.cy, arc.r, 0, Math.PI*2); ctx.strokeStyle = mode==='arc'?'var(--curve)':'var(--circle)'; ctx.lineWidth = 2; ctx.setLineDash([6, 6]); ctx.stroke(); ctx.setLineDash([]); ctx.fillStyle = mode==='arc'?'var(--curve)':'var(--circle)'; [currentPath[0], currentPath[1], tempPoint].forEach(p => { ctx.beginPath(); ctx.arc(p.x, p.y, 2.5, 0, Math.PI*2); ctx.fill(); });
                            } else { drawLine(currentPath[0].x, currentPath[0].y, currentPath[1].x, currentPath[1].y, mode==='arc'?'var(--curve)':'var(--circle)', false); }
                        }
                    }
                }
                else if (['polygonal', 'area'].includes(mode)) { ctx.beginPath(); ctx.moveTo(currentPath[0].x, currentPath[0].y); for (let i = 1; i < currentPath.length; i++) ctx.lineTo(currentPath[i].x, currentPath[i].y); if (tempPoint) ctx.lineTo(tempPoint.x, tempPoint.y); if (mode === 'area' && currentPath.length > 2 && tempPoint == null) ctx.closePath(); const dC = mode === 'area' ? '#10b981' : '#f59e0b'; ctx.strokeStyle = dC; ctx.lineWidth = 2; ctx.setLineDash([6, 6]); ctx.stroke(); ctx.setLineDash([]); ctx.fillStyle = dC; currentPath.forEach(p => { ctx.beginPath(); ctx.arc(p.x, p.y, 2.5, 0, Math.PI*2); ctx.fill(); }); }
            }

            sortedList.forEach(m => {
                const isHigh = (m.id === highlightedMeasureId);
                if (m.cx === undefined) { if (m.type === 'straight') { m.cx = (m.points[0].x + m.points[1].x)/2; m.cy = (m.points[0].y + m.points[1].y)/2; } else if (m.type === 'area') { let cx=0,cy=0; m.points.forEach(p=>{cx+=p.x;cy+=p.y;}); m.cx=cx/m.points.length; m.cy=cy/m.points.length; } else if (m.type === 'polygonal') { m.cx = m.points[m.points.length-1].x; m.cy = m.points[m.points.length-1].y; } }
                if (!m.lblOffset) m.lblOffset = { x: 0, y: -30 }; let rx = m.cx + m.lblOffset.x, ry = m.cy + m.lblOffset.y;
                let lbl = m.name + '\n'; lbl += (m.type === 'area' || m.type === 'autoArea' || m.type === 'circle') ? `${m.valM2} m²` : `${m.valM} m`;
                if (Math.hypot(m.lblOffset.x, m.lblOffset.y) > 25 && m.type !== 'dimension') { ctx.beginPath(); ctx.moveTo(m.cx, m.cy); ctx.lineTo(rx, ry); ctx.strokeStyle = isHigh ? m.color : "rgba(15, 23, 42, 0.4)"; ctx.setLineDash([4,4]); ctx.lineWidth = isHigh ? 2 : 1; ctx.stroke(); ctx.setLineDash([]); }
                renderLabel(rx, ry, lbl, m.color, isHigh);
            });
            if (editingMeasureId) { const m = list.find(val => val.id === editingMeasureId); if (m && m.points && m.type !== 'autoArea' && m.type !== 'autoLine') { ctx.fillStyle = '#ffffff'; ctx.lineWidth = 2; ctx.strokeStyle = '#0ea5e9'; m.points.forEach(p => { ctx.beginPath(); ctx.arc(p.x, p.y, 6, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); }); } }
        }
    </script>
</body>
</html>
"""

components.html(codigo_html, height=900, scrolling=True)
