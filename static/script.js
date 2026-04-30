function pagar(courseId, price, name) {
    if(confirm(`¿Confirmas la compra de ${name} por $${price}?`)) {
        window.location.href = `/completar-pago/${courseId}`;
    }
}

function completarClase(enrollmentId) {
    fetch(`/update_progress/${enrollmentId}`, { method: 'POST' })
    .then(res => res.json())
    .then(data => {
        if(data.status === 'success') {
            const bar = document.getElementById(`bar-${enrollmentId}`);
            if(bar) {
                bar.style.width = '100%';
                bar.style.backgroundColor = '#27ae60';
            }
            alert("¡Excelente trabajo! Clase completada.");
            location.reload(); // Recarga para activar botón de certificado
        }
    });
}

//Developer: Jhonn Pether