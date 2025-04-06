document.addEventListener('DOMContentLoaded', function() {
    // Datos para el gráfico de ventas (estos serán reemplazados por los datos del template)
    const ventasData = {
        labels: ventasLabels,
        datasets: [{
            label: 'Unidades Vendidas',
            data: ventasUnidades,
            backgroundColor: 'rgba(78, 115, 223, 0.2)',
            borderColor: 'rgba(78, 115, 223, 1)',
            borderWidth: 1
        }]
    };

    // Configuración del gráfico
    const ventasConfig = {
        type: 'line',
        data: ventasData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };

    // Crear el gráfico
    new Chart(
        document.getElementById('ventasChart'),
        ventasConfig
    );
});