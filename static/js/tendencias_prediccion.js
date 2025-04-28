/**
 * tendencias_prediccion.js
 * Script para generar gráficas de tendencia de ventas y predicciones
 */

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM cargado, iniciando gráficas de tendencia...');
    
    // Verificar si Chart.js está disponible
    if (typeof Chart === 'undefined') {
        console.error('Chart.js no está cargado. Asegúrate de incluir la biblioteca antes de este script.');
        document.getElementById('curvas-tendencia').innerHTML = 
            '<div class="alert alert-danger">Error: Chart.js no está disponible</div>';
        return;
    }
    
    // Obtener el elemento que contiene los datos
    const chartDataElement = document.getElementById('chart-data');
    if (!chartDataElement) {
        console.error('No se encontró el elemento chart-data');
        return;
    }
    
    // Obtener el contenedor donde se mostrará la gráfica
    const contenedor = document.getElementById('curvas-tendencia');
    if (!contenedor) {
        console.error('No se encontró el contenedor para las gráficas');
        return;
    }
    
    try {
        // Parsear los datos JSON
        const dataAttribute = chartDataElement.getAttribute('data-tendencia-json');
        if (!dataAttribute) {
            throw new Error('El atributo data-tendencia-json está vacío');
        }
        
        const tendenciaData = JSON.parse(dataAttribute);
        console.log('Datos cargados:', Object.keys(tendenciaData).length, 'productos');
        
        // Si no hay datos, mostrar un mensaje
        if (Object.keys(tendenciaData).length === 0) {
            contenedor.innerHTML = '<div class="alert alert-warning">No hay datos disponibles para mostrar</div>';
            return;
        }
        
        // Limpiar el contenedor
        contenedor.innerHTML = '';
        
        // Crear un selector de productos
        const selectorDiv = document.createElement('div');
        selectorDiv.className = 'producto-selector mb-3';
        selectorDiv.innerHTML = `
            <label for="producto-select" class="form-label">Seleccionar producto: </label>
            <select id="producto-select" class="form-select">
                ${Object.keys(tendenciaData).map(producto => 
                    `<option value="${producto}">${producto}</option>`
                ).join('')}
            </select>
        `;
        contenedor.appendChild(selectorDiv);
        
        // Crear el contenedor para el gráfico
        const chartContainer = document.createElement('div');
        chartContainer.className = 'chart-container';
        chartContainer.style.height = '400px';
        chartContainer.style.marginTop = '20px';
        chartContainer.style.position = 'relative';
        contenedor.appendChild(chartContainer);
        
        // Crear el canvas para la gráfica
        const canvas = document.createElement('canvas');
        canvas.id = 'tendencia-chart';
        chartContainer.appendChild(canvas);
        
        // Variable para almacenar la instancia del gráfico
        let myChart = null;
        
        // Función para actualizar el gráfico
        function updateChart(productoSeleccionado) {
            console.log('Actualizando gráfica para:', productoSeleccionado);
            
            // Obtener datos del producto seleccionado
            const data = tendenciaData[productoSeleccionado];
            if (!data) {
                console.error('No hay datos para este producto:', productoSeleccionado);
                chartContainer.innerHTML = `<div class="alert alert-danger">No hay datos disponibles para ${productoSeleccionado}</div>`;
                return;
            }
            
            // Obtener el contexto del canvas
            const ctx = canvas.getContext('2d');
            
            // Destruir el gráfico anterior si existe
            if (myChart) {
                myChart.destroy();
            }
            
            // Determinar dónde termina el histórico y comienza la predicción
            const historicoLength = data.historico.length;
            const totalLength = data.labels.length;
            
            console.log('Datos históricos:', historicoLength, 'Total:', totalLength);
            
            // Buscar información de pedido para este producto en la tabla
            const oportunidadesPedido = Array.from(document.querySelectorAll('.desktop-view .table tbody tr'))
                .filter(row => row.cells && row.cells[0] && row.cells[0].textContent.trim() === productoSeleccionado.trim());
            
            // Variables para información de pedido
            let puntoPedido = null;
            let urgenciaPedido = null;
            let cantidadSugerida = null;
            let fechaPedido = null;
            
            // Si encontramos información de pedido para este producto
            if (oportunidadesPedido.length > 0) {
                const row = oportunidadesPedido[0];
                cantidadSugerida = row.cells[3].textContent.trim();
                fechaPedido = row.cells[4].textContent.trim();
                urgenciaPedido = row.cells[5].textContent.trim().toLowerCase();
                
                console.log('Información de pedido encontrada:', fechaPedido, cantidadSugerida, urgenciaPedido);
                
                // Determinar el punto de pedido en la gráfica
                if (fechaPedido !== "Inmediato") {
                    // Encontrar el índice de la fecha en las etiquetas
                    const fechaIndex = data.labels.findIndex(fecha => fecha === fechaPedido);
                    if (fechaIndex !== -1) {
                        puntoPedido = fechaIndex;
                    }
                } else {
                    // Si es inmediato, marcar en el punto actual
                    puntoPedido = historicoLength;
                }
            }
            
            // Preparar los datos para el gráfico
            // Datos históricos (completados con null para la parte de predicción)
            const datosHistoricos = [...data.historico, ...Array(totalLength - historicoLength).fill(null)];
            
            // Datos de predicción (completados con null para la parte histórica)
            const datosPrediccion = [...Array(historicoLength).fill(null), ...data.prediccion];
            
            // Crear datasets básicos
            const datasets = [
                {
                    label: 'Ventas Históricas',
                    data: datosHistoricos,
                    borderColor: '#4a6fdc',
                    backgroundColor: 'rgba(74, 111, 220, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.1
                },
                {
                    label: 'Predicción',
                    data: datosPrediccion,
                    borderColor: '#ff6b6b',
                    backgroundColor: 'rgba(255, 107, 107, 0.1)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: true,
                    tension: 0.1
                }
            ];
            
            // Añadir marcador para punto de pedido si existe
            if (puntoPedido !== null) {
                // Crear un array con un solo punto en la posición del pedido
                const pedidoData = Array(totalLength).fill(null);
                
                // Determinar el valor Y para el punto de pedido
                let valorY;
                if (puntoPedido < historicoLength) {
                    valorY = data.historico[puntoPedido];
                } else {
                    valorY = data.prediccion[puntoPedido - historicoLength];
                }
                
                // Añadir un poco de margen para que se vea bien
                valorY = Math.max(1, valorY * 1.1);
                
                pedidoData[puntoPedido] = valorY;
                
                // Colores según urgencia
                let colorPedido = '#e74c3c'; // rojo por defecto (alta)
                if (urgenciaPedido === 'media') {
                    colorPedido = '#f39c12';
                } else if (urgenciaPedido === 'baja') {
                    colorPedido = '#27ae60';
                }
                
                // Añadir dataset para el punto de pedido
                datasets.push({
                    label: 'Punto de Pedido',
                    data: pedidoData,
                    borderColor: colorPedido,
                    backgroundColor: colorPedido,
                    borderWidth: 0,
                    pointRadius: 10,
                    pointStyle: 'triangle',
                    pointRotation: 180, // Triángulo apuntando hacia abajo
                    fill: false,
                    showLine: false
                });
                
                // Añadir una línea vertical para el punto de pedido
                const lineaVerticalData = Array(totalLength).fill(null);
                const maxY = Math.max(...data.historico.filter(n => n !== null), ...data.prediccion.filter(n => n !== null)) * 1.2;
                lineaVerticalData[puntoPedido] = maxY;
                
                datasets.push({
                    label: 'Línea de Pedido',
                    data: lineaVerticalData,
                    borderColor: colorPedido,
                    borderWidth: 2,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: false,
                    showLine: true
                });
            }
            
            // Configuración de la gráfica
            const chartConfig = {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: `Tendencia de Ventas: ${productoSeleccionado}`,
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            padding: {
                                top: 10,
                                bottom: 20
                            }
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                            backgroundColor: 'rgba(0, 0, 0, 0.7)',
                            titleFont: {
                                size: 14
                            },
                            bodyFont: {
                                size: 13
                            },
                            callbacks: {
                                footer: function(tooltipItems) {
                                    // Si es el punto de pedido
                                    if (tooltipItems[0].datasetIndex === 2 && tooltipItems[0].raw !== null) {
                                        return [
                                            `¡REALIZAR PEDIDO AQUÍ!`,
                                            `Fecha sugerida: ${fechaPedido}`,
                                            `Cantidad sugerida: ${cantidadSugerida} unidades`,
                                            `Urgencia: ${urgenciaPedido ? urgenciaPedido.toUpperCase() : ''}`
                                        ];
                                    }
                                    // Si es un punto de predicción
                                    else if (tooltipItems[0].datasetIndex === 1 && tooltipItems[0].raw !== null) {
                                        return `Predicción para esta semana: ${tooltipItems[0].raw} unidades`;
                                    }
                                    return '';
                                }
                            }
                        },
                        legend: {
                            position: 'top',
                            labels: {
                                usePointStyle: true,
                                padding: 15
                            }
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Semana',
                                font: {
                                    weight: 'bold'
                                }
                            },
                            grid: {
                                display: false
                            },
                            ticks: {
                                maxRotation: 45,
                                minRotation: 45
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Unidades vendidas',
                                font: {
                                    weight: 'bold'
                                }
                            },
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(0, 0, 0, 0.05)'
                            }
                        }
                    },
                    interaction: {
                        mode: 'nearest',
                        axis: 'x',
                        intersect: false
                    },
                    animation: {
                        duration: 1000,
                        easing: 'easeOutQuart'
                    }
                }
            };
            
            // Crear el gráfico
            try {
                myChart = new Chart(ctx, chartConfig);
                console.log('Gráfica creada exitosamente');
            } catch (error) {
                console.error('Error al crear la gráfica:', error);
                chartContainer.innerHTML = `<div class="alert alert-danger mt-3">Error al crear la gráfica: ${error.message}</div>`;
            }
            
            // Crear un div para mostrar información adicional
            const infoDiv = document.createElement('div');
            infoDiv.className = 'prediccion-info mt-4';
            
            // Determinar el color de urgencia si hay punto de pedido
            let colorUrgencia = '#e74c3c'; // rojo por defecto (alta)
            if (urgenciaPedido === 'media') {
                colorUrgencia = '#f39c12';
            } else if (urgenciaPedido === 'baja') {
                colorUrgencia = '#27ae60';
            }
            
            // Construir el HTML para el resumen de predicción
            let infoHTML = `
                <div class="card shadow-sm">
                    <div class="card-header bg-light">
                        <h5 class="mb-0">Resumen de predicción para ${productoSeleccionado}</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="stat-card p-3 mb-3 bg-light rounded">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="text-muted mb-2">Predicción Mensual</h6>
                                            <h3 class="mb-0">${data.prediccion_mensual}</h3>
                                            <small class="text-muted">unidades</small>
                                        </div>
                                        <div class="stat-icon">
                                            <i class="fas fa-chart-line fa-2x text-primary"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
            `;
            
            // Añadir información de pedido si existe
            if (puntoPedido !== null) {
                infoHTML += `
                            <div class="col-md-6">
                                <div class="stat-card p-3 mb-3 bg-light rounded" style="border-left: 4px solid ${colorUrgencia};">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="text-muted mb-2">Punto de Pedido</h6>
                                            <h3 class="mb-0">${fechaPedido}</h3>
                                            <small class="text-muted">Cantidad: ${cantidadSugerida} unidades</small>
                                            <div class="mt-2">
                                                <span class="badge" style="background-color: ${colorUrgencia}; color: white; padding: 5px 10px;">
                                                    Urgencia: ${urgenciaPedido.toUpperCase()}
                                                </span>
                                            </div>
                                        </div>
                                        <div class="stat-icon">
                                            <i class="fas fa-exclamation-triangle fa-2x" style="color: ${colorUrgencia};"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                `;
            }
            
            // Cerrar las etiquetas HTML
            infoHTML += `
                        </div>
                    </div>
                </div>
            `;
            
            // Establecer el contenido HTML
            infoDiv.innerHTML = infoHTML;
            
            // Reemplazar cualquier información anterior
            const existingInfo = contenedor.querySelector('.prediccion-info');
            if (existingInfo) {
                contenedor.removeChild(existingInfo);
            }
            
            // Añadir la nueva información
            contenedor.appendChild(infoDiv);
        }
        
        // Inicializar el gráfico con el primer producto
        const selectElement = document.getElementById('producto-select');
        if (selectElement && selectElement.options.length > 0) {
            // Asegurarse de que el primer elemento esté seleccionado
            selectElement.selectedIndex = 0;
            console.log('Inicializando con el producto:', selectElement.value);
            
            // Crear el gráfico inicial
            updateChart(selectElement.value);
            
            // Actualizar cuando cambie la selección
            selectElement.addEventListener('change', function() {
                console.log('Producto cambiado a:', this.value);
                updateChart(this.value);
            });
        } else {
            console.error('No se encontró el selector de productos o no tiene valores');
            contenedor.innerHTML += '<div class="alert alert-warning">No hay productos disponibles para mostrar</div>';
        }
    } catch (error) {
        // Capturar y mostrar cualquier error que ocurra
        console.error('Error al procesar los datos de tendencia:', error);
        const contenedor = document.getElementById('curvas-tendencia');
        if (contenedor) {
            contenedor.innerHTML = `
                <div class="alert alert-danger">
                    <strong>Error al cargar la gráfica:</strong> ${error.message}
                    <br>
                    <small>Consulta la consola para más detalles.</small>
                </div>
            `;
        }
    }
});
