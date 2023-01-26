const express = require('express')
const app = express()

var services = [];

/*
// Load services from github on startup
const https = require('https');
const url = "https://raw.githubusercontent.com/kubero-dev/kubero/main/services/index.yaml"
https.get(url, (resp) => {
    let data = '';
    resp.on('data', (chunk) => {
        data += chunk;
    });
    resp.on('end', () => {
        services = YAML.parse(data);
    });
}).on("error", (err) => {
    console.log("Error: " + err.message);
});
*/

// load services from local json file
const fs = require('fs');
const path = require('path');
const indexPath = path.join(__dirname, 'index.json');

try {
    const s = fs.readFileSync(indexPath, 'utf8');
    services = JSON.parse(s);
} catch (err) {
    console.error(err)
}


// GET / - return list of services
app.get('/', (req, res) => {
    console.log(req.headers['x-forwarded-for'], req.headers['user-agent'])
    res.json(services)
})

module.exports = app

// Local testing
if (process.env.NODE_ENV == 'test') {
  app.listen(3000, () => console.log('Example app listening on port 3000!'))
}