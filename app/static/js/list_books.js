(function () {
    const btnsPurchaseBook = document.querySelectorAll('.btnPurchaseBook');
    let isbnBookSelected = null;
    const csrf_token = document.querySelector("[name='csrf-token']").value

    btnsPurchaseBook.forEach((btn) => {
        btn.addEventListener('click', function () {
            isbnBookSelected = this.id;
            confirmPurchase();
        })
    })

    const confirmPurchase = () => {
        Swal.fire({
            title: '¿Confirmar la compra del libro seleccionado?',
            inputAttributes: {
                autocapitalize: 'off'
            },
            showCancelButton: true,
            confirmButtonText: 'Comprar',
            showLoaderOnConfirm: true,
            preConfirm: async () => {
                return await fetch(`${window.origin}/purchase_book`, {
                    method: 'POST',
                    mode: 'same-origin',
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': csrf_token
                    },
                    body: JSON.stringify({
                        'isbn': isbnBookSelected
                    })
                }).then(response => {
                    if (!response.ok) {
                        notificationSwal('Error', response.statusText, 'error', 'Cerrar');
                    }
                    return response.json();
                }).then(data => {
                    if (data.success) {
                        notificationSwal('¡Felicidades!', 'Libro Comprado', 'success', 'Ok');
                    } else {
                        notificationSwal('¡Alerta!', data.mensaje, 'warning', 'Ok');
                    }
                }).catch(error => {
                    notificactionSwal('Error', error, 'error', 'Cerrar');
                });
            },
            allowOutsideClick: () => false,
            allowEscapeKey: () => false
        });
    }
})();