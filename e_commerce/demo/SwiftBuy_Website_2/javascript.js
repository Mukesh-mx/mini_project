function submitForm() {
  const ratingValue = document.querySelector('input[name="rating"]:checked').value;
  const usernameValue = document.getElementById('username').value;
  const commentValue = document.getElementById('comment').value;

  const feedbackEntry = document.createElement('div');
  feedbackEntry.classList.add('feedback-entry');

  const starsElement = document.createElement('div');
  starsElement.classList.add('stars');
  starsElement.textContent = getStarSymbols(ratingValue);
  feedbackEntry.appendChild(starsElement);

  const usernameElement = document.createElement('div');
  usernameElement.classList.add('username');
  usernameElement.textContent = `Username: ${usernameValue}`;
  feedbackEntry.appendChild(usernameElement);

  const commentElement = document.createElement('div');
  commentElement.classList.add('comment');
  commentElement.textContent = `Comment: ${commentValue}`;
  feedbackEntry.appendChild(commentElement);

  const feedbackSection = document.getElementById('feedback');
  feedbackSection.appendChild(feedbackEntry);

  document.getElementById('username').value = '';
  document.getElementById('comment').value = '';
}

function getStarSymbols(count) {
  let stars = '';
  for (let i = 0; i < count; i++) {
    stars += '★';
  }
  return stars;
}
