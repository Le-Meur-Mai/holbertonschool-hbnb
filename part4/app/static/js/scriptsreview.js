document.addEventListener('DOMContentLoaded', () => {
  function getCookie (name) {
    // Function to get a cookie value by its name
    const cookies = document.cookie.split('; ');
    /* If there is several cookies, they will be stocked with a ;
        so we make a list of every key=value */
    for (let k = 0; k < cookies.length; k++) {
      const cookie = cookies[k].trim().split('=');
      if (cookie[0] === name) { return decodeURIComponent(cookie[1]); }
    }
    return (null);
  }

  function checkAuthentication () {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    const loginNav = document.getElementById('login-nav');

    if (!token) {
      window.location.href = '/login';
      return (null);
    } else {
      logoutLink.style.display = 'block';
      loginLink.style.display = 'none';
      loginNav.style.display = 'none';
      return (token);
    }
  }

  const tokenUser = checkAuthentication();

  /* Retrieve the url of the page and then the id in the query */
  const actualUrl = new URL(window.location.href);
  const idPlace = actualUrl.searchParams.get('id');

  const reviewSubmit = document.getElementById('review-form');

  async function addReview (place, text, rating, token) {
    const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
      method: 'POST',
      headers: {
        Authorization: 'Bearer ' + token,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        place_id: place,
        text,
        rating
      })
    });
    if (response.ok) {
      window.location.href = `/place?id=${idPlace}`;
    } else {
      alert('Review failed: ' + response.statusText);
    }
  }

  if (reviewSubmit) {
    reviewSubmit.addEventListener('submit', async (event) => {
      event.preventDefault();
      const ratingPlace = parseInt(document.querySelector('#rating').value);
      const textReview = document.querySelector('#review').value;
      addReview(idPlace, textReview, ratingPlace, tokenUser);
    });
  }
});
