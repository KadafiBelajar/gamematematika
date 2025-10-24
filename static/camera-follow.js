/*
 CameraFollow 2D (Vanilla JS)
 ------------------------------------------------------
 - Menjaga elemen target tetap di tengah kamera (viewport)
 - Mendukung smoothing (lerp), batas dunia (clamp), zoom, deadzone opsional
 - Bekerja pada struktur DOM:

   <div id="camera" class="camera-viewport">
     <div id="world" class="world">
       <div id="player"></div>
       ... objek dunia lain ...
     </div>
   </div>

 - CSS minimal yang direkomendasikan:
   .camera-viewport { position: relative; overflow: hidden; width: 100%; height: 100%; }
   .world { position: relative; transform-origin: 0 0; will-change: transform; }

 - Inisialisasi contoh:
   const camera = new CameraFollow({
     viewport: document.getElementById('camera'),
     world: document.getElementById('world'),
     target: document.getElementById('player'),
     smoothFactor: 0.18,
     zoom: 1,
     clampToWorld: true,
     centerTarget: true,
   });
   camera.start();

 Catatan:
 - Script ini tidak mengatur pergerakan player. Pastikan target (player) bergerak dengan logika game Anda sendiri.
 - Jika struktur layout berbeda dan offsetLeft/Top tidak cocok, gunakan opsi custom getter posisi (getTargetPosition).
*/

