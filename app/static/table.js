document.addEventListener('DOMContentLoaded', function() {
    var input = document.querySelector('.filter-input');
    var tablaLibros = document.getElementById('tabla-libros');
    input.addEventListener('keyup', function() {
        var filtro = input.value.toLowerCase();
        var filas = tablaLibros.getElementsByTagName('tr');
        for (var i = 0; i < filas.length; i++) {
            var celdas = filas[i].getElementsByTagName('td');
            var mostrarFila = false;
            for (var j = 0; j < celdas.length; j++) {
                var textoCelda = celdas[j].innerText.toLowerCase();
                if (textoCelda.indexOf(filtro) > -1) {
                    mostrarFila = true;
                    break;
                }
            }
            filas[i].style.display = mostrarFila ? '' : 'none';
        }
    });
});
