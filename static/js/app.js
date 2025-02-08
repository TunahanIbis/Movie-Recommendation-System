let selectedMovies = [];

const baseImageUrl = "https://image.tmdb.org/t/p/w500"; // This is the base URL for posters
const baseLinkUrl = "https://www.themoviedb.org/movie/"; // This is the base URL for TMDB links

async function loadMovies() {
    const response = await fetch("/random_movies");
    const movies = await response.json();
    const container = document.getElementById("movies");
    container.innerHTML = "";

    movies.forEach(movie => {
        const img = document.createElement("img");
        img.src = baseImageUrl + movie.poster_path;
        img.alt = movie.title;
        img.classList.add("movie");
        img.onclick = () => selectMovie(movie.title, img);
        container.appendChild(img);
    });
}

function selectMovie(title, imgElement) {
    if (selectedMovies.includes(title)) {
        selectedMovies = selectedMovies.filter(m => m !== title);
        imgElement.classList.remove("selected");
    } else if (selectedMovies.length < 3) {
        selectedMovies.push(title);
        imgElement.classList.add("selected");
    }
}

function showRecommendations() {
    let recContainer = document.getElementById("recommendations");

    // Reset the opacity and class for transition
    recContainer.classList.remove("visible");
    recContainer.style.opacity = "0";

    // Trigger a reflow to force the transition
    recContainer.offsetHeight;

    // After resetting, apply the transition and set opacity to 1
    setTimeout(() => {
        // Add the poster-transition class to each poster for transition effect
        const posters = recContainer.querySelectorAll('.movie');
        posters.forEach(poster => {
            poster.classList.add('poster-transition');
        });

        // Set visibility after transition starts
        recContainer.classList.add("visible");
        recContainer.style.opacity = "1"; // Make the recommendations visible
    }, 10); // Short delay before applying transition
}

function hideRecommendations() {
    const recommendations = document.getElementById("recommendations");
    recommendations.classList.add("hidden");
}

async function getRecommendations() {
    if (selectedMovies.length !== 3) {
        alert("ERROR: Please select 3 movies.");
        return;
    }

    const response = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ selected_movies: selectedMovies })
    });

    const data = await response.json();
    console.log("Received Data:", data);
    console.log("Recommendations:", data.recommendations);

    const recContainer = document.getElementById("recommendations");
    recContainer.innerHTML = "<h3 id='recommendation-header'>Recommended Movies:</h3>"; // Add class to header for transition

    // Create rows to display the movies 5 per row
    for (let i = 0; i < data.recommendations.length; i += 5) {
        // Create a new row for each set of 5 movies
        const rowDiv = document.createElement("div");
        rowDiv.classList.add("movie-row");

        // Slice the array to get 5 movies at a time
        const rowMovies = data.recommendations.slice(i, i + 5);

        // Loop over the movies in the current row and append images
        rowMovies.forEach(movie => {
            const movieLink = document.createElement("a");
            movieLink.href = baseLinkUrl + movie.id;
            movieLink.target = "_blank"; // Opens the link in a new tab
            movieLink.rel = "noopener noreferrer"

            const img = document.createElement("img");
            img.src = baseImageUrl + movie.poster_path;
            img.alt = movie.title;
            img.classList.add("movie", "poster-transition");

            movieLink.appendChild(img);

            rowDiv.appendChild(movieLink);
        });

        // Append the rowDiv to the container
        recContainer.appendChild(rowDiv);

        // Add the recommendation description once after the rows are appended
        const description = document.createElement("p");
        description.textContent = "These recommendations are based on your selected movies. Click on any recommended movie to view more details on TMDB!";
        description.id = "recommendation-note"; // Add the ID for transition effect
        description.classList.add("recommendation-text"); // Add CSS class for styling
        recContainer.appendChild(description); // Append after all movie rows

        // Apply the fade-in effect after content is loaded
        setTimeout(() => {
            recContainer.classList.add("visible");
            showRecommendations();
        }, 10);
    }
}

function clearRecommendations() {
    const recContainer = document.getElementById("recommendations");
    recContainer.innerHTML = ""; // Clear the recommendations content

    // Reset the opacity for the next time the recommendations are shown
    recContainer.classList.remove("visible");
    recContainer.style.opacity = "0";
}

function renewRecommendations() {
    // Clear the recommendations and reset the state
    clearRecommendations();

    // Delay the renew to ensure the state is reset
    setTimeout(() => {
        // Now fetch the new recommendations and show them again
        getRecommendations();
    }, 10); // A small delay before fetching and showing new recommendations
}


document.getElementById("clearButton").addEventListener("click", function () {
    clearRecommendations();

    // Clear the selected movies array
    selectedMovies = [];

    // Remove the 'selected' class from all movie images
    const selectedMovieElements = document.querySelectorAll(".movie.selected");
    selectedMovieElements.forEach(function (movie) {
        movie.classList.remove("selected");
    });

    // Reset the displayed recommendations
    const recContainer = document.getElementById("recommendations");
    recContainer.innerHTML = "";  // Clear recommendations
});

document.getElementById("renewButton").addEventListener("click", function () {
    clearRecommendations(); // Ensure this resets the state before new recommendations

    // Clear the selected movies array
    selectedMovies = [];

    // Remove the 'selected' class from all movie images
    const selectedMovieElements = document.querySelectorAll(".movie.selected");
    selectedMovieElements.forEach(function (movie) {
        movie.classList.remove("selected");
    });

    // Reset the displayed recommendations
    const recContainer = document.getElementById("recommendations");
    recContainer.innerHTML = "";  // Clear recommendations

    fetch("/random_movies")
        .then(response => response.json())
        .then(data => {
            // Clear the current movie container
            const movieContainer = document.getElementById("movies");
            movieContainer.innerHTML = "";

            // Create new random movies and display them
            data.forEach(movie => {
                const img = document.createElement("img");
                img.src = baseImageUrl + movie.poster_path;
                img.alt = movie.title;
                img.classList.add("movie");

                img.addEventListener("click", function () {
                    selectMovie(movie.title, img);
                });
                // Append the new image to the movie container
                movieContainer.appendChild(img);
            });
        })
        .catch(error => {
            console.error("Error fetching new movies:", error);
        });
});

loadMovies();