const express = require("express");

console.log("File is being executed");

const app = express();

app.get("/", (req, res) => {
  res.send("Backend is running!");
});

app.listen(5100, () => {
  console.log("Server running on port 5100");
});