import { Wave } from '/static/js/wave.js';

class App {
  constructor() {
    this.canvasWavesMap = new Map();
    this.initWaves();
    window.addEventListener('resize', this.resize.bind(this));
    this.resize();
    requestAnimationFrame(this.animate.bind(this));
  }

  initWaves() {
    // 모든 waveCanvas 클래스를 가진 캔버스 요소를 선택
    const canvases = document.querySelectorAll('.waveCanvas');
    canvases.forEach(canvas => {
      const ctx = canvas.getContext('2d');
      const waves = [
        new Wave('rgba(255, 255, 255, 0.5)', 20, 0.02, 0.02, ctx, canvas),
        new Wave('rgba(255, 255, 255, 0.3)', 30, 0.015, 0.015, ctx, canvas),
        new Wave('rgba(255, 255, 255, 0.2)', 40, 0.01, 0.01, ctx, canvas)
      ];
      this.canvasWavesMap.set(canvas, waves);
    });
  }

  resize() {
    this.canvasWavesMap.forEach(waves => {
      waves.forEach(wave => wave.resize());
    });
  }

  animate() {
    this.canvasWavesMap.forEach((waves, canvas) => {
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      waves.forEach(wave => wave.draw());
    });
    requestAnimationFrame(this.animate.bind(this));
  }
}

// 윈도우 로드 시 App 객체 생성
window.onload = () => {
  new App();
};