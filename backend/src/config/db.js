const { Pool } = require("pg");

const pool = new Pool({
    user: "shivikasingh",
    host: "localhost",
    database: "hybrid_recommendation_db",
    password: "",
    port: 5432,
});

module.exports = pool;