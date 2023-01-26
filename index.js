const express = require('express')
const app = express()


app.get('/', (req, res) => res.send('Hello World!'))

if (process.env.NODE_ENV !== 'test') {
  app.listen(3000, () => console.log('Example app listening on port 3000!'))
}

/*
const http = require('http');
const server = http.createServer(app);
const port = 3000;
server.listen(port, () => console.log(`Example app listening on port ${port}!`));
*/

// export 'app'
module.exports = app