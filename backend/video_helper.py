import cv2
import os
import base64

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
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
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





def cut_image(timestamp: str, video_file_path: str) -> str | None:
    """
    Extracts a frame from a video at a specific timestamp and returns it 
    as a base64 encoded string.

    Args:
        timestamp: The timestamp in "mm:ss.mmm" format (e.g., "02:05.053").
        video_file_path: The path to the video file.

    Returns:
        A base64 encoded string of the frame (in JPEG format), 
        or None if an error occurs.
    """
    
    # 1. Check if the video file exists
    if not os.path.exists(video_file_path):
        print(f"Error: Video file not found at {video_file_path}")
        return None

    # 2. Parse the timestamp string to total milliseconds
    try:
        parts = timestamp.split(':')
        minutes = int(parts[0])
        seconds_with_ms = float(parts[1])
        total_milliseconds = (minutes * 60 + seconds_with_ms) * 1000
    except Exception as e:
        print(f"Error: Invalid timestamp format. Expected 'mm:ss.mmm'. Got: {timestamp}. Error: {e}")
        return None

    # 3. Open the video file
    cap = cv2.VideoCapture(video_file_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_file_path}")
        return None
        
    try:
        # 4. Seek to the specified timestamp
        # cv2.CAP_PROP_POS_MSEC is the property for setting the position in milliseconds
        cap.set(cv2.CAP_PROP_POS_MSEC, total_milliseconds)
        
        # 5. Read the frame at that position
        ret, frame = cap.read()
        
        if not ret:
            print(f"Error: Could not read frame at timestamp {timestamp} ({total_milliseconds}ms)")
            return None

        # 6. Encode the frame (NumPy array) to a JPEG image in memory
        # 'success' is a boolean, 'buffer' holds the image data
        success, buffer = cv2.imencode('.jpg', frame)
        # Save encoded JPEG to the current working directory
        # filename = f"frame_{int(total_milliseconds)}ms.jpg"
        # file_path = os.path.join(os.getcwd(), filename)
        # if success:
        #     with open(file_path, "wb") as f:
        #         f.write(buffer.tobytes())
        #     print(f"Saved frame to {file_path}")
        if not success:
            print("Error: Failed to encode frame to JPEG")
            return None
            
        # 7. Encode the in-memory image buffer to base64
        base64_data = base64.b64encode(buffer)
        
        # 8. Decode the base64 bytes to a standard utf-8 string
        base64_string = base64_data.decode('utf-8')
        
        return base64_string

    except Exception as e:
        print(f"An error occurred during video processing: {e}")
        return None
    finally:
        # 9. Always release the video capture object to free up resources
        cap.release()