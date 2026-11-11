import { useEffect, useState } from "react";
import { Image as KonvaImage } from "react-konva";
import bedIconPath from "../../../icons/bed.png";
import sofaIconPath from "../../../icons/sofa.png";
import deskIconPath from "../../../icons/desk.png";
import cabinetIconPath from "../../../icons/cabinet.png";
import chairIconPath from "../../../icons/dining_chair.png";
import armchairIconPath from "../../../icons/armchair.png";
import officeChairIconPath from "../../../icons/office_chair.png";
import diningTableIconPath from "../../../icons/dining_table.png";
import roundDiningTableIconPath from "../../../icons/dinigtable_round.png";
import fridgeIconPath from "../../../icons/fridge.png";
import tvConsoleIconPath from "../../../icons/tvconsole.png";
import rugIconPath from "../../../icons/rug.png";

const ICON_PATHS = {
  Bed: bedIconPath,
  Sofa: sofaIconPath,
  Cabinet: cabinetIconPath,
  Chair: chairIconPath,
  Armchair: armchairIconPath,
  "Office chair": officeChairIconPath,
  Desk: deskIconPath,
  "Dining table": diningTableIconPath,
  "Round dining table": roundDiningTableIconPath,
  Fridge: fridgeIconPath,
  "TV console": tvConsoleIconPath,
  Rug: rugIconPath,
  Other: armchairIconPath,
};

export const FURNITURE_ICON_TINTS = {
  Bed: null,
  Sofa: null,
  Cabinet: null,
  Chair: null,
  Armchair: null,
  "Office chair": null,
  Desk: null,
  "Dining table": null,
  "Round dining table": null,
  Fridge: null,
  "TV console": null,
  Rug: null,
  Other: null,
};

function DefaultIcon({ type, width, height, tint = null, x = 0, y = 0 }) {
  const [image, setImage] = useState(null);
  const imagePath = ICON_PATHS[type] || ICON_PATHS.Other;

  useEffect(() => {
    const loadedImage = new window.Image();
    loadedImage.onload = () => {
      const canvas = document.createElement("canvas");
      canvas.width = loadedImage.naturalWidth;
      canvas.height = loadedImage.naturalHeight;
      const context = canvas.getContext("2d", { willReadFrequently: true });
      if (!context) {
        setImage(loadedImage);
        return;
      }

      context.drawImage(loadedImage, 0, 0);
      if (tint) {
        context.globalCompositeOperation = "source-atop";
        context.globalAlpha = 0.35;
        context.fillStyle = tint;
        context.fillRect(0, 0, canvas.width, canvas.height);
      }
      setImage(canvas);
    };
    loadedImage.src = imagePath;
    return () => {
      loadedImage.onload = null;
    };
  }, [imagePath, tint, type]);

  if (!image) {
    return null;
  }

  return (
    <KonvaImage
      image={image}
      x={x}
      y={y}
      width={width}
      height={height}
    />
  );
}

export default DefaultIcon;
