document.addEventListener('DOMContentLoaded', () => {
  // Display logout or not
  function checkAuthentication () {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    const addReview = document.getElementById('add-review');
    const loginNav = document.getElementById('login-nav');

    if (!token) {
      loginLink.style.display = 'block';
      logoutLink.style.display = 'none';
      addReview.style.display = 'none';
    } else {
      addReview.style.display = 'block';
      logoutLink.style.display = 'block';
      loginLink.style.display = 'none';
      loginNav.style.display = 'none';
    }
  }

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

  function logoutUser () {
    // Delete the cookie by rewriting it with a bad expiration date
    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1960 00:00:00 UTC';
    window.location.href = '/login';
  }

  checkAuthentication();

  const logoutLink = document.getElementById('logout-link');
  logoutLink.addEventListener('click', logoutUser);
});
