

// modal cartel

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


    document.addEventListener('DOMContentLoaded', function () {
        var ctx = document.getElementById('stockChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Producto 1', 'Producto 2', 'Producto 3'],
                datasets: [{
                    data: [10, 20, 30],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            }
        });
    });

