document.addEventListener('DOMContentLoaded', function() {
    // Obtener los datos desde el elemento oculto
    const chartDataElement = document.getElementById('chart-data');
    
    if (!chartDataElement) {
        console.error('No se encontró el elemento con los datos de los gráficos');
        return;
    }
    
    // Función para parsear datos JSON de forma segura
    function safeJSONParse(str, defaultValue) {
        try {
            return JSON.parse(str) || defaultValue;
        } catch (e) {
            console.error('Error al parsear JSON:', e);
            return defaultValue;
        }
    }
    
    // Extraer datos de los atributos
    const ventasLabels = safeJSONParse(chartDataElement.dataset.ventasLabels, []);
    const ventasUnidades = safeJSONParse(chartDataElement.dataset.ventasDatos, []);
    const preciosLabels = safeJSONParse(chartDataElement.dataset.preciosLabels, []);
    const preciosValores = safeJSONParse(chartDataElement.dataset.preciosDatos, []);
    const stockLabels = safeJSONParse(chartDataElement.dataset.stockLabels, []);
    const stockValores = safeJSONParse(chartDataElement.dataset.stockDatos, []);
    
    // Datos para el gráfico de ventas
    const ventasData = {
        labels: ventasLabels,
        datasets: [{
            label: 'Unidades Vendidas',
            data: ventasUnidades,
            backgroundColor: 'rgba(78, 115, 223, 0.2)',
            borderColor: 'rgba(78, 115, 223, 1)',
            borderWidth: 2,
            tension: 0.3
        }]
    };

    // Datos para el gráfico de precios
    const preciosData = {
        labels: preciosLabels,
        datasets: [{
            label: 'Precio',
            data: preciosValores,
            backgroundColor: 'rgba(28, 200, 138, 0.2)',
            borderColor: 'rgba(28, 200, 138, 1)',
            borderWidth: 2,
            tension: 0.3
        }]
    };

    // Datos para el gráfico de stock
    const stockData = {
        labels: stockLabels,
        datasets: [{
            label: 'Stock',
            data: stockValores,
            backgroundColor: 'rgba(246, 194, 62, 0.2)',
            borderColor: 'rgba(246, 194, 62, 1)',
            borderWidth: 2,
            tension: 0.3
        }]
    };

    // Configuración común para los gráficos
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: false
            }
        }
    };

    // Crear gráficos solo si existen los elementos en el DOM
    const ventasChart = document.getElementById('ventasChart');
    if (ventasChart) {
        new Chart(ventasChart, {
            type: 'line',
            data: ventasData,
            options: commonOptions
        });
    }
    
    const preciosChart = document.getElementById('preciosChart');
    if (preciosChart) {
        new Chart(preciosChart, {
            type: 'line',
            data: preciosData,
            options: commonOptions
        });
    }
    
    const stockChart = document.getElementById('stockChart');
    if (stockChart) {
        new Chart(stockChart, {
            type: 'line',
            data: stockData,
            options: commonOptions
        });
    }
});