import axios from "axios";
import { useState, useEffect, useRef, useCallback } from "react";
import "./App.css";

function App() {

  const [videos, setVideos] = useState([]); 

  const [latency, setLatency] = useState(0);

  const [loading, setLoading] = useState(false);

  const [totalLatency, setTotalLatency] = useState(0);

  const [expandedCards, setExpandedCards] = useState({});

  const loadingRef = useRef(false);

  const totalStartRef = useRef(0);

  const videoRefs = useRef([]);

  const pageRef = useRef(1);

  const videom = {
    beauty:"/videos/beauty.mp4",
    food:"/videos/food.mp4",
    fitness:"/videos/fitness.mp4",
    travel:"/videos/travel.mp4",
    education:"/videos/education.mp4",
    fashion:"/videos/fashion.mp4",
    gaming:"/videos/gaming.mp4",
    sports:"/videos/sports.mp4",
    comedy:"/videos/comedy.mp4",
    tech:"/videos/tech.mp4",
    memes:"/videos/memes.mp4",
    music:"/videos/music.mp4",
    news:"/videos/news.mp4",
    
  };

  const toggleCreator = (index) => {
  setExpandedCards((prev) => ({ ...prev, [index]: !prev[index] }));
  };

  const fetchRecommendations = useCallback(async () => {
    if (loadingRef.current) return;
    loadingRef.current = true;
    setLoading(true);
    try {
      totalStartRef.current = performance.now();
      const start = performance.now();
      const response = await axios.get(`http://localhost:5100/recommendations/1?page=${pageRef.current}`);
      if (response.data.length === 0) {return;}
      const end = performance.now();
      setLatency(Math.round(end - start));
      const mappedVideos = response.data.map((item) => ({
        video: videom[item.category],
      }));
      setVideos((prev) => [...prev, ...mappedVideos]);
      pageRef.current++;
      } catch (err) {
      console.error(err);
      } finally {
      loadingRef.current = false;
      setLoading(false);
      }
      }, []);

  useEffect(() => {
    fetchRecommendations();
  }, [fetchRecommendations]);

  useEffect(() => {
    if (videos.length > 0) {
      const end = performance.now();
      setTotalLatency(Math.round(end - totalStartRef.current));
    }
  }, [videos]);

  
  const observerRef = useRef(null);

  const botRef = useCallback(
    (node) => {    
      if (observerRef.current) {
        observerRef.current.disconnect();
      }
      observerRef.current = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && !loadingRef.current) {
          fetchRecommendations();
        }
      });
      if (node) {
        observerRef.current.observe(node);
      }},
      [fetchRecommendations]
      );

  useEffect(() => {
    return () => {
      if (observerRef.current) observerRef.current.disconnect();
    };
  }, []);

  useEffect(() => {
    const videoObserver = new IntersectionObserver(
     (entries) => {
      entries.forEach((entry) => {
      const video = entry.target;
      if (entry.isIntersecting) {
        video.play();}
      else {
                    video.pause();
                }
      });
      },
      {
           threshold: 0.7,
        }
      );
      videoRefs.current.forEach((video) => {
        if (video) {
            videoObserver.observe(video);
        }
       });
     return () => {
        videoObserver.disconnect();
    };
    }, [videos]);

  return (
    <>
      <header className="header">
        <div className="fst">Hybrid</div>
        <div className="logo">Recommender</div>
      </header>

      <div className="container">
        <aside className="sidebar">
          <div className="sidebar-top">
            <h2>Discover</h2>
            <div className="menu active">
              <i className="fa-solid fa-house"></i>
              <span>Home</span>
            </div>
            <div className="menu">
              <i className="fa-solid fa-fire"></i>
              <span>Trending</span>
            </div>
            <div className="menu">
              <i className="fa-solid fa-heart"></i>
              <span>Liked</span>
            </div>
            <div className="menu">
              <i className="fa-solid fa-bookmark"></i>
              <span>Saved</span>
            </div>
          </div>
          <div className="interest-section">
            <h3>Your Interests</h3>
            <div className="interest-list">
              <div className="interest">Technology</div>
              <div className="interest">Gaming</div>
              <div className="interest">Movies</div>
              <div className="interest">Music</div>
              <div className="interest add-interest">+ Add Interest</div>
            </div>
          </div>
        </aside>

        <main className="content">
          {videos.map((video, index) => (
            <div
              className="recommendation-card"
              key={index}
              ref={index === videos.length - 1 ? botRef : null}
            >
              <div className="videow">
              <video className="vd"  muted loop controls={false}  ref={(el) => (videoRefs.current[index] = el)}>
                <source src={video.video} type="video/mp4" />
              </video>
              <div
  className={`creator-info ${expandedCards[index] ? "expanded" : ""}`}
  onClick={() => toggleCreator(index)}
>
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXDHgy4mAawWIxo8VpdUhUESZMbZW2S6E-CsaYLOKNxQ&s"   className="dp"/>
  {expandedCards[index] && (
    <div className="creator-text">
      <p className="creator-name">Hybrid Recommender</p>
      <p className="creator-title">Recommended For You</p>
    </div>
  )}
</div>
              <div className="action-buttons">
                <button className="action-btn">
                  <img  src="https://www.freepnglogos.com/uploads/like-png/like-icon-line-iconset-iconsmind-35.png" className="ic"/>
                </button>
                <button className="action-btn">
                  <img src="https://www.freeiconspng.com/uploads/share-sharing-icon-29.png" className="ic" />
                </button>
                <button className="action-btn">
                  <img src="https://www.shareicon.net/download/2017/05/24/886404_save_512x512.png" className="ic"/>
                </button>
              </div>
              </div>
            </div>
          ))}
        </main>

        <aside className="latency">
          <h2>Performance</h2>
          <div className="latency-card">
            <p>API Latency</p>
            <span>{latency} ms</span>
          </div>
          <div className="latency-card">
            <p>Total Latency</p>
            <span>{totalLatency} ms</span>
          </div>
        </aside>
        
      </div>
    </>
  );
}

export default App;
