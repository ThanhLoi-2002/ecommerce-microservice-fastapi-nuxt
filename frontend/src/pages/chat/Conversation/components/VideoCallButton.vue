<template>
  <div>
    <!-- Video Call Button in Chat Header -->
    <button @click="startVideoCall" class="btn btn-link text-secondary" title="Gọi video">
      <i class="pi pi-video"></i>
    </button>

    <!-- Video Call Modal -->
    <div v-if="isCallActive" class="video-call-modal" :class="{ 'minimized': isMinimized }">
      <!-- Call Header -->
      <div class="call-header">
        <div class="call-info">
          <img :src="remoteUser.avatar" class="remote-avatar" alt="Avatar">
          <div class="call-details">
            <div class="remote-name">{{ remoteUser.name }}</div>
            <div class="call-status">{{ callStatus }}</div>
          </div>
        </div>
        <div class="call-actions">
          <button @click="toggleMinimize" class="btn-icon" title="Thu nhỏ">
            <i :class="['pi', isMinimized ? 'pi-window-maximize' : 'pi-window-minimize']"></i>
          </button>
          <button @click="endCall" class="btn-icon btn-danger" title="Kết thúc">
            <i class="pi pi-times"></i>
          </button>
        </div>
      </div>

      <!-- Video Container -->
      <div v-show="!isMinimized" class="video-container">
        <!-- Remote Video (Main) -->
        <div class="remote-video-wrapper">
          <video ref="remoteVideo" class="remote-video" autoplay playsinline></video>
          <div v-if="!isRemoteVideoEnabled" class="video-placeholder">
            <img :src="remoteUser.avatar" class="placeholder-avatar" alt="Avatar">
            <div class="placeholder-text">Camera đã tắt</div>
          </div>
        </div>

        <!-- Local Video (Picture-in-Picture) -->
        <div class="local-video-wrapper" :class="{ 'dragging': isDragging }" 
             @mousedown="startDrag" 
             :style="localVideoPosition">
          <video ref="localVideo" class="local-video" autoplay muted playsinline></video>
          <div v-if="!isLocalVideoEnabled" class="video-placeholder-small">
            <i class="pi pi-user"></i>
          </div>
        </div>

        <!-- Control Panel -->
        <div class="control-panel">
          <button @click="toggleMicrophone" 
                  class="btn-control" 
                  :class="{ 'active': isMicEnabled }">
            <i :class="['pi', isMicEnabled ? 'pi-microphone' : 'pi-microphone-slash']"></i>
          </button>

          <button @click="toggleCamera" 
                  class="btn-control" 
                  :class="{ 'active': isLocalVideoEnabled }">
            <i :class="['pi', isLocalVideoEnabled ? 'pi-video' : 'pi-video-slash']"></i>
          </button>

          <button @click="toggleScreenShare" 
                  class="btn-control" 
                  :class="{ 'active': isScreenSharing }">
            <i class="pi pi-desktop"></i>
          </button>

          <button @click="endCall" class="btn-control btn-end-call">
            <i class="pi pi-phone"></i>
          </button>

          <button @click="toggleSettings" class="btn-control">
            <i class="pi pi-cog"></i>
          </button>
        </div>

        <!-- Settings Panel -->
        <div v-if="showSettings" class="settings-panel">
          <div class="settings-header">
            <h6>Cài đặt</h6>
            <button @click="toggleSettings" class="btn-close">
              <i class="pi pi-times"></i>
            </button>
          </div>
          <div class="settings-content">
            <div class="setting-group">
              <label>Camera</label>
              <select v-model="selectedCamera" @change="changeCamera" class="form-control">
                <option v-for="device in videoDevices" :key="device.deviceId" :value="device.deviceId">
                  {{ device.label || `Camera ${device.deviceId.substring(0, 8)}` }}
                </option>
              </select>
            </div>
            <div class="setting-group">
              <label>Microphone</label>
              <select v-model="selectedMicrophone" @change="changeMicrophone" class="form-control">
                <option v-for="device in audioDevices" :key="device.deviceId" :value="device.deviceId">
                  {{ device.label || `Microphone ${device.deviceId.substring(0, 8)}` }}
                </option>
              </select>
            </div>
            <div class="setting-group">
              <label>Loa</label>
              <select v-model="selectedSpeaker" class="form-control">
                <option v-for="device in speakerDevices" :key="device.deviceId" :value="device.deviceId">
                  {{ device.label || `Speaker ${device.deviceId.substring(0, 8)}` }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Call Duration -->
      <div v-show="!isMinimized" class="call-duration">
        {{ formattedDuration }}
      </div>
    </div>

    <!-- Incoming Call Modal -->
    <div v-if="isIncomingCall" class="incoming-call-modal">
      <div class="incoming-call-content">
        <img :src="remoteUser.avatar" class="caller-avatar" alt="Avatar">
        <h5 class="caller-name">{{ remoteUser.name }}</h5>
        <p class="call-type">Cuộc gọi video đến...</p>
        <div class="incoming-call-actions">
          <button @click="declineCall" class="btn-incoming btn-decline">
            <i class="pi pi-times"></i>
            Từ chối
          </button>
          <button @click="acceptCall" class="btn-incoming btn-accept">
            <i class="pi pi-video"></i>
            Chấp nhận
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';

interface RemoteUser {
  id: number;
  name: string;
  avatar: string;
}

interface Props {
  remoteUser: RemoteUser;
}

const props = defineProps<Props>();

// Refs
const localVideo = ref<HTMLVideoElement>();
const remoteVideo = ref<HTMLVideoElement>();
let localStream: MediaStream | null = null;
let remoteStream: MediaStream | null = null;

// State
const isCallActive = ref(false);
const isIncomingCall = ref(false);
const isMinimized = ref(false);
const isMicEnabled = ref(true);
const isLocalVideoEnabled = ref(true);
const isRemoteVideoEnabled = ref(true);
const isScreenSharing = ref(false);
const showSettings = ref(false);
const callStatus = ref('Đang kết nối...');
const callDuration = ref(0);
let callTimer: number | null = null;

// Devices
const videoDevices = ref<MediaDeviceInfo[]>([]);
const audioDevices = ref<MediaDeviceInfo[]>([]);
const speakerDevices = ref<MediaDeviceInfo[]>([]);
const selectedCamera = ref<any>('');
const selectedMicrophone = ref<any>('');
const selectedSpeaker = ref<any>('');

// Drag functionality
const isDragging = ref(false);
const localVideoPosition = ref({ top: '20px', right: '20px' });
let dragStartX = 0;
let dragStartY = 0;
let dragStartTop = 0;
let dragStartRight = 0;

// Computed
const formattedDuration = computed(() => {
  const hours = Math.floor(callDuration.value / 3600);
  const minutes = Math.floor((callDuration.value % 3600) / 60);
  const seconds = callDuration.value % 60;
  
  if (hours > 0) {
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  }
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
});

// Methods
const startVideoCall = async () => {
  isCallActive.value = true;
  callStatus.value = 'Đang gọi...';
  
  try {
    await getMediaDevices();
    await initializeLocalStream();
    
    // Simulate call connection (in real app, use WebRTC)
    setTimeout(() => {
      callStatus.value = 'Đã kết nối';
      startCallTimer();
      simulateRemoteStream();
    }, 2000);
  } catch (error) {
    console.error('Error starting call:', error);
    console.warn('Camera/Microphone not available, using simulated stream');
    
    // Use simulated stream if real devices not available
    createSimulatedStream();
    
    setTimeout(() => {
      callStatus.value = 'Đã kết nối (Chế độ giả lập)';
      startCallTimer();
      simulateRemoteStream();
    }, 2000);
  }
};

const acceptCall = async () => {
  isIncomingCall.value = false;
  isCallActive.value = true;
  callStatus.value = 'Đã kết nối';
  
  try {
    await getMediaDevices();
    await initializeLocalStream();
    startCallTimer();
    simulateRemoteStream();
  } catch (error) {
    console.error('Error accepting call:', error);
    console.warn('Using simulated stream');
    createSimulatedStream();
    startCallTimer();
    simulateRemoteStream();
  }
};

const declineCall = () => {
  isIncomingCall.value = false;
};

const endCall = () => {
  // Stop all streams
  if (localStream) {
    localStream.getTracks().forEach(track => track.stop());
    
    // Clean up simulated stream resources
    if ((localStream as any)._simulationInterval) {
      clearInterval((localStream as any)._simulationInterval);
    }
    if ((localStream as any)._audioContext) {
      (localStream as any)._oscillator.stop();
      (localStream as any)._audioContext.close();
    }
    
    localStream = null;
  }
  
  if (remoteStream) {
    remoteStream.getTracks().forEach(track => track.stop());
    
    // Clean up simulated stream resources
    if ((remoteStream as any)._simulationInterval) {
      clearInterval((remoteStream as any)._simulationInterval);
    }
    if ((remoteStream as any)._audioContext) {
      (remoteStream as any)._oscillator.stop();
      (remoteStream as any)._audioContext.close();
    }
    
    remoteStream = null;
  }
  
  // Clear timer
  if (callTimer) {
    clearInterval(callTimer);
    callTimer = null;
  }
  
  // Reset state
  isCallActive.value = false;
  isMinimized.value = false;
  callDuration.value = 0;
  isScreenSharing.value = false;
};

const toggleMinimize = () => {
  isMinimized.value = !isMinimized.value;
};

const toggleMicrophone = () => {
  isMicEnabled.value = !isMicEnabled.value;
  if (localStream) {
    localStream.getAudioTracks().forEach(track => {
      track.enabled = isMicEnabled.value;
    });
  }
};

const toggleCamera = () => {
  isLocalVideoEnabled.value = !isLocalVideoEnabled.value;
  if (localStream) {
    localStream.getVideoTracks().forEach(track => {
      track.enabled = isLocalVideoEnabled.value;
    });
  }
};

const toggleScreenShare = async () => {
  if (!isScreenSharing.value) {
    try {
      const screenStream = await navigator.mediaDevices.getDisplayMedia({
        video: true,
        audio: true
      });
      
      // Replace video track
      const screenTrack: any = screenStream.getVideoTracks()[0];
      const sender = localStream?.getVideoTracks()[0];
      
      if (localVideo.value) {
        localVideo.value.srcObject = screenStream;
      }
      
      isScreenSharing.value = true;
      
      screenTrack.onended = () => {
        isScreenSharing.value = false;
        initializeLocalStream();
      };
    } catch (error) {
      console.error('Error sharing screen:', error);
    }
  } else {
    isScreenSharing.value = false;
    initializeLocalStream();
  }
};

const toggleSettings = () => {
  showSettings.value = !showSettings.value;
};

const getMediaDevices = async () => {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices();
    videoDevices.value = devices.filter(d => d.kind === 'videoinput');
    audioDevices.value = devices.filter(d => d.kind === 'audioinput');
    speakerDevices.value = devices.filter(d => d.kind === 'audiooutput');
    
    if (videoDevices.value.length > 0) {
      selectedCamera.value = videoDevices.value[0]?.deviceId;
    }
    if (audioDevices.value.length > 0) {
      selectedMicrophone.value = audioDevices.value[0]?.deviceId;
    }
  } catch (error) {
    console.error('Error getting devices:', error);
  }
};

