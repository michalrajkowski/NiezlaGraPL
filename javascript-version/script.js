// List of image names (your specific list of image names)
const imageNames = [
  "loc_castle.webp",
  "loc_lake.png",
  "loc_tavern.webp",
  "loc_cementary.webp",
  "loc_mountain.webp",
  "loc_tower.webp",
  "loc_forest.webp",
  "loc_plains.webp",
  "loc_village.webp",
  "christmasland.png",
];

// Configure Fuse.js for fuzzy searching
const options = {
  includeScore: true,  // Optionally include score to see how well it matches
  threshold: 0.3,      // Adjust threshold for fuzziness (lower is stricter)
  keys: []             // No specific keys, we're searching the whole name
};

// Create a new Fuse instance with the image names
const fuse = new Fuse(imageNames, options);

document.addEventListener("DOMContentLoaded", () => {
    
    let printLink = document.getElementById("print");
    let container = document.getElementById("container");

    printLink.addEventListener("click", event => {
        event.preventDefault();
        printLink.style.display = "none";
        window.print();
    }, false);

    container.addEventListener("click", event => {
        printLink.style.display = "flex";
    }, false);
    
    const cardsContainer = document.getElementById("cards-container");

    // Fetch card data from the JSON file
    fetch("data/json/christmas_land.json")
        .then(response => response.json())
        .then(cards => {
            cards.forEach(card => {
                console.log("Card processed")
                // Fetch and insert the card HTML template
                let THIS_CARD_HTML = ''
                const NORMAL_CARD_HTML = 'card.html'
                const REVERSE_CARD_HTML = 'card_reverse.html'
                if (card.reverse && card.reverse !== 0) {
                    THIS_CARD_HTML= REVERSE_CARD_HTML
                }else{
                    THIS_CARD_HTML=NORMAL_CARD_HTML
                }

                fetch(THIS_CARD_HTML)
                    .then(response => response.text())
                    .then(cardHTML => {
                        const cardElement = document.createElement("div");
                        cardElement.innerHTML = cardHTML;

                        // Populate fields dynamically
                        cardElement.querySelector("#card-name").textContent = card.name;
                        
                        
                        if (Array.isArray(card.artUrl) && card.artUrl.length > 0) {
                            // If artUrl is an array, use the first image (or implement your own logic)
                            const cardImage = cardElement.querySelector("#card-art");
                            cardImage.src = card.artUrl[0]; // Set the first image
                            cardImage.style = "position:absolute; left: 0; top: 0; width: 50%;"

                            const cardImageSecond = cardElement.querySelector("#card-art-two");
                            if (cardImageSecond) { // Check if the second image exists
                                cardImageSecond.src = card.artUrl[1]; // Set the second image
                                cardImageSecond.style= "position:absolute; right: 0; top: 0; width: 50%;";
                            }
                        } else if (card.artUrl && card.artUrl !== "") {
                            const cardImageSecond = cardElement.querySelector("#card-art-two");
                            cardImageSecond.style = "display:none;";
                            // If artUrl is a string and not empty, set it directly
                            const cardImage = cardElement.querySelector("#card-art");
                            cardImage.src = card.artUrl;
                        }

                        // Load location icon
                        if (card.location && card.location !== "") {
                            const image_path = getClosestImageName(card.location);
                            const locationImage = cardElement.querySelector("#location-art");
                            locationImage.src = image_path;
                        }else{
                            const locationImage = cardElement.querySelector("#location-art");
                            locationImage.style = "display:none;";
                        }

                        if (card.range && card.range > 0){
                            const rangeContainer = cardElement.querySelector("#range-container");
                            for (let i = 0; i < card.range; i++) {
                                const rangeIcon = document.createElement('div');
                                rangeIcon.classList.add('range-icon');
                                
                                // Create the img element
                                const img = document.createElement('img');
                                img.src = "assets/extra_icons/range_icon.webp"; // Image source
                                img.alt = "xd"; // Alt text for accessibility
                                
                                // Append the image to the div
                                rangeIcon.appendChild(img);
                                rangeContainer.appendChild(rangeIcon);
                            } 
                        }else{
                            const rangeContainer = cardElement.querySelector("#range-container");
                            rangeContainer.style = "display:none;";
                        }

                        if (card.bottomtext && card.bottomtext !== ""){
                            const bottomTextContainer = cardElement.querySelector("#bottom-text-container");
                            bottomTextContainer.innerHTML = "<span>"+card.bottomtext+"</span>";
                        }else{
                            const bottomTextContainer = cardElement.querySelector("#bottom-text-container");
                            bottomTextContainer.style = "display:none;";
                        }

                        // Add flames for card burning if needed
                        if (card.burning && card.burning != 0){
                            
                        }else{
                            const flameContainer = cardElement.querySelector("#flame-container");
                            flameContainer.style = "display:none;";
                        }

                        // Load card description
                        cardElement.querySelector("#card-description").innerHTML = card.description;

                        // Render mana cost squares if card type is player
                        if (card.type === 'player' && card.cost) {
                            renderManaCost(cardElement, card.cost)
                        }

                        if (card.power) {
                            renderCardPower(cardElement, card.power);
                        }

                        // Append card to container
                        cardsContainer.appendChild(cardElement)    
                    });
            });
        })
        .catch(err => console.error("Failed to load card data:", err));
});

