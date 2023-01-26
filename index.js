const express = require('express')
const app = express()
const YAML = require('yaml')

var services = [];

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