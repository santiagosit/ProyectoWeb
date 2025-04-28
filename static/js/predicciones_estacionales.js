document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar elementos del DOM
    const generar_prediccion_buttons = document.querySelectorAll('.generar-prediccion');
    const ver_tendencias_buttons = document.querySelectorAll('.ver-tendencias');
    
    // Configurar event listeners para los botones de predicción
    generar_prediccion_buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productoId = this.dataset.productoId;
            const mes = this.dataset.mes;
            cargarPrediccion(productoId, mes);
        });
    });
    
    // Configurar event listeners para los botones de tendencias
    ver_tendencias_buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productoId = this.dataset.productoId;
            cargarTendencias(productoId);
        });
    });
    
    // Función para cargar predicciones
    function cargarPrediccion(productoId, mes) {
        // Mostrar el modal con spinner de carga
        const prediccionModal = new bootstrap.Modal(document.getElementById('prediccionModal'));
        prediccionModal.show();
        
        // Realizar la petición AJAX
        fetch(`/predicciones/generar-prediccion/${productoId}/${mes}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta del servidor');
                }
                return response.json();
            })
            .then(data => {
                // Actualizar el contenido del modal con los datos recibidos
                document.getElementById('producto-nombre').textContent = data.producto.nombre;
                document.getElementById('mes-prediccion').textContent = data.mes_nombre;
                document.getElementById('temporada').textContent = data.temporada;
                document.getElementById('confianza').textContent = data.confianza;
                
                document.getElementById('demanda-estimada').textContent = data.demanda_estimada;
                document.getElementById('precio-estimado').textContent = data.precio_estimado;
                document.getElementById('stock-recomendado').textContent = data.stock_recomendado;
                
                // Configurar el color y texto de la oportunidad de compra
                const oportunidadElement = document.getElementById('oportunidad-compra');
                oportunidadElement.textContent = data.es_oportunidad_compra ? 'SÍ' : 'NO';
                oportunidadElement.className = data.es_oportunidad_compra ? 'text-success' : 'text-danger';
                
                // Mostrar factores estacionales
                document.getElementById('factores-estacionales').textContent = data.factores_estacionales;
                
                // Mostrar recomendación
                document.getElementById('recomendacion').textContent = data.recomendacion;
            })
            .catch(error => {
                console.error('Error al cargar la predicción:', error);
                document.getElementById('prediccionModalBody').innerHTML = `
                    <div class="alert alert-danger">
                        <strong>Error:</strong> No se pudo cargar la predicción. Por favor, intente nuevamente.
                    </div>
                `;
            });
    }
    
    // Función para cargar tendencias
    function cargarTendencias(productoId) {
        // Mostrar el modal con spinner de carga
        const tendenciasModal = new bootstrap.Modal(document.getElementById('tendenciasModal'));
        tendenciasModal.show();
        
        // Realizar la petición AJAX
        fetch(`/predicciones/analisis-tendencias/${productoId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta del servidor');
                }
                return response.json();
            })
            .then(data => {
                // Crear el gráfico de tendencias
                crearGraficoTendencias(data);
                
                // Mostrar oportunidades de compra
                mostrarOportunidadesCompra(data.oportunidades);
            })
            .catch(error => {
                console.error('Error al cargar las tendencias:', error);
                document.querySelector('#tendenciasModal .modal-body').innerHTML = `
                    <div class="alert alert-danger">
                        <strong>Error:</strong> No se pudieron cargar las tendencias. Por favor, intente nuevamente.
                    </div>
                `;
            });
    }
    
    // Función para crear el gráfico de tendencias
    function crearGraficoTendencias(data) {
        const ctx = document.getElementById('tendenciasChart').getContext('2d');
        
        // Destruir el gráfico existente si hay uno
        if (window.tendenciasChart) {
            window.tendenciasChart.destroy();
        }
        
        // Crear nuevo gráfico
        window.tendenciasChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [...data.datos_historicos.meses, ...data.predicciones.meses],
                datasets: [
                    {
                        label: 'Ventas (unidades)',
                        data: [...data.datos_historicos.ventas, ...data.predicciones.ventas],
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        yAxisID: 'y',
                        fill: true,
                        pointStyle: 'circle',
                        pointRadius: 5,
                        pointHoverRadius: 8,
                        pointBackgroundColor: function(context) {
                            const index = context.dataIndex;
                            return index >= data.datos_historicos.meses.length ? 'rgba(255, 99, 132, 1)' : 'rgba(75, 192, 192, 1)';
                        }
                    },
                    {
                        label: 'Precio ($)',
                        data: [...data.datos_historicos.precios, ...data.predicciones.precios],
                        borderColor: 'rgba(153, 102, 255, 1)',
                        backgroundColor: 'rgba(153, 102, 255, 0.2)',
                        yAxisID: 'y1',
                        fill: true,
                        pointStyle: 'triangle',
                        pointRadius: 5,
                        pointHoverRadius: 8,
                        pointBackgroundColor: function(context) {
                            const index = context.dataIndex;
                            return index >= data.datos_historicos.meses.length ? 'rgba(255, 159, 64, 1)' : 'rgba(153, 102, 255, 1)';
                        }
                    }
                ]
            },
            options: {
                responsive: true,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                stacked: false,
                plugins: {
                    title: {
                        display: true,
                        text: `Tendencias para ${data.producto.nombre}`
                    },
                    tooltip: {
                        callbacks: {
                            footer: function(tooltipItems) {
                                const dataIndex = tooltipItems[0].dataIndex;
                                return dataIndex >= data.datos_historicos.meses.length ? 'PREDICCIÓN' : 'HISTÓRICO';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Ventas (unidades)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        grid: {
                            drawOnChartArea: false,
                        },
                        title: {
                            display: true,
                            text: 'Precio ($)'
                        }
                    }
                }
            }
        });
    }
    
    // Función para mostrar oportunidades de compra
    function mostrarOportunidadesCompra(oportunidades) {
        const contenedor = document.getElementById('oportunidadesCompra');
        
        if (oportunidades && oportunidades.length > 0) {
            let html = '<ul class="oportunidades-list">';
            
            oportunidades.forEach(oportunidad => {
                html += `
                    <li class="oportunidad-item">
                        <span class="badge ${oportunidad.prioridad === 'Alta' ? 'bg-success' : 'bg-warning'}">${oportunidad.prioridad}</span>
                        <strong>${oportunidad.mes}:</strong> ${oportunidad.descripcion}
                    </li>
                `;
            });
            
            html += '</ul>';
            contenedor.innerHTML = html;
        } else {
            contenedor.innerHTML = '<p class="text-muted">No se han identificado oportunidades de compra para este producto.</p>';
        }
    }
    
    // Función para obtener cookie CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
