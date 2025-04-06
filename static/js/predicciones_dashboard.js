document.addEventListener('DOMContentLoaded', function() {
    const tipoChartElement = document.getElementById('tipoChart');
    const prioridadChartElement = document.getElementById('prioridadChart');
    
    if (tipoChartElement && prioridadChartElement) {
        // Fetch data from API
        fetch('/predicciones/api/datos-predicciones/')
            .then(response => response.json())
            .then(data => {
                // Create charts with the fetched data
                createCharts(data);
            })
            .catch(error => {
                console.error('Error fetching chart data:', error);
            });
    }
    
    function createCharts(data) {
        // Datos para gráfico de tipos
        const tipoData = {
            labels: data.tipo.labels,
            datasets: [{
                data: data.tipo.values,
                backgroundColor: [
                    'rgba(78, 115, 223, 0.8)',
                    'rgba(28, 200, 138, 0.8)',
                    'rgba(246, 194, 62, 0.8)',
                    'rgba(231, 74, 59, 0.8)'
                ],
                borderWidth: 1
            }]
        };

        // Datos para gráfico de prioridades
        const prioridadData = {
            labels: data.prioridad.labels,
            datasets: [{
                data: data.prioridad.values,
                backgroundColor: [
                    'rgba(231, 74, 59, 0.8)',
                    'rgba(246, 194, 62, 0.8)',
                    'rgba(54, 185, 204, 0.8)'
                ],
                borderWidth: 1
            }]
        };

        // Configuración de gráficos
        const tipoConfig = {
            type: 'pie',
            data: tipoData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        };

        const prioridadConfig = {
            type: 'doughnut',
            data: prioridadData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        };

        // Crear gráficos
        new Chart(tipoChartElement, tipoConfig);
        new Chart(prioridadChartElement, prioridadConfig);
    }
});