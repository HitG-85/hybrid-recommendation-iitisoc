import axios from "axios";
import {useState,useEffect,useRef} from "react";
import "./App.css";

function App() {
  const [videos,setVideos]=useState([]);
  const [latency, setLatency] = useState(0);
  const [loading, setLoading] = useState(false);
const videom = {
  beauty: "/videos/beauty.mp4",
  food: "/videos/food.mp4",
  fitness: "/videos/fitness.mp4",
  travel: "/videos/travel.mp4",
  education: "/videos/education.mp4",
  fashion: "/videos/fashion.mp4",
  gaming: "/videos/gaming.mp4",
  sports: "/videos/sports.mp4",
  comedy: "/videos/comedy.mp4",
  tech: "/videos/tech.mp4",
  memes: "/videos/memes.mp4",
};
  
async function fetchRecommendations() {

    if (loading) return;

    setLoading(true);

    try {

        const start = performance.now();

        const response = await axios.get(
            "http://localhost:5100/recommendations/1"
        );

        const end = performance.now();
        setLatency(Math.round(end - start));

        const mappedVideos = response.data.map(item => ({
            video: videom[item.category]
        }));

        setVideos(prev => [...prev, ...mappedVideos]);

    } catch (err) {

        console.error(err);

    } finally {

        setLoading(false);

    }
}
useEffect(() => {
    fetchRecommendations();
}, []);
const botref = useRef(null);

useEffect(() => {
    const observer = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting && !loading) {
            fetchRecommendations();
        }
    });
    const current = botref.current;

    if (current) {
        observer.observe(current);
    }

    return () => {
        if (current) observer.unobserve(current);
    };
}, []);
    return (
        <>
            <div className="nav">
                <div className="bnm">
                    HYBRID-RECOMMENDER
                </div>
                <div className="lt">
                    <div className="hd">TOTAL LATENCY</div>
                    <div className="apilt">API Latency:{latency}ms</div>
                    <div className="ml">ML Compute Latency:</div>
                </div>
            </div>
            {videos.map((video,index)=>(
            <div className="disp" key={index}  ref={index === videos.length - 1 ? botref : null}>
                <video className="vd" autoPlay muted loop controls={false}>
                <source src={video.video} type="video/mp4" />
                 </video>
                <div className="btns">
                    <div className="b1 b">
                        <img src="https://www.freepnglogos.com/uploads/like-png/like-icon-line-iconset-iconsmind-35.png" alt="" className="lk" />
                    </div>
                    <div className="b2 b">
                        <img src="https://www.freeiconspng.com/uploads/share-sharing-icon-29.png" alt="" className="shr" />
                    </div>
                    <div className="b3 b">
                        <img src="https://www.shareicon.net/download/2017/05/24/886404_save_512x512.png" alt="" className="sv" />
                    </div>
                </div>
            </div>
            ))}

        </>
    );
}

export default App;