import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { styled } from 'nativewind'; // Using Tailwind as requested

const StyledView = styled(View);
const StyledText = styled(Text);

const PODUploadScreen = () => {
  // Mobile-Optimized Frictionless Interaction
  const handleUpload = async () => {
    // Logic for capturing image and sending to Django API
    console.log("Triggering Optimized POD Upload...");
  };

  return (
    <StyledView className="flex-1 bg-white p-6 justify-center">
      <StyledText className="text-2xl font-bold text-center mb-10">
        SymFlow Driver POD
      </StyledText>
      
      {/* Large target area for drivers in high-stress environments */}
      <TouchableOpacity 
        onPress={handleUpload}
        className="bg-blue-600 p-8 rounded-2xl shadow-lg"
      >
        <StyledText className="text-white text-center font-bold text-xl">
          CAPTURE & UPLOAD PROOF
        </StyledText>
      </TouchableOpacity>
    </StyledView>
  );
};

export default PODUploadScreen;