const initializeLocalStream = async () => {
  try {
    const constraints: MediaStreamConstraints = {
      video: selectedCamera.value ? { deviceId: selectedCamera.value } : true,
      audio: selectedMicrophone.value ? { deviceId: selectedMicrophone.value } : true
    };
    
    localStream = await navigator.mediaDevices.getUserMedia(constraints);
    
    if (localVideo.value) {
      localVideo.value.srcObject = localStream;
    }
  } catch (error) {
    console.error('Error initializing local stream:', error);
    throw error;
  }
};

const createSimulatedStream = () => {
  // Create canvas for simulated video
  const canvas = document.createElement('canvas');
  canvas.width = 640;
  canvas.height = 480;
  const ctx = canvas.getContext('2d');
  
  if (!ctx) return;
  
  // Animated gradient background
  let hue = 0;
  const drawFrame = () => {
    // Create gradient
    const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
    gradient.addColorStop(0, `hsl(${hue}, 70%, 50%)`);
    gradient.addColorStop(0.5, `hsl(${hue + 60}, 70%, 50%)`);
    gradient.addColorStop(1, `hsl(${hue + 120}, 70%, 50%)`);
    
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw user icon
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.font = 'bold 120px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('👤', canvas.width / 2, canvas.height / 2 - 40);
    
    // Draw text
    ctx.font = 'bold 24px Arial';
    ctx.fillText('Camera Giả Lập', canvas.width / 2, canvas.height / 2 + 80);
    
    // Add time
    ctx.font = '18px Arial';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
    ctx.fillText(new Date().toLocaleTimeString(), canvas.width / 2, canvas.height / 2 + 120);
    
    hue = (hue + 0.5) % 360;
  };
  
  // Animate canvas
  const interval = setInterval(drawFrame, 1000 / 30); // 30 FPS
  
  // Get stream from canvas
  const canvasStream = canvas.captureStream(30);
  
  // Create audio context for simulated audio
  const audioContext = new AudioContext();
  const oscillator = audioContext.createOscillator();
  const gainNode = audioContext.createGain();
  
  oscillator.frequency.value = 0; // Silent
  gainNode.gain.value = 0;
  
  oscillator.connect(gainNode);
  gainNode.connect(audioContext.destination);
  oscillator.start();
  
  const audioDestination = audioContext.createMediaStreamDestination();
  gainNode.connect(audioDestination);
  
  // Combine video and audio streams
  localStream = new MediaStream([
    ...canvasStream.getVideoTracks(),
    ...audioDestination.stream.getAudioTracks()
  ]);
  
  if (localVideo.value) {
    localVideo.value.srcObject = localStream;
  }
  
  // Store interval for cleanup
  (localStream as any)._simulationInterval = interval;
  (localStream as any)._audioContext = audioContext;
  (localStream as any)._oscillator = oscillator;
  
  // Mark as simulated
  isLocalVideoEnabled.value = true;
  isMicEnabled.value = true;
};

