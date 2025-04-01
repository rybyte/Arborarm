import React from "react";
import { DronTypes } from "./sections/DronTypes";
import { Footer } from "./sections/Footer";
import "./style.css";

export const ElementX = () => {
  return (
    <div className="element-x">
      <div className="div-2">
        <div className="overlap-group">
          <div className="about-drons">
            <div className="arbor-arm">ARBORARM</div>

            <p className="text-wrapper-13">
              Aerial Recovery System for Residential Areas
            </p>
          </div>
        </div>

        <img
          className="FPV-DRONE"
          alt="Fpv DRONE"
          src="https://c.animaapp.com/9xMPmSwX/img/fpv-drone.png"
        />

        <DronTypes />
        <img
          className="LOGO"
          alt="Logo"
          src="https://c.animaapp.com/9xMPmSwX/img/logo-5.png"
        />

        <header className="header">
          <div className="frame">
            <div className="navbar">
              <div className="text-wrapper-14">Home</div>

              <div className="text-wrapper-15">Technology</div>

              <div className="text-wrapper-16">Training</div>

              <div className="text-wrapper-17">About Us</div>
            </div>

            <div className="group-7">
              <div className="text-wrapper-18">Sign in</div>

              <div className="text-wrapper-19">/</div>

              <div className="text-wrapper-20">Sign up</div>
            </div>

            <div className="bg" />
          </div>
        </header>

        <Footer />
      </div>
    </div>
  );
};
