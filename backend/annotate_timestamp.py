import cv2
import os

def format_time(milliseconds):
    """Converts milliseconds to HH:MM:SS:ms format"""
    total_seconds = int(milliseconds / 1000)
    ms = int(milliseconds % 1000)
    total_minutes = int(total_seconds / 60)
    sec = int(total_seconds % 60)
    total_hours = int(total_minutes / 60)
    mins = int(total_minutes % 60)
    
    # Format as HH:MM:SS:ms
    return f"{total_hours:02d}:{mins:02d}:{sec:02d}:{ms:03d}"

def add_timestamps_to_video(input_path, output_path):
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    # Open the video file
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Define the codec and create VideoWriter object
    # 'avc1' (H.264) is preferred for strict MP4 compatibility
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f"Processing video... (FPS: {fps})")

    frame_count = 0
    while True:
        # Read a new frame
        ret, frame = cap.read()
        
        # If frame is read correctly, ret is True
        if not ret:
            print("Finished processing video.")
            break
        
        # Get the current timestamp in milliseconds
        milliseconds = cap.get(cv2.CAP_PROP_POS_MSEC)
        timestamp_text = format_time(milliseconds)

        # --- Text and background settings ---
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        font_thickness = 2
        text_color = (255, 255, 255)  # White
        bg_color = (0, 0, 0)        # Black
        
        # Position for the text (bottom-left corner)
        pos = (10, height - 20) 

        # Get text size to draw a background rectangle
        (text_w, text_h), baseline = cv2.getTextSize(timestamp_text, font, font_scale, font_thickness)
        
        # Draw the black background rectangle
        cv2.rectangle(
            frame, 
            (pos[0], pos[1] + baseline), 
            (pos[0] + text_w, pos[1] - text_h - baseline), 
            bg_color, 
            -1  # -1 fills the rectangle
        )
        
        # Put the white timestamp text on top of the rectangle
        cv2.putText(
            frame, 
            timestamp_text, 
            (pos[0], pos[1]), 
            font, 
            font_scale, 
            text_color, 
            font_thickness, 
            cv2.LINE_AA
        )
        
        # Write the modified frame to the output file
        out.write(frame)
        frame_count += 1

    # Release everything when job is finished
    cap.release()
    out.release()
    print(f"Successfully saved new video to {output_path}")

# --- --- --- --- ---
#      RUN THE SCRIPT
# --- --- --- --- ---

# 1. Change this to your input video file
input_video = "cut-video.mp4" 

# 2. This will be the name of your new file
output_video = "output_with_timestamps.mp4" 

add_timestamps_to_video(input_video, output_video)