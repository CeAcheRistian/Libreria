const notificationSwal = (titleText, text, icon, confirmButtonText) => {
    Swal.fire({
        titleText: titleText,
        text: text,
        icon: icon,
        confirmButtonText: confirmButtonText
    });
}