const simulateRemoteStream = async () => {
  // Try to get real stream first
  try {
    remoteStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    if (remoteVideo.value) {
      remoteVideo.value.srcObject = remoteStream;
    }
    return;
  } catch (error) {
    console.warn('Cannot access real devices for remote stream, using simulation');
  }
  
  // Create simulated remote stream
  const canvas = document.createElement('canvas');
  canvas.width = 1280;
  canvas.height = 720;
  const ctx = canvas.getContext('2d');
  
  if (!ctx) return;
  
  // Animated background for remote user
  let hue = 180;
  let time = 0;
  
  const drawFrame = () => {
    time += 0.05;
    
    // Create animated gradient
    const gradient = ctx.createRadialGradient(
      canvas.width / 2 + Math.sin(time) * 100,
      canvas.height / 2 + Math.cos(time) * 100,
      50,
      canvas.width / 2,
      canvas.height / 2,
      canvas.width / 2
    );
    
    gradient.addColorStop(0, `hsl(${hue}, 60%, 40%)`);
    gradient.addColorStop(0.5, `hsl(${hue + 60}, 60%, 30%)`);
    gradient.addColorStop(1, `hsl(${hue + 120}, 60%, 20%)`);
    
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw remote user avatar/icon
    ctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
    ctx.font = 'bold 200px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('🎭', canvas.width / 2, canvas.height / 2 - 60);
    
    // Draw user name
    ctx.font = 'bold 48px Arial';
    ctx.fillText(props.remoteUser.name, canvas.width / 2, canvas.height / 2 + 150);
    
    // Draw status
    ctx.font = '32px Arial';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.fillText('Camera Giả Lập', canvas.width / 2, canvas.height / 2 + 220);
    
    // Add audio wave animation
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
    ctx.lineWidth = 3;
    ctx.beginPath();
    for (let i = 0; i < canvas.width; i += 10) {
      const y = canvas.height - 50 + Math.sin(i * 0.05 + time * 5) * 20;
      if (i === 0) {
        ctx.moveTo(i, y);
      } else {
        ctx.lineTo(i, y);
      }
    }
    ctx.stroke();
    
    hue = (hue + 0.3) % 360;
  };
  
  // Animate at 30 FPS
  const interval = setInterval(drawFrame, 1000 / 30);
  
  // Get stream from canvas
  const canvasStream = canvas.captureStream(30);
  
  // Create silent audio
  const audioContext = new AudioContext();
  const oscillator = audioContext.createOscillator();
  const gainNode = audioContext.createGain();
  
  oscillator.frequency.value = 0;
  gainNode.gain.value = 0;
  
  oscillator.connect(gainNode);
  const audioDestination = audioContext.createMediaStreamDestination();
  gainNode.connect(audioDestination);
  oscillator.start();
  
  // Combine streams
  remoteStream = new MediaStream([
    ...canvasStream.getVideoTracks(),
    ...audioDestination.stream.getAudioTracks()
  ]);
  
  if (remoteVideo.value) {
    remoteVideo.value.srcObject = remoteStream;
  }
  
  // Store for cleanup
  (remoteStream as any)._simulationInterval = interval;
  (remoteStream as any)._audioContext = audioContext;
  (remoteStream as any)._oscillator = oscillator;
  
  isRemoteVideoEnabled.value = true;
};

