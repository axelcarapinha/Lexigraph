/* 
    Delete the word with id "wordId" from the database 
    after the user clicked on the cross button
    (i.e., basic request to the backend)
*/
function deleteWord(wordId) {
    fetch("/delete-word", { // sends a request to the delete-word endpoint (that returns a promise)
      method: "POST",
      body: JSON.stringify({ wordId: wordId }),
    }).then((_res) => { // async operation
      window.location.href = "/"; // refreshes the page
    });
  }