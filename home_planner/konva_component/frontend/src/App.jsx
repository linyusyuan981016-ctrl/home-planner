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

import DefaultIcon, { FURNITURE_ICON_TINTS } from "./defaultIcons.jsx";


function App(props) {
  const args = props.args || {};

  const furniture = args.furniture || [];
  const roomId = String(args.room_id || "default");
  const roomWidth = Number(args.room_width || 400);
  const roomLength = Number(args.room_length || 300);
  const roomHeight = Number(args.room_height || 250);
  const roomLabel = args.room_label || "Room";
  const displayUnit = args.display_unit || "m";
  const rooms = args.rooms || [{
    id: roomId,
    label: roomLabel,
    width: roomWidth,
    length: roomLength,
    height: roomHeight,
    x: 0,
    y: 0,
    openings: [],
  }];
  const unitFactors = { m: 100, inch: 2.54, feet: 30.48 };
  const unitFactor = unitFactors[displayUnit] || 1;
  const formatDimension = (value) => `${(Number(value) / unitFactor).toFixed(2)} ${displayUnit}`;
  const roomColors = args.room_colors || {
    "Living room": "#f4d8d1",
    Bedroom: "#d7d2ef",
    Kitchen: "#e8e1ba",
    Bathroom: "#cfe8f7",
    Other: "#eef2f7",
  };
  const appBackground = "#f7f5f2";

  const canvasWidth = 840;
  const canvasHeight = 640;
  const maxWidth = 700;
  const maxHeight = 500;
  const [planRooms, setPlanRooms] = useState(rooms);
  const minRoomX = Math.min(...planRooms.map((room) => Number(room.x)));
  const minRoomY = Math.min(...planRooms.map((room) => Number(room.y)));
  const maxRoomX = Math.max(...planRooms.map((room) => Number(room.x) + Number(room.width)));
  const maxRoomY = Math.max(...planRooms.map((room) => Number(room.y) + Number(room.length)));
  const planWidth = maxRoomX - minRoomX;
  const planLength = maxRoomY - minRoomY;

  const scaleX = maxWidth / planWidth;
  const scaleY = maxHeight / planLength;
  const scale = Math.min(scaleX, scaleY);

  const planX = 80 - minRoomX * scale;
  const planY = 60 - minRoomY * scale;
  const roomX = planX;
  const roomY = planY;
  const storageKey = `home-planner-furniture-${roomId}`;
  const [items, setItems] = useState(furniture);
  const roomsJson = JSON.stringify(rooms);
  const roomOrigins = new Map(planRooms.map((room) => [room.id, {
    x: planX + Number(room.x) * scale,
    y: planY + Number(room.y) * scale,
  }]));


  // When Python sends updated furniture,
  // update the Konva furniture list.
  const furnitureJson = JSON.stringify(furniture);
  useEffect(() => {
    setItems(JSON.parse(furnitureJson));
  }, [furnitureJson, storageKey]);

  useEffect(() => {
    setPlanRooms(JSON.parse(roomsJson));
  }, [roomsJson]);


  // Tell Streamlit how tall the component should be.
  useEffect(() => {
    Streamlit.setFrameHeight(canvasHeight);
  }, []);


  function handleDragEnd(itemId, e) {
    const group = e.target;
    const item = items.find((candidate) => candidate.id === itemId);
    const origin = roomOrigins.get(item?.room_id) || { x: roomX, y: roomY };

    const newX = (group.x() - origin.x) / scale;
    const newY = (group.y() - origin.y) / scale;

    const updatedItems = items.map((item) => {
      if (item.id === itemId) {
        return {
          ...item,
          x: newX,
          y: newY,
        };
      }

      return item;
    });
    setItems(updatedItems);
    Streamlit.setComponentValue({ furniture: updatedItems, openings: {}, rooms: {} });
  }

  function handleFurnitureResizeEnd(item, event, rotated) {
    event.cancelBubble = true;
    const handle = event.target;
    const displayWidth = Math.max(20, handle.x()) / scale;
    const displayDepth = Math.max(20, handle.y()) / scale;
    const updatedItems = items.map((current) => (
      current.id === item.id
        ? {
            ...current,
            width: rotated ? displayDepth : displayWidth,
            depth: rotated ? displayWidth : displayDepth,
          }
        : current
    ));
    setItems(updatedItems);
    Streamlit.setComponentValue({ furniture: updatedItems, openings: {}, rooms: {} });
  }

  function handleOpeningDragEnd(room, opening, event) {
    event.cancelBubble = true;
    const group = event.target;
    const origin = roomOrigins.get(room.id);
    const absolutePosition = group.getAbsolutePosition();
    const localX = (absolutePosition.x - origin.x) / scale;
    const localY = (absolutePosition.y - origin.y) / scale;
    const candidates = [
      { wall_id: "top", distance: Math.abs(localY) },
      { wall_id: "bottom", distance: Math.abs(localY - Number(room.length)) },
      { wall_id: "left", distance: Math.abs(localX) },
      { wall_id: "right", distance: Math.abs(localX - Number(room.width)) },
    ];
    const wallId = candidates.sort((a, b) => a.distance - b.distance)[0].wall_id;
    const horizontal = wallId === "top" || wallId === "bottom";
    const wallLength = horizontal ? Number(room.width) : Number(room.length);
    const openingLength = Math.min(Number(opening.width), wallLength);
    const offset = Math.max(0, Math.min(
      (horizontal ? localX : localY) - openingLength / 2,
      wallLength - openingLength,
    ));
    const snappedX = horizontal
      ? (offset + openingLength / 2) * scale
      : wallId === "right" ? Number(room.width) * scale : 0;
    const snappedY = horizontal
      ? wallId === "bottom" ? Number(room.length) * scale : 0
      : (offset + openingLength / 2) * scale;
    group.position({ x: snappedX, y: snappedY });
    const updatedRooms = planRooms.map((entry) => ({
      ...entry,
      openings: entry.openings.map((existing) => (
        entry.id === room.id && existing.id === opening.id
          ? { ...existing, wall_id: wallId, offset, width: openingLength }
          : existing
      )),
    }));
    setPlanRooms(updatedRooms);
    const updatedOpenings = Object.fromEntries(updatedRooms.map((entry) => [
      entry.id,
      Object.fromEntries(entry.openings.map((existing) => [existing.id, {
        wall_id: existing.wall_id,
        offset: existing.offset,
        width: existing.width,
      }])),
    ]));
      Streamlit.setComponentValue({ furniture: items, openings: updatedOpenings, rooms: {} });
  }

  function handleRoomDragEnd(room, event) {
    event.cancelBubble = true;
    const handle = event.target;
    const origin = roomOrigins.get(room.id);
    const absolutePosition = handle.getAbsolutePosition();
    const nextX = Number(room.x) + (absolutePosition.x - origin.x - 6) / scale;
    const nextY = Number(room.y) + (absolutePosition.y - origin.y - 6) / scale;
    const updatedRooms = planRooms.map((entry) => (
      entry.id === room.id ? { ...entry, x: nextX, y: nextY } : entry
    ));
    setPlanRooms(updatedRooms);
    Streamlit.setComponentValue({
      furniture: items,
      openings: {},
      rooms: Object.fromEntries(updatedRooms.map((entry) => [
        entry.id,
        { x: entry.x, y: entry.y },
      ])),
    });
  }


  return (
    <Stage
      width={canvasWidth}
      height={canvasHeight}
    >
      <Layer>
        <Rect
          x={0}
          y={0}
          width={canvasWidth}
          height={canvasHeight}
          fill={appBackground}
          listening={false}
        />

        {planRooms.map((room) => {
          const origin = roomOrigins.get(room.id);
          const widthPx = Number(room.width) * scale;
          const lengthPx = Number(room.length) * scale;

          return (
              <Group
                key={`${room.id}:${room.x}:${room.y}`}
                x={origin.x}
                y={origin.y}
              >
              <Rect
                x={0}
                y={0}
                width={widthPx}
                height={lengthPx}
                stroke="black"
                strokeWidth={3}
                fill={roomColors[room.room_type] || roomColors.Other}
              />
              <Text
                x={6}
                y={6}
                width={widthPx - 12}
                text={`${room.label}\n${formatDimension(room.width)} × ${formatDimension(room.length)}`}
                fontSize={14}
                fill="#111827"
                listening={false}
              />
              {args.connected && (
                <Text
                  x={6}
                  y={6}
                  width={Math.min(widthPx - 12, 90)}
                  height={22}
                  text="Move room"
                  fontSize={11}
                  fill="#475569"
                  draggable
                  dragBoundFunc={(position) => ({
                    x: Math.max(origin.x + 6, Math.min(position.x, origin.x + widthPx - 96)),
                    y: Math.max(origin.y + 6, Math.min(position.y, origin.y + lengthPx - 28)),
                  })}
                  onMouseDown={(event) => { event.cancelBubble = true; }}
                  onTouchStart={(event) => { event.cancelBubble = true; }}
                  onDragEnd={(event) => handleRoomDragEnd(room, event)}
                />
              )}
              {room.openings.map((opening) => {
                const alongHorizontalWall = opening.wall_id === "top" || opening.wall_id === "bottom";
                const openingPixels = Number(opening.width) * scale;
                const centerX = alongHorizontalWall
                  ? (Number(opening.offset) + Number(opening.width) / 2) * scale
                  : opening.wall_id === "right" ? widthPx : 0;
                const centerY = alongHorizontalWall
                  ? opening.wall_id === "bottom" ? lengthPx : 0
                  : (Number(opening.offset) + Number(opening.width) / 2) * scale;

                return (
                  <Group
                    key={`${opening.id}:${opening.wall_id}:${opening.offset}`}
                    x={centerX}
                    y={centerY}
                    draggable
                    onMouseDown={(event) => { event.cancelBubble = true; }}
                    onTouchStart={(event) => { event.cancelBubble = true; }}
                    onDragStart={(event) => { event.cancelBubble = true; }}
                    dragBoundFunc={(position) => {
                      const horizontal = opening.wall_id === "top" || opening.wall_id === "bottom";
                      const halfWidth = horizontal ? openingPixels / 2 : 8;
                      const halfHeight = horizontal ? 8 : openingPixels / 2;
                      return {
                        x: Math.max(
                          origin.x + halfWidth,
                          Math.min(position.x, origin.x + widthPx - halfWidth),
                        ),
                        y: Math.max(
                          origin.y + halfHeight,
                          Math.min(position.y, origin.y + lengthPx - halfHeight),
                        ),
                      };
                    }}
                    onDragEnd={(event) => handleOpeningDragEnd(room, opening, event)}
                  >
                    <Rect
                      x={alongHorizontalWall ? -openingPixels / 2 : -8}
                      y={alongHorizontalWall ? -8 : -openingPixels / 2}
                      width={alongHorizontalWall ? openingPixels : 16}
                      height={alongHorizontalWall ? 16 : openingPixels}
                      fill="#ffffff"
                      stroke={opening.type === "door" ? "#b45309" : "#0284c7"}
                      strokeWidth={4}
                    />
                    <Text
                      x={-openingPixels / 2}
                      y={-24}
                      width={openingPixels}
                      align="center"
                      text={opening.name || opening.type}
                      fontSize={11}
                      listening={false}
                    />
                  </Group>
                );
              })}
            </Group>
          );
        })}


        {/* Furniture */}
        {items.map((item) => {
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
     

          const itemRoom = rooms.find((room) => room.id === item.room_id);
          const origin = roomOrigins.get(item.room_id) || { x: roomX, y: roomY };
          const x = origin.x + Number(item.x) * scale;
          const y = origin.y + Number(item.y) * scale;


          return (
            <Group
              key={item.id}
              x={x}
              y={y}
              draggable={true}

              dragBoundFunc={(pos) => {
                const minX = origin.x;
                const minY = origin.y;
                const maxX = origin.x + Number(itemRoom?.width || roomWidth) * scale - displayWidthPx;
                const maxY = origin.y + Number(itemRoom?.length || roomLength) * scale - displayDepthPx;

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
                handleDragEnd(item.id, e)

                
              }
            >

              <DefaultIcon
                type={item.furniture_type || "Other"}
                width={displayWidthPx}
                height={displayDepthPx}
                tint={FURNITURE_ICON_TINTS[item.furniture_type]}
              />
              {/* Furniture length dimension */}
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
                text={formatDimension(
                  rotation === 90 || rotation === 270
                    ? item.depth
                    : item.width
                )}
                fontSize={12}
              />


              {/* Furniture breadth dimension */}
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
                text={formatDimension(
                  rotation === 90 || rotation === 270
                    ? item.width
                    : item.depth
                )}
                fontSize={12}
                rotation={90}
              />


              <Group
                x={displayWidthPx}
                y={displayDepthPx}
                draggable
                onMouseDown={(event) => { event.cancelBubble = true; }}
                onTouchStart={(event) => { event.cancelBubble = true; }}
                onDragStart={(event) => { event.cancelBubble = true; }}
                dragBoundFunc={(position) => ({
                  x: Math.max(
                    x + 20,
                    Math.min(
                      position.x,
                      x + Number(itemRoom?.width || roomWidth) * scale - Number(item.x) * scale,
                    ),
                  ),
                  y: Math.max(
                    y + 20,
                    Math.min(
                      position.y,
                      y + Number(itemRoom?.length || roomLength) * scale - Number(item.y) * scale,
                    ),
                  ),
                })}
                onDragEnd={(event) => handleFurnitureResizeEnd(item, event, rotation === 90 || rotation === 270)}
              >
                <Rect
                  x={-7}
                  y={-7}
                  width={14}
                  height={14}
                  fill="#0f766e"
                  stroke="#ffffff"
                  strokeWidth={2}
                  cornerRadius={3}
                />
                <Text
                  x={-6}
                  y={-8}
                  width={12}
                  height={14}
                  text="↘"
                  align="center"
                  verticalAlign="middle"
                  fontSize={11}
                  fill="#ffffff"
                  listening={false}
                />
              </Group>


            </Group>
          );
        })}

      </Layer>
    </Stage>
  );
}


export default withStreamlitConnection(App);