const changeCamera = async () => {
  if (localStream) {
    localStream.getVideoTracks().forEach(track => track.stop());
  }
  await initializeLocalStream();
};

const changeMicrophone = async () => {
  if (localStream) {
    localStream.getAudioTracks().forEach(track => track.stop());
  }
  await initializeLocalStream();
};

const startCallTimer = () => {
  callTimer = window.setInterval(() => {
    callDuration.value++;
  }, 1000);
};

// Drag handlers
const startDrag = (e: MouseEvent) => {
  isDragging.value = true;
  dragStartX = e.clientX;
  dragStartY = e.clientY;
  
  const rect = (e.target as HTMLElement).getBoundingClientRect();
  dragStartTop = rect.top;
  dragStartRight = window.innerWidth - rect.right;
  
  document.addEventListener('mousemove', onDrag);
  document.addEventListener('mouseup', stopDrag);
};

const onDrag = (e: MouseEvent) => {
  if (!isDragging.value) return;
  
  const deltaX = e.clientX - dragStartX;
  const deltaY = e.clientY - dragStartY;
  
  const newTop = dragStartTop + deltaY;
  const newRight = dragStartRight - deltaX;
  
  localVideoPosition.value = {
    top: `${Math.max(0, newTop)}px`,
    right: `${Math.max(0, newRight)}px`
  };
};

