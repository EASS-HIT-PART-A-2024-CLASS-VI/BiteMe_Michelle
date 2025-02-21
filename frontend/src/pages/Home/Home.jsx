import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";
import banner from "../../assets/banner.png"; // Path to your banner image

function Home() {
    return (
        <div className="home">
            <img src={banner} alt="BiteMe Banner" className="home-banner" />
            <div className="home-content">

                <Link to="/restaurants">
                    <button className="home-button">Explore Our Restaurants Now</button>
                </Link>
            </div>
        </div>
    );
}

export default Home;
