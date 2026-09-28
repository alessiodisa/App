// Serves the latest United Instagram posts to the site's carousel.
// Reads the access token from the IG_ACCESS_TOKEN environment variable
// (set in Netlify site settings, never committed to the repo).
exports.handler = async function () {
  const token = process.env.IG_ACCESS_TOKEN;

  if (!token) {
    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ posts: [], configured: false }),
    };
  }

  try {
    const fields = "id,caption,media_type,media_url,thumbnail_url,permalink,timestamp";
    const url = `https://graph.instagram.com/me/media?fields=${fields}&limit=8&access_token=${encodeURIComponent(token)}`;
    const res = await fetch(url);

    if (!res.ok) {
      const detail = await res.text();
      return {
        statusCode: 200,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ posts: [], configured: true, error: detail }),
      };
    }

    const data = await res.json();
    const posts = (data.data || [])
      .filter((p) => p.media_type === "IMAGE" || p.media_type === "CAROUSEL_ALBUM" || p.media_type === "VIDEO")
      .map((p) => ({
        id: p.id,
        caption: (p.caption || "").split("\n")[0].slice(0, 140),
        image: p.media_type === "VIDEO" ? p.thumbnail_url : p.media_url,
        permalink: p.permalink,
      }))
      .filter((p) => p.image);

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
        // Cache for 30 minutes so we don't hammer the Instagram API.
        "Cache-Control": "public, max-age=1800",
      },
      body: JSON.stringify({ posts, configured: true }),
    };
  } catch (err) {
    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ posts: [], configured: true, error: String(err) }),
    };
  }
};
