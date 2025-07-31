import { View, Text, StyleSheet, Animated } from "react-native";
import React, { useRef, useEffect, useState } from "react";
import { LinearGradient } from "expo-linear-gradient";

export default function App() {
  const animation = useRef(new Animated.Value(0)).current;
  const [gradientColors, setGradientColors] = useState(["#000", "#222"]);

  
  useEffect(() => {
    const loop = Animated.loop(
      Animated.sequence([
        Animated.timing(animation, {
          toValue: 1,
          duration: 5000,
          useNativeDriver: false,
        }),
        Animated.timing(animation, {
          toValue: 0,
          duration: 2000,
          useNativeDriver: false,
        }),
      ])
    );
    loop.start();
  }, [animation]);
  
  useEffect(() => {
    const listener = animation.addListener(({ value }) => {
      const interpolateColor = (start, end) => {
        const s = parseInt(start.slice(1), 16);
        const e = parseInt(end.slice(1), 16);
        const r = Math.round(((e >> 16) - (s >> 16)) * value + (s >> 16));
        const g = Math.round(
          (((e >> 8) & 0xff) - ((s >> 8) & 0xff)) * value + ((s >> 8) & 0xff)
        );
        const b = Math.round(((e & 0xff) - (s & 0xff)) * value + (s & 0xff));
        return `rgb(${r},${g},${b})`;
      };
      setGradientColors([
        interpolateColor("#9bc063", "#253324"), // green to black
        interpolateColor("#455d3b", "#253324"),
      ]);
    });
    return () => {
      animation.removeListener(listener);
    };
  }, [animation]);


  return (
    <View style={styles.container}>
      <Animated.View style={StyleSheet.absoluteFill}>
        <LinearGradient
          colors={gradientColors}
          style={StyleSheet.absoluteFill}
          start={{ x: 0.5, y: 0.5 }}
          end={{ x: 1, y: 1 }}
        />
      </Animated.View>
      <Text style={styles.text}>Hello World</Text>
    </View>
  );
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#386641",
  },
  text: {
    fontSize: 32,
    color: "#fff",
    fontWeight: "bold",
  },
});
