import { useEffect, useState } from "react";
import { Image as KonvaImage } from "react-konva";
import bedIconPath from "../../../icons/bed_icon.png";
import sofaIconPath from "../../../icons/sofa_icon.png";
import cabinetIconPath from "../../../icons/cabinet.png";
import chairIconPath from "../../../icons/chair.png";
import deskIconPath from "../../../icons/desk.png";
import diningTableIconPath from "../../../icons/dining_table.png";
import fridgeIconPath from "../../../icons/fridge.png";
import rugIconPath from "../../../icons/rug.png";

const ICON_PATHS = {
  Bed: bedIconPath,
  Sofa: sofaIconPath,
  Cabinet: cabinetIconPath,
  Chair: chairIconPath,
  Desk: deskIconPath,
  "Dining table": diningTableIconPath,
  Fridge: fridgeIconPath,
  Rug: rugIconPath,
  Other: cabinetIconPath,
};

export const FURNITURE_ICON_TINTS = {
  Bed: null,
  Sofa: null,
  Cabinet: null,
  Chair: null,
  Desk: null,
  "Dining table": null,
  Fridge: null,
  Rug: null,
  Other: null,
};

function DefaultIcon({ type, width, height, tint = null }) {
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
      if (type === "Rug") {
        const pixels = context.getImageData(0, 0, canvas.width, canvas.height);
        for (let index = 0; index < pixels.data.length; index += 4) {
          const [red, green, blue] = pixels.data.slice(index, index + 3);
          if (red > 246 && green > 246 && blue > 246) {
            pixels.data[index + 3] = 0;
          }
        }
        context.putImageData(pixels, 0, 0);
      }
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

  const fit = Math.min(width / image.width, height / image.height);
  const imageWidth = image.width * fit;
  const imageHeight = image.height * fit;

  return (
    <KonvaImage
      image={image}
      x={(width - imageWidth) / 2}
      y={(height - imageHeight) / 2}
      width={imageWidth}
      height={imageHeight}
    />
  );
}

export default DefaultIcon;
