// Código para la página de recomendaciones de pedidos
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap si existen
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    if (typeof bootstrap !== 'undefined') {
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Inicializar elementos colapsables
    var collapsibleElements = document.querySelectorAll('.collapse-trigger');
    collapsibleElements.forEach(function(element) {
        element.addEventListener('click', function() {
            var targetId = this.getAttribute('data-target');
            var targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                if (targetElement.classList.contains('show')) {
                    targetElement.classList.remove('show');
                    var icon = this.querySelector('.collapse-icon');
                    if (icon) icon.textContent = '+';
                } else {
                    targetElement.classList.add('show');
                    var icon = this.querySelector('.collapse-icon');
                    if (icon) icon.textContent = '-';
                }
            }
        });
    });
    
    // Inicializar filtros de tabla
    var filterInput = document.getElementById('filter-productos');
    if (filterInput) {
        filterInput.addEventListener('keyup', function() {
            var filterValue = this.value.toLowerCase();
            var rows = document.querySelectorAll('tbody tr');
            
            rows.forEach(function(row) {
                var text = row.textContent.toLowerCase();
                if (text.indexOf(filterValue) > -1) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
    
    // Inicializar ordenamiento de tablas
    var sortableHeaders = document.querySelectorAll('.sortable');
    sortableHeaders.forEach(function(header) {
        header.addEventListener('click', function() {
            var table = this.closest('table');
            if (!table) return;
            
            var index = Array.from(this.parentNode.children).indexOf(this);
            var tbody = table.querySelector('tbody');
            if (!tbody) return;
            
            var rows = Array.from(tbody.querySelectorAll('tr'));
            var direction = this.classList.contains('asc') ? -1 : 1;
            
            // Alternar dirección
            sortableHeaders.forEach(function(h) {
                h.classList.remove('asc', 'desc');
            });
            this.classList.toggle('asc', direction === 1);
            this.classList.toggle('desc', direction === -1);
            
            // Ordenar filas
            rows.sort(function(a, b) {
                var aCell = a.children[index];
                var bCell = b.children[index];
                
                if (!aCell || !bCell) return 0;
                
                var aValue = aCell.textContent.trim();
                var bValue = bCell.textContent.trim();
                
                // Detectar si es un valor numérico
                if (!isNaN(parseFloat(aValue)) && !isNaN(parseFloat(bValue))) {
                    return direction * (parseFloat(aValue) - parseFloat(bValue));
                } else {
                    return direction * aValue.localeCompare(bValue);
                }
            });
            
            // Reordenar en el DOM
            rows.forEach(function(row) {
                tbody.appendChild(row);
            });
        });
    });
    
    // Añadir clases de estilo a las tablas
    var tables = document.querySelectorAll('.data-table');
    tables.forEach(function(table) {
        // Añadir clases para filas con hover
        var rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row) {
            row.addEventListener('mouseover', function() {
                this.classList.add('row-hover');
            });
            row.addEventListener('mouseout', function() {
                this.classList.remove('row-hover');
            });
        });
    });
});
