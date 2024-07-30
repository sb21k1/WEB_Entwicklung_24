document.addEventListener('DOMContentLoaded', () => {
    let selectedTags = [];

    function updateTagSelection(tagElement, tagName) {
        if (tagElement.classList.contains('selected')) {
            tagElement.classList.remove('selected');
            selectedTags = selectedTags.filter(tag => tag !== tagName);
        } else {
            tagElement.classList.add('selected');
            selectedTags.push(tagName);
        }
        console.log('Aktuelle ausgewählte Tags:', selectedTags);
    }

    function handleTagClick(event) {
        const tagElement = event.target.closest('.tag_template');
        if (tagElement) {
            const tagName = tagElement.dataset.tag;
            updateTagSelection(tagElement, tagName);
        }
    }

    document.querySelectorAll('.dialog').forEach(dialog => {
        dialog.addEventListener('click', handleTagClick);
    });

    document.querySelector('.search_button_contents').addEventListener('click', () => {
        if (selectedTags.length > 0) {
            fetch('/recieveTags', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ tags: selectedTags }),
                })
                .then(response => response.json())
                .then(result => {
                    console.log(`Server-Antwort: ${result.status}`);
                    // Reload page after successful POST request
                    window.location.reload();
                })
                .catch(error => {
                    console.error('Fehler beim Senden der Anfrage:', error);
                });
        } else {
            console.log('Keine Tags ausgewählt.');
        }
    });
});