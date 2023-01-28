const express = require('express')
var cors = require('cors');
const app = express()
app.use(cors());

var services = [];

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