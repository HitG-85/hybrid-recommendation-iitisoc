const express = require("express");
const pool = require("../config/db");
const router = express.Router();

router.get("/recommendations/:userId", async (req, res) => {
  const userId = parseInt(req.params.userId, 10);
  const start = Date.now();
  if (Number.isNaN(userId)) {
    return res.status(400).json({
      error: "Invalid userId",
      details: "userId must be a valid integer",
    });
  }

  try {
    const query = `
      SELECT user_id, item_id, score, rank
      FROM recommendations
      WHERE user_id = $1
      ORDER BY rank
      LIMIT 10
    `;
    const { rows } = await pool.query(query, [userId]);
    const end = Date.now();

    console.log(`Recommendation DB query took ${end - start} ms`);
    return res.json(rows);
  } catch (error) {
    const end = Date.now();
    console.error(`Recommendation DB query failed after ${end - start} ms`, error);
    return res.status(500).json({
      error: "Failed to fetch recommendations",
      details: error.message,
    });
  }
});

module.exports = router;