// Keep dashboard interactivity focused to chart rendering and minor UI positioning.
document.addEventListener('DOMContentLoaded', function () {
  if (window.SpendWiseCharts && window.SpendWiseCharts.applyBarAndTargetPositions) {
    window.SpendWiseCharts.applyBarAndTargetPositions();
  }

  var labelsNode = document.getElementById('monthly-chart-labels');
  var valuesNode = document.getElementById('monthly-chart-values');
  var monthlyChartCanvas = document.getElementById('monthlyChart');

  if (!(labelsNode && valuesNode && monthlyChartCanvas && window.Chart)) {
    return;
  }

  var monthLabels = JSON.parse(labelsNode.textContent || '[]');
  var monthValues = JSON.parse(valuesNode.textContent || '[]');
  var currencySymbol = monthlyChartCanvas.dataset.currencySymbol || '€';

  // Guard against repeated script execution creating stacked chart instances.
  if (window.monthlySpendingChart) {
    window.monthlySpendingChart.destroy();
  }

  window.monthlySpendingChart = new Chart(monthlyChartCanvas.getContext('2d'), {
    type: 'bar',
    data: {
      labels: monthLabels,
      datasets: [
        {
          label: 'Total Spending',
          data: monthValues,
          backgroundColor: 'rgba(75, 107, 255, 0.55)',
          borderColor: 'rgba(75, 107, 255, 1)',
          borderWidth: 1,
          borderRadius: 8,
          maxBarThickness: 32,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return currencySymbol + ' ' + value;
            },
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
      },
    },
  });
});
