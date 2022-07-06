// Leafly Database Test

const inputEl = document.getElementById("input-el")
const inputBtn = document.getElementById("input-btn")
const nameEl = document.getElementById("name-el")
const resultEl = document.getElementById("result-el")
const namesBtn = document.getElementById("names-btn")
const imgEl = document.getElementById("img-el")
const randomBtn = document.getElementById("random-btn")

function toObject(names, values) {
	// might be useful to use on some types of data
    let result = {};
    for (let i = 0; i < names.length; i++)
         result[names[i]] = values[i];
    return result;
}

namesBtn.addEventListener("click", function() {
	
	// clear screen
	nameEl.textContent = ""
	resultEl.innerHTML = ""
	imgEl.innerHTML = ""

	url = `http://127.0.0.1:5000/names`

	const request = new XMLHttpRequest()
	request.open('GET', url, true)
	
	request.onload = function () {
		console.log(this.response)
		const data = JSON.parse(this.response)
		console.log(data)
		// resultEl.innerHTML = data
		// PROBLEM: if null value returned, get a CORS error on flask: may need to fix in flask
		// display strain doesnt exist message if null received from request
		// for (let i = 0; i < data.length; i++)
		// 	resultEl.innerHTML += `${data[i]}<br>`
	}
})

inputBtn.addEventListener("click", function() {

	// clear screen
	nameEl.textContent = ""
	resultEl.innerHTML = ""
	imgEl.innerHTML = ""
	const name = inputEl.value

	// create request text containing input strain name
	url = `http://127.0.0.1:5000/strain/${name}`

	// Send request to flask API address
	const request = new XMLHttpRequest()
	request.open('GET', url, true)
	
	request.onload = function() {
		const data = JSON.parse(this.response)
		// PROBLEM: if null value returned, get a CORS error on flask: may need to fix in flask
		// display strain doesnt exist message if null received from request
		nameEl.textContent = data.name
		resultEl.innerHTML += `<li>Type: ${data.type}</li>`
		resultEl.innerHTML += `<li>THC level: ${data.thc_level}%</li>`
		resultEl.innerHTML += `<li>${data.description}.</li><br>`
		imgEl.innerHTML = `<img src="${data.img_url}">`
	}

	request.send()
})

randomBtn.addEventListener("click", function() {
	// randomly pick a strain ID and return data like above
	// may use the same function here
})