function ConfirmarVenta() {
    const modal = document.getElementById('confirmModal');
    const confirmBtn = document.getElementById('confirmBtn');
    const cancelBtn = document.getElementById('cancelBtn');

    modal.style.display = 'flex';

    return new Promise((resolve) => {
        confirmBtn.onclick = () => {
            modal.style.display = 'none';
            resolve(true); // Confirmar la venta
        };

        cancelBtn.onclick = () => {
            modal.style.display = 'none';
            resolve(false); // Cancelar la venta
        };
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const confirmButton = document.querySelector('.btn_aceptar_venta');
    confirmButton.addEventListener('click', async (e) => {
        e.preventDefault(); // Evitar el envío inmediato del formulario
        const confirmed = await ConfirmarVenta();
        if (confirmed) {
            document.querySelector('form').submit(); // Enviar formulario si se confirma
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const tablaVenta = document.querySelector('#tabla-venta tbody');
    const totalInput = document.getElementById('total');

    function actualizarTotal() {
        let total = 0;
        tablaVenta.querySelectorAll('.subtotal').forEach(subtotal => {
            total += parseFloat(subtotal.textContent) || 0;
        });
        totalInput.value = total.toFixed(2);
    }

    function actualizarSubtotal(fila) {
        const cantidad = parseInt(fila.querySelector('.cantidad').value) || 1;
        const precio = parseFloat(fila.querySelector('.precio').textContent) || 0;

        const subtotal = cantidad * precio;
        fila.querySelector('.subtotal').textContent = subtotal.toFixed(2);

        fila.querySelector('input[name="cantidades[]"]').value = cantidad;
        fila.querySelector('input[name="subtotales[]"]').value = subtotal.toFixed(2);

        actualizarTotal();
    }

    document.querySelectorAll('.agregar-producto').forEach(button => {
        button.addEventListener('click', function () {
            const id = this.dataset.id;
            const nombre = this.dataset.nombre;
            const precio = parseFloat(this.dataset.precio).toFixed(2);

            let filaExistente = Array.from(tablaVenta.querySelectorAll('input[name="productos[]"]'))
                .find(input => input.value === id);

            if (filaExistente) {
                let fila = filaExistente.closest('tr');
                let cantidadInput = fila.querySelector('.cantidad');
                cantidadInput.value = parseInt(cantidadInput.value) + 1;

                actualizarSubtotal(fila);
            } else {
                let fila = document.createElement('tr');
                fila.innerHTML = `
                    <td>${nombre}</td>
                    <td class="precio">${precio}</td>
                    <td><input type="number" class="cantidad" value="1" min="1"></td>
                    <td class="subtotal">${precio}</td>
                    <input type="hidden" name="productos[]" value="${id}">
                    <input type="hidden" name="cantidades[]" value="1">
                    <input type="hidden" name="subtotales[]" value="${precio}">
                    <td><button type="button" class="btn btn-danger eliminar-producto">Eliminar</button></td>
                `;
                tablaVenta.appendChild(fila);

                fila.querySelector('.cantidad').addEventListener('input', () => actualizarSubtotal(fila));
                fila.querySelector('.eliminar-producto').addEventListener('click', function () {
                    fila.remove();
                    actualizarTotal();
                });
            }
            actualizarTotal();
        });
    });

    let hoy = new Date().toISOString("en-CA").split('T')[0];
    document.getElementById('fecha_hs').value = hoy;
});



