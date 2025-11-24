const API_URL = 'http://127.0.0.1:5000/api/v1';

document.addEventListener('DOMContentLoaded', async () => {
    const loginLink = document.getElementById("login-link");
    const logoutLink = document.getElementById("logout-link");
    const token = getToken();

    // Cacher le bouton login si connecté
    if (loginLink) {
        loginLink.style.display = token ? "none" : "block";
    }

    // Cacher le bouton logout si déconnecté
    if (logoutLink) {
        logoutLink.addEventListener('click', logoutUser);
        logoutLink.style.display = token ? "block" : "none";
    }

    const reviewForm = document.getElementById('review-form');
    const placeDetailsContainer = document.getElementById('place-details');
    const placeId = getPlaceIdFromURL();

    // Redirection seulement si formulaire review est présent et le user est non connecté
    if (reviewForm && !token) {
        window.location.href = 'index.html';
    }
    
    // Cacher le bouton add_review si non connecté
    const addReviewButton = document.querySelector('.add-review-button');
    if (addReviewButton) {
        addReviewButton.style.display = token ? 'block' : 'none';
    }

    if (placeDetailsContainer && placeId) {
        await fetchPlaceDetails(token, placeId);
        await fetchAndDisplayReviews(placeId, token);
    }   

    /* ---------------------- AFFICHAGE PLACES ---------------------- */
    const placesContainer = document.querySelector('.places');

    if (placesContainer) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
                method: 'GET',
                headers: token ? { 'Authorization': `Bearer ${token}` } : {}
            });

            if (!response.ok) {
                throw new Error('Erreur lors de la récupération des places');
            }

            const places = await response.json();
            displayPlaces(places, placesContainer);

        } catch (error) {
            console.error('Fetch failed:', error);
            placesContainer.innerHTML = `<p style="color:red;">Erreur: ${error.message}</p>`;
        }
    }

    /* ---------------------- FILTRE PRIX ---------------------- */
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', filterByPrice);
    }

    /* ---------------------- LOGIN FORM ---------------------- */
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault(); // Empêche le reload de la page

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;
            const errorMessage = document.getElementById("error-message");

            // Validation basique
            if (!email || !password) {
                errorMessage.textContent = "Email et mot de passe requis";
                return;
            }

            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok && data.access_token) {
                    document.cookie = `token=${data.access_token}; path=/; SameSite=Lax`;
                    window.location.href = 'index.html';
                } else {
                    errorMessage.textContent = data.error || 'Login failed';
                }

            } catch (err) {
                console.error("Erreur fetch login :", err);
                document.getElementById("error-message").textContent = "Erreur serveur";
            }
        });
    }

    /* ---------------------- SUBMIT REVIEW ---------------------- */
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review-text').value.trim();
            const ratingValue = parseInt(document.getElementById('rating').value);

            if (!reviewText) {
                alert('Merci d’écrire un avis avant de soumettre.');
                return;
            }

            try {
                await submitReview(token, placeId, reviewText, ratingValue);
            } catch (err) {
                console.error('Erreur lors de la soumission:', err);
                alert('Erreur serveur');
            }
        });
    }
});

/* ---------------------- HELPER FUNCTIONS ---------------------- */
function getToken() {
    return getCookie("token");
}

