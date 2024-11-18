
// Filtrado de productos por búsqueda
document.addEventListener('DOMContentLoaded', function () {
    const buscarProducto = document.getElementById('buscarProducto');
    const listaProductos = document.getElementById('lista-productos');

    buscarProducto.addEventListener('keyup', function () {
        const texto = buscarProducto.value.toLowerCase();
        const filas = listaProductos.querySelectorAll('tr');

        filas.forEach(fila => {
            const nombreProducto = fila.querySelector('td:nth-child(2)').textContent.toLowerCase();
            fila.style.display = nombreProducto.includes(texto) ? '' : 'none';
        });
    });
});

// Configuración y cálculo de la venta
document.addEventListener('DOMContentLoaded', function () {
    const tablaVenta = document.querySelector('#tabla-venta tbody');
    const totalInput = document.getElementById('total');

    function actualizarTotal() {
        const subtotales = document.querySelectorAll('.subtotal');
        let total = 0;
        subtotales.forEach(subtotal => {
            total += parseFloat(subtotal.textContent) || 0;
        });
        totalInput.value = total.toFixed(2);
    }

    document.querySelectorAll('.agregar-producto').forEach(button => {
        button.addEventListener('click', function () {
            const id = this.dataset.id;
            const nombre = this.dataset.nombre;
            const precio = parseFloat(this.dataset.precio).toFixed(2);
            const filaExistente = Array.from(tablaVenta.querySelectorAll('input[name="productos[]"]')).find(input => input.value === id);

            if (filaExistente) {
                const fila = filaExistente.closest('tr');
                const cantidadInput = fila.querySelector('.cantidad');
                const nuevaCantidad = parseInt(cantidadInput.value) + 1;
                cantidadInput.value = nuevaCantidad;

                const descuento = parseFloat(fila.querySelector('.descuento').value);
                const subtotal = (nuevaCantidad * precio) * (1 - descuento / 100);
                fila.querySelector('.subtotal').textContent = subtotal.toFixed(2);
            } else {
                const fila = document.createElement('tr');
                fila.innerHTML = `

                    <td>${nombre}</td>
                    <td>${precio}</td>
                    <td><input type="number" class="cantidad" value="1" min="1"></td>
                    
                    <td class="subtotal">${precio}</td>
                
                    <input type="hidden" name="productos[]" value="${id}">
                    <input type="hidden" name="cantidades[]" value="1">
                    <input type="hidden" name="descuentos[]" value="0">
                    <input type="hidden" name="subtotales[]" value="${precio}">
                    <td><button type="button" class="btn btn-danger eliminar-producto">Eliminar</button></td>
                `;
                tablaVenta.appendChild(fila);

                fila.querySelector('.cantidad, .descuento').addEventListener('input', actualizarTotal);
                fila.querySelector('.eliminar-producto').addEventListener('click', function () {
                    fila.remove();
                    actualizarTotal();
                });
            }
            actualizarTotal();
        });
    });
});
document.addEventListener('DOMContentLoaded', function () {
     let hoy = new Date().toISOString("en-CA").split('T')[0];
     document.getElementById('fecha_hs').value = hoy;
})

  document.addEventListener('DOMContentLoaded', function () {
      var modal = document.getElementById('modal');
      var closeBtn = document.querySelector('.close');

      // Verificar si el modal y el botón de cerrar existen
      if (modal && closeBtn) {
          // Mostrar modal si contiene mensajes
          if (modal.querySelector('p')) {
              modal.style.display = 'flex';
          }

          // Cerrar modal al hacer clic en la "x"
          closeBtn.addEventListener('click', function () {
              modal.style.display = 'none';
          });

          // Cerrar modal al hacer clic fuera del contenido
          window.addEventListener('click', function (event) {
              if (event.target === modal) {
                  modal.style.display = 'none';
              }
          });
      }
  });