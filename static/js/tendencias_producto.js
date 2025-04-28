document.addEventListener('DOMContentLoaded', function() {
    // Obtener los datos desde el elemento oculto
    const chartDataElement = document.getElementById('chart-data');
    const contenedor = document.getElementById('curvas-tendencia');
    if (!chartDataElement || !contenedor) {
        console.error('No se encontró el elemento con los datos de los gráficos');
        return;
    }
    // Parsear el JSON de tendencias
    let tendenciaData = {};
    try {
        tendenciaData = JSON.parse(chartDataElement.dataset.tendenciaJson);
    } catch (e) {
        console.error('Error al parsear JSON de tendencia:', e);
        return;
    }
    // Por cada producto, crear un canvas y graficar la curva de ventas y la predicción
    Object.entries(tendenciaData).forEach(([producto, datos]) => {
        // Crear elementos
        const card = document.createElement('div');
        card.className = 'tendencia-card';
        const title = document.createElement('h4');
        title.textContent = producto;
        const canvas = document.createElement('canvas');
        canvas.id = 'chart-' + producto.replace(/\s+/g, '-').toLowerCase();
        canvas.height = 180;
        // Sugerencia
        const sugerencia = document.createElement('div');
        sugerencia.className = 'tendencia-sugerencia';
        sugerencia.innerHTML = `<b>Predicción próxima semana:</b> ${datos.prediccion} unidades.<br>` +
            (datos.prediccion > 0 ? 'Sugerencia: Evalúa realizar pedido si el stock será insuficiente.' : 'Sin ventas proyectadas.');
        // Añadir al DOM
        card.appendChild(title);
        card.appendChild(canvas);
        card.appendChild(sugerencia);
        contenedor.appendChild(card);
        // Preparar datos para Chart.js
        const labels = datos.labels.concat(['Predicción']);
        const data = datos.data.concat([datos.prediccion]);
        new Chart(canvas, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Unidades Vendidas',
                    data: data,
                    backgroundColor: 'rgba(78, 115, 223, 0.2)',
                    borderColor: 'rgba(78, 115, 223, 1)',
                    borderWidth: 2,
                    tension: 0.3,
                    pointBackgroundColor: labels.map((l,i) => i === labels.length-1 ? 'rgba(28, 200, 138, 1)' : 'rgba(78, 115, 223, 1)'),
                    pointRadius: labels.map((l,i) => i === labels.length-1 ? 6 : 3),
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(ctx) {
                                if(ctx.dataIndex === data.length-1) return 'Predicción: ' + ctx.parsed.y;
                                return 'Unidades: ' + ctx.parsed.y;
                            }
                        }
                    }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    });
});

// Estilos para las tarjetas de tendencia
const style = document.createElement('style');
style.innerHTML = `
.tendencia-card {
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    padding: 1rem 1.5rem 1.5rem 1.5rem;
    margin-bottom: 2rem;
    width: 100%;
    max-width: 480px;
    display: inline-block;
    vertical-align: top;
    margin-right: 2rem;
}
.tendencia-card h4 {
    margin: 0 0 0.5rem 0;
    font-size: 1.1rem;
    color: #2d3748;
}
.tendencia-sugerencia {
    margin-top: 0.75rem;
    padding: 0.5rem;
    background: #f8fafc;
    border-left: 3px solid #4a6fdc;
    border-radius: 4px;
    font-size: 0.95rem;
    color: #333;
}
@media (max-width: 900px) {
    .tendencia-card {
        max-width: 100%;
        margin-right: 0;
        display: block;
    }
}`;
document.head.appendChild(style);