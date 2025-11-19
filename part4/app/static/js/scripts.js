/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
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
          box.innerHTML = `<h3>${place.title}</h3>
          <p>Price per night: $${place.price}</p>
          <a href="place?id=${place.id}"><button class=details-button>View Details</button></a>`;
          card_place.appendChild(box);
        }
      }

      displayPlaces(data);

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
