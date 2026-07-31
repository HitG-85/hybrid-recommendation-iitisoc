const express = require("express");
const pool = require("../config/db");
const { getCachedRecommendations, setCachedRecommendations } = require("../config/redis");
const router = express.Router();

router.get("/recommendations/:userId", async (req, res) => {
  const userId = parseInt(req.params.userId, 10);
  const page = parseInt(req.query.page || "1", 10);
  const limit = 10;
  const offset = (page - 1) * limit;
  const start = Date.now();
  if (Number.isNaN(userId)) {
    return res.status(400).json({
      error: "Invalid userId",
      details: "userId must be a valid integer",
    });
  }

  try {
    const cacheKey = `recommendations:user:${userId}:page:${page}`;
    const cached = await getCachedRecommendations(cacheKey);

    if (cached) {
      return res.json({
        recommendations: cached,
        queryTime: 0,
        cacheStatus: "HIT",
      });
    }

    const query = `
      SELECT
        r.user_id,
        r.item_id,
        i.category,
        r.score,
        r.rank
      FROM recommendations r
      JOIN items i
      ON r.item_id = i.id
      WHERE r.user_id = $1
      ORDER BY r.rank
      LIMIT $2
      OFFSET $3
    `;
    const { rows } = await pool.query(query, [userId, limit, offset]);
    const end = Date.now();
    const queryTime = end - start;

    await setCachedRecommendations(cacheKey, rows);

    console.log(`Recommendation DB query took ${queryTime} ms`);
    return res.json({
      recommendations: rows,
      queryTime,
      cacheStatus: "MISS",
    });
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