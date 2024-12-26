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
    fetch("data/json/cards.json")
        .then(response => response.json())
        .then(cards => {
            cards.forEach(card => {
                console.log("Card processed")
                // Fetch and insert the card HTML template
                fetch('card.html')
                    .then(response => response.text())
                    .then(cardHTML => {
                        const cardElement = document.createElement("div");
                        cardElement.innerHTML = cardHTML;

                        // Populate fields dynamically
                        cardElement.querySelector("#card-name").textContent = card.name;
                        //cardElement.querySelector("#card-cost").textContent = card.cost;
                        cardElement.querySelector("#card-description").textContent = card.description;
                        // cardElement.querySelector("#card-type").textContent = card.type;

                        // const cardImage = cardElement.querySelector("#card-art");
                        // cardImage.src = card.imageUrl;  // Assuming the image URL is stored in the card data

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

// Function to render mana cost
/*
function renderManaCost(cardElement, cost) {
    const manaContainer = cardElement.querySelector("#mana-cost-container");

    // Assuming cost is an array of colors (e.g., ["red", "green", "blue"])
    cost.forEach(manaColor => {
        const manaSquare = document.createElement("div");
        manaSquare.classList.add("mana-cost-square");
        manaSquare.style.backgroundColor = manaColor; // Set the color of the square
        manaContainer.appendChild(manaSquare);
    });
}
*/