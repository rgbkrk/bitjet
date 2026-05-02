// bitjet — binary visualization as fixed-size blocks on a canvas.
// One ESM module loaded by anywidget. Mutates state via model.set/save_changes
// so the Python side sees every slider/mode change in real time.

function render({ model, el }) {
  el.innerHTML = `
    <div class="bitjet" style="font-family: ui-monospace, SFMono-Regular, Menlo, monospace; display: flex; flex-direction: column; gap: 8px;">
      <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 12px;">
        <label style="display: flex; gap: 6px; align-items: center;">
          mode
          <select data-role="mode">
            <option value="bit">bit</option>
            <option value="byte">byte</option>
          </select>
        </label>
        <label style="display: flex; gap: 6px; align-items: center; flex: 1; min-width: 240px;">
          width
          <input type="range" data-role="width" min="1" max="1024" step="1" style="flex: 1;" />
          <span data-role="width-label" style="min-width: 4ch; text-align: right;"></span>
        </label>
        <label style="display: flex; gap: 6px; align-items: center;">
          block
          <input type="range" data-role="block" min="1" max="16" step="1" style="width: 100px;" />
          <span data-role="block-label" style="min-width: 2ch; text-align: right;"></span>
        </label>
        <span data-role="meta" style="color: #888;"></span>
      </div>
      <div style="overflow: auto; max-height: 600px;">
        <canvas style="image-rendering: pixelated; background: #111; border: 1px solid #333; border-radius: 4px;"></canvas>
      </div>
    </div>
  `;

  const modeSelect = el.querySelector("[data-role='mode']");
  const widthInput = el.querySelector("[data-role='width']");
  const widthLabel = el.querySelector("[data-role='width-label']");
  const blockInput = el.querySelector("[data-role='block']");
  const blockLabel = el.querySelector("[data-role='block-label']");
  const meta = el.querySelector("[data-role='meta']");
  const canvas = el.querySelector("canvas");
  const ctx = canvas.getContext("2d");

  const getBytes = () => {
    const data = model.get("data");
    if (data instanceof DataView) {
      return new Uint8Array(data.buffer, data.byteOffset, data.byteLength);
    }
    if (data instanceof ArrayBuffer) return new Uint8Array(data);
    return new Uint8Array(0);
  };

  const draw = () => {
    const bytes = getBytes();
    const mode = model.get("mode");
    const datawidth = Math.max(1, model.get("datawidth") | 0);
    const block = Math.max(1, model.get("block_size") | 0);

    const unitCount = mode === "bit" ? bytes.byteLength * 8 : bytes.byteLength;
    const cols = datawidth;
    const rows = Math.max(1, Math.ceil(unitCount / cols));

    const pxWidth = cols * block;
    const pxHeight = rows * block;
    canvas.width = pxWidth;
    canvas.height = pxHeight;
    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, pxWidth, pxHeight);

    if (mode === "bit") {
      for (let i = 0; i < unitCount; i++) {
        const byte = bytes[i >> 3];
        const bit = (byte >> (7 - (i & 7))) & 1;
        if (!bit) continue;
        const col = i % cols;
        const row = (i - col) / cols;
        ctx.fillStyle = "#f0f0f0";
        ctx.fillRect(col * block, row * block, block, block);
      }
    } else {
      for (let i = 0; i < unitCount; i++) {
        const v = bytes[i];
        const col = i % cols;
        const row = (i - col) / cols;
        ctx.fillStyle = `rgb(${v}, ${v}, ${v})`;
        ctx.fillRect(col * block, row * block, block, block);
      }
    }

    if (modeSelect.value !== mode) modeSelect.value = mode;
    if (widthInput.valueAsNumber !== datawidth) widthInput.value = String(datawidth);
    widthLabel.textContent = String(datawidth);
    if (blockInput.valueAsNumber !== block) blockInput.value = String(block);
    blockLabel.textContent = String(block);
    meta.textContent = `${bytes.byteLength} bytes · ${cols} × ${rows} ${mode}s · ${pxWidth}×${pxHeight}px`;
  };

  // `input` redraws live, `change` is what commits to the kernel so we
  // don't spam CRDT writes on every pixel of a slider drag.
  widthInput.addEventListener("input", () => {
    widthLabel.textContent = String(widthInput.valueAsNumber);
  });
  widthInput.addEventListener("change", () => {
    model.set("datawidth", widthInput.valueAsNumber);
    model.save_changes();
  });
  blockInput.addEventListener("input", () => {
    blockLabel.textContent = String(blockInput.valueAsNumber);
  });
  blockInput.addEventListener("change", () => {
    model.set("block_size", blockInput.valueAsNumber);
    model.save_changes();
  });
  modeSelect.addEventListener("change", () => {
    model.set("mode", modeSelect.value);
    model.save_changes();
  });

  draw();
  model.on("change:data", draw);
  model.on("change:datawidth", draw);
  model.on("change:block_size", draw);
  model.on("change:mode", draw);
}

export default { render };
