import { useEffect, useState } from "react";
import {
  Stage,
  Layer,
  Rect,
  Text,
  Group,
  Line,
} from "react-konva";

import {
  Streamlit,
  withStreamlitConnection,
} from "streamlit-component-lib";


function App(props) {
  const args = props.args || {};

  const furniture = args.furniture || [];
  const roomWidth = Number(args.room_width || 400);
  const roomLength = Number(args.room_length || 300);
  const roomHeight = Number(args.room_height || 250);

  const maxWidth = 700;
  const maxHeight = 500;

  const scaleX = maxWidth / roomWidth;
  const scaleY = maxHeight / roomLength;
  const scale = Math.min(scaleX, scaleY);

  const roomWidthPx = roomWidth * scale;
  const roomLengthPx = roomLength * scale;

  const roomX=80;
  const roomY=60;

  const [items, setItems] = useState(furniture);


  // When Python sends updated furniture,
  // update the Konva furniture list.
  useEffect(() => {
    setItems(furniture);
  }, [JSON.stringify(furniture)]);


  // Tell Streamlit how tall the component should be.
  useEffect(() => {
    Streamlit.setFrameHeight(roomLengthPx + 80);
  }, [roomLengthPx]);


  function handleDragEnd(index, e) {
    const group = e.target;

    // Convert pixels back to centimeters.
    const newX = (group.x() - roomX) / scale;
    const newY = (group.y() - roomY) / scale;

    const updatedItems = items.map((item, i) => {
      if (i === index) {
        return {
          ...item,
          x: newX,
          y: newY,
        };
      }

      return item;
    });
    
    // Update React immediately.
    setItems(updatedItems);

    // Send ALL furniture positions back to Python.
    Streamlit.setComponentValue(updatedItems);
  }


  return (
    <Stage
      width={roomWidthPx + 140}
      height={roomLengthPx + 140}
    >
      <Layer>

        {/* Room boundary */}
        <Rect
          x={roomX}
          y={roomY}
          width={roomWidthPx}
          height={roomLengthPx}
          stroke="black"
          strokeWidth={3}
        />
        {/* Room width dimension */}
        <Line
          points={[
            roomX,
            roomY - 25,
            roomX + roomWidthPx,
            roomY - 25
          ]}
          stroke="black"
          strokeWidth={1}
        />

        <Line
          points={[
            roomX,
            roomY - 32,
            roomX,
            roomY - 18
          ]}
          stroke="black"
        />

        <Line
          points={[
            roomX + roomWidthPx,
            roomY - 32,
            roomX + roomWidthPx,
            roomY - 18
          ]}
          stroke="black"
        />

        <Text
          x={roomX}
          y={roomY - 48}
          width={roomWidthPx}
          align="center"
          text={`${roomWidth.toFixed(1)} cm`}
          fontSize={14}
        />


        {/* Room length dimension */}
        <Line
          points={[
            roomX - 30,
            roomY,
            roomX - 30,
            roomY + roomLengthPx
          ]}
          stroke="black"
          strokeWidth={1}
        />

        <Line
          points={[
            roomX - 37,
            roomY,
            roomX - 23,
            roomY
          ]}
          stroke="black"
        />

        <Line
          points={[
            roomX - 37,
            roomY + roomLengthPx,
            roomX - 23,
            roomY + roomLengthPx
          ]}
          stroke="black"
        />

        <Text
          x={10}
          y={roomY + roomLengthPx / 2 - 10}
          text={`${roomLength.toFixed(1)} cm`}
          fontSize={14}
          rotation={-90}
        />
        <Text
          x={30}
          y={30}
          text={`Room: ${roomWidth.toFixed(1)} × ${roomLength.toFixed(1)} cm\nHeight: ${roomHeight.toFixed(1)} cm`}
          fontSize={16}
          fill="black"
          listening={false}
        />


        {/* Furniture */}
        {items.map((item, index) => {
          const widthPx =
            Number(item.width) * scale;

          const depthPx =
            Number(item.depth) * scale;
          
          const rotation = Number(
            item.rotation || 0
          );

          const displayWidthPx =
            rotation === 90 || rotation === 270
              ? depthPx
              : widthPx;

          const displayDepthPx =
            rotation === 90 || rotation === 270
              ? widthPx
              : depthPx;
     

          const x =
            roomX + Number(item.x) * scale;

          const y =
            roomY + Number(item.y) * scale;


          return (
            <Group
              key={item.id}
              x={x}
              y={y}
              draggable={true}

              dragBoundFunc={(pos) => {
                const minX = roomX;
                const minY = roomY;

                const maxX =
                  roomX +
                  roomWidthPx -
                  displayWidthPx;

                const maxY =
                  roomY +
                  roomLengthPx -
                  displayDepthPx;

                return {
                  x: Math.max(
                    minX,
                    Math.min(pos.x, maxX)
                  ),

                  y: Math.max(
                    minY,
                    Math.min(pos.y, maxY)
                  ),
                };
              }}

              onDragEnd={(e) =>
                handleDragEnd(index, e) 

                
              }
            >

              {/* Furniture rectangle */}
              <Rect
                x={0}
                y={0}
                width={displayWidthPx}
                height={displayDepthPx}
                fill="#dddddd"
                stroke="black"
                strokeWidth={2}
              />
              {/* Furniture width dimension */}
              <Line
                points={[
                  0,
                  -12,
                  displayWidthPx,
                  -12
                ]}
                stroke="black"
                strokeWidth={1}
              />

              <Text
                x={0}
                y={-30}
                width={displayWidthPx}
                align="center"
                text={`${
                  rotation === 90 || rotation === 270
                    ? Number(item.depth).toFixed(1)
                    : Number(item.width).toFixed(1)
                } cm`}
                fontSize={12}
              />


              {/* Furniture depth dimension */}
              <Line
                points={[
                  displayWidthPx + 12,
                  0,
                  displayWidthPx + 12,
                  displayDepthPx
                ]}
                stroke="black"
                strokeWidth={1}
              />

              <Text
                x={displayWidthPx + 18}
                y={displayDepthPx / 2}
                text={`${
                  rotation === 90 || rotation === 270
                    ? Number(item.width).toFixed(1)
                    : Number(item.depth).toFixed(1)
                } cm`}
                fontSize={12}
                rotation={90}
              />


              {/* Furniture name */}
              <Text
                x={0}
                y={depthPx / 2 - 16}
                width={displayWidthPx}
                text={`${item.name}\n${Number(item.width).toFixed(1)} × ${Number(item.depth).toFixed(1)} cm`}
                align="center"
                fontSize={14}
                listening={false}
              />


            </Group>
          );
        })}

      </Layer>
    </Stage>
  );
}


export default withStreamlitConnection(App);