(function (global) {
  'use strict';

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function lerp(current, target, t) {
    return current + (target - current) * t;
  }

  class CameraFollow {
    constructor(options) {
      if (!options) throw new Error('CameraFollow requires options');

      this.viewport = options.viewport;
      this.world = options.world;
      this.target = options.target;

      if (!this.viewport || !this.world || !this.target) {
        throw new Error('[CameraFollow] viewport, world, dan target wajib diisi');
      }

      // Opsi
      this.smoothFactor = typeof options.smoothFactor === 'number' ? clamp(options.smoothFactor, 0, 1) : 0.18;
      this.clampToWorld = options.clampToWorld !== undefined ? !!options.clampToWorld : true;
      this.centerTarget = options.centerTarget !== undefined ? !!options.centerTarget : true;
      this.followX = options.followX !== undefined ? !!options.followX : true;
      this.followY = options.followY !== undefined ? !!options.followY : true;
      this.deadzone = options.deadzone || null; // { width, height } dalam px (opsional)
      this.zoom = typeof options.zoom === 'number' ? Math.max(0.01, options.zoom) : 1;

      // Custom getter posisi target (opsional)
      // getTargetPosition: () => ({ x, y }) koordinat di dalam world (px)
      this.getTargetPosition = typeof options.getTargetPosition === 'function' ? options.getTargetPosition : null;

      // State kamera (dalam satuan px pada koordinat viewport final)
      this.translateX = 0;
      this.translateY = 0;

      // Cache ukuran dunia (tanpa transform)
      this.worldWidth = options.worldWidth || this.world.scrollWidth || this.world.clientWidth;
      this.worldHeight = options.worldHeight || this.world.scrollHeight || this.world.clientHeight;

      this.enabled = true;
      this.running = false;
      this._raf = null;
      this._lastTs = 0;

      // Pastikan transform-origin agar rumus translasi + scale konsisten
      this.world.style.transformOrigin = '0 0';

      // Responsif: perbarui dimensi saat resize
      this._onResize = () => {
        this.worldWidth = this.world.scrollWidth || this.world.clientWidth;
        this.worldHeight = this.world.scrollHeight || this.world.clientHeight;
      };
      window.addEventListener('resize', this._onResize);

      // Inisialisasi transform awal
      this._applyTransform();
    }

    destroy() {
      this.stop();
      window.removeEventListener('resize', this._onResize);
    }

    start() {
      if (this.running) return;
      this.running = true;
      this._lastTs = performance.now();
      this._loop(this._lastTs);
    }

    stop() {
      this.running = false;
      if (this._raf) cancelAnimationFrame(this._raf);
      this._raf = null;
    }

    setEnabled(enabled) { this.enabled = !!enabled; }

    setTarget(element) {
      if (!element) return;
      this.target = element;
    }

    setZoom(zoom) {
      this.zoom = Math.max(0.01, zoom);
      this._applyTransform();
    }

    setWorldSize(width, height) {
      if (typeof width === 'number') this.worldWidth = width;
      if (typeof height === 'number') this.worldHeight = height;
    }

    centerOnTarget(immediate = false) {
      const desired = this._computeDesiredTranslation();
      if (immediate) {
        this.translateX = desired.x;
        this.translateY = desired.y;
        this._applyTransform();
      }
      return desired;
    }

    _loop = (ts) => {
      if (!this.running) return;
      const dtMs = ts - this._lastTs;
      this._lastTs = ts;

      if (this.enabled) {
        this._update(dtMs);
      }

      this._raf = requestAnimationFrame(this._loop);
    }

    _update(dtMs) {
      // Konversi smoothFactor menjadi faktor lerp berbasis waktu (stabil pada ~60fps)
      const t = 1 - Math.pow(1 - this.smoothFactor, Math.max(1, dtMs / (1000 / 60)));

      const desired = this._computeDesiredTranslation();

      // Lerp menuju posisi yang diinginkan
      if (this.followX) this.translateX = lerp(this.translateX, desired.x, t);
      if (this.followY) this.translateY = lerp(this.translateY, desired.y, t);

      // Terapkan batas dunia
      if (this.clampToWorld) {
        const vpW = this.viewport.clientWidth;
        const vpH = this.viewport.clientHeight;
        const scaledWorldW = this.worldWidth * this.zoom;
        const scaledWorldH = this.worldHeight * this.zoom;

        const minX = Math.min(0, vpW - scaledWorldW);
        const maxX = 0;
        const minY = Math.min(0, vpH - scaledWorldH);
        const maxY = 0;

        this.translateX = clamp(this.translateX, minX, maxX);
        this.translateY = clamp(this.translateY, minY, maxY);
      }

      this._applyTransform();
    }

    _computeDesiredTranslation() {
      const vpRect = this.viewport.getBoundingClientRect();

      let targetCenterX, targetCenterY;

      if (this.getTargetPosition) {
        // Posisi target disuplai oleh game (koordinat dunia, tanpa transform)
        const pos = this.getTargetPosition();
        targetCenterX = pos.x;
        targetCenterY = pos.y;
      } else {
        // Estimasi via DOM: gunakan offset relatif ke world jika memungkinkan
        // Fallback ke rect (dengan delta terhadap viewport)
        const worldRect = this.world.getBoundingClientRect();
        const targetRect = this.target.getBoundingClientRect();

        // Hitung pusat target dalam koordinat dunia approx
        // Mengurangi worldRect karena world dipindah pakai transform
        targetCenterX = (targetRect.left + targetRect.width / 2) - worldRect.left;
        targetCenterY = (targetRect.top + targetRect.height / 2) - worldRect.top;
      }

      // Titik pusat viewport dalam koordinat dunia yang sudah diskala
      const vpCenterX = this.viewport.clientWidth / 2;
      const vpCenterY = this.viewport.clientHeight / 2;

      // Posisi target yang ingin dicapai di layar (tengah viewport)
      // Hitung translasi dunia yang diperlukan agar (targetCenter * zoom) berada di (vpCenter)
      const desiredX = vpCenterX - (targetCenterX * this.zoom);
      const desiredY = vpCenterY - (targetCenterY * this.zoom);

      // Deadzone: hanya geser jika target keluar dari zona toleransi di sekitar pusat
      if (this.deadzone && (this.deadzone.width || this.deadzone.height)) {
        const dzW = this.deadzone.width || 0;
        const dzH = this.deadzone.height || 0;

        // Posisi target di layar jika memakai translasi saat ini
        const currentScreenX = (targetCenterX * this.zoom) + this.translateX;
        const currentScreenY = (targetCenterY * this.zoom) + this.translateY;

        const left = vpCenterX - dzW / 2;
        const right = vpCenterX + dzW / 2;
        const top = vpCenterY - dzH / 2;
        const bottom = vpCenterY + dzH / 2;

        let outX = 0, outY = 0;
        if (this.followX) {
          if (currentScreenX < left) outX = left - currentScreenX;
          else if (currentScreenX > right) outX = right - currentScreenX;
        }
        if (this.followY) {
          if (currentScreenY < top) outY = top - currentScreenY;
          else if (currentScreenY > bottom) outY = bottom - currentScreenY;
        }

        // Koreksi hanya sebesar pelanggaran deadzone
        return {
          x: this.translateX + outX,
          y: this.translateY + outY,
        };
      }

      // Default: selalu center (atau sesuai followX/followY)
      return {
        x: this.followX ? desiredX : this.translateX,
        y: this.followY ? desiredY : this.translateY,
      };
    }

    _applyTransform() {
      // Karena urutan transform CSS menyebabkan translate terpengaruh scale jika scale diletakkan setelahnya,
      // kita simpan translate dalam satuan layar (px final), lalu bagi dengan zoom agar offset yang diterapkan
      // menghasilkan perpindahan layar yang diinginkan.
      const tx = this.translateX / this.zoom;
      const ty = this.translateY / this.zoom;
      this.world.style.transform = `translate3d(${tx}px, ${ty}px, 0) scale(${this.zoom})`;
    }
  }

  // Export
  if (typeof window !== 'undefined') {
    global.CameraFollow = CameraFollow;
  }
})(typeof window !== 'undefined' ? window : globalThis);
