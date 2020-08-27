const express = require('express');
const serveStatic = require('serve-static');
const history = require('connect-history-api-fallback');

const app = express();
//add this middleware
app.use(history());

app.use(serveStatic(__dirname + "/dist"));
const port = process.env.PORT || 8000;
app.listen(port);
console.log('server started ' + port);