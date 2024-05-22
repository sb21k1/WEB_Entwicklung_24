document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.filter_button');
    const dialogs = document.querySelectorAll('.dialog');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const dialogId = this.getAttribute('data-dialog');
            const dialog = document.getElementById(dialogId);
            if (dialog) {
                hideAllDialogs();
                positionDialog(dialog, this);
                dialog.style.display = 'block';
            }
        });
    });

    dialogs.forEach(dialog => {
        const closeBtn = dialog.querySelector('.close_dialog');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                dialog.style.display = 'none';
            });
        }
    });

    document.addEventListener('click', function(event) {
        const isClickInsideDialog = Array.from(dialogs).some(dialog =>
            dialog.contains(event.target)
        );

        const isClickInsideButton = Array.from(buttons).some(button =>
            button.contains(event.target)
        );

        if (!isClickInsideDialog && !isClickInsideButton) {
            hideAllDialogs();
        }
    });

    function hideAllDialogs() {
        dialogs.forEach(dialog => {
            dialog.style.display = 'none';
        });
    }

    function positionDialog(dialog, button) {
        const buttonRect = button.getBoundingClientRect();
        dialog.style.left = buttonRect.left + 'px';
        dialog.style.top = (buttonRect.top + buttonRect.height) + 'px';
    }
});