const stopDrag = () => {
  isDragging.value = false;
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mouseup', stopDrag);
};

// Simulate incoming call (for testing)
const simulateIncomingCall = () => {
  isIncomingCall.value = true;
};

onMounted(() => {
  // Simulate incoming call after 3 seconds (for testing)
  // setTimeout(simulateIncomingCall, 3000);
});

onUnmounted(() => {
  if (localStream) {
    localStream.getTracks().forEach(track => track.stop());
  }
  if (remoteStream) {
    remoteStream.getTracks().forEach(track => track.stop());
  }
  if (callTimer) {
    clearInterval(callTimer);
  }
});
</script>

<style scoped>
/* Video Call Modal */
.video-call-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #1a1a1a;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.video-call-modal.minimized {
  top: auto;
  left: auto;
  right: 20px;
  bottom: 20px;
  width: 300px;
  height: auto;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

/* Call Header */
.call-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 10;
}

.call-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.remote-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.remote-name {
  color: #fff;
  font-weight: 600;
  font-size: 1rem;
}

.call-status {
  color: #aaa;
  font-size: 0.875rem;
}

.call-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-icon:hover {
  background: rgba(255, 255, 255, 0.2);
}

.btn-icon.btn-danger {
  background: #dc3545;
}

.btn-icon.btn-danger:hover {
  background: #c82333;
}

