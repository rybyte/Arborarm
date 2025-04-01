import React from "react";
import "./style.css";

export const DronTypes = () => {
  return (
    <div className="DRON-TYPES">
      <div className="title">
        <div className="types-of-drones">TYPES OF DRONES</div>

        <div className="rectangle" />

        <img
          className="line"
          alt="Line"
          src="https://c.animaapp.com/9xMPmSwX/img/line-1.svg"
        />
      </div>

      <div className="element">
        <p className="div">
          <span className="text-wrapper">01.</span>

          <span className="span"> visuals Model</span>
        </p>
      </div>

      <div className="element-2">
        <p className="div">
          <span className="text-wrapper-2">02.</span>

          <span className="text-wrapper-3"> Retrieval Model</span>
        </p>

        <p className="hardware-as-the">
          <span className="text-wrapper-4">
            Hardware:
            <br />
            <br />
          </span>

          <span className="text-wrapper-5">
            As the Retrieval Model is a larger, enhanced version of Visuals
            Model, it is also a quadcopter for similar said reason.
            <br />
            <br />
            <br />{" "}
          </span>

          <span className="text-wrapper-4">
            Drone Frame:
            <br />
          </span>

          <span className="text-wrapper-5">
            <br />
            Frame 
            <br />
            Like Visual’s Model, Material: Carbon Fibre
            <br />
            Slightly increased size but has a similar design language to
            Visual’s drone
            <br />
            <br />
            Prop Guards 
            <br />
            Currently re-designing the prop guard design and yet to decide on
            material
            <br />
            Prop Size is 8-inch Diameter
            <br />
            <br />
            As the total Size of Drone is including prop guards is 300mm x 300mm
            x 50mm, it is sufficiently small enough to manoeuvre close to the
            trees while strong enough to prevent heavy drift from winds.
          </span>
        </p>

        <p className="electronics">
          <span className="text-wrapper-4">
            Electronics:
            <br />
          </span>

          <span className="text-wrapper-5">
            <br />
          </span>

          <span className="text-wrapper-6">
            Retrieval drone is powered by a 6S (22.2V) LiPo battery system. A
            full list of the Hardware used can be found in Appendix A.2.
            <br />
            <br />
            The drone will be drawing on 12.67 A @ 22.2V, at 50% throttle, and
            49.1 A @ 22.2V at 100% throttle. The power is distributed from the
            battery to the motors, and to the ESC, FC and RPi via the Holybro
            PM06, which is a Power Distribution Board that is giving output of
            5V. 
            <br />
          </span>

          <span className="text-wrapper-5"> </span>

          <span className="text-wrapper-4">
            Flight specifics:
            <br />
          </span>

          <span className="text-wrapper-5">
            <br />
            Based on its weight and power configuration, Visual Model has the
            following characteristics
            <br />
            Average Flight Time: 30 minutes per charge under optimal conditions
            <br />
            Drone Weight: ~700 grams
            <br />
            Max Take-Off Weight (MTOW): ~4000 grams 
            <br />
            <br />
            Comparing the data gathered to other commercially viable drones in
            terms of flight time it is about the same. Additionally, the added
            MTOW would allow us to add on heavier attachments.
            <br />
          </span>
        </p>
      </div>

      <div className="element-wrapper">
        <p className="div">
          <span className="text-wrapper">03.</span>

          <span className="span"> Многороторные дроны</span>
        </p>
      </div>

      <div className="element-ROV-wrapper">
        <p className="div">
          <span className="text-wrapper">04.</span>

          <span className="span"> Подводные дроны (ROV)</span>
        </p>
      </div>

      <div className="div-wrapper">
        <p className="div">
          <span className="text-wrapper">05.</span>

          <span className="span"> Грузовые дроны</span>
        </p>
      </div>

      <div className="element-3">
        <p className="div">
          <span className="text-wrapper">06.</span>

          <span className="span"> Нано-дроны</span>
        </p>
      </div>

      <div className="element-4">
        <p className="div">
          <span className="text-wrapper">07.</span>

          <span className="span"> Одновинтовые вертолеты</span>
        </p>
      </div>

      <div className="element-5">
        <p className="div">
          <span className="text-wrapper">08.</span>

          <span className="span">
            {" "}
            Гибридные дроны вертикального взлета и посадки
          </span>
        </p>
      </div>

      <div className="element-6">
        <p className="div">
          <span className="text-wrapper">09.</span>

          <span className="span"> Дроны вертикального взлета и посадки</span>
        </p>
      </div>

      <div className="element-7">
        <p className="div">
          <span className="text-wrapper">10.</span>

          <span className="span"> Гоночные дроны</span>
        </p>
      </div>

      <div className="element-8">
        <p className="div">
          <span className="text-wrapper">11.</span>

          <span className="span"> Дроны на солнечных батареях</span>
        </p>
      </div>

      <div className="element-9">
        <p className="div">
          <span className="text-wrapper">12. </span>

          <span className="span">Военные и разведывательные дроны</span>
        </p>
      </div>
    </div>
  );
};
