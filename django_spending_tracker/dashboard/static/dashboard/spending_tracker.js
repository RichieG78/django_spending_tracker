// Spending Tracker interactivity is limited to chart positioning and the pie chart.
document.addEventListener('DOMContentLoaded', function () {
  if (window.SpendWiseCharts && window.SpendWiseCharts.applyBarAndTargetPositions) {
    window.SpendWiseCharts.applyBarAndTargetPositions();
  }

  var labelsNode = document.getElementById('spend-breakdown-labels');
  var valuesNode = document.getElementById('spend-breakdown-values');
  var pieCanvas = document.getElementById('spendingBreakdownChart');

  if (!(labelsNode && valuesNode && pieCanvas && window.Chart)) {
    return;
  }

  var labels = JSON.parse(labelsNode.textContent || '[]');
  var values = JSON.parse(valuesNode.textContent || '[]');
  var currencySymbol = pieCanvas.dataset.currencySymbol || '€';
  var total = values.reduce(function (sum, value) {
    return sum + value;
  }, 0);

  if (window.spendingBreakdownChartInstance) {
    window.spendingBreakdownChartInstance.destroy();
  }

  window.spendingBreakdownChartInstance = new Chart(pieCanvas.getContext('2d'), {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [
        {
          data: values,
          backgroundColor: ['#4b6bff', '#35c5ff', '#2fbf9b'],
          borderColor: '#ffffff',
          borderWidth: 3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            usePointStyle: true,
            boxWidth: 10,
          },
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              var value = Number(context.raw || 0);
              var percentage = total > 0 ? ((value / total) * 100).toFixed(2) : '0.00';
              return context.label + ': ' + currencySymbol + ' ' + value.toFixed(2) + ' (' + percentage + '%)';
            },
          },
        },
      },
    },
  });
});
