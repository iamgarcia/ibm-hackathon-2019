// Create a request variable and assign a new XMLHttpRequest object to it
const request = new XMLHttpRequest()
const url = 'https://requesthelpnow-insightful-elephant.mybluemix.net/api/reports'
// Open a new connection, using the GET request on the URL endpoint
request.open('GET', url)
// Send request
request.send()

request.onload = function () {

    var data = JSON.parse(this.response)

    if(request.status >= 200 && request.status < 400) {
        data.forEach(report => {
            // Log each report's properties
            console.log(report.desc)
        })
    } else {
        console.log('error')
    }
    
}