function renderManaCost(cardElement, cost) {
    const manaContainer = cardElement.querySelector("#mana-cost-container");
    cost.forEach(manaColor => {
        const manaSquare = document.createElement("div");
        manaSquare.classList.add("mana-cost-square");


        // Choose the proper color for element
        if (manaColor.includes('/')) {
            const parts = manaColor.split('/');
            if (parts.length > 2){
                manaSquare.style.background = `linear-gradient(45deg, ${parts[0]} 33%, black 34%, ${parts[1]} 34%, ${parts[1]} 64%, black 65%, ${parts[2]} 66%)`;
            }else{
                manaSquare.style.background = `linear-gradient(45deg, ${parts[0]} 49%, black 50%, ${parts[1]} 51%)`;
            }
        }else{
            manaSquare.style.backgroundColor = manaColor; // Set the color of the square
        }
        manaContainer.appendChild(manaSquare);
    });
}

function renderCardPower(cardElement, power) {
    const powerContainer = cardElement.querySelector("#power-container"); // Add an appropriate container in your HTML template
    power.forEach(([color, value]) => {
        const powerElement = document.createElement("div");
        powerElement.classList.add("power-element");

        // Set the styles based on power color
        powerElement.style.backgroundColor = color;
        // Choose the proper color for element
        if (color.includes('/')) {
            const parts = color.split('/');
            if (parts.length > 2){
                powerElement.style.background = `linear-gradient(45deg, ${parts[0]} 33%, black 34%, ${parts[1]} 34%, ${parts[1]} 64%, black 65%, ${parts[2]} 66%)`;
            }else{
                powerElement.style.background = `linear-gradient(45deg, ${parts[0]} 49%, black 50%, ${parts[1]} 51%)`;
            }
        }else{
            powerElement.style.backgroundColor = color; // Set the color of the square
        }

        powerElement.textContent = value; // Display the value

        powerContainer.appendChild(powerElement);
    });
}

function getClosestImageName(inputString) {
    // Search for the input string in the image names
    const result = fuse.search(inputString);
  
    // Check if any results are found, return the closest match
    if (result.length > 0) {
      const closestImage = result[0].item;  // The item is the matched image name
      return `assets/locations/${closestImage}`;
    } else {
      return "No match found";
    }
}

function swapElements(cardElement, element1Id, element2Id) {
    const element1 = cardElement.querySelector(`#${element1Id}`);
    const element2 = cardElement.querySelector(`#${element2Id}`);
    
    if (element1 && element2) {
        const parent = element1.parentNode;
        parent.insertBefore(element2, element1);
    } else {
        console.error("Elements not found inside the card element.");
    }
}