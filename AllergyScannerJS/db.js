var admin = require("firebase-admin");

var serviceAccount = require("path/to/serviceAccountKey.json");

const db = firebase.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

module.exports = db;