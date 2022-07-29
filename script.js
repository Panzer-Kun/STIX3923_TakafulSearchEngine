let searchBox = document.querySelector('#SearchBox');
let searchButton = document.querySelector('#SearchBtn');
let searchResult = document.querySelectorAll('.resultText');
let resultTitle = document.querySelectorAll('.resultTitle');
let dataList = document.querySelector('#KeywordSuggestion');
let selectedChoice = document.querySelector('#choice');
let csvData = [];


window.onload = setAutoComplete;

const searchEngineURL ='https://63c9-2001-e68-5403-474f-b936-71a0-e364-7da4.ap.ngrok.io/search';

searchButton.addEventListener('click', click);

searchBox.addEventListener("keyup", (evt) => {
    if (evt.key === "Enter") click();
});

function click() {
    let query = searchBox.value;
    searchBox.value = '';  
    console.log(query);
    let formatted = query.replace(' ', '+');
    window.location.href="./search.html?q=" + formatted;

    /*fetch(searchEngineURL + '?q=' + formatted)
    .then(response => {
        if (response.ok) {
            return response.json();
        }
    })
    .then(data => {
        console.log(data);
        resultTitle.innerText = data['query'];
        searchResult.innerText = data['retrieved'];
    });*/
}

function getParam(q) {
    let params = new URLSearchParams(q);
    if (params.has('q')) {
        query= params.get('q');

        searchBox.value = query;

        fetch(searchEngineURL + window.location.search)
        .then(response => {
            if (response.ok) {
                return response.json();
            }
        })
        .then(data => {
            console.log(data);
            resultTitle[0].innerText = data['query'];
            searchResult[0].innerText = data['retrieved'];
        });
        fetch(searchEngineURL + window.location.search + '&model=glove')
        .then(response => {
            if (response.ok) {
                return response.json();
            }
        })
        .then(data => {
            console.log(data);
            resultTitle[1].innerText = data['query'];
            searchResult[1].innerText = data['retrieved'];
        });
    }
    else {
        window.location = "./";
    }
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
    if(window.location.pathname.includes("/search.html")){
        getParam(window.location.search);
    }
   

    Papa.parse("https://panzer-kun.github.io/SearchEngine/AIA_TakafulCombinedLatest.csv", {
        download: true,
        complete: data => {
            console.log(data);
            csvData = data.data;
            
            setList();
        },
    });
}

function setList(reset) {
    if (reset != null) searchBox.value = "";
    document.querySelectorAll("#KeywordSuggestion > option").forEach(item => item.remove());

    let cat = selectedChoice.value;

    let choices = [];

    csvData.forEach(element => {
        if (element[2] === cat) {
            choices.push(element);
        }
    });

    console.log("Updated choices: " + choices.length);

    choices.forEach(element => {
        let option = document.createElement("option");
        option.value = element[0];
        dataList.appendChild(option);
    });
}

selectedChoice.addEventListener("change", () => setList(true));
