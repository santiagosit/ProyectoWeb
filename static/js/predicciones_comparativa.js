// Código para gráficos de comparativa de precios
document.addEventListener('DOMContentLoaded', function() {
    // Obtener datos de los elementos JSON
    var productosData = [];
    var mesesLabels = [];
    
    try {
        var datosProductosElement = document.getElementById('datos-productos');
        var datosMesesElement = document.getElementById('datos-meses');
        
        if (datosProductosElement) {
            productosData = JSON.parse(datosProductosElement.textContent);
        }
        
        if (datosMesesElement) {
            mesesLabels = JSON.parse(datosMesesElement.textContent);
        }
        
        // Inicializar gráficos para cada producto
        if (productosData.length > 0) {
            productosData.forEach(function(producto) {
                crearGraficoComparativa(producto, mesesLabels);
            });
        }
    } catch (error) {
        console.error('Error al cargar los datos:', error);
    }

    // Inicializar gráficos si estamos en la página de comparativa
    inicializarGraficosComparativa();
});