/* Video Container */
.video-container {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* Remote Video */
.remote-video-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
  background: #000;
}

.remote-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.placeholder-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 16px;
  border: 4px solid rgba(255, 255, 255, 0.3);
}

.placeholder-text {
  color: #fff;
  font-size: 1rem;
}

/* Local Video (PIP) */
.local-video-wrapper {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 200px;
  height: 150px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  cursor: move;
  z-index: 20;
  border: 2px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.2s;
}

.local-video-wrapper:hover {
  transform: scale(1.05);
}

.local-video-wrapper.dragging {
  cursor: grabbing;
  transform: scale(1.05);
}

.local-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-placeholder-small {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.video-placeholder-small .pi {
  font-size: 3rem;
  color: #fff;
}

/* Control Panel */
.control-panel {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 16px;
  padding: 16px 24px;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 50px;
  z-index: 30;
}

.btn-control {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  font-size: 1.25rem;
}

.btn-control:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.btn-control.active {
  background: #0d6efd;
}

.btn-control.btn-end-call {
  background: #dc3545;
  transform: rotate(135deg);
}

.btn-control.btn-end-call:hover {
  background: #c82333;
}

/* Settings Panel */
.settings-panel {
  position: absolute;
  right: 20px;
  bottom: 120px;
  width: 320px;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  padding: 20px;
  z-index: 40;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.settings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.settings-header h6 {
  color: #fff;
  margin: 0;
  font-size: 1.1rem;
}

.btn-close {
  background: none;
  border: none;
  color: #fff;
  cursor: pointer;
  font-size: 1.25rem;
  padding: 0;
  width: 24px;
  height: 24px;
}

.settings-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.setting-group label {
  color: #fff;
  font-size: 0.875rem;
  margin-bottom: 8px;
  display: block;
}

.setting-group select {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 0.875rem;
}

.setting-group select option {
  background: #1a1a1a;
  color: #fff;
}

/* Call Duration */
.call-duration {
  position: absolute;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  color: #fff;
  font-size: 1rem;
  background: rgba(0, 0, 0, 0.5);
  padding: 8px 16px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  z-index: 15;
}

/* Incoming Call Modal */
.incoming-call-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.incoming-call-content {
  text-align: center;
  animation: slideUp 0.4s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.caller-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 20px;
  border: 4px solid #0d6efd;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(13, 110, 253, 0.7);
  }
  50% {
    box-shadow: 0 0 0 20px rgba(13, 110, 253, 0);
  }
}

.caller-name {
  color: #fff;
  font-size: 1.5rem;
  margin-bottom: 8px;
}

.call-type {
  color: #aaa;
  font-size: 1rem;
  margin-bottom: 32px;
}

.incoming-call-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.btn-incoming {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 32px;
  border-radius: 12px;
  border: none;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-incoming i {
  font-size: 1.5rem;
}

.btn-decline {
  background: #dc3545;
  color: #fff;
}

.btn-decline:hover {
  background: #c82333;
  transform: scale(1.05);
}

.btn-accept {
  background: #28a745;
  color: #fff;
}

.btn-accept:hover {
  background: #218838;
  transform: scale(1.05);
}

/* Responsive */
@media (max-width: 768px) {
  .local-video-wrapper {
    width: 120px;
    height: 90px;
    top: 10px;
    right: 10px;
  }
  
  .control-panel {
    gap: 12px;
    padding: 12px 16px;
  }
  
  .btn-control {
    width: 48px;
    height: 48px;
    font-size: 1rem;
  }
  
  .settings-panel {
    width: calc(100% - 40px);
    left: 20px;
    right: 20px;
  }
}
</style>