function getCookie(name) {
    const cookies = document.cookie.split("; ");
    for (const cookie of cookies) {
        const [key, value] = cookie.split("=");
        if (key === name) return value;
    }
    return null;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

/* ---------------------- AUTH ---------------------- */
function checkAuthentication() {
    const token = getCookie("token");
    const loginLink = document.getElementById("login-link");

    console.log("Token trouvé :", token);
    console.log("Login link:", loginLink);

    if (!token) {
        window.location.href = 'index.html'; // redirige si non connecté
    }

    if (token && loginLink) {
        loginLink.style.display = "none";
    }

    const addReviewButton = document.querySelector('.add-review-button');
    if (addReviewButton) {
        addReviewButton.style.display = token ? 'block' : 'none';
    }

    return token;
}

function logoutUser() {
    console.log("Cookie AVANT suppression:", document.cookie);
    
    // Supprimer le cookie
    document.cookie = "token=; path=/; max-age=0; SameSite=Lax";
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC; SameSite=Lax";
    
    console.log("Cookie APRÈS suppression:", document.cookie);
    
    setTimeout(() => {
        console.log("Cookie AVANT reload:", document.cookie);
        window.location.reload();
    }, 100);
}

/* ---------------------- AFFICHAGE PLACES ---------------------- */
function displayPlaces(places, container) {
    container.innerHTML = "";
    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.innerHTML = `
            <h2>${place.title}</h2>
            <p>Prix par nuit: ${place.price}€</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        container.appendChild(card);
    });
}

/* ---------------------- FILTRE PRIX ---------------------- */
function filterByPrice(event) {
    const maxPrice = parseInt(event.target.value);
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
        const priceText = card.querySelector('p').textContent;
        const price = parseInt(priceText.match(/\d+/)[0]);

        card.style.display = (price <= maxPrice || maxPrice === 0) ? "block" : "none";
    });
}

/* ---------------------- PLACE DETAILS ---------------------- */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        if (!response.ok) throw new Error("Impossible de récupérer les détails");

        const place = await response.json();
        displayPlaceDetails(place);
    } catch (err) {
        console.error("Erreur fetch place details :", err);
        const detailsContainer = document.querySelector('.place-details');
        if (detailsContainer) detailsContainer.innerHTML = `<p style="color:red;">Erreur: ${err.message}</p>`;
    }
}

function displayPlaceDetails(place) {
    const container = document.getElementById("place-details");

    if (!container) return;

    const addReviewButton = document.querySelector('.add-review-button');
    if (addReviewButton) {
        addReviewButton.href = `add_review.html?id=${place.id}`;
    }

    container.innerHTML = `
        <h2>${place.title}</h2>
        <p>${place.description}</p>
        <p>Prix: ${place.price}€</p>
        <p>Latitude: ${place.latitude}, Longitude: ${place.longitude}</p>
        <p>Propriétaire: ${place.owner.first_name} ${place.owner.last_name} (${place.owner.email})</p>
        <p>Ammenities: ${place.amenities.length ? place.amenities.join(", ") : "Aucun"}</p>
    `;
}

async function submitReview(token, placeId, reviewText, ratingValue) {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            'place_id': placeId,
            'text': reviewText,
            'rating': ratingValue
        })
    });

    if (response.ok) {
        alert('Avis soumis avec succès !');
        document.getElementById('review-form').reset();
    } else {
        const data = await response.json();
        alert('Erreur : ' + (data.error || 'Impossible de soumettre l’avis'));
    }
}

// Redirection seulement sur les pages qui requièrent un token
function requireAuthForReviewPage() {
    const token = getToken();
    const reviewForm = document.getElementById('review-form');
    if (reviewForm && !token) {
        window.location.href = 'index.html';
    }
    return token;
}

async function fetchAndDisplayReviews(placeId, token) {
    const container = document.getElementById("reviews-container");
    if (!container) return;

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}/reviews`, {
            method: 'GET',
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });

        if (!response.ok) throw new Error("Impossible de récupérer les avis");

        const reviews = await response.json();
        if (!reviews.length) {
            container.innerHTML = "<p>Aucun avis pour le moment.</p>";
            return;
        }

        container.innerHTML = ""; // vider le texte par défaut

        reviews.forEach(review => {
            const div = document.createElement('div');
            div.className = 'review-card';
            div.innerHTML = `
                <p><strong>${review.user_first_name} ${review.user_last_name}</strong> a écrit :</p>
                <p>${review.text}</p>
                <p><strong>Note:</strong> ${review.rating}/5</p>
            `;
            container.appendChild(div);
        });
    } catch (err) {
        console.error("Erreur fetch reviews :", err);
        container.innerHTML = `<p style="color:red;">Erreur: ${err.message}</p>`;
    }
}
