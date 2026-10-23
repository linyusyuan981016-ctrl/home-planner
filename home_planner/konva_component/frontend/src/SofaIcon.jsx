import { Group, Rect, Line } from "react-konva";

function SofaIcon({ width, height }) {
  const outline = "#9c5b43";
  const frame = "#df8f70";
  const cushion = "#f2c0a3";
  const inset = "#eca887";
  const strokeWidth = Math.max(1.5, Math.min(width, height) * 0.025);

  return (
    <Group>
      <Rect
        x={width * 0.035}
        y={height * 0.045}
        width={width * 0.93}
        height={height * 0.91}
        cornerRadius={Math.min(width, height) * 0.19}
        fill={frame}
        stroke={outline}
        strokeWidth={strokeWidth * 1.7}
      />
      <Rect
        x={width * 0.11}
        y={height * 0.13}
        width={width * 0.78}
        height={height * 0.23}
        cornerRadius={Math.min(width, height) * 0.1}
        fill={inset}
        stroke={outline}
        strokeWidth={strokeWidth}
      />
      <Rect
        x={width * 0.075}
        y={height * 0.34}
        width={width * 0.12}
        height={height * 0.52}
        cornerRadius={Math.min(width, height) * 0.07}
        fill={frame}
        stroke={outline}
        strokeWidth={strokeWidth}
      />
      <Rect
        x={width * 0.805}
        y={height * 0.34}
        width={width * 0.12}
        height={height * 0.52}
        cornerRadius={Math.min(width, height) * 0.07}
        fill={frame}
        stroke={outline}
        strokeWidth={strokeWidth}
      />
      <Rect
        x={width * 0.205}
        y={height * 0.39}
        width={width * 0.285}
        height={height * 0.44}
        cornerRadius={Math.min(width, height) * 0.07}
        fill={cushion}
        stroke={outline}
        strokeWidth={strokeWidth}
      />
      <Rect
        x={width * 0.51}
        y={height * 0.39}
        width={width * 0.285}
        height={height * 0.44}
        cornerRadius={Math.min(width, height) * 0.07}
        fill={cushion}
        stroke={outline}
        strokeWidth={strokeWidth}
      />
      <Line
        points={[width * 0.16, height * 0.88, width * 0.84, height * 0.88]}
        stroke={outline}
        strokeWidth={strokeWidth}
      />
    </Group>
  );
}

export default SofaIcon;
