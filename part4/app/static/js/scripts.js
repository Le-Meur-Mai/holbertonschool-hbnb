/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  /* Managing the display of all places */
    const url = '/api/v1/places';
    const filter = document.querySelector('#price-filter')

    fetch(url)
    .then(response => response.json())
    .then(data => {
      const card_place = document.querySelector('#places-list');

      function displayPlaces(dataList) {
        card_place.innerHTML = ""
        for (let i = 0; dataList[i]; i++)
        {
          const box = document.createElement('div');
          box.className ='place-card';
          let place = dataList[i];
          box.innerHTML = `<div class="box-content">
          <h3>${place.title}</h3>
          <p>Price per night: $${place.price}</p>
          </div>
          <a href="place?id=${place.id}"><button class=details-button>View Details</button></a>`;
          card_place.appendChild(box);
        }
      }

      displayPlaces(data);

      /* Managing the authentification */

      function checkAuthentication() {
        const token = getCookie('token');
        const loginLink = document.getElementById('login-link');

        if (!token) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
        }
      }
      function getCookie(name) {
      // Function to get a cookie value by its name
        const cookies = document.cookie.split('; ');
        /* If there is several cookies, they will be stocked with a ;
        so we make a list of every key=value */
        for (let k = 0 ; k < cookies.length; k++) {
          const cookie = cookies[k].trim().split('=');
          if (cookie[0] === name)
            return decodeURIComponent(cookie[1]);
        }
        return (null);
      }

      checkAuthentication();

      /* Managing the price Filter */

      function selectByPrice(dataList) {
        const priceFilter = parseInt(document.querySelector('#price-filter').value);
        if (!isNaN(priceFilter)) {
          newData = [];
          for(let j = 0; dataList[j]; j++) {
            if (dataList[j].price <= priceFilter) {
              newData.push(dataList[j])
            }
          }
          displayPlaces(newData)
        } else {
          displayPlaces(dataList)
        }
      }

      filter.addEventListener("change", () => selectByPrice(data))
    })
    .catch(error => {
      console.log('error', error);
    });
  });
