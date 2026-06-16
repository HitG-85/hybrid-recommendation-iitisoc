const express = require("express");
const pool = require("./config/db");

const app = express();

pool.connect()
    .then(() => {
        console.log("Connected to PostgreSQL");
    })
    .catch((err) => {
        console.error("Connection failed:", err);
    });

app.get("/", (req, res) => {
  res.send("Backend is running");
});

app.listen(5100, () => {
  console.log("Server running on port 5100");
});