let searchBox = document.querySelector('#SearchBox');
let searchButton = document.querySelector('#SearchBtn');
let searchResult = document.querySelector('#resultText');
let resultTitle = document.querySelector('#resultTitle');

window.onload = setAutoComplete;

const searchEngineURL = 'https://dd54-2001-e68-5403-a01f-d892-2e49-ff08-e880.ap.ngrok.io/search';

searchButton.addEventListener('click', click);

function click() {
    let query = searchBox.value;
    searchBox.value = '';  
    console.log(query);
    let formatted = query.replace(' ', '+');

    fetch(searchEngineURL + '?q=' + formatted)
    .then(response => {
        if (response.ok) {
            return response.json();
        }
    })
    .then(data => {
        console.log(data);
        resultTitle.innerText = data['query'];
        searchResult.innerText = data['retrieved'];
    })
}

//"https://raw.githubusercontent.com/Panzer-Kun/SearchEngine/main/AIA_TakafulCombined.csv"
function setAutoComplete() {
    fetch("https://panzer-kun.github.io/SearchEngine/AIA_TakafulCombined.csv",
        {
            method: "get",
            headers: {
                "content-type": "text/csv; charset=UTF-8",
            },
        })
        .then(response => {
            if (response.ok) {
                return response.text();
            }
        })
        .then(data => {
            console.log(data);
        })
}
