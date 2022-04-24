let searchBox = document.querySelector('#SearchBox');
let searchButton = document.querySelector('#SearchBtn');
let searchResult = document.querySelector('#resultText');
let resultTitle = document.querySelector('#resultTitle');
let dataList = document.querySelector("#KeywordSuggestion");

window.onload = setAutoComplete;

const searchEngineURL = 'http://127.0.0.1:5000/search';

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
    /*fetch("https://panzer-kun.github.io/SearchEngine/AIA_TakafulCombined.csv",
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
        });*/
    
    Papa.parse("https://panzer-kun.github.io/SearchEngine/AIA_TakafulCombined.csv", {
        download: true,
        complete: data => {
            console.log(data);
            
            data.data.array.forEach(element => {
                let option = document.createElement("option");
                option.value = element[0];
                dataList.appendChild(option);
            });
        },
    });
}