// Shared chart layout helpers for dashboard pages.
window.SpendWiseCharts = window.SpendWiseCharts || {};

window.SpendWiseCharts.applyBarAndTargetPositions = function applyBarAndTargetPositions() {
  document.querySelectorAll('.chart-bar[data-width]').forEach(function (bar) {
    var width = parseFloat(bar.getAttribute('data-width') || '0');
    if (!Number.isFinite(width)) {
      width = 0;
    }
    width = Math.max(0, Math.min(100, width));
    bar.style.width = width + '%';
  });

  document.querySelectorAll('.target-text[data-left], .target-line[data-left]').forEach(function (el) {
    var left = parseFloat(el.getAttribute('data-left') || '0');
    if (!Number.isFinite(left)) {
      left = 0;
    }
    left = Math.max(0, Math.min(100, left));
    el.style.left = left + '%';
  });
};
