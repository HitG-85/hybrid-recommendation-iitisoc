const redis = require("redis");

const client = redis.createClient({
  url: "redis://localhost:6379",
});

client.on("error", (err) => {
  console.error("Redis Client Error", err);
});

let connectionPromise = null;

async function ensureConnected() {
  if (client.isOpen) {
    return client;
  }

  if (!connectionPromise) {
    connectionPromise = client.connect().catch((err) => {
      connectionPromise = null;
      throw err;
    });
  }

  return connectionPromise;
}

async function getCachedRecommendations(key) {
  try {
    await ensureConnected();
    const cached = await client.get(key);
    return cached ? JSON.parse(cached) : null;
  } catch (error) {
    console.error("Redis get failed", error);
    return null;
  }
}

async function setCachedRecommendations(key, value, ttlSeconds = 300) {
  try {
    await ensureConnected();
    await client.setEx(key, ttlSeconds, JSON.stringify(value));
    return true;
  } catch (error) {
    console.error("Redis set failed", error);
    return false;
  }
}

module.exports = {
  client,
  ensureConnected,
  getCachedRecommendations,
  setCachedRecommendations,
};
