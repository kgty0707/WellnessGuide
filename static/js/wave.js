import { Point } from '/static/js/point.js';

export class Wave {
  constructor(color, amplitude = 5, frequency = 0.02, speed = 0.02, ctx, canvas) {
    this.color = color;
    this.ctx = ctx;
    this.canvas = canvas;
    this.points = [];
    this.numberOfPoints = 7; // 점의 개수
    this.amplitude = amplitude; // 파도의 높이
    this.frequency = frequency; // 파도의 주기
    this.speed = speed; // 파도의 속도
    this.init();
  }

  init() {
    this.resize();
  }

  resize() {
    this.stageWidth = this.canvas.clientWidth;
    this.stageHeight = this.canvas.clientHeight;
    this.canvas.width = this.stageWidth * 2; // 레티나 디스플레이 고려
    this.canvas.height = this.stageHeight * 2;
    this.ctx.scale(2, 2);
    this.centerY = this.stageHeight / 1.2;

    // 점 간격 계산
    this.pointGap = this.stageWidth / (this.numberOfPoints - 1);

    // 점 초기화
    this.points = [];
    for (let i = 0; i < this.numberOfPoints; i++) {
      const x = this.pointGap * i;
      const y = this.centerY;
      this.points.push(new Point(i, x, y, this.amplitude, this.frequency, this.speed));
    }
  }

  draw() {
    // 캔버스 지우기 제거
    this.ctx.beginPath();

    // 시작점으로 이동
    this.ctx.moveTo(this.points[0].x, this.points[0].y);

    // 점들을 곡선으로 연결
    for (let i = 0; i < this.numberOfPoints; i++) {
      const point = this.points[i];
      const nextPoint = this.points[i + 1];

      // 현재 점 업데이트
      point.update();

      if (nextPoint) {
        const midX = (point.x + nextPoint.x) / 2;
        const midY = (point.y + nextPoint.y) / 2;
        this.ctx.quadraticCurveTo(point.x, point.y, midX, midY);
      }
    }

    // 마지막 점으로 선 그리기
    this.ctx.lineTo(this.points[this.numberOfPoints - 1].x, this.points[this.numberOfPoints - 1].y);

    // 하단을 따라 닫기
    this.ctx.lineTo(this.stageWidth, this.stageHeight);
    this.ctx.lineTo(0, this.stageHeight);
    this.ctx.closePath();

    // 파도 색상 설정 및 채우기
    this.ctx.fillStyle = this.color;
    this.ctx.fill();
  }
}
