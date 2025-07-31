import React, { useEffect, useState, useRef } from "react";
import {
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
  TouchableOpacity,
  Alert,
} from "react-native";
import { Camera, useCameraDevices } from "react-native-vision-camera";
import CustomCamera from "../components/Camera";
import { Ionicons } from "@expo/vector-icons";
import { Animated } from "react-native";

export default function CameraScreen({ onBack }) {
  const [hasPermission, setHasPermission] = useState(false);
  const [permissionStatus, setPermissionStatus] = useState("");
  const [selectedCamera, setSelectedCamera] = useState(0);
  const [isSquare, setIsSquare] = useState(false);
  const borderRadiusAnim = useRef(new Animated.Value(32)).current;
  const cameraRef = useRef(null);

  const sendPhotoToBackend = async (uri) => {
    const formData = new FormData();
    formData.append("file", {
      uri,
      name: "photo.jpg",
      type: "image/jpeg",
    });
    try {
      console.log("Sending photo to backend:", uri);
      const response = await fetch("http://192.168.0.239:8000/upload-frame/", {
        method: "POST",
        body: formData,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      const result = await response.json();
      console.log("Backend response:", result);
      Alert.alert(
        "Feedback",
        Array.isArray(result.feedback)
          ? result.feedback.join("\n")
          : result.feedback || result.error
      );
    } catch (error) {
      console.log("Upload failed:", error);
      Alert.alert("Upload failed", error.message);
    }
  };
  const handleCirclePress = async () => {
    if (cameraRef.current) {
      try {
        const photo = await cameraRef.current.takePhoto({
          flash: "off",
        });
        // photo.path is the local file path
        await sendPhotoToBackend("file://" + photo.path);
      } catch (e) {
        Alert.alert("Error", "Failed to take photo: " + e.message);
      }
    }
    /*setIsSquare((prev) => !prev);
    Animated.timing(borderRadiusAnim, {
      toValue: isSquare ? 32 : 8, // 32 for circle, 8 for square
      duration: 300,
      useNativeDriver: false,
    }).start();*/
  };

  useEffect(() => {
    (async () => {
      const { Camera } = await import("react-native-vision-camera");
      const status = await Camera.requestCameraPermission();
      console.log("Camera Status: ", status);
      setPermissionStatus(status);
      setHasPermission(
        status === "granted" || status === "authorized" || status === "limited"
      );
    })();
  }, []);
  const devices = useCameraDevices();
  console.log("All Devices:", Object.keys(devices));
  const device = devices[5];

  if (!hasPermission) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" />
        <Text style={{ color: "#fff" }}></Text>
      </View>
    );
  }

  if (!device) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" />
        <Text style={{ color: "#fff" }}>
          Loading camera...{" "}
          {device ? JSON.stringify(device, null, 2) : "No device found"}
        </Text>
      </View>
    );
  }
  if (!device) return null;
  return (
    <View style={styles.container}>
      <Camera
        ref={cameraRef}
        device={device}
        isActive={true}
        style={StyleSheet.absoluteFill}
        photo={true}
      />
      <View style={styles.bottomBar}>
        <Ionicons name="camera-reverse" size={32} color="#fff" />

        <TouchableOpacity onPress={handleCirclePress}>
          <Animated.View
            style={[styles.circleBorder, { borderRadius: borderRadiusAnim }]}
          >
            {/* You can put your Ionicons or any content here */}
          </Animated.View>
        </TouchableOpacity>

        <Ionicons name="close" size={32} color="#fff" onPress={onBack} />
      </View>
    </View>
  );
  /*
  return (
    <View style={styles.container}>
      <CustomCamera device={device} />
      <TouchableOpacity style={styles.closeButton} onPress={onBack}>
        <Text style={styles.closeText}>Close</Text>
      </TouchableOpacity>
    </View>
  );*/
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#000",
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    zIndex: 999,
  },
  centered: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#000",
  },
  bottomBar: {
    width: "100%",
    justifyContent: "center",
    alignItems: "center",
    marginTop: "auto", // Pushes the bar to the bottom
    // Optionally add paddingBottom for safe area
    paddingBottom: 30,
    flexDirection: "row",
    alignContent: "center",
  },

  closeText: { color: "#fff", fontSize: 16 },

  circleBorder: {
    width: 64,
    height: 64,
    borderRadius: 32,
    borderWidth: 4,
    borderColor: "#fff",
    justifyContent: "center",
    alignItems: "center",
    marginHorizontal: 40,
    // Glow effect (iOS)
    shadowColor: "#FF8C00",
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.5,
    shadowRadius: 16,
    // Glow effect (Android)
    elevation: 12,
    backgroundColor: "#FF8C00",
  },
});
