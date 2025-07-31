import React, { useState, useCallback } from "react";
import {
  Text,
  StyleSheet,
  View,
  Dimensions,
  TouchableOpacity,
  TextInput,
  ScrollView,
} from "react-native";
import AnimatedContainer from "../components/AnimatedContainer";
import { VideoView, useVideoPlayer } from "expo-video";
import { Ionicons } from "@expo/vector-icons";
import CameraScreen from "./CameraScreen";

import { StatusBar } from "expo-status-bar";

const { width, height } = Dimensions.get("window");

export default function Coach() {
  const [showCamera, setShowCamera] = useState(false);

  const player = useVideoPlayer(
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
    (player) => {
      player.loop = true;
      player.play();
    }
  );

  const handleCameraBack = useCallback(() => {
    setShowCamera(false);
  }, []);

  if (showCamera) {
    return <CameraScreen onBack={handleCameraBack} />;
  }

  return (
    <View style={styles.container}>
      <StatusBar style="light" />
      <AnimatedContainer />

      <View style={styles.content}>
        <View style={styles.searchContainer}>
          <TouchableOpacity style={styles.searchIcon}>
            <Ionicons name="search" size={24} color="#FF8C00" />
          </TouchableOpacity>
          <TextInput
            style={styles.searchInput}
            placeholder="search workouts"
            placeholderTextColor="white"
          />
        </View>
        <View style={styles.videoContent}>
          <VideoView
            style={styles.video}
            player={player}
            allowsFullscreen
            allowsPictureInPicture
            contentFit="cover"
          />
        </View>
        <View style={styles.descContainer}>
          <View style={styles.titleContainer}>
            <Text style={styles.title}>Double Biceps Curl</Text>
            <Text style={styles.targetMuscleText}>Target Muscle: Biceps</Text>
          </View>

          <View style={styles.description}>
            <ScrollView>
              <Text style={styles.descriptionText}>
                Stand with feet shoulder-width apart, holding a dumbbell in each
                hand with arms at your sides. Keep your elbows close to your
                body and slowly curl both weights up towards your shoulders,
                squeezing your biceps at the top. Lower the weights back down
                with control to the starting position. Focus on slow, controlled
                movements and avoid swinging or using momentum. Stand with feet
                shoulder-width apart, holding a dumbbell in each hand with arms
                at your sides. Keep your elbows close to your body and slowly
                curl both weights up towards your shoulders, squeezing your
                biceps at the top. Lower the weights back down with control to
                the starting position. Focus on slow, controlled movements and
                avoid swinging or using momentum.
              </Text>
            </ScrollView>
          </View>
        </View>
        <TouchableOpacity
          activeOpacity={0.8}
          onPress={() => {
            console.log("Check Your Form pressed");
            setShowCamera(true);
            // Form analysis feature coming soon
          }}
          style={styles.analyserCard}
        >
          <View style={styles.card}>
            {/* Top Left Corner */}
            <View style={[styles.corner, styles.topLeft]} />
            {/* Top Right Corner */}
            <View style={[styles.corner, styles.topRight]} />
            {/* Bottom Left Corner */}
            <View style={[styles.corner, styles.bottomLeft]} />
            {/* Bottom Right Corner */}
            <View style={[styles.corner, styles.bottomRight]} />

            <View style={styles.cardContent}>
              <Ionicons name="camera" size={50} color="#ffffff" />
              <Text style={styles.cardTitle}>Check Your Form </Text>
            </View>
          </View>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
  },
  content: {
    flex: 1,
    paddingBottom: height * 0.1,
    paddingTop: height * 0.07,

    //backgroundColor: "orange",
  },
  searchContainer: {
    flex: 0.4,
    flexDirection: "row",
    borderColor: "#FF8C00",
    borderRadius: 10,
    borderWidth: 1,
    //elevation: 30,
    alignItems: "center",
    margin: 10,
  },
  searchIcon: {
    // Add styling for the search icon container
    padding: 10,
  },
  searchInput: {
    // Add this missing style
    flex: 1,
    height: 40,
    color: "white",
    fontSize: 16,
    paddingRight: 10,
  },
  videoContent: {
    flex: 3,
    width: width,
    padding: 0,
    borderRadius: 10,
    marginTop: 10,
    //backgroundColor: "red",
  },
  video: {
    flex: 1,
    width: "100%",
    height: "100%",
    borderRadius: 20, // Reduce border radius for better visibility
    overflow: "hidden",
    backgroundColor: "#333",
  },
  descContainer: {
    flex: 2.5,
    width: width,
    padding: 10,
    borderRadius: 50,
    //backgroundColor: "green",
  },
  descriptionText: {
    color: "#ffffff",
    fontSize: 14,
    lineHeight: 20,
    textAlign: "left",
  },
  titleContainer: {
    flex: 1,
    width: width,
    marginTop: 10,
    //backgroundColor: "purple",
  },
  title: {
    color: "#FF8C00",
    fontSize: 24,
    fontWeight: "900",
    textTransform: "uppercase",
  },
  targetMuscleText: {
    color: "#ffffff",
    fontSize: 16,
    fontWeight: "500",
    textTransform: "uppercase",
    opacity: 0.5,
  },
  analyserCard: {
    flex: 1.2,
    marginTop: 10,
    marginBottom: 20,
    justifyContent: "center",
    alignItems: "center",
    width: width,
    paddingHorizontal: 20,
  },

  cardContent: {
    justifyContent: "center",
    alignItems: "center",
    flexDirection: "row",
  },

  description: {
    flex: 3,
    //backgroundColor: "black",
    width: width,
  },
  textItems: { color: "white" },

  card: {
    width: width * 0.9,
    height: height * 0.12,
    backgroundColor: "#e47d00",
    borderRadius: 20,
    justifyContent: "center",
    alignItems: "center",
    flexDirection: "row",
    shadowColor: "#b35300",
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.5,
    shadowRadius: 20,
    elevation: 8,
  },
  cardTitle: {
    color: "white",
    fontWeight: "900",
    fontSize: 24,
    lineHeight: 24,
    marginLeft: 10,
  },

  corner: {
    position: "absolute",
    width: 20,
    height: 20,
    borderColor: "#FFFFFF", // Green color
    borderWidth: 3,
  },
  topLeft: {
    top: 8,
    left: 8,
    borderRightWidth: 0,
    borderBottomWidth: 0,
    borderTopLeftRadius: 5,
  },
  topRight: {
    top: 8,
    right: 8,
    borderLeftWidth: 0,
    borderBottomWidth: 0,
    borderTopRightRadius: 5,
  },
  bottomLeft: {
    bottom: 8,
    left: 8,
    borderRightWidth: 0,
    borderTopWidth: 0,
    borderBottomLeftRadius: 5,
  },
  bottomRight: {
    bottom: 8,
    right: 8,
    borderLeftWidth: 0,
    borderTopWidth: 0,
    borderBottomRightRadius: 5,
  },
});
