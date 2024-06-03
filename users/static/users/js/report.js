    var ctx = document.getElementById('capitalPieChart').getContext('2d');
    var capitalPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: {{ capital_structure_labels|safe }},
            datasets: [{
                data: {{ percentages|safe }},
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });
