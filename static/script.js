function updateBuildingSizeLabels() {
    const buildingType = document.getElementById('building-type').value;
    const buildingSizeSelect = document.getElementById('building-size');

    if (buildingSizeSelect && buildingSizeSelect.options.length >= 3) {
        if (buildingType === 'commercial') {
            buildingSizeSelect.options[0].textContent = 'Small (less than 5000sqft)';
            buildingSizeSelect.options[1].textContent = 'Medium (5000 - 10000sqft)';
            buildingSizeSelect.options[2].textContent = 'Large (>10000sqft)';
        } else {
            buildingSizeSelect.options[0].textContent = 'Small (less than 1000sqft)';
            buildingSizeSelect.options[1].textContent = 'Medium (1000 - 3000sqft)';
            buildingSizeSelect.options[2].textContent = 'Large (>3000sqft)';
        }
    } else {
        console.error("Building size select element or its options are not correctly defined.");
    }
}

document.getElementById('building-type').addEventListener('change', updateBuildingSizeLabels);

document.getElementById('retrofit-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let buildingType = document.getElementById('building-type').value;
    let buildingSize = document.getElementById('building-size').value;
    let energyUsage = document.getElementById('energy-usage').value;

    fetch('/get-recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            building_type: buildingType,
            building_size: buildingSize,
            energy_usage: energyUsage
        })
    })
    .then(response => response.json())
    .then(data => {
        let recommendationsHTML = `<h3>${data.message}</h3>`;
        data.recommendations.forEach(function(rec) {
            recommendationsHTML += `<p>${rec}</p>`;
        });

        // Display recommendations in a popup window
        let popupWindow = window.open("", "_blank");
        popupWindow.document.write(`
            <html>
            <head>
                <title>Recommendations</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h3 { color: #333; }
                    p { margin-bottom: 10px; }
                </style>
            </head>
            <body>
                ${recommendationsHTML}
            </body>
            </html>
        `);
        popupWindow.document.close();
    })
    .catch(error => {
        console.error('Error fetching recommendations:', error);
        let popupWindow = window.open("", "_blank");
        popupWindow.document.write('<p>Sorry, an error occurred while fetching the recommendations.</p>');
        popupWindow.document.close();
    });
});
