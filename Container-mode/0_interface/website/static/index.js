document.addEventListener('DOMContentLoaded', function() {
  // Checks if thre is a query parameter indicating the page has reloaded
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has('reloaded')) {
      // Remove the query parameter to avoid repeated alerts
      urlParams.delete('reloaded');
      window.history.replaceState({}, '', `${window.location.pathname}?${urlParams}`);
  }
});

function deleteWord(wordId) {
  fetch('/delete-word', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ wordId })
  })
  .then(response => response.json())
  .then(data => {
      console.log('Word deleted successfully');
      location.reload(); // Reloads the page to update the list
  })
  .catch(error => {
      console.error('Error:', error);
  });
}

function addCardToAnki(wordId) {
    // Requests permission to use AnkiConnect API (https://foosoft.net/projects/anki-connect/)
    const requestPermission = JSON.stringify({
        action: 'requestPermission',
        version: 6
    });

    fetch('http://127.0.0.1:8765', { // assumes that Anki is running on the user machine
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: requestPermission
    })
    .then(response => response.json())
    .then(permissionData => {
        if (permissionData.permission === 'granted') {

            // Adds the card to Anki's database using Ankiconnect
            fetch(`/get-card-notes/${wordId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Error fetching card notes: ' + data.error);
                    return;
                }

                const cardNotes = data.card_notes;
                if (cardNotes.length === 0) {
                    alert('No card notes found.');
                    return;
                }

                // Extract the first note from cardNotes
                const cardNote = cardNotes[0];
                const cardNoteString = JSON.stringify({
                    action: 'addNote',
                    version: 6,
                    params: {
                        note: cardNote
                    }
                });

                // Make a POST request to AnkiConnect's API
                fetch('http://127.0.0.1:8765', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: cardNoteString
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert('Error adding card: ' + data.error);
                    } else {
                        console.log('Success:', data);
                        alert('Card added successfully: ' + JSON.stringify(data));
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred: ' + error);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to fetch card notes');
            });
        } else {
            alert('Permission to use AnkiConnect was denied.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to request permission from AnkiConnect: ' + error);
    });
}