const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const config = require('./config');

const app = express(); //this is our application/website, which is important

app.use(express.json());
app.use(cors());
app.use(bodyParser.json());

app.use(bodyParser.urlencoded({ extended: true }));

app.listen(config.port, () => console.log('App is listening on url http://localhost:' + config.port));
