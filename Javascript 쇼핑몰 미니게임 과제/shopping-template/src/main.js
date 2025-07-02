
//Fetch the items from the Json file
function loadItems(){
    return fetch('data/data.json')
    .then(response => response.json())
    .then(json => json.itmes);
}

// main
loadItems()
.then(items => {
    console.log(items);
   //  displayItems(items);
   //  setEventListener(items) 
})
.catch(console.log)