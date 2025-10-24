// ==========================================
// CAMERA 2D FOLLOW (DOM-based)
// ==========================================
// Fungsionalitas:
// - Mengikuti target (elemen DOM) dan menjaga tetap di tengah viewport
// - Smoothing/lerp (damping)
// - Zoom with clamping (min/max)
// - Clamp posisi kamera terhadap batas dunia (opsional)
// - Pixel snapping agar tampilan tidak blur
//
// Cara pakai singkat:
// const camera = new Camera2D({
//   viewport: document.querySelector('[data-camera-viewport]'),
//   world: document.querySelector('[data-world]'),
//   target: document.querySelector('[data-player]'),
//   damping: 0.12,
//   zoom: 1,
//   minZoom: 0.5,
//   maxZoom: 3,
//   pixelSnap: true,
//   bounds: { minX: 0, minY: 0, maxX: worldWidth, maxY: worldHeight }
// });
// camera.start();
// camera.setZoom(1.2);
// camera.setTarget(newPlayerEl);
// camera.setBounds({ minX: 0, minY: 0, maxX: 4000, maxY: 2000 });

(function () {
  'use strict';

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function lerp(start, end, t) {
    return start + (end - start) * t;
  }

  function getElementCenterInWorld(el) {
    if (!el || !el.parentElement) return { x: 0, y: 0 };
    const rect = el.getBoundingClientRect();
    const parentRect = el.parentElement.getBoundingClientRect();
    // Koordinat dunia relatif terhadap world element (tanpa transform)
    const x = rect.left - parentRect.left + rect.width / 2;
    const y = rect.top - parentRect.top + rect.height / 2;
    return { x, y };
  }

  class Camera2D {
    constructor(options) {
      if (!options || !options.viewport || !options.world) {
        throw new Error('Camera2D requires options.viewport and options.world');
      }

      this.viewport = options.viewport;
      this.world = options.world;
      this.target = options.target || null;

      this.zoom = typeof options.zoom === 'number' ? options.zoom : 1;
      this.minZoom = typeof options.minZoom === 'number' ? options.minZoom : 0.25;
      this.maxZoom = typeof options.maxZoom === 'number' ? options.maxZoom : 4;
      this.damping = typeof options.damping === 'number' ? options.damping : 0.15; // 0..1
      this.pixelSnap = options.pixelSnap !== undefined ? !!options.pixelSnap : true;
      this.bounds = options.bounds || null; // { minX, minY, maxX, maxY } in world coords

      // Camera center (world coordinates)
      this.cameraCenterX = 0;
      this.cameraCenterY = 0;
      this.desiredCenterX = 0;
      this.desiredCenterY = 0;

      this._rafId = null;
      this._running = false;

      // Optimization: cache viewport size
      this.viewportWidth = this.viewport.clientWidth;
      this.viewportHeight = this.viewport.clientHeight;

      this._handleResize = this._handleResize.bind(this);
      window.addEventListener('resize', this._handleResize);

      // Ensure world has will-change for smoother transforms
      this.world.style.willChange = 'transform';
      this.world.style.transformOrigin = '0 0';

      // Initial fit if target available
      if (this.target) {
        const c = getElementCenterInWorld(this.target);
        this.cameraCenterX = c.x;
        this.cameraCenterY = c.y;
        this.desiredCenterX = c.x;
        this.desiredCenterY = c.y;
        this._applyTransform(true);
      } else {
        this._applyTransform(true);
      }
    }

    destroy() {
      this.stop();
      window.removeEventListener('resize', this._handleResize);
    }

    _handleResize() {
      this.viewportWidth = this.viewport.clientWidth;
      this.viewportHeight = this.viewport.clientHeight;
      // Re-apply transform after resize to avoid jumps
      this._applyTransform(true);
    }

    setTarget(targetEl) {
      this.target = targetEl || null;
      if (!this.target) return;
      const c = getElementCenterInWorld(this.target);
      this.cameraCenterX = c.x;
      this.cameraCenterY = c.y;
      this.desiredCenterX = c.x;
      this.desiredCenterY = c.y;
      this._applyTransform(true);
    }

    setZoom(zoomValue, immediate) {
      const newZoom = clamp(zoomValue, this.minZoom, this.maxZoom);
      this.zoom = newZoom;
      if (immediate) {
        this._applyTransform(true);
      }
    }

    setBounds(bounds) {
      if (!bounds) {
        this.bounds = null;
        return;
      }
      const { minX, minY, maxX, maxY } = bounds;
      this.bounds = { minX, minY, maxX, maxY };
    }

    start() {
      if (this._running) return;
      this._running = true;
      const tick = () => {
        if (!this._running) return;
        this.update();
        this._rafId = window.requestAnimationFrame(tick);
      };
      this._rafId = window.requestAnimationFrame(tick);
    }

    stop() {
      this._running = false;
      if (this._rafId) {
        window.cancelAnimationFrame(this._rafId);
        this._rafId = null;
      }
    }

    update() {
      if (this.target) {
        const c = getElementCenterInWorld(this.target);
        this.desiredCenterX = c.x;
        this.desiredCenterY = c.y;
      }

      // Smooth follow
      const t = clamp(this.damping, 0, 1);
      this.cameraCenterX = lerp(this.cameraCenterX, this.desiredCenterX, t);
      this.cameraCenterY = lerp(this.cameraCenterY, this.desiredCenterY, t);

      // Clamp to bounds if provided
      if (this.bounds) {
        const halfW = this.viewportWidth / (2 * this.zoom);
        const halfH = this.viewportHeight / (2 * this.zoom);
        const minCenterX = this.bounds.minX + halfW;
        const maxCenterX = this.bounds.maxX - halfW;
        const minCenterY = this.bounds.minY + halfH;
        const maxCenterY = this.bounds.maxY - halfH;
        // If world smaller than viewport, center within bounds gracefully
        const centerX = (minCenterX > maxCenterX)
          ? (this.bounds.minX + this.bounds.maxX) / 2
          : clamp(this.cameraCenterX, minCenterX, maxCenterX);
        const centerY = (minCenterY > maxCenterY)
          ? (this.bounds.minY + this.bounds.maxY) / 2
          : clamp(this.cameraCenterY, minCenterY, maxCenterY);
        this.cameraCenterX = centerX;
        this.cameraCenterY = centerY;
      }

      this._applyTransform(false);
    }

    _applyTransform(immediate) {
      // Compose transform: place world so cameraCenter maps to viewport center
      // Using: translate(viewportCenter) scale(zoom) translate(-cameraCenter)
      const vpHalfW = this.viewportWidth / 2;
      const vpHalfH = this.viewportHeight / 2;

      // Pixel snapping to avoid blur (applied in world coordinate before scale)
      const cx = this.pixelSnap ? Math.round(this.cameraCenterX) : this.cameraCenterX;
      const cy = this.pixelSnap ? Math.round(this.cameraCenterY) : this.cameraCenterY;

      // Build transform string. Translate to viewport center in screen px, then scale, then translate world by negative center
      const transform = `translate3d(${vpHalfW}px, ${vpHalfH}px, 0) scale(${this.zoom}) translate3d(${-cx}px, ${-cy}px, 0)`;

      if (immediate) {
        this.world.style.transition = 'transform 0s';
      } else {
        this.world.style.transition = 'transform 0s'; // We interpolate via JS, so CSS transition off
      }

      this.world.style.transform = transform;
    }

    // Utility: set camera center directly (world coords)
    centerOn(worldX, worldY, immediate) {
      this.desiredCenterX = worldX;
      this.desiredCenterY = worldY;
      if (immediate) {
        this.cameraCenterX = worldX;
        this.cameraCenterY = worldY;
        this._applyTransform(true);
      }
    }
  }

  // Auto export to window
  if (typeof window !== 'undefined') {
    window.Camera2D = Camera2D;
  }
})();
