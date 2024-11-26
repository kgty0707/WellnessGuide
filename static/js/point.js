export class Point {
  constructor(index, x, y, amplitude, frequency, speed) {
    this.index = index;
    this.x = x;
    this.y = y;
    this.amplitude = amplitude;
    this.frequency = frequency;
    this.speed = speed;
    this.baseY = y;
    this.angle = Math.random() * Math.PI * 2;
  }

  update() {
    this.angle += this.speed;
    this.y = this.baseY + Math.sin(this.angle) * this.amplitude;
  }
}
