const input = document.querySelector('#videoInput');
const dropzone = document.querySelector('#dropzone');
const wrap = document.querySelector('#videoWrap');
const video = document.querySelector('#preview');
const canvas = document.querySelector('#selector');
const ctx = canvas.getContext('2d');
const rights = document.querySelector('#rights');
const button = document.querySelector('#processButton');
const statusBox = document.querySelector('#status');
const fields = ['x', 'y', 'width', 'height'].map(id => document.querySelector(`#${id}`));
let selectedFile = null;
let start = null;

function setStatus(text, error = false) { statusBox.textContent = text; statusBox.className = error ? 'error' : ''; }
function validSelection() { return selectedFile && +fields[2].value >= 8 && +fields[3].value >= 8 && rights.checked; }
function refreshButton() { button.disabled = !validSelection(); }
function drawSelection() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const [x, y, w, h] = fields.map(field => +field.value);
  if (!video.videoWidth || w < 1 || h < 1) return;
  const sx = canvas.width / video.videoWidth, sy = canvas.height / video.videoHeight;
  ctx.fillStyle = 'rgba(217,255,67,.22)'; ctx.strokeStyle = '#d9ff43'; ctx.lineWidth = 3;
  ctx.fillRect(x*sx, y*sy, w*sx, h*sy); ctx.strokeRect(x*sx, y*sy, w*sx, h*sy);
  document.querySelector('#regionMeta').textContent = `x:${x} · y:${y} · ${w}×${h}px`;
}
function loadFile(file) {
  if (!file) return;
  selectedFile = file; video.src = URL.createObjectURL(file); dropzone.hidden = true; wrap.hidden = false;
  document.querySelector('#fileMeta').textContent = `${file.name} · ${(file.size/1048576).toFixed(1)} MB`;
  setStatus(''); refreshButton();
}
video.addEventListener('loadedmetadata', () => {
  canvas.width = video.clientWidth; canvas.height = video.clientHeight;
  document.querySelector('#fileMeta').textContent += ` · ${video.videoWidth}×${video.videoHeight}`;
});
canvas.addEventListener('pointerdown', event => { start = {x:event.offsetX,y:event.offsetY}; canvas.setPointerCapture(event.pointerId); });
canvas.addEventListener('pointermove', event => {
  if (!start) return;
  const scaleX = video.videoWidth/canvas.clientWidth, scaleY = video.videoHeight/canvas.clientHeight;
  const left = Math.max(0, Math.min(start.x,event.offsetX)), top = Math.max(0,Math.min(start.y,event.offsetY));
  const right = Math.min(canvas.clientWidth,Math.max(start.x,event.offsetX)), bottom = Math.min(canvas.clientHeight,Math.max(start.y,event.offsetY));
  const values = [left*scaleX,top*scaleY,(right-left)*scaleX,(bottom-top)*scaleY].map(v => Math.max(0,Math.round(v/2)*2));
  fields.forEach((field,index) => field.value = values[index]); drawSelection(); refreshButton();
});
canvas.addEventListener('pointerup', () => { start = null; });
window.addEventListener('resize', () => { canvas.width=video.clientWidth;canvas.height=video.clientHeight;drawSelection(); });
fields.forEach(field => field.addEventListener('input', () => { drawSelection(); refreshButton(); }));
rights.addEventListener('change', refreshButton); input.addEventListener('change', () => loadFile(input.files[0]));
['dragenter','dragover'].forEach(name => dropzone.addEventListener(name, event => { event.preventDefault();dropzone.classList.add('drag'); }));
['dragleave','drop'].forEach(name => dropzone.addEventListener(name, event => { event.preventDefault();dropzone.classList.remove('drag'); }));
dropzone.addEventListener('drop', event => loadFile(event.dataTransfer.files[0]));
button.addEventListener('click', async () => {
  button.disabled=true; setStatus('Đang xử lý… Video dài có thể mất vài phút.');
  const form = new FormData(); form.append('video',selectedFile); fields.forEach(field => form.append(field.id,field.value)); form.append('mask_shape',document.querySelector('#mask_shape').value); form.append('rights_attested','true');
  try {
    const response = await fetch('/api/process',{method:'POST',body:form});
    if (!response.ok) { const data=await response.json(); throw new Error(data.detail || 'Xử lý thất bại'); }
    const blob=await response.blob(), link=document.createElement('a'); link.href=URL.createObjectURL(blob); link.download=`cleaned-${selectedFile.name.replace(/\.[^.]+$/,'')}.mp4`; link.click();
    setStatus('Hoàn tất. File đã được tải xuống.');
  } catch (error) { setStatus(error.message,true); }
  finally { refreshButton(); }
});
